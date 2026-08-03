from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from PySide6.QtCore import QThread, Signal
from nomad_camels.frontpanels.settings_window import hash_api_key
from nomad_camels.utility import load_save_functions
import uvicorn
import sqlite3
import os
import json
import uuid
from pydantic import BaseModel, Field
import math
import asyncio


def sanitize_dict(d):
    """
    Recursively sanitize a dictionary by replacing infinite and NaN float values.

    This function iterates over the provided dictionary and its nested dictionaries or lists.
    If a float value is found that is infinite or NaN, it is replaced with a string
    ("inf" or "nan", respectively).

    Args:
        d (dict): The dictionary to sanitize.

    Returns:
        dict: The sanitized dictionary with infinite or NaN floats replaced by string representations.
    """
    for key, value in d.items():
        if isinstance(value, float):
            if math.isinf(value):
                d[key] = "inf"  # Replace with None or another placeholder
            if math.isnan(value):
                d[key] = "nan"
        elif isinstance(value, dict):
            sanitize_dict(value)
        elif isinstance(value, list):
            for i in range(len(value)):
                if isinstance(value[i], float):
                    if math.isinf(value[i]):
                        value[i] = "inf"  # Replace with None or another placeholder
                    if math.isnan(value[i]):
                        value[i] = "nan"
                elif isinstance(value[i], dict):
                    sanitize_dict(value[i])
    return d


class Variables(BaseModel):
    """
    Pydantic model for passing variables to a protocol.

    Attributes:
        variables (dict): A dictionary containing key-value pairs to be passed to the protocol.
    """

    variables: dict = Field(
        ...,
        json_schema_extra={
            "description": "A dictionary of variables to pass to the protocol",
            "example": {"key1": "value1", "key2": "value2"},
        },
    )


class ProtocolRunResponse(BaseModel):
    """
    Pydantic model for the protocol run response.

    Attributes:
        check_protocol_status_here (str): A URL endpoint to check the status of the protocol run.
    """

    check_protocol_status_here: str = Field(
        ..., description="A URL to check the protocol status"
    )


def protocol_run_response(protocol_uuid: str) -> dict:
    """Build the stable response used by OASIS after a protocol was started."""
    status_url = f"/api/v1/protocols/results/{protocol_uuid}"
    return {
        # Keep the existing field for backwards compatibility with API clients.
        "check protocol status here": status_url,
        "run_id": protocol_uuid,
        "status_url": status_url,
        "result_url": f"{status_url}/file",
    }


def validate_api_key(api_key: str) -> bool:
    """
    Validate the given API key by checking its hashed value in the database.

    This function connects to the SQLite database, hashes the provided API key, and then
    queries the `api_keys` table to verify if the key exists.

    Args:
        api_key (str): The API key to validate.

    Returns:
        bool: True if the API key is valid, False otherwise.

    Raises:
        sqlite3.OperationalError: If an unexpected database error occurs.
    """
    # Establish the SQLite connection and cursor
    data_base_path = os.path.join(load_save_functions.appdata_path, "CAMELS_API.db")
    conn = sqlite3.connect(data_base_path)
    c = conn.cursor()
    hashed_key = hash_api_key(api_key)
    # Catch exception where the api:keys table does not exist anymore
    try:
        c.execute("SELECT * FROM api_keys WHERE key = ?", (hashed_key,))
    except sqlite3.OperationalError as e:
        if "no such table: api_keys" in str(e):
            conn.close()
            return False
        else:
            raise e  # Re-raise the exception if it's not the specific one we're looking for
    result = c.fetchone()
    conn.close()
    return result is not None


def get_api_key_protocol_scope(api_key: str):
    """Return the protocols allowed by a key, or ``None`` for a global key."""
    data_base_path = os.path.join(load_save_functions.appdata_path, "CAMELS_API.db")
    conn = sqlite3.connect(data_base_path)
    try:
        c = conn.cursor()
        columns = {row[1] for row in c.execute("PRAGMA table_info(api_keys)")}
        # Keys created by older CAMELS versions were global keys.
        if "protocol_name" not in columns:
            return None
        hashed_key = hash_api_key(api_key)
        rows = c.execute(
            "SELECT protocol_name FROM api_keys WHERE key = ?", (hashed_key,)
        ).fetchall()
    finally:
        conn.close()
    if any(row[0] is None for row in rows):
        return None
    return {row[0] for row in rows if row[0]}


