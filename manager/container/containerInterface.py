#!/usr/bin/env python3
from abc import ABC, abstractmethod

class ContainerInterface(ABC):
    
    @abstractmethod
    def start_manager(self) -> None:
        """Must handle establishing the connection."""
        pass

    @abstractmethod
    def stop_manager(self) -> None:
        """Must handle closing the connection."""
        pass

    @abstractmethod
    def list_containers(self, all: bool = True) -> list:
        """Must return a list of containers."""
        pass