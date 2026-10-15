import socket, os, threading, time, logging
from .socket_communication import SOCKET_PATH, write_message, read_message #pyright: ignore[reportMissingImports]

logger = logging.getLogger("socket")
def handle_connection(conn):
    data = None
    try:
        data = read_message(conn)
        if not data:
            logger.warning("Socket request: empty message")
            return
       
        response = data if data else {"time": time.time()}
        write_message(conn,response)
        logger.info("Socket response sent for: %s", data.get("command","None"))

    finally:
        command = data["command"] if data else None
        print(f"Socket request: {command if command else "None"}")
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