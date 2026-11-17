"""Tests for the outbound OASIS remote agent against a minimal fake broker."""

import asyncio
import json
import threading
import time
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

websockets = pytest.importorskip("websockets")
from websockets.asyncio.server import serve  # noqa: E402

from nomad_camels.api import remote_agent, remote_config  # noqa: E402
from nomad_camels.api.api import FastapiThread  # noqa: E402

TOKEN = "good-token"


class FakeBroker:
    """Runs a websockets server in a thread and records the agent's messages."""

    def __init__(self):
        self.messages = []
        self.connections = 0
        self.close_code = None  # close the first session with this code
        self.reject_status = None  # reject handshakes with this HTTP status
        self.loop = asyncio.new_event_loop()
        self.ws = None
        self.port = None
        self.connected = threading.Event()
        ready = threading.Event()
        self.thread = threading.Thread(target=self._run, args=(ready,), daemon=True)
        self.thread.start()
        assert ready.wait(5)

    def _run(self, ready):
        asyncio.set_event_loop(self.loop)

        async def main():
            self.stopped = asyncio.Event()
            async with serve(self._handler, "127.0.0.1", 0, process_request=self._check,
                             subprotocols=[remote_agent.SUBPROTOCOL]) as server:
                self.port = server.sockets[0].getsockname()[1]
                ready.set()
                await self.stopped.wait()

        self.loop.run_until_complete(main())
        self.loop.close()

    def _check(self, connection, request):
        if self.reject_status:
            return connection.respond(self.reject_status, "rejected\n")
        if request.headers.get("Authorization") != f"Bearer {TOKEN}":
            return connection.respond(401, "invalid token\n")
        return None

    async def _handler(self, ws):
        self.connections += 1
        hello = json.loads(await ws.recv())
        self.messages.append(hello)
        await ws.send(json.dumps({"version": 1, "type": "welcome", "id": "w", "session_id": "s1"}))
        self.ws = ws
        self.connected.set()
        if self.close_code:
            code, self.close_code = self.close_code, None
            await ws.close(code)
            return
        async for raw in ws:
            self.messages.append(json.loads(raw))

    @property
    def url(self):
        return f"ws://127.0.0.1:{self.port}/camels-remote/agent"

    def send(self, message):
        asyncio.run_coroutine_threadsafe(self.ws.send(json.dumps(message)), self.loop).result(5)

    def wait_for(self, predicate, timeout=5):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            for message in list(self.messages):
                if predicate(message):
                    return message
            time.sleep(0.02)
        raise AssertionError(f"no matching message in {self.messages}")

    def close(self):
        self.loop.call_soon_threadsafe(self.stopped.set)
        self.thread.join(5)


@pytest.fixture
def camels_app():
    main_window = MagicMock()
    main_window.protocols_dict = {
        "remote": SimpleNamespace(name="remote", description="", variables={"n": 3}, oasis_remote_control=True),
        "local": SimpleNamespace(name="local", description="", variables={}, oasis_remote_control=False),
    }
    main_window.get_measurement_status.return_value = {"status": "Idle", "protocol_name": ""}
    return FastapiThread(main_window, api_port=8000).get_agent_app()


@pytest.fixture
def broker():
    fake = FakeBroker()
    yield fake
    fake.close()


def wait_state(agent, state, timeout=10):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if agent.state == state:
            return
        time.sleep(0.02)
    raise AssertionError(f"agent state is {agent.state!r} ({agent.detail}), expected {state!r}")


def make_agent(broker, app, token=TOKEN):
    states = []
    agent = remote_agent.RemoteAgent(
        broker.url, token, app, camels_version="test",
        on_state=lambda state, detail: states.append(state),
        measurement_provider=lambda: {"status": "Idle"},
    )
    agent.states = states
    return agent


def command(broker, operation, payload=None, command_id="c1"):
    broker.send({"version": 1, "type": "command", "id": "m", "command_id": command_id,
                 "operation": operation, "payload": payload or {}})
    return broker.wait_for(lambda m: m.get("type") == "command_result" and m.get("command_id") == command_id)


def test_hello_and_list_protocols(broker, camels_app):
    agent = make_agent(broker, camels_app)
    agent.start()
    try:
        wait_state(agent, remote_agent.STATE_ONLINE)
        hello = broker.messages[0]
        assert hello["type"] == "hello"
        assert hello["version"] == 1
        assert "list_protocols" in hello["operations"]
        assert hello["measurement"] == {"status": "Idle"}

        result = command(broker, "list_protocols")
        # The agent sees only protocols enabled for remote control.
        assert result["status"] == "completed"
        assert result["result"] == {"Protocols": ["remote"]}
    finally:
        agent.stop()
    assert agent.state == remote_agent.STATE_STOPPED


