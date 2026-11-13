import pytest
from abc import ABC, abstractmethod
from typing import Type
from pydantic import BaseModel

from manager.discovery.engine import DiscoverEngine
from manager.discovery.decorator import discovery_method_tags, discovery_selector_namespace

# Angenommen, diese Klassen kommen aus deinem Code:
class PotentialMethod:
    def __init__(self, method: str, schema: Type[BaseModel] | None, zones: list, selector: str, action: str, interface_class: Type):
        self.method = method
        self.schema = schema
        self.zones = zones
        self.selector = selector
        self.action = action
        self.interface_class = interface_class

# --- DUMMIES FÜR DAS INTERFACE UND DIE PYDANTIC SCHEMAS ---
class FakeSchema(BaseModel):
    target: str

@discovery_selector_namespace("fake")
class FakeInterface(ABC):
    @discovery_method_tags("read",["public", "system"])
    @abstractmethod
    def get_status(self, payload: FakeSchema) -> dict:
        pass

# --- DIE FAKE IMPLEMENTIERUNG ---
class FakeProjectService(FakeInterface):
    def get_status(self, payload: FakeSchema) -> dict:
        return {"status": "running"}


# --- MOCK COMMAND REGISTRY (Um Aufrufe aufzuzeichnen) ---
class MockCommandRegistry:
    def __init__(self):
        self.added_commands = []

    def add(self, keyPath: str, keyAction: str, function, schema):
        # Wir speichern die Parameter ab, um sie im Test zu überprüfen
        self.added_commands.append({
            "keyPath": keyPath,
            "keyAction": keyAction,
            "function": function,
            "schema": schema
        })


# --- DER EIGENTLICHE TEST ---

def test_discover_and_fill_registry_success():
    # 1. Setup: Registries vorbereiten
    public_registry = MockCommandRegistry()
    system_registry = MockCommandRegistry()
    
    registries = {
        "public": public_registry,
        "system": system_registry
    }
    
    # 2. Engine initialisieren
    engine = DiscoverEngine(registries=registries)
    
    # 3. Wir simulieren das 'interface_file', indem wir ein Objekt bauen,
    # das unsere Fake-Klasse als Attribut besitzt (so wie inspect.getmembers es lesen würde)
    class FakeModule:
        FakeInterfaceClass = FakeInterface
        
    # 4. Instanzen bereitstellen
    service_instance = FakeProjectService()
    
    # 5. Aktion ausführen
    engine.fill_command_registry(interface_file=FakeModule, instances=[service_instance])
    
    # 6. Assertions (Überprüfungen):
    # Wurde der Befehl in der 'public'-Registry registriert?
    assert len(public_registry.added_commands) == 1
    cmd_public = public_registry.added_commands[0]
    assert cmd_public["keyPath"] == "fake"
    assert cmd_public["keyAction"] == "read"
    assert cmd_public["schema"] == FakeSchema
    assert cmd_public["function"] == service_instance.get_status

    # Wurde der Befehl auch in der 'system'-Registry registriert?
    assert len(system_registry.added_commands) == 1
    assert system_registry.added_commands[0]["keyPath"] == "project.static"


def test_discover_engine_raises_attribute_error_when_implementation_missing():
    # Testet das "laute Scheitern", wenn das Interface nicht implementiert wurde
    registries = {"public": MockCommandRegistry()}
    engine = DiscoverEngine(registries=registries)
    
    class FakeModule:
        FakeInterfaceClass = FakeInterface
        
    # Wir übergeben KEINE Instanzen (leere Liste)
    with pytest.raises(AttributeError) as exc_info:
        engine.fill_command_registry(interface_file=FakeModule, instances=[])
        
    # Prüfen, ob die Fehlermeldung aussagekräftig ist
    assert "Keine Implementierung für die Methode 'get_status'" in str(exc_info.value)
    assert "FakeInterface" in str(exc_info.value)
