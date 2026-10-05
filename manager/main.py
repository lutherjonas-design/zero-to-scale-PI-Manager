#!/usr/bin/env python3
from fastapi import FastAPI
import socket, os, threading, time
from pathlib import Path

SOCKET_PATH = Path(__file__).resolve().parent.parent.joinpath(".env").read_text().strip()

app = FastAPI()

def handle_connection(conn):
    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            return
        response = f"{data} | {time.time()}"
        conn.sendall(response.encode())
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