def test_operations_and_errors(broker, camels_app):
    agent = make_agent(broker, camels_app)
    agent.start()
    try:
        wait_state(agent, remote_agent.STATE_ONLINE)
        schema = command(broker, "get_protocol_schema", {"protocol": "remote"}, "c1")
        assert schema["status"] == "completed"

        hidden = command(broker, "get_protocol_schema", {"protocol": "local"}, "c2")
        assert hidden["status"] == "rejected"
        assert hidden["error"]["code"] == "not_found"

        unknown = command(broker, "run_shell", {"cmd": "dir"}, "c3")
        assert unknown["error"]["code"] == "unknown_operation"

        bad = command(broker, "get_protocol_schema", {"protocol": 5}, "c4")
        assert bad["error"]["code"] == "invalid_parameters"

        # Path parameters are encoded, so they cannot reach other routes.
        escape = command(broker, "get_protocol_schema", {"protocol": "../../info"}, "c5")
        assert escape["error"]["code"] == "not_found"

        status = command(broker, "get_measurement_status", None, "c6")
        assert status["result"] == {"status": "Idle", "protocol_name": "", "remote_control_paused": False}
    finally:
        agent.stop()


@pytest.fixture
def control_app(tmp_path, monkeypatch):
    """Agent app whose main window can be made busy; run records go to tmp."""
    from nomad_camels.utility import load_save_functions

    monkeypatch.setattr(load_save_functions, "appdata_path", str(tmp_path))
    main_window = MagicMock()
    main_window.protocols_dict = {
        "remote": SimpleNamespace(name="remote", description="", variables={"n": 3}, oasis_remote_control=True),
    }
    main_window.busy = False
    main_window.measurement_busy = lambda: main_window.busy
    main_window.running_protocol = main_window.protocols_dict["remote"]
    main_window.get_measurement_status.return_value = {"status": "Running", "protocol_name": "remote"}
    thread = FastapiThread(main_window, api_port=8000)
    thread.started_runs = []
    thread.stopped = []
    thread.start_protocol_signal.connect(lambda *args: thread.started_runs.append(args))
    thread.stop_protocol_signal.connect(lambda: thread.stopped.append(True))
    thread.saved = []
    thread.save_protocol_variables_signal.connect(lambda *args: thread.saved.append(args))
    return main_window, thread


def test_control_operations(broker, control_app, qtbot):
    main_window, thread = control_app
    agent = make_agent(broker, thread.get_agent_app())
    agent.start()
    try:
        wait_state(agent, remote_agent.STATE_ONLINE)
        run_id = "0f8fad5b-d9cb-469f-a165-70867728950e"
        started = command(broker, "start_measurement",
                          {"protocol": "remote", "variables": {"n": 5}, "run_id": run_id}, "s1")
        assert started["status"] == "completed", started
        assert started["result"]["run_id"] == run_id
        # The signal reaches the GUI thread through its event loop.
        qtbot.waitUntil(lambda: thread.started_runs == [("remote", run_id, {"n": 5})])

        # The same run_id again (a retry) starts nothing.
        again = command(broker, "start_measurement",
                        {"protocol": "remote", "variables": {"n": 5}, "run_id": run_id}, "s2")
        assert again["result"]["duplicate"] is True
        qtbot.wait(100)
        assert len(thread.started_runs) == 1

        # A second measurement while one is running is refused, with CAMELS' reason.
        main_window.busy = True
        busy = command(broker, "start_measurement", {"protocol": "remote", "variables": {}}, "s3")
        assert busy["error"] == {"code": "busy", "message": "Another measurement is running in CAMELS."}

        unknown_variable = command(broker, "start_measurement",
                                   {"protocol": "remote", "variables": {"x": 1}}, "s4")
        assert unknown_variable["error"]["code"] in ("invalid_parameters", "busy")

        stopped = command(broker, "stop_measurement", None, "s5")
        assert stopped["result"] == {"status": "stopping", "protocol_name": "remote"}
        qtbot.waitUntil(lambda: thread.stopped == [True])

        main_window.busy = False
        idle = command(broker, "stop_measurement", None, "s6")
        assert idle["result"] == {"status": "idle"}

        saved = command(broker, "save_protocol_parameters",
                        {"protocol": "remote", "variables": {"n": 7}}, "s7")
        assert saved["status"] == "completed"
        qtbot.waitUntil(lambda: thread.saved == [("remote", {"n": 7})])

        not_object = command(broker, "save_protocol_parameters",
                             {"protocol": "remote", "variables": [1]}, "s8")
        assert not_object["error"]["code"] == "invalid_parameters"
    finally:
        agent.stop()


