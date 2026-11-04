#!/usr/bin/env python3
from contextlib import asynccontextmanager
from fastapi import FastAPI #pyright: ignore[reportMissingImports]
import logging
from manager.socket.socket_server import UnixSocketServer

logging.basicConfig(level=logging.INFO)
logger_lifespan = logging.getLogger("lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    socket_handler = UnixSocketServer()
    socket_handler.start()
    logger_lifespan.info("Startet Socket-Listener")
    logger_lifespan.info("Start-Up done")

    yield

    logger_lifespan.info("Shutdown startet...")
    socket_handler.stop()
    logger_lifespan.info("Shutdown done")

app = FastAPI(lifespan=lifespan)