def write_protocol_result_path_to_db(
    api_uuid, message="currently running", protocol_name=None
):
    """
    Write or update the protocol run status in the database.

    This function ensures that the table exists, then inserts or replaces a record
    with the provided UUID and status message.

    Args:
        api_uuid (str): The unique identifier for the protocol run.
        message (str, optional): The status message. Defaults to "currently running".
    """
    # Database setup
    data_base_path = os.path.join(load_save_functions.appdata_path, "CAMELS_API.db")
    conn = sqlite3.connect(data_base_path, check_same_thread=False)
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS protocol_run_status (
            uuid TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            protocol_name TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()

    columns = {row[1] for row in c.execute("PRAGMA table_info(protocol_run_status)")}
    if "protocol_name" not in columns:
        c.execute("ALTER TABLE protocol_run_status ADD COLUMN protocol_name TEXT")
        conn.commit()

    # Preserve the protocol name when the GUI later replaces the status with a file path.
    c.execute(
        """
        INSERT INTO protocol_run_status (uuid, status, protocol_name)
        VALUES (?, ?, ?)
        ON CONFLICT(uuid) DO UPDATE SET
            status = excluded.status,
            protocol_name = COALESCE(excluded.protocol_name, protocol_run_status.protocol_name)
        """,
        (api_uuid, message, protocol_name),
    )
    conn.commit()
    # Close the database connection
    conn.close()


def is_valid_path(file_path):
    """
    Check if the provided file path exists.

    Args:
        file_path (str): The file path to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


def cast_or_create_uuid_str(_uuid: uuid.UUID = None) -> str:
    """
    Cast a UUID to a string or create a new one if not provided.

    Args:
        _uuid (uuid.UUID, optional): The UUID to cast. If None, a new UUID is created. Defaults to None.

    Returns:
        str: The string representation of the UUID.
    """
    if _uuid is None:
        return str(uuid.uuid4())
    else:
        return str(_uuid)


# Initialize HTTP Bearer Authentication
security = HTTPBearer()


async def validate_credentials(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Validate the API credentials provided via HTTP Bearer authentication.

    This function checks the provided credentials against the stored API keys. If the key
    is valid, it returns True; otherwise, it raises an HTTPException with a 401 status code.

    Args:
        credentials (HTTPAuthorizationCredentials): The credentials extracted from the request.

    Returns:
        bool: True if credentials are valid.

    Raises:
        HTTPException: If the API key is invalid.
    """
    api_key = credentials.credentials
    # The api_key is directly taken from credentials.password
    if api_key and validate_api_key(api_key):
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "Bearer"},
    )


