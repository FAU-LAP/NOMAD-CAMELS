import sys
from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from PySide6.QtCore import QThread, Signal
from nomad_camels.frontpanels.settings_window import hash_api_key
from nomad_camels.utility import load_save_functions, variables_handling
import uvicorn
import sqlite3
import os
import threading
import time
import json
import uuid
from pydantic import BaseModel, Field
import math
import asyncio


def sanitize_dict(d):
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
    variables: dict = Field(
        ...,
        json_schema_extra={
            "description": "A dictionary of variables to pass to the protocol",
            "example": {"key1": "value1", "key2": "value2"},
        },
    )


# Define the response model
class ProtocolRunResponse(BaseModel):
    check_protocol_status_here: str = Field(
        ..., description="A URL to check the protocol status"
    )


# Define the validate_api_key function
def validate_api_key(api_key: str) -> bool:
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


def write_protocol_result_path_to_db(api_uuid, message="currently running"):
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
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()

    # Insert new entry with UUID and status "currently running"
    c.execute(
        """
        INSERT OR REPLACE INTO protocol_run_status (uuid, status)
        VALUES (?, ?)
        """,
        (api_uuid, message),
    )
    conn.commit()
    # Close the database connection
    conn.close()


def is_valid_path(file_path):
    return os.path.exists(file_path)


def cast_or_create_uuid_str(_uuid: uuid.UUID = None) -> str:
    "Function to cast a given UUID as string or create a new one"
    if _uuid is None:
        return str(uuid.uuid4())
    else:
        return str(_uuid)


# Initialize HTTP Bearer Authentication
security = HTTPBearer()


# Define the dependency for API key validation
async def validate_credentials(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    api_key = credentials.credentials
    # The api_key is directly taken from credentials.password
    if api_key and validate_api_key(api_key):
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "Bearer"},
    )