def test_paused_control_allows_only_reading(broker, control_app, qtbot):
    main_window, thread = control_app
    agent = make_agent(broker, thread.get_agent_app())
    agent.control_paused = True
    agent.start()
    try:
        wait_state(agent, remote_agent.STATE_ONLINE)
        for i, operation in enumerate(
            ["start_measurement", "stop_measurement", "save_protocol_parameters", "close_plots"]
        ):
            result = command(broker, operation, {"protocol": "remote", "variables": {}}, f"p{i}")
            assert result["error"]["code"] == "paused", operation
        qtbot.wait(100)
        assert thread.started_runs == [] and thread.stopped == []
        assert command(broker, "list_protocols", None, "r1")["status"] == "completed"
        status = command(broker, "get_measurement_status", None, "r3")["result"]
        assert status["remote_control_paused"] is True
        assert command(broker, "get_plot_data", None, "r2")["result"] == {"open_plot_count": 0, "plots": []}
    finally:
        agent.stop()


def test_plot_data_through_the_agent(broker, control_app):
    from nomad_camels.main_classes.remote_plot_cache import RemotePlotCache

    main_window, thread = control_app
    cache = RemotePlotCache(title="IV", x_label="V", y_label="I", y_names=["I"])
    thread.register_plot_cache("p1", cache)
    for i in range(3):
        cache.append(i, {"I": i * 2})
    agent = make_agent(broker, thread.get_agent_app())
    agent.start()
    try:
        wait_state(agent, remote_agent.STATE_ONLINE)
        first = command(broker, "get_plot_data", None, "d1")["result"]["plots"][0]
        assert first["x"] == [0, 1, 2] and first["traces"][0]["y"] == [0, 2, 4]
        cache.append(3, {"I": 6})
        cursor = {"p1": {"generation": first["generation"], "since": first["end"], "version": first["version"]}}
        # The cursor is sent as an object and reaches CAMELS as JSON.
        new = command(broker, "get_plot_data", {"cursor": cursor}, "d2")["result"]["plots"][0]
        assert new["reset"] is False and new["x"] == [3] and new["traces"][0]["y"] == [6]
        assert "fits" not in new
    finally:
        agent.stop()


def test_invalid_token_stops_retrying(broker, camels_app):
    agent = make_agent(broker, camels_app, token="bad")
    agent.start()
    try:
        wait_state(agent, remote_agent.STATE_UNAUTHORIZED)
        assert not agent.running or agent.state == remote_agent.STATE_UNAUTHORIZED
        time.sleep(0.3)
        assert broker.connections == 0
    finally:
        agent.stop()


@pytest.mark.parametrize(
    "code, state",
    [
        (remote_agent.CLOSE_REVOKED, remote_agent.STATE_UNAUTHORIZED),
        (remote_agent.CLOSE_REPLACED, remote_agent.STATE_REPLACED),
        (remote_agent.CLOSE_UNSUPPORTED_VERSION, remote_agent.STATE_OUTDATED),
    ],
)
def test_final_close_codes_stop_the_agent(broker, camels_app, code, state):
    broker.close_code = code
    agent = make_agent(broker, camels_app)
    agent.start()
    try:
        wait_state(agent, state)
        time.sleep(0.3)
        assert broker.connections == 1
    finally:
        agent.stop()


def test_reconnects_after_connection_loss(broker, camels_app, monkeypatch):
    monkeypatch.setattr(remote_agent.random, "uniform", lambda a, b: 0.1)
    broker.close_code = 1011
    agent = make_agent(broker, camels_app)
    agent.start()
    try:
        deadline = time.monotonic() + 10
        while broker.connections < 2 and time.monotonic() < deadline:
            time.sleep(0.05)
        assert broker.connections == 2
        wait_state(agent, remote_agent.STATE_ONLINE)
        assert remote_agent.STATE_RETRYING in agent.states
    finally:
        agent.stop()


