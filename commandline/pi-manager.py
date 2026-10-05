#!/usr/bin/env python3
import socket, sys

SOCKET_PATH = "/tmp/my_app.sock"

msg = sys.argv[1] if len(sys.argv) > 1 else "ping"

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect(SOCKET_PATH)
    client.sendall(msg.encode())
    print(client.recv(1024).decode())