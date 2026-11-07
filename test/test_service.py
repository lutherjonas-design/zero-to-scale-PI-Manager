#!/usr/bin/env python3
import pytest
# Passe die Imports an deine genaue Ordnerstruktur an
from manager.interfaces import ServiceStatusSchema, ServiceListProjectSchema
from manager.service.service import StaticProjectService  # Angenommen, es liegt in services.py

@pytest.fixture
def static_service():
    """Fixture, die das Service-Objekt für die Tests bereitstellt."""
    return StaticProjectService()

def test_get_status_returns_correct_string(static_service):
    # 1. Arrange: Valides Pydantic-Objekt bauen
    mock_data = ServiceStatusSchema(target="MeinTestProjekt")
    
    # 2. Act: Methode aufrufen
    result = static_service.get_status(mock_data)
    
    # 3. Assert: Überprüfen, ob die Antwort stimmt
    assert "status" in result
    assert result["status"] == "Das Projekt 'MeinTestProjekt' läuft stabil (Statische Antwort)"

def test_list_projects_returns_list(static_service):
    # 1. Arrange: Schema für die Projektliste bauen (Felder an dein Schema anpassen)
    mock_data = ServiceListProjectSchema() 
    
    # 2. Act
    result = static_service.list_projects(mock_data)
    
    # 3. Assert
    assert "projects" in result
    assert result["projects"] == ["1", "2", "3"]
