#!/usr/bin/env python3
import pytest  #pyright: ignore[reportMissingImports]
from unittest.mock import Mock
from pydantic import BaseModel, ValidationError

from manager.registry.command_registry import CommandRegistry

class DummyUserSchema(BaseModel):
    username: str
    age: int

@pytest.fixture
def command_registry():
    """Fixture, die das Service-Objekt für die Tests bereitstellt."""
    return CommandRegistry()

def test_adding_command(c_r):
    mock_command = Mock()
    def fake_function(data: DummyUserSchema):
        return mock_command(data)

    c_r.add("service","status",fake_function)
    valid_payload = {"username":"ben", "age":20}

    c_r.execute(keyPath="user", keyAction="create", payload=valid_payload)

    mock_command.assert_called_once()
    called_arg = mock_command.call_args[0][0]
    assert isinstance(called_arg, DummyUserSchema)
    assert called_arg.username == "Alex"
    assert called_arg.age == 30

# --- TEST 2: Fehlgeschlagene Validierung ---
def test_execute_with_invalid_payload_raises_validation_error(c_r):
    mock_command = Mock()
    def fake_command(data: DummyUserSchema):
        return mock_command(data)

    c_r.registry[("user", "create")] = fake_command
    invalid_payload_1 = {"username": "Alex", "age": "str"}
    invalid_payload_2 = {"username": "Alex", "age": "1"}
    
    with pytest.raises(ValidationError):
        c_r.execute(keyPath="user", keyAction="create", payload=invalid_payload_1)

    with pytest.raises(ValidationError):
        c_r.execute(keyPath="user", keyAction="create", payload=invalid_payload_2)

    mock_command.assert_not_called()

def test_execute_unregistered_command_raises_key_error(c_r):
    with pytest.raises(KeyError) as exc_info:
        c_r.execute(keyPath="unknown", keyAction="action", payload={})
        
    assert "Command path:'unknown', action:'action' not registered" in str(exc_info.value)
