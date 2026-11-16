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
    method: str
    path: str
    params: tuple[str, ...] = ()


# The complete whitelist. Operations that change CAMELS state are added in
# later phases, together with their safeguards.
OPERATIONS: dict[str, Operation] = {
    "get_service_info": Operation("GET", "/api/v1/info"),
    "list_protocols": Operation("GET", "/api/v1/protocols"),
    "get_protocol_schema": Operation("GET", "/api/v1/protocols/{protocol}/schema", ("protocol",)),
    "get_protocol_definition": Operation("GET", "/api/v1/protocols/{protocol}/JSON", ("protocol",)),
    "get_run_status": Operation("GET", "/api/v1/protocols/results/{run_id}", ("run_id",)),
    "get_measurement_status": Operation("GET", "/api/v1/gui/measurement-status"),
}

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


def error_for_status(status_code: int) -> CommandError:
    if status_code == 404:
        return CommandError("not_found", "Not found.")
    if status_code in (400, 422):
        return CommandError("invalid_parameters", "The parameters were rejected.")
    if status_code == 409:
        return CommandError("busy", "Another measurement is running.")
    return CommandError("internal", f"CAMELS answered with HTTP {status_code}.")


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
        path = build_path(operation, payload)
        response = await self._client.request(operation.method, path, timeout=30)
        if response.status_code >= 300:
            raise error_for_status(response.status_code)
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
