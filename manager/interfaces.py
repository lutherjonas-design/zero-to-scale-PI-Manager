#!/usr/bin/env python3
from abc import ABC, abstractmethod
from pydantic import BaseModel # pyright: ignore[reportMissingImports]

from manager.discovery.decorator import discovery_selector_namespace, discovery_method_tags
# ---------- Socket ----------
class SocketServerInterface(ABC):
    @abstractmethod
    def start(self) -> None:
        """Starts the Server in the background (Thread/Task)."""
        pass
    @abstractmethod
    def stop(self) -> None:
        """Stops the Server and cleans up."""
        pass

# ---------- Service ----------
class ServiceBaseSchema(BaseModel):
    #model_config = ConfigDict(extra="forbid")
    pass

class ServiceStatusSchema(ServiceBaseSchema):
    target: str

class ServiceListProjectSchema(ServiceBaseSchema):
    filter: str | None = None

@discovery_selector_namespace("service")
class ServiceActionInterface(ABC):
    @discovery_method_tags("status",["system","public"])
    @abstractmethod
    def get_status(self, payload:ServiceStatusSchema) -> dict:
        """Give back the state of a project."""
        pass
    @discovery_method_tags("list",["system","public"])
    @abstractmethod
    def list_projects(self, payload:ServiceListProjectSchema) -> dict:
        """give a list of all projects"""
        pass

# ---------- Docker ----------

# ---------- Project ----------

# ---------- Health ----------