def test_server_error_status_retries(broker, camels_app, monkeypatch):
    monkeypatch.setattr(remote_agent.random, "uniform", lambda a, b: 0.05)
    broker.reject_status = 502
    agent = make_agent(broker, camels_app)
    agent.start()
    try:
        wait_state(agent, remote_agent.STATE_RETRYING)
        assert "502" in agent.detail
        broker.reject_status = None
        wait_state(agent, remote_agent.STATE_ONLINE, timeout=15)
    finally:
        agent.stop()


# ----------------------------------------------------------------------
# remote_config
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "url, base",
    [
        ("oasis.example.org", "https://oasis.example.org"),
        ("https://10.188.162.32:8443/nomad-oasis/", "https://10.188.162.32:8443/nomad-oasis"),
        ("https://host/nomad-oasis/camels-remote", "https://host/nomad-oasis"),
        ("http://127.0.0.1:8000", "http://127.0.0.1:8000"),
    ],
)
def test_normalize_oasis_url(url, base):
    assert remote_config.normalize_oasis_url(url) == base


@pytest.mark.parametrize("url", ["http://10.188.162.32/nomad-oasis", "ftp://host", "https://host/?a=1", ""])
def test_normalize_oasis_url_rejects(url):
    with pytest.raises(remote_config.RemoteConfigError):
        remote_config.normalize_oasis_url(url)


def test_agent_url():
    assert remote_config.agent_url("https://h:8443/nomad-oasis") == "wss://h:8443/nomad-oasis/camels-remote/agent"
    assert remote_config.pair_url("https://h/x") == "https://h/x/camels-remote/pair"


def test_token_round_trip_is_not_plain_text_on_windows():
    stored = remote_config.protect_token("secret-token-value")
    assert remote_config.unprotect_token(stored) == "secret-token-value"
    if stored["scheme"] == "dpapi":
        assert "secret-token-value" not in json.dumps(stored)


def test_config_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(remote_config.load_save_functions, "appdata_path", str(tmp_path))
    assert remote_config.load_config().paired is False
    config = remote_config.RemoteConfig(enabled=True, oasis_url="https://h", device_id="dev_1",
                                        token=remote_config.protect_token("t"))
    remote_config.save_config(config)
    loaded = remote_config.load_config()
    assert loaded.paired and loaded.enabled
    assert remote_config.unprotect_token(loaded.token) == "t"
    assert remote_config.unpair().paired is False



# ----------------------------------------------------------------------
# Settings dialog
# ----------------------------------------------------------------------
def test_remote_control_dialog(qtbot, tmp_path, monkeypatch):
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import QWidget
    from nomad_camels.frontpanels.remote_control_dialog import Remote_Control_Dialog

    monkeypatch.setattr(remote_config.load_save_functions, "appdata_path", str(tmp_path))

    class FakeMainWindow(QWidget):
        remote_agent_state_signal = Signal(str, str)

        def __init__(self):
            super().__init__()
            self.remote_agent_state = ("stopped", "")
            self.started = 0
            self.stopped = 0

        def start_remote_agent(self):
            self.started += 1

        def stop_remote_agent(self):
            self.stopped += 1

    main_window = FakeMainWindow()
    qtbot.addWidget(main_window)
    dialog = Remote_Control_Dialog(main_window)
    assert dialog.label_device.text() == "not paired"
    assert not dialog.checkBox_enable.isEnabled()

    # A failed pairing shows the reason and stores nothing.
    dialog.lineEdit_url.setText("http://10.0.0.1")
    dialog.lineEdit_code.setText("ABCD-EFGH")
    dialog.pair()
    assert "https" in dialog.label_state.text()
    assert not remote_config.load_config().paired

    # A successful pairing enables remote control and starts the agent.
    def fake_pair(url, code, ca_file=""):
        config = remote_config.RemoteConfig(oasis_url="https://oasis", device_id="dev_1",
                                            device_name="Lab", token=remote_config.protect_token("t"))
        remote_config.save_config(config)
        return config

    monkeypatch.setattr(remote_config, "pair", fake_pair)
    dialog.lineEdit_url.setText("https://oasis")
    dialog.pair()
    assert remote_config.load_config().enabled
    assert main_window.started == 1
    assert dialog.checkBox_enable.isChecked()
    assert "dev_1" in dialog.label_device.text()

    main_window.remote_agent_state_signal.emit("online", "session x")
    assert dialog.label_state.text() == "Connected"

    dialog.checkBox_enable.setChecked(False)
    assert not remote_config.load_config().enabled
    assert main_window.stopped >= 2

    dialog.unpair()
    assert not remote_config.load_config().paired
    assert dialog.label_device.text() == "not paired"
    dialog.close()
