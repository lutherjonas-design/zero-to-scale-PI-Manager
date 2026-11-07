#!/usr/bin/env python3
from typing import get_type_hints

class CommandRegistry:
    def __init__(self) -> None:
        self.registry = {}
    def add(self,keyPath:str,keyAction:str,function):
        if not (keyPath and keyAction and function):
            raise KeyError("Path, Action und Funktion müssen angegeben werden.")
        self.registry[str(keyPath),str(keyAction)] = function

    def execute(self,keyPath:str,keyAction:str,payload: dict):
        if (str(keyPath),str(keyAction)) not in self.registry:
            raise KeyError(f"Command path:'{keyPath}', action:'{keyAction}' not registered")

        command = self.registry[str(keyPath),str(keyAction)]

        type_hints = get_type_hints(command)

        type_hints.pop('return', None)

        if len(type_hints) == 0:
            return command()

        if len(type_hints) == 1:
            param_name = list(type_hints.keys())[0]
            schema_class = type_hints[param_name]
            validated_data = schema_class(**payload)

            return command(validated_data)
