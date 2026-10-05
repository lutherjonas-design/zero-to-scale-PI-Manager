#!/usr/bin/env python3
import socket, sys
from pathlib import Path

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

SOCKET_PATH = Path(__file__).resolve().parent.parent.joinpath("path.env").read_text().strip()

msg = sys.argv[1] if len(sys.argv) > 1 else "ping"
try:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        client.sendall(msg.encode())
        print(client.recv(1024).decode())
except ConnectionRefusedError or FileNotFoundError as e:
    print(f"{RED}ERROR: {e}{RESET}")