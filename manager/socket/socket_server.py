import socket, os, threading, logging
from pydantic import ValidationError

from manager.interfaces import SocketServerInterface
# the following depends on the shared folder and needs to be
# coppied into manager and commandline. 
from manager.socket_communication import SOCKET_PATH, write_message, read_message # pyright: ignore[reportMissingImports]

logger = logging.getLogger(__name__)

class UnixSocketServer(SocketServerInterface):
    def __init__(self,command_handler):
        # Hier speichern wir die Abhängigkeit. Jede Verbindung kann nun darauf zugreifen!
        self._stop_event = threading.Event()
        self._server_thread = None
        self._server_socket = None
        self.command_handler = command_handler

    def _handle_connection(self, conn):
        data = None
        try:
            data = read_message(conn)
            if not data:
                logger.warning("Socket request: empty message")
                return
            try:
                response = self.command_handler.execute(data["selector"],data["action"],data.get("payload",None))
            
            except KeyError as e:
                logger.warning(f"Command not found: {data['selector']} {data['action']}")
                response = {"error": "not_found", "message": str(e)}

            except ValidationError as e:
                # Passiert, wenn die Payload da ist, aber nicht zum Pydantic-Schema passt
                logger.warning(f"validation error for: {data['selector']} {data['action']}:")
                logger.warning(e.json(indent=2))  # Zeigt dir exakt, welches Feld fehlt oder falsch ist
                response = {"error": "bad_request", "details": e.errors()}

            write_message(conn, response)
            logger.info("Socket response sent for: %s", data.get("selector", "None"))

        finally:
            selector = data["selector"] if data else None
            print(f"Socket request: {selector if selector else 'None'}")
            conn.close()

    def _listen_loop(self):
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
            
        self._server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server_socket.bind(SOCKET_PATH)
        self._server_socket.listen(5)
        os.chmod(SOCKET_PATH, 0o777)
        
        # Setze einen Timeout, damit der Socket blockierende accepts regelmäßig abbricht
        # und prüft, ob das stop_event gesetzt wurde
        self._server_socket.settimeout(1.0)

        while not self._stop_event.is_set():
            try:
                conn, _ = self._server_socket.accept()
                threading.Thread(
                    target=self._handle_connection, 
                    args=(conn,), 
                    daemon=True
                ).start()
            except socket.timeout:
                continue # Timeout erreicht, Schleife prüft stop_event neu
            except Exception as e:
                if not self._stop_event.is_set():
                    logger.error(f"Socket error: {e}")

        self._server_socket.close()

    def start(self):
        logger.info("Starting UNIX socket listener thread")
        self._stop_event.clear()
        # starts a loop, that's waiting for connections, these connections will not be hold
        # long and returned promptly, by design
        self._server_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._server_thread.start()

    def stop(self):
        logger.info("Shutting down UNIX socket listener")
        self._stop_event.set()
        if self._server_thread:
            self._server_thread.join(timeout=10)