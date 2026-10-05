#!/usr/bin/env python3
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "fastapi-service"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()