#!/usr/bin/env python3
from abc import ABC, abstractmethod
from pydantic import BaseModel

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
    
class ServiceActionInterface(ABC):
    @abstractmethod
    def get_status(self, data:ServiceStatusSchema) -> dict:
        """Give back the state of a project."""
        pass

    @abstractmethod
    def list_projects(self, data:ServiceListProjectSchema) -> dict:
        """give a list of all projects"""
        pass

# ---------- Docker ----------

# ---------- Project ----------

# ---------- Health ----------