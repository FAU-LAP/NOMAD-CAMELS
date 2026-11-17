"""Outbound connection from CAMELS to the OASIS broker.

The agent opens a WebSocket to OASIS, so the lab computer needs no inbound
port. OASIS sends commands down this connection, and the agent runs them
against the CAMELS API routes in-process (``httpx.ASGITransport``). Only the
operations listed in ``OPERATIONS`` can be run; there is no generic
forwarding.

See ``docs/camels_remote_protocol.md`` in the OASIS repository.
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
import socket
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable
from urllib.parse import quote

log = logging.getLogger("nomad_camels.remote_agent")

SUBPROTOCOL = "camels-remote.v1"
PROTOCOL_VERSION = 1
MAX_MESSAGE_BYTES = 1024 * 1024
PING_INTERVAL_SECONDS = 20
HELLO_TIMEOUT_SECONDS = 15
MAX_BACKOFF_SECONDS = 60

CLOSE_REVOKED = 4401
CLOSE_REPLACED = 4409
CLOSE_UNSUPPORTED_VERSION = 4426


@dataclass(frozen=True)
class Operation:
    """One allowed CAMELS route.

    Args:
        params: Payload fields inserted into the path (non-empty strings).
        query: ``(payload field, query name)`` pairs for the query string.
        body: Payload fields sent as the JSON body.
        control: The operation changes CAMELS state; refused while remote
            control is paused on the lab computer.
    """

    method: str
    path: str
    params: tuple[str, ...] = ()
    query: tuple[tuple[str, str], ...] = ()
    body: tuple[str, ...] = ()
    control: bool = False


# The complete whitelist. There is no generic forwarding.
OPERATIONS: dict[str, Operation] = {
    # Reading
    "get_service_info": Operation("GET", "/api/v1/info"),
    "list_protocols": Operation("GET", "/api/v1/protocols"),
    "get_protocol_schema": Operation("GET", "/api/v1/protocols/{protocol}/schema", ("protocol",)),
    "get_protocol_definition": Operation("GET", "/api/v1/protocols/{protocol}/JSON", ("protocol",)),
    "get_run_status": Operation("GET", "/api/v1/protocols/results/{run_id}", ("run_id",)),
    "get_measurement_status": Operation("GET", "/api/v1/gui/measurement-status"),
    "get_plot_count": Operation("GET", "/api/v1/gui/plots"),
    "get_plot_data": Operation("GET", "/api/v1/gui/plot-caches", query=(("cursor", "cursor"),)),
    "get_pid_plots": Operation("GET", "/api/v1/gui/pid-plots", query=(("protocol", "protocol_name"),)),
    # Changing
    "save_protocol_parameters": Operation(
        "POST", "/api/v1/protocols/{protocol}/parameters", ("protocol",), body=("variables",), control=True
    ),
    "start_measurement": Operation(
        "POST",
        "/api/v1/actions/run/protocols/{protocol}",
        ("protocol",),
        query=(("run_id", "protocol_uuid"),),
        body=("variables",),
        control=True,
    ),
    "stop_measurement": Operation("POST", "/api/v1/actions/stop", control=True),
    "close_plots": Operation("POST", "/api/v1/gui/plots/close", control=True),
}

# Remembered results of started runs, so that a repeated start command with
# the same run_id (for example a retry after a lost answer) starts nothing.
MAX_REMEMBERED_RUNS = 200

# Agent states shown in the CAMELS settings.
STATE_STOPPED = "stopped"
STATE_CONNECTING = "connecting"
STATE_ONLINE = "online"
STATE_RETRYING = "retrying"
STATE_UNAUTHORIZED = "unauthorized"
STATE_REPLACED = "replaced"
STATE_OUTDATED = "outdated"

FINAL_STATES = {STATE_STOPPED, STATE_UNAUTHORIZED, STATE_REPLACED, STATE_OUTDATED}


class CommandError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def envelope(type_: str, **fields) -> dict:
    return {"version": PROTOCOL_VERSION, "type": type_, "id": uuid.uuid4().hex, "ts": utc_now(), **fields}


def build_path(operation: Operation, payload: dict) -> str:
    values = {}
    for name in operation.params:
        value = payload.get(name)
        if not isinstance(value, str) or not value:
            raise CommandError("invalid_parameters", f"'{name}' must be a non-empty string.")
        values[name] = quote(value, safe="")
    return operation.path.format(**values)


def build_query(operation: Operation, payload: dict) -> dict:
    query = {}
    for field, name in operation.query:
        value = payload.get(field)
        if value is None:
            continue
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        if not isinstance(value, (str, int, float)) or isinstance(value, bool):
            raise CommandError("invalid_parameters", f"'{field}' has an invalid type.")
        query[name] = str(value)
    return query


def build_body(operation: Operation, payload: dict):
    if not operation.body:
        return None
    body = {}
    for field in operation.body:
        value = payload.get(field, {})
        if not isinstance(value, dict):
            raise CommandError("invalid_parameters", f"'{field}' must be an object.")
        body[field] = value
    return body


def error_for_status(status_code: int, detail: str = "") -> CommandError:
    detail = detail[:300]
    if status_code == 404:
        return CommandError("not_found", detail or "Not found.")
    if status_code in (400, 422):
        return CommandError("invalid_parameters", detail or "The parameters were rejected.")
    if status_code == 409:
        return CommandError("busy", detail or "Another measurement is running.")
    return CommandError("internal", detail or f"CAMELS answered with HTTP {status_code}.")


def response_detail(response) -> str:
    """The ``detail`` text of a FastAPI error response, if it has one."""
    try:
        detail = response.json().get("detail")
    except (ValueError, AttributeError):
        return ""
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list) and detail and isinstance(detail[0], dict):
        # Validation errors: report the first one.
        return str(detail[0].get("msg", ""))
    return ""


class RemoteAgent:
    """Keeps the connection to OASIS in a background thread.

    Args:
        url: ``wss://`` URL of the broker's agent endpoint.
        token: Device token from pairing.
        asgi_app: CAMELS FastAPI app used for the operations.
        ssl_context: Context for ``wss://`` URLs, ``None`` for ``ws://``.
        on_state: Called with ``(state, detail)`` from the agent thread.
    """

    def __init__(
        self,
        url: str,
        token: str,
        asgi_app,
        ssl_context=None,
        camels_version: str = "",
        on_state: Callable[[str, str], None] | None = None,
        measurement_provider: Callable[[], dict] | None = None,
    ):
        self.url = url
        self._token = token
        self.app = asgi_app
        self.ssl_context = ssl_context
        self.camels_version = camels_version
        self.on_state = on_state
        self.measurement_provider = measurement_provider
        self.state = STATE_STOPPED
        self.detail = ""
        self._thread: threading.Thread | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._task: asyncio.Task | None = None
        self._started = threading.Event()
        # Set from the GUI thread; read before each operation that changes
        # CAMELS state.
        self.control_paused = False
        self._started_runs: dict[str, dict] = {}
        self._start_lock: asyncio.Lock | None = None

    # ------------------------------------------------------------------
    # Thread control
    # ------------------------------------------------------------------
    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._started.clear()
        self._thread = threading.Thread(target=self._thread_main, name="CAMELS remote agent", daemon=True)
        self._thread.start()
        self._started.wait(5)

    def stop(self, timeout: float = 5) -> None:
        """Close the connection and end the thread. Safe from any thread."""
        loop, task = self._loop, self._task
        if loop is not None and task is not None and not loop.is_closed():
            try:
                loop.call_soon_threadsafe(task.cancel)
            except RuntimeError:
                pass
        if self._thread is not None:
            self._thread.join(timeout)
        self._thread = None

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _thread_main(self) -> None:
        loop = asyncio.new_event_loop()
        self._loop = loop
        asyncio.set_event_loop(loop)
        self._task = loop.create_task(self._main())
        self._started.set()
        try:
            loop.run_until_complete(self._task)
        except asyncio.CancelledError:
            self._set_state(STATE_STOPPED, "")
        except Exception:
            log.exception("remote agent stopped after an unexpected error")
            self._set_state(STATE_STOPPED, "Unexpected error, see the log.")
        finally:
            loop.close()

    def _set_state(self, state: str, detail: str = "") -> None:
        if (state, detail) == (self.state, self.detail):
            return
        self.state = state
        self.detail = detail
        log.info("remote agent: %s %s", state, detail)
        if self.on_state is not None:
            try:
                self.on_state(state, detail)
            except Exception:
                log.exception("remote agent state callback failed")

    # ------------------------------------------------------------------
    # Connection loop
    # ------------------------------------------------------------------
    async def _main(self) -> None:
        import httpx
        import websockets
        from websockets.exceptions import ConnectionClosed, InvalidHandshake, InvalidStatus, InvalidURI

        attempt = 0
        transport = httpx.ASGITransport(app=self.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://camels-agent") as client:
            self._client = client
            while True:
                self._set_state(STATE_CONNECTING, self.url)
                final = None
                detail = "Connection ended."
                try:
                    async with websockets.connect(
                        self.url,
                        additional_headers={"Authorization": f"Bearer {self._token}"},
                        subprotocols=[SUBPROTOCOL],
                        ssl=self.ssl_context,
                        ping_interval=PING_INTERVAL_SECONDS,
                        ping_timeout=PING_INTERVAL_SECONDS,
                        max_size=MAX_MESSAGE_BYTES,
                        open_timeout=20,
                        user_agent_header="NOMAD-CAMELS remote agent",
                    ) as ws:
                        await self._session(ws)
                except InvalidStatus as exc:
                    status = exc.response.status_code
                    if status == 401:
                        final = (STATE_UNAUTHORIZED, "OASIS rejected the device token. Pair this computer again.")
                    else:
                        detail = f"OASIS answered HTTP {status}."
                except InvalidURI as exc:
                    final = (STATE_STOPPED, f"Invalid OASIS address: {exc}")
                except ConnectionClosed as exc:
                    code = exc.rcvd.code if exc.rcvd is not None else None
                    if code == CLOSE_REVOKED:
                        final = (STATE_UNAUTHORIZED, "OASIS revoked this device. Pair this computer again.")
                    elif code == CLOSE_REPLACED:
                        final = (STATE_REPLACED, "Another CAMELS instance connected with this device token.")
                    elif code == CLOSE_UNSUPPORTED_VERSION:
                        final = (STATE_OUTDATED, "OASIS does not support this CAMELS version.")
                    else:
                        detail = "Connection lost."
                except (OSError, InvalidHandshake, asyncio.TimeoutError) as exc:
                    detail = describe_network_error(exc)
                except ValueError:
                    detail = "OASIS sent an unexpected answer."
                if final is not None:
                    self._set_state(*final)
                    return
                if self.state == STATE_ONLINE:
                    # The last session worked, so start the backoff again.
                    attempt = 0
                delay = min(MAX_BACKOFF_SECONDS, 2**attempt) * random.uniform(0.8, 1.2)
                attempt += 1
                self._set_state(STATE_RETRYING, f"{detail} Retrying in {delay:.0f} s.")
                await asyncio.sleep(delay)

    async def _session(self, ws) -> None:
        send_lock = asyncio.Lock()

        async def send(message: dict) -> None:
            async with send_lock:
                await ws.send(json.dumps(message))

        await send(
            envelope(
                "hello",
                camels_version=self.camels_version,
                hostname=socket.gethostname(),
                operations=sorted(OPERATIONS),
                measurement=self._measurement(),
            )
        )
        welcome = json.loads(await asyncio.wait_for(ws.recv(), HELLO_TIMEOUT_SECONDS))
        if welcome.get("type") != "welcome":
            await ws.close(1002, "expected welcome")
            return
        self._set_state(STATE_ONLINE, f"session {welcome.get('session_id', '')}")

        tasks: set[asyncio.Task] = set()
        try:
            while True:
                raw = await ws.recv()  # raises ConnectionClosed
                try:
                    message = json.loads(raw)
                except (TypeError, ValueError):
                    log.warning("remote agent: ignored a message that is not JSON")
                    continue
                if not isinstance(message, dict):
                    continue
                if message.get("type") == "command":
                    task = asyncio.ensure_future(self._handle_command(message, send))
                    tasks.add(task)
                    task.add_done_callback(tasks.discard)
                else:
                    log.info("remote agent: ignored message type %r", message.get("type"))
        finally:
            for task in tasks:
                task.cancel()

    def _measurement(self):
        if self.measurement_provider is None:
            return None
        try:
            return self.measurement_provider()
        except Exception:
            log.exception("remote agent: reading the measurement status failed")
            return None

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------
    async def _handle_command(self, message: dict, send) -> None:
        command_id = message.get("command_id")
        operation_name = message.get("operation")
        log.info(
            "remote command %s operation=%s requested_by=%s",
            command_id,
            operation_name,
            message.get("requested_by"),
        )
        try:
            result = await self.run_operation(operation_name, message.get("payload") or {})
            reply = envelope("command_result", command_id=command_id, status="completed", result=result)
        except CommandError as exc:
            reply = envelope(
                "command_result",
                command_id=command_id,
                status="rejected",
                error={"code": exc.code, "message": exc.message},
            )
        except Exception:
            log.exception("remote command %s failed", command_id)
            reply = envelope(
                "command_result",
                command_id=command_id,
                status="rejected",
                error={"code": "internal", "message": "The operation failed in CAMELS."},
            )
        try:
            await send(reply)
        except Exception:
            log.warning("remote agent: could not send the result of %s", command_id)

    async def run_operation(self, name, payload: dict):
        operation = OPERATIONS.get(name) if isinstance(name, str) else None
        if operation is None:
            raise CommandError("unknown_operation", f"Operation {name!r} is not allowed.")
        if not isinstance(payload, dict):
            raise CommandError("invalid_parameters", "The payload must be an object.")
        if operation.control and self.control_paused:
            raise CommandError("paused", "Remote control is paused on the lab computer.")
        if name == "get_measurement_status":
            result = await self._request(operation, payload)
            if isinstance(result, dict):
                # Lets OASIS show why it cannot start or stop anything.
                result["remote_control_paused"] = bool(self.control_paused)
            return result
        if name != "start_measurement":
            return await self._request(operation, payload)
        # One start at a time, and a repeated run_id starts nothing again.
        if self._start_lock is None:
            self._start_lock = asyncio.Lock()
        async with self._start_lock:
            run_id = payload.get("run_id")
            if isinstance(run_id, str) and run_id in self._started_runs:
                return {**self._started_runs[run_id], "duplicate": True}
            result = await self._request(operation, payload)
            if isinstance(run_id, str) and run_id:
                self._started_runs[run_id] = result
                while len(self._started_runs) > MAX_REMEMBERED_RUNS:
                    self._started_runs.pop(next(iter(self._started_runs)))
            return result

    async def _request(self, operation: Operation, payload: dict):
        path = build_path(operation, payload)
        query = build_query(operation, payload)
        body = build_body(operation, payload)
        response = await self._client.request(
            operation.method, path, params=query or None, json=body, timeout=30
        )
        if response.status_code >= 300:
            raise error_for_status(response.status_code, response_detail(response))
        try:
            return response.json()
        except ValueError:
            raise CommandError("internal", "CAMELS returned a response that is not JSON.")


def describe_network_error(exc: Exception) -> str:
    import ssl

    if isinstance(exc, ssl.SSLCertVerificationError):
        return f"Certificate check failed ({exc.verify_message}). Set the CA certificate file."
    if isinstance(exc, ssl.SSLError):
        return f"TLS failed: {exc}."
    if isinstance(exc, socket.gaierror):
        return "The OASIS host name could not be resolved."
    if isinstance(exc, ConnectionRefusedError):
        return "OASIS refused the connection. Check the address and port."
    if isinstance(exc, (TimeoutError, asyncio.TimeoutError)):
        return "OASIS did not answer in time."
    return f"{type(exc).__name__}: {exc}."
