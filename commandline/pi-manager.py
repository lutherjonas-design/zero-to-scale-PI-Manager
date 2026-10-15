#!/usr/bin/env python3
import socket, sys, argparse
from socket_communication import SOCKET_PATH, write_message, read_message

RED, GREEN, YELLOW, RESET = "\033[31m", "\033[32m", "\033[33m", "\033[0m"

def command_parse():
    parser = argparse.ArgumentParser(description="CLI to interact with custom deployment and management Tool of Dockers")
    parser.add_argument(
        "command",
        nargs="?"
    )

def socket_transaction(payload):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        # Send
        write_message(client,payload)
        # Recive
        return read_message(client)
            
def message_renderer(response_dict):
    print(f"Recieved: {response_dict}")

def main():
    response_dict = None
    msg_string = sys.argv[1] if len(sys.argv) > 1 else "ping"
    
    payload = {"command": msg_string}
    try:
        response_dict = socket_transaction(payload)
    except (ConnectionRefusedError, FileNotFoundError) as e:
        print(f"{RED}ERROR: {e}{RESET}")
    message_renderer(response_dict)
