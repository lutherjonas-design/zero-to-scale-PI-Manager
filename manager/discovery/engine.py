#!/usr/bin/env python3
import inspect
import typing
from abc import ABC
from dataclasses import dataclass#
from pydantic import BaseModel # pyright: ignore[reportMissingImports]

@dataclass
class PotentialMethod:
    method:str
    schema:type[BaseModel] | None
    registries:str
    selector:str
    action:str
    interface_class: type

class DiscoverEngine():
    def __init__(self,registries: dict):
        # registries = {"public":CommandRegistry(),"system":-"-,...}
        self.registries = registries

    def _discover_commands(self,interface_file):
        command_classes = []
        for name, obj in inspect.getmembers(interface_file, inspect.isclass):
            if issubclass(obj, ABC) and obj is not ABC: # only ABC classes (scip schemas)
                command_classes.append(obj)

        method_list = []
        for command_class in command_classes:
            selector = getattr(command_class, "_selection_namespace", None)
            if not selector: # selector is the first key for the command registry
                continue

            # Check all methods of the classes
            for method_name in dir(command_class):
                interface_method = getattr(command_class, method_name)
                if not callable(interface_method):
                    continue

                # collect needed Data from the Interface
                data = getattr(interface_method, "_expose_data", None)
                if not data:
                    continue
                type_hints = typing.get_type_hints(interface_method)
                # Schema or None
                schema = type_hints.get("payload", None)
                if schema is type(None):
                    schema = None
                method_list.append(PotentialMethod(
                    method=method_name
                    ,schema=schema
                    ,registries=data["registries"]
                    ,selector=selector
                    ,action=data["action"]
                    ,interface_class=command_class
                ))
        return method_list
    
    def fill_command_registry(self,interface_file,instances):
        method_list = self._discover_commands(interface_file=interface_file)

        print(len(method_list))
        
        for command in method_list:
            actual_function = None
            
            for instance in instances:
                # 1. Prüfen, ob diese Instanz überhaupt das gesuchte Interface implementiert
                if not isinstance(instance, command.interface_class):
                    continue
                
                # 2. Prüfen, ob die Methode auf dieser Instanz existiert
                if hasattr(instance, command.method):
                    actual_function = getattr(instance, command.method)
                    break  # Richtige Instanz und Methode gefunden, Loop abbrechen
                
            if not actual_function:
                # Laut scheitern, wenn das Interface nicht implementiert wurde!
                raise AttributeError(
                    f"Fehler im Interface '{command.interface_class.__name__}': "
                    f"Keine Implementierung für die Methode '{command.method}' in den übergebenen Instanzen gefunden!"
                )

            # An die echten Registries verteilen
            for registry_zone in command.registries:
                if registry_zone in self.registries:
                    self.registries[registry_zone].add(
                        keyPath=command.selector,
                        keyAction=command.action,
                        function=actual_function,
                        schema=command.schema,
                    )