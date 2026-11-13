#!/usr/bin/env python3
"""AI generated and tested by me"""

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..Interfaces import ProjectInterface


def v0_to_v1(data: dict[str, Any]) -> dict[str, Any]:
    upgraded = data.copy()
    if "Dependencies" in upgraded:
        upgraded.setdefault("dependencies", upgraded["Dependencies"])
        del upgraded["Dependencies"]
    if "lifecycle" in upgraded:
        upgraded.setdefault("life_cycle", upgraded["lifecycle"])
        del upgraded["lifecycle"]
    upgraded["schema_version"] = 1
    return upgraded


MIGRATIONS: list[Callable[[dict[str, Any]], dict[str, Any]]] = [v0_to_v1]


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
    life_cycle: Lifecycle = Lifecycle.SLEEP
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
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def list_project(self) -> list[Path]:
        if not self.path.is_dir():
            raise NotADirectoryError(f"Project root is not a directory: {self.path}")
        return sorted(
            {
                project_directory
                for project_directory in self.path.iterdir()
                if project_directory.is_dir()
                and (project_directory / "service.yml").is_file()
            },
            key=str,
        )

    def get_project_info(self, project_path: str | Path) -> ServiceConfig:
        path = Path(project_path)
        if path.is_file():
            project_directory = path.parent
        else:
            project_directory = path
        if not project_directory.is_absolute() and not project_directory.exists():
            project_directory = self.path / project_directory
        manifest_path = project_directory / "service.yml"

        if project_directory.resolve().parent != self.path.resolve():
            raise ValueError(
                f"Project directory must be an immediate subdirectory of {self.path}: "
                f"{project_directory}"
            )
        if path.is_file() and path.name != "service.yml":
            raise ValueError(f"Expected a service.yml manifest, got {path}")
        if not manifest_path.is_file():
            raise FileNotFoundError(f"No service.yml manifest found in {project_directory}")

        with manifest_path.open(encoding="utf-8") as manifest_file:
            data = yaml.safe_load(manifest_file)
        if not isinstance(data, dict):
            raise ValueError(f"Expected a YAML mapping in {manifest_path}")

        original_version = data.get("schema_version", 0)
        data = self._upgrade_schema(data)
        config = ServiceConfig.model_validate(data)
        upgraded_version = data["schema_version"]
        if original_version != upgraded_version:
            manifest_path.write_text(
                yaml.safe_dump(
                    config.model_dump(mode="json", exclude={"project_path"}),
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
        return config.model_copy(update={"project_path": project_directory})

    @staticmethod
    def _upgrade_schema(data: dict[str, Any]) -> dict[str, Any]:
        upgraded = data.copy()
        version = upgraded.get("schema_version", 0)
        if not isinstance(version, int) or isinstance(version, bool) or version < 0:
            raise ValueError(f"Invalid schema_version: {version!r}")
        if version > len(MIGRATIONS):
            raise ValueError(f"Unsupported schema_version: {version}")
        while version < len(MIGRATIONS):
            upgraded = MIGRATIONS[version](upgraded)
            version = upgraded["schema_version"]
        return upgraded
