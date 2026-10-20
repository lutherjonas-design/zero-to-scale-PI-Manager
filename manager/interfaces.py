#!/usr/bin/env python3
from abc import ABC, abstractmethod

class SocketServerInterface(ABC):
    @abstractmethod
    def start(self) -> None:
        """Startet den Server im Hintergrund (Thread/Task)."""
        pass
    @abstractmethod
    def stop(self) -> None:
        """Stoppt den Server und räumt Ressourcen auf."""
        pass