#!/usr/bin/env python3
from manager.interfaces import ServiceActionInterface, ServiceStatusSchema, ServiceListProjectSchema

class ProjectService(ServiceActionInterface):
    def __init__(self,REPO_PATH):
        self.REPO_PATH = REPO_PATH

    def get_status(self, payload: ServiceStatusSchema) -> dict:
        # Hier nutzen wir das saubere, validierte Pydantic-Objekt
        return {"status": f"Das Projekt '{payload.target}' läuft stabil (Statische Antwort)"}

    def list_projects(self, payload: ServiceListProjectSchema) -> dict:
        return {"projects": ["1","2","3"]}