class FastapiThread(QThread):
    """Runs FastAPI inside a PySide6 QThread to avoid blocking the GUI."""

    # Define signals for communicating with the main window
    # Signal to start a protocol
    start_protocol_signal = Signal(str, str, object)
    # Signal to send error message to main window, clears the fastapi_thread variable
    port_error_signal = Signal(str)
    # Signal to set the available user names
    set_user_signal = Signal(str)
    # Signal to set the sample in the main window
    set_sample_signal = Signal(str)
    # Signal to set the session name in the main window
    set_session_signal = Signal(str)
    # Signal to queue a protocol
    queue_protocol_signal = Signal(str, str)
    # Signal to remove a protocol from the queue
    remove_queue_protocol_signal = Signal(str)
    # Signal to check the checkbox of the next protocol in the queue
    set_checkbox_signal = Signal(str)
    # Signal to change the variables when adding a protocol to the queue
    queue_protocol_with_variables_signal = Signal(str, dict, int, str)
    # Signal to update the variables of a protocol that is already in the queue
    change_variables_queued_protocol_signal = Signal(str, dict, int)

    def __init__(self, main_window, api_port):
        super().__init__()
        # get the main window so that we have access to all the settings and dictionaries
        self.main_window = main_window
        self.api_port = api_port
        self.protocol_runs = {}  # Dictionary to store the protocol runs
        self.app = None
        self.server = None
        self.loop = None  # Custom asyncio loop

    def run(self):
        """Start FastAPI inside an asyncio event loop running in a separate thread."""
        self.app = FastAPI()  # Initialize FastAPI app
        self.define_routes(self.app)  # Define the API routes

        self.loop = (
            asyncio.new_event_loop()
        )  # Create a new asyncio loop for this thread
        asyncio.set_event_loop(self.loop)

        # Start Uvicorn as an asyncio task
        self.loop.run_until_complete(self.start_server())

    async def start_server(self):
        """Starts the FastAPI server using Uvicorn inside an async loop."""
        config = uvicorn.Config(
            self.app,
            host="127.0.0.1",
            port=self.api_port,
            log_level="info",
            reload=False,
            workers=1,  # Ensure only one worker to avoid multi-thread issues
        )
        self.server = uvicorn.Server(config)

        try:
            await self.server.serve()
        except Exception as e:
            print(f"Error starting FastAPI: {e}")
            self.port_error_signal.emit(f"Failed to start server: {e}")

    def stop_server(self):
        """Safely shuts down the FastAPI server running inside the QThread."""
        if self.server is not None:
            print("Stopping FastAPI server...")
            self.server.should_exit = True  # Signals Uvicorn to stop

        # if self.loop is not None:
        #     self.loop.call_soon_threadsafe(self.loop.stop)  # Stop the event loop safely

        self.quit()  # Quit the QThread
        self.wait()  # Ensure the thread has fully stopped

    def define_routes(self, app: FastAPI):
        """Define all FastAPI routes within the server thread"""

        # [Your route definitions remain unchanged]
        # Example:
        @app.get("/api/v1/protocols")
        async def get_protocols(api_key: str = Depends(validate_credentials)):
            """Get the list of available protocols"""
            return JSONResponse(
                content={"Protocols": list(self.main_window.protocols_dict.keys())}
            )

        # Get the available variables of a protocol
        @app.get("/api/v1/protocols/variables/{protocol_name}")
        async def get_protocol_variables(
            protocol_name: str, api_key: str = Depends(validate_credentials)
        ):
            """Get the available variables of a protocol"""
            return JSONResponse(
                content={
                    "Variables": list(
                        self.main_window.protocols_dict[protocol_name].variables
                    )
                }
            )

        # Get a JSON representation of the protocol
        @app.get("/api/v1/protocols/{protocol_name}/JSON")
        async def get_protocol_json(
            protocol_name: str, api_key: str = Depends(validate_credentials)
        ):
            """Get a JSON representation of the protocol"""
            protocol_class_instance = self.main_window.protocols_dict[protocol_name]
            protocol = load_save_functions.get_save_str(protocol_class_instance)
            cleaned_protocol = sanitize_dict(protocol)
            return JSONResponse(
                content=cleaned_protocol,
            )

        # Get JSON representation of the current CAMELS settings (also called preferences)
        @app.get("/api/v1/settings/JSON")
        async def get_settings_json(api_key: str = Depends(validate_credentials)):
            """Get a JSON representation of the current CAMELS settings"""
            settings = self.main_window.preferences
            cleaned_settings = sanitize_dict(settings)
            return JSONResponse(
                content=cleaned_settings,
            )

        # Run a protocol by name
        @app.get(
            "/api/v1/actions/run/protocols/{protocol_name}",
            response_model=ProtocolRunResponse,
        )
        async def run_protocol(
            protocol_name: str,
            protocol_uuid: uuid.UUID = None,
            api_key: str = Depends(validate_credentials),
        ):
            """Run a protocol by name"""
            # Generate or use the provided syntax checked UUID as casted string
            protocol_uuid = cast_or_create_uuid_str(_uuid=protocol_uuid)

            write_protocol_result_path_to_db(protocol_uuid)

            self.start_protocol_signal.emit(str(protocol_name), protocol_uuid, None)
            return JSONResponse(
                content={
                    "check protocol status here": f"/api/v1/protocols/results/{protocol_uuid}"
                }
            )

        # Run a protocol by name and pass variables to it (only already defined variables can be passed)
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
            """Run a protocol by name and pass variables to it (only already defined variables can be passed)"""
            # Get dictionary from the variables model
            variables = variables.model_dump()
            response = await get_protocol_variables(protocol_name)
            response_content = response.body.decode("utf-8")
            accepted_variables = json.loads(response_content)["Variables"]
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

            write_protocol_result_path_to_db(protocol_uuid)

            self.start_protocol_signal.emit(
                str(protocol_name), protocol_uuid, variables["variables"]
            )
            return JSONResponse(
                content={
                    "check protocol status here": f"/api/v1/protocols/results/{protocol_uuid}"
                }
            )

        # Get the status of a protocol run by UUID
        @app.get("/api/v1/protocols/results/{protocol_uuid}")
        async def get_protocol_status(
            protocol_uuid: str, api_key: str = Depends(validate_credentials)
        ):
            """Get the status of a protocol run by UUID"""
            # Database setup
            data_base_path = os.path.join(
                load_save_functions.appdata_path, "CAMELS_API.db"
            )
            conn = sqlite3.connect(data_base_path, check_same_thread=False)
            c = conn.cursor()

            # Query the status of the protocol run by UUID
            c.execute(
                """
                SELECT status FROM protocol_run_status WHERE uuid = ?
                """,
                (protocol_uuid,),
            )
            result = c.fetchone()
            # Close the database connection
            conn.close()
            if result:
                return JSONResponse(
                    content={"uuid": protocol_uuid, "status": result[0]}
                )
            else:
                return JSONResponse(
                    content={"error": "UUID not found"}, status_code=404
                )

        # Get the literal hdf5 file of a successful protocol run by UUID
        @app.get("/api/v1/protocols/results/{protocol_uuid}/file")
        async def get_protocol_hdf5(
            protocol_uuid: str, api_key: str = Depends(validate_credentials)
        ):
            """Get the literal hdf5 file of a successful protocol run by UUID"""
            # Database setup
            data_base_path = os.path.join(
                load_save_functions.appdata_path, "CAMELS_API.db"
            )
            conn = sqlite3.connect(data_base_path, check_same_thread=False)
            c = conn.cursor()

            # Query the status of the protocol run by UUID
            c.execute(
                """
                SELECT status FROM protocol_run_status WHERE uuid = ?
                """,
                (protocol_uuid,),
            )
            status = c.fetchone()[0]
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

        # Get the current protocol queue
        @app.get("/api/v1/queue")
        async def get_queue(api_key: str = Depends(validate_credentials)):
            """Get the current protocol queue"""
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
            """Add a protocol to the queue by name"""
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

        # Add protocol to queue with variables
        @app.post("/api/v1/actions/queue/protocols/{protocol_name}")
        async def queue_protocol_with_variables(
            protocol_name: str,
            variables: Variables,
            protocol_uuid: uuid.UUID = None,
            api_key: str = Depends(validate_credentials),
        ):
            """Add a protocol to the queue by name and pass variables to it"""
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

        # Change variables of a protocol already in the queue
        @app.post("/api/v1/actions/queue/variables/protocols/{protocol_name}_{index}")
        async def change_variables_queued_protocol(
            protocol_name: str,
            index: int,
            variables: Variables,
            api_key: str = Depends(validate_credentials),
        ):
            """Change the variables of a protocol already in the queue"""
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

        # Remove protocol from queue
        @app.get("/api/v1/actions/queue/remove/protocols/{protocol_name}_{index}")
        async def remove_protocol(
            protocol_name: str, index: int, api_key: str = Depends(validate_credentials)
        ):
            """Remove a protocol from the queue by name"""
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

        # Check the ready checkbox of protocols in the queue
        @app.get("/api/v1/actions/queue/ready/protocols/{protocol_name}_{index}")
        async def protocol_ready(
            protocol_name: str, index: int, api_key: str = Depends(validate_credentials)
        ):
            """Check the ready checkbox of protocols in the queue"""
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
            """Get the list of available samples"""
            return JSONResponse(content=self.main_window.sampledata)

        @app.get("/api/v1/actions/set/samples/{sample_name}")
        async def set_samples(
            sample_name: str, api_key: str = Depends(validate_credentials)
        ):
            """Set the active sample"""
            self.set_sample_signal.emit(str(sample_name))
            await asyncio.sleep(0.01)
            if self.main_window.active_sample == sample_name:
                return JSONResponse(content={"status": "success setting sample name"})
            else:
                return JSONResponse(content={"status": "failed setting sample name"})

        @app.get("/api/v1/users")
        async def get_users(api_key: str = Depends(validate_credentials)):
            """Get the list of available users"""
            return JSONResponse(content=self.main_window.userdata)

        @app.get("/api/v1/actions/set/users/{user_name}")
        async def set_users(
            user_name: str, api_key: str = Depends(validate_credentials)
        ):
            """Set the active user"""
            self.set_user_signal.emit(str(user_name))
            await asyncio.sleep(0.01)
            if self.main_window.active_user == user_name:
                return JSONResponse(content={"status": "success setting user name"})
            else:
                return JSONResponse(content={"status": "failed setting user name"})

        @app.get("/api/v1/session")
        async def get_session(api_key: str = Depends(validate_credentials)):
            """Get the current session name"""
            return JSONResponse(content=self.main_window.lineEdit_session.text())

        @app.get("/api/v1/actions/set/session/{session_name}")
        async def set_session(
            session_name: str, api_key: str = Depends(validate_credentials)
        ):
            """Set the active session name"""
            self.set_session_signal.emit(str(session_name))
            await asyncio.sleep(0.01)
            if self.main_window.lineEdit_session.text() == session_name:
                return JSONResponse(content={"status": "success setting session name"})
            else:
                return JSONResponse(content={"status": "failed setting session name"})

        # Root redirects to the API documentation
        @app.get("/")
        async def root():
            return RedirectResponse(url="/docs", status_code=302)

        # Define a favicon endpoint
        @app.get("/favicon.ico")
        async def favicon():
            icon_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../graphics/camels_icon_high_res.ico",
            )
            return FileResponse(icon_path)

        @app.get("/logout")
        async def logout():
            """Logout the user"""
            raise HTTPException(status_code=401, detail="Successful Logout completed")
