#!/usr/bin/env python3
from fastapi import FastAPI #pyright: ignore[reportMissingImports]
import threading
from .local_socket import socket_listener #pyright: ignore

app = FastAPI()

@app.on_event("startup")
def start_listener():
    # Seperated way to run the commandline side of the project.
    threading.Thread(target=socket_listener, daemon=True).start()