#!/usr/bin/env python3
from contextlib import asynccontextmanager
from fastapi import FastAPI #pyright: ignore[reportMissingImports]
import logging
from manager.socket.socket_server import UnixSocketServer

logging.basicConfig(level=logging.INFO)
logger_lifespan = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    socket_handler = UnixSocketServer()
    logger_lifespan.info("Starte Socket-Listener...")
    socket_handler.start()
    logger_lifespan.info("Start-Up erfolgreich abgeschlossen")
    yield
    logger_lifespan.info("Shutdown gestartet...")
    socket_handler.stop()
    logger_lifespan.info("Shutdown erfolgreich beendet")

    

app = FastAPI(lifespan=lifespan)
