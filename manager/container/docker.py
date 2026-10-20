#!/usr/bin/env python3
import docker #pyright: ignore[reportMissingModuleSource]
from . import ContainerInterface

class DockerManager(ContainerInterface):
    def __init__(self):
        self.client = None

    def start_manager(self):
        self.client = docker.from_env()
        self.client.ping()

    def stop_manager(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def list_containers(self, all=True):
        if self.client is None:
            raise RuntimeError("Docker manager not started")
        return self.client.containers.list(all=all)