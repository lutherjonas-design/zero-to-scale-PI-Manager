#!/usr/bin/env python3
import inspect
import typing
from abc import ABC

class DiscoverEngine():
    def __init__(self,registries: dict): # registries = {"public":CommandRegistry(),"system":-"-,...}
        self.registries = registries

    def _discover_commands(self,interface_file):
        command_classes = []
        for name, obj in inspect.getmembers(interface_file, inspect.isclass):
            if issubclass(obj, ABC) and obj is not ABC: # only ABC classes (scip schemas)
                command_classes.append(obj)

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

                # 5. MATCHING: Die echte Funktion aus deinen übergebenen Code-Instanzen holen
                # Wir suchen in deinen Services nach einer Methode mit exakt demselben Namen
                actual_function = None
                for instance in instances:
                    if hasattr(instance, method_name):
                        actual_function = getattr(instance, method_name)
                        break

                if not actual_function:
                    # Laut scheitern, wenn das Interface nicht implementiert wurde!
                    raise AttributeError(
                        f"Keine Implementierung für die Interface-Methode '{method_name}' gefunden!"
                    )

                # 6. An deine echten Registries verteilen
                for registry_zone in data["zones"]:
                    if registry_zone in self.registries:
                        # Hier rufen wir die .add()-Methode deiner echten CommandRegistry auf
                        self.registries[registry_zone].add(
                            keyPath=selector,
                            keyAction=data["action"],
                            function=actual_function,
                            schema=schema,
                        )

    
    def fill_command_registry(self,InterfaceFile):
        pass