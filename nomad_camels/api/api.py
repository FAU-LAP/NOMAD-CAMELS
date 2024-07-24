from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from PySide6.QtCore import QThread, Signal
from nomad_camels.frontpanels.settings_window import hash_api_key
from nomad_camels.utility import load_save_functions
import uvicorn
import sqlite3
import os
import threading


# Define the validate_api_key function
def validate_api_key(api_key: str) -> bool:
    # Establish the SQLite connection and cursor
    data_base_path = os.path.join(
        load_save_functions.appdata_path, "CAMELS_API_keys.db"
    )
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
            raise  # Re-raise the exception if it's not the specific one we're looking for
    result = c.fetchone()
    conn.close()
    return result is not None


# Initialize HTTP Basic Authentication
security = HTTPBasic()


# Define the dependency for API key validation
async def validate_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    print("Still using this function validate credentials")
    api_key = credentials.password
    # The api_key is directly taken from credentials.password
    if api_key and validate_api_key(api_key):
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "Basic"},
    )


class FastapiThread(QThread):
    # Define signals for communicating with the main window
    start_protocol = Signal(str)
    port_error_signal = Signal(str)  # Signal to send error message to main window

    def __init__(self, main_window, api_port):
        super().__init__()
        self.main_window = main_window
        self.api_port = api_port
        self._stop_event = threading.Event()
        self.app = FastAPI()  # Initialize the FastAPI app

    def run(self):
        app = self.app

        @app.get("/protocols")
        async def get_protocols(api_key: str = Depends(validate_credentials)):
            return JSONResponse(
                content={"Protocols": list(self.main_window.protocols_dict.keys())}
            )

        @app.get("/protocols/{protocol_name}")
        async def run_protocol(
            protocol_name: str, api_key: str = Depends(validate_credentials)
        ):
            self.start_protocol.emit(str(protocol_name))
            return JSONResponse(content={"status": "success"})

        # TODO
        # Fix this to actually work using the body of the POST!!
        # @app.post("/protocol/{protocol_name}")
        # async def run_protocol(protocol_name: str, api_key: str = Depends(validate_credentials)):
        #     self.start_protocol.emit(str(protocol_name))
        #     return JSONResponse(content={"status": "success"})

        @app.get("/")
        async def root():
            return RedirectResponse(url="/docs")

        @app.get("/favicon.ico")
        async def favicon():
            icon_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../graphics/camels_icon_high_res.ico",
            )
            return FileResponse(icon_path)

        # Start the uvicorn server
        try:
            self.server_config = uvicorn.Config(
                app, host="127.0.0.1", port=int(self.api_port), log_level="info"
            )
            self.server = uvicorn.Server(self.server_config)

            # Run the server
            self.server.run()
        except ValueError:  # Catching ValueError for invalid port conversion
            print(f"Invalid port number: {self.api_port}")
            self.port_error_signal.emit("Invalid port number")
        except Exception as e:
            print(f"Error starting server: {e}")
            self.port_error_signal.emit("Failed to start server")

    def stop_server(self):  #  Method to trigger shutdown
        if self.server is not None:
            self.server.should_exit = True
            self._stop_event.set()
            self.quit()
            self.wait()
