#!/usr/bin/env python3
from fastapi import APIRouter
api_router = APIRouter()

# projects routes
api_router.include_router(project_router, prefix="/projects", tags=["projects"])
api_router.include_router(files_router, prefix="/files", tags=["files"])

@api_router.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
