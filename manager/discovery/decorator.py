#!/usr/bin/env python3
def discovery_selector_namespace(selector_name: str):
    def decorator(clas): # Short for class, since that is a pre defined word
        clas._selection_namespace = selector_name
        return clas
    return decorator

def discovery_method_tags(action: str, zones: list[str]):
    def decorator(func):
        # Wir speichern alle Infos in einem kleinen Dict auf der Funktion
        func._discovery_data = {
            "action": action,
            "registries": zones
        }
        return func
    return decorator