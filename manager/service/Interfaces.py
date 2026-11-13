#!/usr/bin/env python3
from abc import ABC, abstractmethod
from pydantic import BaseModel # pyright: ignore[reportMissingImports]

class ProjectInterface(ABC):
    @abstractmethod
    def list_project(self)->list:
        """"""
        pass