class FastapiThread(QThread):
    """
    QThread subclass to run a FastAPI server in a separate thread to avoid blocking the GUI.

    Signals:
        start_protocol_signal (Signal): Signal to start a protocol.
        port_error_signal (Signal): Signal to send error messages related to the API port.
        set_user_signal (Signal): Signal to update the active user.
        set_sample_signal (Signal): Signal to update the active sample.
        set_session_signal (Signal): Signal to update the active session.
        queue_protocol_signal (Signal): Signal to queue a protocol without variables.
        remove_queue_protocol_signal (Signal): Signal to remove a protocol from the queue.
        set_checkbox_signal (Signal): Signal to check the next protocol in the queue.
        queue_protocol_with_variables_signal (Signal): Signal to queue a protocol with variables.
        change_variables_queued_protocol_signal (Signal): Signal to update variables of a queued protocol.
    """

    # Define signals for communicating with the main window
    start_protocol_signal = Signal(str, str, object)
    port_error_signal = Signal(str)
    set_user_signal = Signal(str)
    set_sample_signal = Signal(str)
    set_session_signal = Signal(str)
    queue_protocol_signal = Signal(str, str)
    remove_queue_protocol_signal = Signal(str)
    set_checkbox_signal = Signal(str)
    queue_protocol_with_variables_signal = Signal(str, dict, int, str)
    change_variables_queued_protocol_signal = Signal(str, dict, int)
    close_plots_signal = Signal()

    def __init__(self, main_window, api_port):
        """
        Initialize the FastapiThread with the main window and API port.

        Args:
            main_window: Reference to the main application window for accessing settings and protocol data.
            api_port (int or str): The port number on which the FastAPI server will run.
        """
        super().__init__()
        # get the main window so that we have access to all the settings and dictionaries
        self.main_window = main_window
        self.api_port = api_port
        self.protocol_runs = {}  # Dictionary to store the protocol runs
        self.app = None
        self.server = None
        self.loop = None  # Custom asyncio loop
        self._stop_requested = False

    def run(self):
        """
        Run the FastAPI server in this thread.

        This method initializes the FastAPI application, defines all the API routes, creates a new
        asyncio event loop, and starts the Uvicorn server until completion.
        """
        try:
            self.app = FastAPI()  # Initialize FastAPI app
            self.define_routes(self.app)  # Define the API routes
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.start_server())
        except Exception as exc:
            # A failed API must never take down the Qt application. In
            # particular, malformed or occupied ports used to escape the
            # coroutine before the error signal could be emitted.
            print(f"Error starting FastAPI: {exc}")
            self.port_error_signal.emit(f"Failed to start server: {exc}")
        finally:
            if self.loop is not None and not self.loop.is_closed():
                self.loop.close()

    async def start_server(self):
        """
        Start the FastAPI server using Uvicorn within the asyncio event loop.

        This asynchronous method configures Uvicorn with the FastAPI application and attempts to
        serve the API. In case of an error, it emits a port error signal.
        """
        try:
            port = int(self.api_port)
            if not 1 <= port <= 65535:
                raise ValueError("API port must be between 1 and 65535")
            config = uvicorn.Config(
                self.app,
                host="0.0.0.0",
                port=port,
                log_level="warning",
                access_log=False,
                reload=False,
                workers=1,  # Ensure only one worker to avoid multi-thread issues
            )
            self.server = uvicorn.Server(config)
            await self.server.serve()
            if not self.server.started and not self._stop_requested:
                raise RuntimeError(f"API server could not bind to port {port}")
        except Exception as e:
            print(f"Error starting FastAPI: {e}")
            self.port_error_signal.emit(f"Failed to start server: {e}")

    def stop_server(self):
        """
        Safely shut down the FastAPI server.

        This method signals the Uvicorn server to exit and stops the QThread.
        """
        self._stop_requested = True
        if self.server is not None:
            print("Stopping FastAPI server...")
            if self.loop is not None and self.loop.is_running():
                self.loop.call_soon_threadsafe(
                    setattr, self.server, "should_exit", True
                )
            else:
                self.server.should_exit = True
        # ``quit`` does not stop Uvicorn's asyncio loop. Use a bounded wait so
        # an API shutdown problem cannot freeze or terminate the CAMELS GUI.
        if not self.wait(3000):
            print("FastAPI server is still stopping in the background.")

    def define_routes(self, app: FastAPI):
        """
        Define all API routes for the FastAPI server.

        Args:
            app (FastAPI): The FastAPI application instance on which routes are defined.

        Note:
            The following route definitions include endpoints for retrieving protocols,
            settings, running protocols (with and without variables), managing the protocol queue,
            and various helper endpoints (e.g., for user and sample management).
        """

        def get_protocol_by_name(protocol_name: str):
            """Find a protocol by its current display name or dictionary key."""
            protocol = self.main_window.protocols_dict.get(protocol_name)
            if protocol is not None:
                return protocol
            return next(
                (
                    candidate
                    for candidate in self.main_window.protocols_dict.values()
                    if candidate.name == protocol_name
                ),
                None,
            )

        def get_oasis_protocol(protocol_name: str, api_key: str):
            """Return an externally enabled protocol or a non-enumerating 404."""
            protocol = get_protocol_by_name(protocol_name)
            allowed_protocols = get_api_key_protocol_scope(api_key)
            if (
                protocol is None
                or not getattr(protocol, "oasis_remote_control", False)
                or (
                    allowed_protocols is not None
                    and protocol_name not in allowed_protocols
                )
            ):
                raise HTTPException(status_code=404, detail="Protocol not found")
            return protocol

        def require_global_api_key(api_key: str):
            """Protect legacy global-control endpoints from protocol-scoped keys."""
            if get_api_key_protocol_scope(api_key) is not None:
                raise HTTPException(
                    status_code=403,
                    detail="This API key is limited to a specific protocol.",
                )

        @app.get("/api/v1/health")
        async def health():
            """Unauthenticated liveness endpoint for the OASIS backend."""
            return {"status": "ok", "api_version": "v1"}

        @app.get("/api/v1/protocols")
        async def get_protocols(api_key: str = Depends(validate_credentials)):
            """
            Retrieve the list of available protocols.

            Args:
                api_key (str): API key for authentication (validated via dependency).

            Returns:
                JSONResponse: A JSON response containing the list of protocol names.
            """
            allowed_protocols = get_api_key_protocol_scope(api_key)
            protocols = [
                protocol.name
                for protocol in self.main_window.protocols_dict.values()
                if getattr(protocol, "oasis_remote_control", False)
                and (
                    allowed_protocols is None
                    or protocol.name in allowed_protocols
                )
            ]
            return JSONResponse(content={"Protocols": protocols})

        @app.get("/api/v1/protocols/variables/{protocol_name}")
        async def get_protocol_variables(
            protocol_name: str, api_key: str = Depends(validate_credentials)
        ):
            """
            Retrieve the available variables for a specific protocol.

            Args:
                protocol_name (str): The name of the protocol.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response containing a list of acceptable variables for the protocol.
            """
            protocol = get_oasis_protocol(protocol_name, api_key)
            return JSONResponse(content={"Variables": list(protocol.variables)})

        @app.get("/api/v1/protocols/{protocol_name}/schema")
        async def get_protocol_schema(
            protocol_name: str, api_key: str = Depends(validate_credentials)
        ):
            """Return the editable parameter names and their CAMELS defaults.

            OASIS uses this endpoint to build the protocol form. CAMELS remains
            the authority that accepts or rejects submitted variable names.
            """
            protocol = get_oasis_protocol(protocol_name, api_key)
            return JSONResponse(
                content={
                    "protocol_name": protocol.name,
                    "description": protocol.description,
                    "parameters": sanitize_dict(dict(protocol.variables)),
                }
            )

        @app.get("/api/v1/protocols/{protocol_name}/JSON")
        async def get_protocol_json(
            protocol_name: str, api_key: str = Depends(validate_credentials)
        ):
            """
            Retrieve a JSON representation of the specified protocol.

            Args:
                protocol_name (str): The name of the protocol.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response containing the sanitized protocol details.
            """
            protocol_class_instance = get_oasis_protocol(protocol_name, api_key)
            protocol = load_save_functions.get_save_str(protocol_class_instance)
            cleaned_protocol = sanitize_dict(protocol)
            return JSONResponse(
                content=cleaned_protocol,
            )

        @app.get("/api/v1/settings/JSON")
        async def get_settings_json(api_key: str = Depends(validate_credentials)):
            """
            Retrieve a JSON representation of the current CAMELS settings.

            Args:
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response containing the sanitized settings.
            """
            require_global_api_key(api_key)
            settings = self.main_window.preferences
            cleaned_settings = sanitize_dict(settings)
            return JSONResponse(
                content=cleaned_settings,
            )

        @app.get("/api/v1/gui/plots")
        async def get_open_plot_count(
            api_key: str = Depends(validate_credentials),
        ):
            """Return the number of currently open CAMELS plot windows."""
            return JSONResponse(
                content={"open_plot_count": len(self.main_window.open_plots)}
            )

        @app.post("/api/v1/gui/plots/close")
        async def close_open_plots(
            api_key: str = Depends(validate_credentials),
        ):
            """Close CAMELS plot windows through the GUI thread."""
            open_plot_count = len(self.main_window.open_plots)
            self.close_plots_signal.emit()
            return JSONResponse(
                content={"closed_plot_count": open_plot_count, "status": "requested"}
            )

        @app.get("/api/v1/gui/pid-plots")
        async def get_pid_plots(
            api_key: str = Depends(validate_credentials),
        ):
            """Return live PID-controller plot data for the active scoped run."""
            running_protocol = getattr(self.main_window, "running_protocol", None)
            if running_protocol is None:
                return JSONResponse(content={"pid_plots": []})

            # A protocol-scoped key may view only the PID devices belonging to
            # the protocol it is currently allowed to control.
            get_oasis_protocol(running_protocol.name, api_key)
            devices = getattr(self.main_window, "current_protocol_devices", {}) or {}
            pid_plots = []
            for device_name, device in devices.items():
                snapshot = getattr(device, "get_plot_data_snapshot", None)
                if callable(snapshot):
                    pid_plots.append(
                        {"device_name": device_name, **sanitize_dict(snapshot())}
                    )
            return JSONResponse(content={"pid_plots": pid_plots})

        @app.get(
            "/api/v1/actions/run/protocols/{protocol_name}",
            response_model=ProtocolRunResponse,
        )
        async def run_protocol(
            protocol_name: str,
            protocol_uuid: uuid.UUID = None,
            api_key: str = Depends(validate_credentials),
        ):
            """
            Run a protocol by its name.

            This endpoint initiates a protocol run by generating (or using) a UUID, storing the run status
            in the database, and emitting a signal to start the protocol.

            Args:
                protocol_name (str): The name of the protocol to run.
                protocol_uuid (uuid.UUID, optional): An optional UUID for the run. Defaults to None.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response with a URL to check the protocol run status.
            """
            get_oasis_protocol(protocol_name, api_key)
            # Generate or use the provided syntax checked UUID as casted string
            protocol_uuid = cast_or_create_uuid_str(_uuid=protocol_uuid)

            write_protocol_result_path_to_db(
                protocol_uuid, protocol_name=protocol_name
            )

            self.start_protocol_signal.emit(str(protocol_name), protocol_uuid, None)
            return JSONResponse(content=protocol_run_response(protocol_uuid))

        @app.post(
            "/api/v1/actions/run/protocols/{protocol_name}",
            response_model=ProtocolRunResponse,
        )
        async def run_protocol_with_variables(
            protocol_name: str,
            variables: Variables,
            protocol_uuid: uuid.UUID = None,
            api_key: str = Depends(validate_credentials),
        ):
            """
            Run a protocol with provided variables.

            This endpoint checks that the provided variables are accepted by the protocol,
            stores the run status in the database, and emits a signal to start the protocol with variables.

            Args:
                protocol_name (str): The name of the protocol.
                variables (Variables): A Pydantic model containing the variables to pass.
                protocol_uuid (uuid.UUID, optional): An optional UUID for the run. Defaults to None.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response with a URL to check the protocol run status.

            Raises:
                HTTPException: If any variable provided is not accepted by the protocol.
            """
            # Get dictionary from the variables model
            variables = variables.model_dump()
            protocol = get_oasis_protocol(protocol_name, api_key)
            accepted_variables = protocol.variables
            # Check if all variables are in accepted variables
            for key in variables["variables"]:
                if key not in accepted_variables:
                    print(
                        f"Variable {key} is not accepted by the protocol {protocol_name}"
                    )
                    raise HTTPException(
                        status_code=400,
                        detail=f"Variable {key} is not accepted by the protocol {protocol_name}",
                    )

            # Generate or use the provided syntax checked UUID as casted string
            protocol_uuid = cast_or_create_uuid_str(_uuid=protocol_uuid)

            write_protocol_result_path_to_db(
                protocol_uuid, protocol_name=protocol_name
            )

            self.start_protocol_signal.emit(
                str(protocol_name), protocol_uuid, variables["variables"]
            )
            return JSONResponse(content=protocol_run_response(protocol_uuid))

        @app.get("/api/v1/protocols/results/{protocol_uuid}")
        async def get_protocol_status(
            protocol_uuid: str, api_key: str = Depends(validate_credentials)
        ):
            """
            Retrieve the status of a protocol run by its UUID.

            This endpoint queries the database for the protocol run status.

            Args:
                protocol_uuid (str): The UUID of the protocol run.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response containing the protocol run status or an error if not found.
            """
            # Database setup
            data_base_path = os.path.join(
                load_save_functions.appdata_path, "CAMELS_API.db"
            )
            conn = sqlite3.connect(data_base_path, check_same_thread=False)
            c = conn.cursor()

            # Query the status of the protocol run by UUID
            c.execute(
                """
                SELECT status, protocol_name FROM protocol_run_status WHERE uuid = ?
                """,
                (protocol_uuid,),
            )
            result = c.fetchone()
            # Close the database connection
            conn.close()
            allowed_protocols = get_api_key_protocol_scope(api_key)
            if result and (
                allowed_protocols is None or result[1] in allowed_protocols
            ):
                return JSONResponse(
                    content={"uuid": protocol_uuid, "status": result[0]}
                )
            else:
                return JSONResponse(
                    content={"error": "UUID not found"}, status_code=404
                )

        @app.get("/api/v1/protocols/results/{protocol_uuid}/file")
        async def get_protocol_hdf5(
            protocol_uuid: str, api_key: str = Depends(validate_credentials)
        ):
            """
            Retrieve the HDF5 file generated by a successful protocol run.

            This endpoint checks the status in the database and returns the file if the protocol has finished.

            Args:
                protocol_uuid (str): The UUID of the protocol run.
                api_key (str): API key for authentication.

            Returns:
                FileResponse or JSONResponse: The HDF5 file as a FileResponse if available,
                otherwise a JSON error message with an appropriate status code.
            """
            # Database setup
            data_base_path = os.path.join(
                load_save_functions.appdata_path, "CAMELS_API.db"
            )
            conn = sqlite3.connect(data_base_path, check_same_thread=False)
            c = conn.cursor()

            # Query the status of the protocol run by UUID
            c.execute(
                """
                SELECT status, protocol_name FROM protocol_run_status WHERE uuid = ?
                """,
                (protocol_uuid,),
            )
            result = c.fetchone()
            allowed_protocols = get_api_key_protocol_scope(api_key)
            if result is None or (
                allowed_protocols is not None and result[1] not in allowed_protocols
            ):
                conn.close()
                return JSONResponse(
                    content={"error": "UUID not found"}, status_code=404
                )
            status = result[0]
            if status == "currently running":
                return JSONResponse(
                    content={
                        "error": "Protocol is currently running. You can access the results once the protocol has finished."
                    },
                    status_code=202,
                )
            if status == "added to queue":
                return JSONResponse(
                    content={
                        "error": "Protocol is in the queue and was not started yet. You can access the results once the protocol has finished."
                    },
                    status_code=202,
                )
            file_path = os.path.abspath(status)
            # Close the database connection
            conn.close()
            if file_path:
                if is_valid_path(file_path):
                    return FileResponse(file_path, filename=os.path.basename(file_path))
                else:
                    return JSONResponse(
                        content={"error": "File does not exists"}, status_code=404
                    )
            else:
                return JSONResponse(
                    content={"error": "UUID not found"}, status_code=404
                )

        def get_live_plot_ports(protocol_uuid: str, api_key: str):
            """Return browser-plot ports for the currently active API run."""
            get_protocol_status(protocol_uuid, api_key)
            if getattr(self.main_window, "active_api_uuid", None) != protocol_uuid:
                return []
            module = getattr(self.main_window, "protocol_module", None)
            return list(getattr(module, "web_ports", [])) if module else []

        @app.get("/api/v1/runs/{protocol_uuid}/data")
        async def get_live_plot_data(
            protocol_uuid: str, api_key: str = Depends(validate_credentials)
        ):
            ports = get_live_plot_ports(protocol_uuid, api_key)
            return JSONResponse(content={
                "run_id": protocol_uuid,
                "plot_urls": [f"http://127.0.0.1:{port}/data" for port in ports],
            })

        @app.get("/api/v1/runs/{protocol_uuid}/plotly", response_class=HTMLResponse)
        async def get_live_plotly_page(
            protocol_uuid: str, api_key: str = Depends(validate_credentials)
        ):
            ports = get_live_plot_ports(protocol_uuid, api_key)
            frames = "".join(
                f'<iframe src="http://127.0.0.1:{port}/" title="CAMELS Plot" '
                'style="width:100%;height:620px;border:0"></iframe>'
                for port in ports
            )
            if not frames:
                frames = "<p>No browser Plotly widget is active for this run.</p>"
            return HTMLResponse(f"<html><body>{frames}</body></html>")

        @app.get("/api/v1/queue")
        async def get_queue(api_key: str = Depends(validate_credentials)):
            """
            Retrieve the current protocol queue.

            Args:
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response containing the list of queued protocols with their indexes.
            """
            require_global_api_key(api_key)
            protocols = list(
                self.main_window.run_queue_widget.protocol_name_variables.values()
            )
            indexed_protocols = [
                [index] + protocol for index, protocol in enumerate(protocols)
            ]
            return JSONResponse(content=indexed_protocols)

        @app.get("/api/v1/actions/queue/protocols/{protocol_name}")
        async def queue_protocol(
            protocol_name: str,
            protocol_uuid: uuid.UUID = None,
            api_key: str = Depends(validate_credentials),
        ):
            """
            Add a protocol to the queue by its name.

            This endpoint generates (or uses) a UUID, writes the status "added to queue" to the database,
            and emits a signal to add the protocol to the queue.

            Args:
                protocol_name (str): The name of the protocol.
                protocol_uuid (uuid.UUID, optional): An optional UUID for the run. Defaults to None.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response indicating success along with the UUID of the queued protocol.

            Raises:
                HTTPException: If the protocol could not be added to the queue.
            """
            require_global_api_key(api_key)
            # Generate or use the provided syntax checked UUID as casted string
            protocol_uuid = cast_or_create_uuid_str(_uuid=protocol_uuid)
            write_protocol_result_path_to_db(protocol_uuid, "added to queue")
            try:
                self.queue_protocol_signal.emit(str(protocol_name), protocol_uuid)
            except ValueError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to add protocol {protocol_name} to queue as the protocol was not found.\n{e}",
                ) from e
            await asyncio.sleep(0.05)
            protocol_values = list(
                self.main_window.run_queue_widget.protocol_name_variables.values()
            )
            if len(protocol_values) > 0:
                # Get the name of the last protocol in the queue
                last_protocol = protocol_values[-1]
                last_protocol_name = last_protocol[0]
                # Check if the provided protocol name matches the last one in the queue
                if protocol_name == last_protocol_name:
                    return JSONResponse(
                        content={
                            "status": "success adding protocol to queue",
                            "uuid": protocol_uuid,
                        }
                    )
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to add protocol {protocol_name} to queue as the protocol was not found.",
                    )
            else:
                # Return a failure response if the queue is empty
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to add protocol {protocol_name} to queue as the protocol was not found.",
                )

        @app.post("/api/v1/actions/queue/protocols/{protocol_name}")
        async def queue_protocol_with_variables(
            protocol_name: str,
            variables: Variables,
            protocol_uuid: uuid.UUID = None,
            api_key: str = Depends(validate_credentials),
        ):
            """
            Add a protocol with variables to the queue.

            This endpoint validates the provided variables, writes the status "added to queue" to the database,
            and emits a signal to add the protocol along with its variables to the queue.

            Args:
                protocol_name (str): The name of the protocol.
                variables (Variables): The variables to pass to the protocol.
                protocol_uuid (uuid.UUID, optional): An optional UUID for the run. Defaults to None.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response indicating success along with the UUID of the queued protocol.

            Raises:
                HTTPException: If the protocol could not be added to the queue.
            """
            require_global_api_key(api_key)
            # Get dictionary from the variables model
            variables = variables.model_dump()
            # Generate or use the provided syntax checked UUID as casted string
            protocol_uuid = cast_or_create_uuid_str(_uuid=protocol_uuid)
            write_protocol_result_path_to_db(protocol_uuid, "added to queue")

            try:
                self.queue_protocol_with_variables_signal.emit(
                    str(protocol_name),
                    variables["variables"],
                    -1,
                    protocol_uuid,
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to add protocol {protocol_name} to queue as the protocol was not found.\n{e}",
                ) from e
            await asyncio.sleep(0.05)
            protocol_values = list(
                self.main_window.run_queue_widget.protocol_name_variables.values()
            )
            if len(protocol_values) > 0:
                # Get the name of the last protocol in the queue
                last_protocol = protocol_values[-1]
                last_protocol_name = last_protocol[0]
                # Check if the provided protocol name matches the last one in the queue
                if protocol_name == last_protocol_name:
                    return JSONResponse(
                        content={
                            "status": "success adding protocol to queue",
                            "uuid": protocol_uuid,
                        }
                    )
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to add protocol {protocol_name} to queue as the protocol was not found.",
                    )
            else:
                # Return a failure response if the queue is empty
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to add protocol {protocol_name} to queue as the protocol was not found.",
                )

        @app.post("/api/v1/actions/queue/variables/protocols/{protocol_name}_{index}")
        async def change_variables_queued_protocol(
            protocol_name: str,
            index: int,
            variables: Variables,
            api_key: str = Depends(validate_credentials),
        ):
            """
            Change the variables for a protocol that is already in the queue.

            This endpoint validates and updates the variables for a protocol present in the queue,
            emitting a signal to update the variables in the user interface.

            Args:
                protocol_name (str): The name of the protocol.
                index (int): The index position of the protocol in the queue.
                variables (Variables): The new variables to set.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response indicating whether the update was successful.

            Raises:
                HTTPException: If the protocol is not found in the queue.
            """
            require_global_api_key(api_key)
            # Get dictionary from the variables model
            variables = variables.model_dump()
            # Get the current queue
            queue_response = await get_queue(api_key)
            # Extract the queue content from the JSON response
            queue_content = queue_response.body.decode("utf-8")
            queue_list = json.loads(queue_content)
            qt_items = list(
                self.main_window.run_queue_widget.protocol_name_variables.keys()
            )
            # make negative indexes work
            if index < 0:
                index = len(qt_items) + index
            for item in queue_list:
                if item[1] == protocol_name and item[0] == index:
                    try:
                        self.change_variables_queued_protocol_signal.emit(
                            str(qt_items[index]),
                            variables["variables"],
                            index,
                        )
                    except ValueError as e:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Failed to update protocol {protocol_name} in queue as the protocol was not found.\n{e}",
                        ) from e
            await asyncio.sleep(0.05)
            protocol_values = list(
                self.main_window.run_queue_widget.protocol_name_variables.values()
            )
            if len(protocol_values) > 0:
                # Get the name of the last protocol in the queue
                last_protocol = protocol_values[-1]
                last_protocol_name = last_protocol[0]
                # Check if the provided protocol name matches the last one in the queue
                if protocol_name == last_protocol_name:
                    return JSONResponse(
                        content={"status": "success updating protocol in queue"}
                    )
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to update protocol {protocol_name} in queue as the protocol was not found.",
                    )
            else:
                # Return a failure response if the queue is empty
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to update protocol {protocol_name} in queue as the protocol was not found.",
                )

        @app.get("/api/v1/actions/queue/remove/protocols/{protocol_name}_{index}")
        async def remove_protocol(
            protocol_name: str, index: int, api_key: str = Depends(validate_credentials)
        ):
            """
            Remove a protocol from the queue based on its name and position.

            Args:
                protocol_name (str): The name of the protocol.
                index (int): The index position of the protocol in the queue.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response indicating the success of the removal.

            Raises:
                HTTPException: If the protocol is not found at the given position.
            """
            require_global_api_key(api_key)
            # Get the current queue
            queue_response = await get_queue(api_key)
            # Extract the queue content from the JSON response
            queue_content = queue_response.body.decode("utf-8")
            queue_list = json.loads(queue_content)
            qt_items = list(
                self.main_window.run_queue_widget.protocol_name_variables.keys()
            )
            # Negative index work as well
            if index < 0:
                index = len(qt_items) + index
            for item in queue_list:
                if item[1] == protocol_name and item[0] == index:
                    self.remove_queue_protocol_signal.emit(str(qt_items[index]))
                    return JSONResponse(
                        content={"status": "success removing protocol from queue"}
                    )
            raise HTTPException(
                status_code=500,
                detail=f"Failed to remove protocol {protocol_name} with index {index} from queue as the protocol was not found at that position.",
            )

        @app.get("/api/v1/actions/queue/ready/protocols/{protocol_name}_{index}")
        async def protocol_ready(
            protocol_name: str, index: int, api_key: str = Depends(validate_credentials)
        ):
            """
            Mark a protocol in the queue as ready by checking its checkbox.

            Args:
                protocol_name (str): The name of the protocol.
                index (int): The index position of the protocol in the queue.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response indicating the success of the operation.

            Raises:
                HTTPException: If the protocol is not found at the specified position.
            """
            require_global_api_key(api_key)
            # Get the current queue
            queue_response = await get_queue(api_key)
            # Extract the queue content from the JSON response
            queue_content = queue_response.body.decode("utf-8")
            queue_list = json.loads(queue_content)
            qt_items = list(
                self.main_window.run_queue_widget.protocol_name_variables.keys()
            )
            if index < 0:
                index = len(qt_items) + index
            for item in queue_list:
                if item[1] == protocol_name and item[0] == index:
                    self.set_checkbox_signal.emit(str(qt_items[index]))
                    return JSONResponse(content={"status": "success checking protocol"})
            raise HTTPException(
                status_code=500,
                detail=f"Failed to check next protocol {protocol_name} with index {index} from queue as the protocol was not found at that position.",
            )

        @app.get("/api/v1/samples")
        async def get_samples(api_key: str = Depends(validate_credentials)):
            """
            Retrieve the list of available samples.

            Args:
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response containing the sample data.
            """
            require_global_api_key(api_key)
            return JSONResponse(content=self.main_window.sampledata)

        @app.get("/api/v1/actions/set/samples/{sample_name}")
        async def set_samples(
            sample_name: str, api_key: str = Depends(validate_credentials)
        ):
            """
            Set the active sample for the application.

            Args:
                sample_name (str): The name of the sample to activate.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response indicating whether the sample was successfully set.
            """
            require_global_api_key(api_key)
            self.set_sample_signal.emit(str(sample_name))
            await asyncio.sleep(0.01)
            if (
                self.main_window.active_sample == sample_name
                or sample_name in self.main_window.active_sample.split(" / ")
            ):
                return JSONResponse(content={"status": "success setting sample name"})
            else:
                return JSONResponse(content={"status": "failed setting sample name"})

        @app.get("/api/v1/users")
        async def get_users(api_key: str = Depends(validate_credentials)):
            """
            Retrieve the list of available users.

            Args:
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response containing the user data.
            """
            require_global_api_key(api_key)
            return JSONResponse(content=self.main_window.userdata)

        @app.get("/api/v1/actions/set/users/{user_name}")
        async def set_users(
            user_name: str, api_key: str = Depends(validate_credentials)
        ):
            """
            Set the active user for the application.

            Args:
                user_name (str): The name of the user to activate.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response indicating whether the user was successfully set.
            """
            require_global_api_key(api_key)
            self.set_user_signal.emit(str(user_name))
            await asyncio.sleep(0.01)
            if self.main_window.active_user == user_name:
                return JSONResponse(content={"status": "success setting user name"})
            else:
                return JSONResponse(content={"status": "failed setting user name"})

        @app.get("/api/v1/session")
        async def get_session(api_key: str = Depends(validate_credentials)):
            """
            Retrieve the current session name.

            Args:
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response containing the current session name.
            """
            require_global_api_key(api_key)
            return JSONResponse(content=self.main_window.lineEdit_session.text())

        @app.get("/api/v1/actions/set/session/{session_name}")
        async def set_session(
            session_name: str, api_key: str = Depends(validate_credentials)
        ):
            """
            Set the active session name for the application.

            Args:
                session_name (str): The name of the session to activate.
                api_key (str): API key for authentication.

            Returns:
                JSONResponse: A JSON response indicating whether the session name was successfully set.
            """
            require_global_api_key(api_key)
            self.set_session_signal.emit(str(session_name))
            await asyncio.sleep(0.01)
            if self.main_window.lineEdit_session.text() == session_name:
                return JSONResponse(content={"status": "success setting session name"})
            else:
                return JSONResponse(content={"status": "failed setting session name"})

        @app.get("/")
        async def root():
            """
            Redirect to the API documentation.

            Returns:
                RedirectResponse: A redirect to the API docs.
            """
            return RedirectResponse(url="/docs", status_code=302)

        @app.get("/favicon.ico")
        async def favicon():
            """
            Serve the favicon for the API.

            Returns:
                FileResponse: The favicon file.
            """
            icon_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../graphics/camels_icon_high_res.ico",
            )
            return FileResponse(icon_path)

        @app.get("/logout")
        async def logout():
            """
            Logout the current user.

            Raises:
                HTTPException: Always raises a 401 HTTPException to indicate logout.
            """
            raise HTTPException(status_code=401, detail="Successful Logout completed")
