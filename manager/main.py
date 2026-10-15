#!/usr/bin/env python3
from fastapi import FastAPI #pyright: ignore[reportMissingImports]
import socket, os, threading, time
from .socket_communication import SOCKET_PATH, write_message, read_message #pyright: ignore[reportMissingImports]

app = FastAPI()

def handle_connection(conn):
    try:
        data = read_message(conn)
        if not data:
            return
        response = f"{data} | {time.time()}"
        write_message(conn,response)
    finally:
        conn.close()

def socket_listener():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)
    os.chmod(SOCKET_PATH, 0o777)
    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_connection, args=(conn,), daemon=True).start()

@app.on_event("startup")
def start_listener():
    threading.Thread(target=socket_listener, daemon=True).start()