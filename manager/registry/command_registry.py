#!/usr/bin/env python3
class CommandRegistry:
    def __init__(self) -> None:
        self.registry = {}

    def list_commands(self):
        return [command.__name__ for command, _ in self.registry.values()]

    def add(self,keyPath:str,keyAction:str,function, schema=None):
        if not (keyPath and keyAction and function):
            raise KeyError("Path, Action und Funktion müssen angegeben werden.")
        self.registry[str(keyPath),str(keyAction)] = (function,schema)

    def execute(self,keyPath:str,keyAction:str,payload: dict):
        if (str(keyPath),str(keyAction)) not in self.registry:
            raise KeyError(f"Command path:'{keyPath}', action:'{keyAction}' not registered")
        
        command,schema = self.registry[str(keyPath),str(keyAction)]

        if not schema:
            if payload:
                raise ValueError(f"invalid input for command path:'{keyPath}', action:'{keyAction}'")
            return command()
        
        validated_data = schema(**payload)
        return command(validated_data)
