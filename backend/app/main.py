from fastapi import FastAPI

from .config import settings

app = FastAPI(title=settings.app_name)


@app.get("/")
def root():
    return {"service": settings.app_name, "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}
