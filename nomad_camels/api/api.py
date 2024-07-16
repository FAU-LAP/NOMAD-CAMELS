from fastapi import FastAPI
from fastapi.responses import JSONResponse
from PySide6.QtCore import QThread, Signal
import uvicorn


class FastapiThread(QThread):
    # Define signals for communicating with the main window
    protocol_started = Signal(str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def run(self):
        app = FastAPI()

        @app.get('/get_protocols')
        async def get_protocols():
            return JSONResponse(content={"Protocols": list(self.main_window.protocols_dict.keys())})

        @app.get('/run_protocol/{protocol_name}')
        async def run_protocol(protocol_name: str):
            self.protocol_started.emit(str(protocol_name))
            return JSONResponse(content={"status": "success"})

        @app.get("/")
        async def root():
            return {"message": "Hello World"}

        # Start the uvicorn server
        config = uvicorn.Config(app, host="127.0.0.1", port=5000, log_level="info")
        server = uvicorn.Server(config)

        # Run the server
        server.run()
