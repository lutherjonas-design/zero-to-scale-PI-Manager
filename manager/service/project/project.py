#!/usr/bin/env python3
"""AI generated and tested by me"""
from ..Interfaces import ProjectInterface
from enum import Enum
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator

class ServiceTag(str, Enum):
    MANAGER = "manager"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DB = "db"
    WORKER = "worker"

class Lifecycle(str, Enum):
    SLEEP = "sleep"
    ALWAYS_ON = "always_on"
    ON_DEMAND = "on_demand"

class ServiceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    name: str = Field(..., min_length=1, pattern=r"^[a-z0-9-]+$")
    tags: list[ServiceTag] = Field(default_factory=list)
    lifecycle: Lifecycle = Lifecycle.SLEEP
    dev: list[Literal["hot_reload", "debug_logs", "expose_ports"]] = Field(default_factory=list)
    active: bool = True
    dependencies: list[str] = Field(default_factory=list)
    env: list[str] = Field(default_factory=list)

    # Attached by ProjectApps after loading from disk
    project_path: Path | None = Field(default=None, exclude=True)

    # Guards against YAML parsing empty keys (e.g. "dev:") as None instead of []
    @field_validator("tags", "dev", "dependencies", "env", mode="before")
    @classmethod
    def coerce_none_to_list(cls, value):
        return [] if value is None else value

class ProjectApps(ProjectInterface):
    def __init__(self,Path):
        self.path = Path

    def list_project(self):
        return glob(self.path)