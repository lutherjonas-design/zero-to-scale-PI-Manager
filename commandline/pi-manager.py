#!/usr/bin/env python3
import socket, sys
from socket_communication import SOCKET_PATH, write_message, read_message

RED, GREEN, YELLOW, RESET = "\033[31m", "\033[32m", "\033[33m", "\033[0m"


msg_string = sys.argv[1] if len(sys.argv) > 1 else "ping"
payload = {"command": msg_string}
try:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        # Send
        write_message(client,payload)
        # Recive
        response_dict = read_message(client)
        print(f"Recieved: {response_dict}")
except (ConnectionRefusedError, FileNotFoundError) as e:
    print(f"{RED}ERROR: {e}{RESET}")
