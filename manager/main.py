#!/usr/bin/env python3
from contextlib import asynccontextmanager
from fastapi import FastAPI #pyright: ignore[reportMissingImports]
import logging

import manager.interfaces as CommandInterfaces

from manager.socket.socket_server import UnixSocketServer
from manager.registry.command_registry import CommandRegistry
from manager.service.service import StaticProjectService
from manager.discovery.engine import DiscoverEngine

logging.basicConfig(level=logging.INFO)
logger_lifespan = logging.getLogger("lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    service_handler = StaticProjectService()

    public_command_registry,system_command_registry = CommandRegistry(), CommandRegistry()
    auto_discovery = DiscoverEngine({"public":public_command_registry,"system":system_command_registry})
    auto_discovery.fill_command_registry(CommandInterfaces, [service_handler])
    logger_lifespan.info(system_command_registry)

    socket_handler = UnixSocketServer(command_handler = system_command_registry)
    
    # If possible this should be last, since it will work without needing the yield point.
    socket_handler.start()
    logger_lifespan.info("Startet Socket-Listener")

    logger_lifespan.info("Start-Up done")

    yield

    logger_lifespan.info("Shutdown startet...")
    socket_handler.stop()
    logger_lifespan.info("Shutdown done")

app = FastAPI(lifespan=lifespan)
