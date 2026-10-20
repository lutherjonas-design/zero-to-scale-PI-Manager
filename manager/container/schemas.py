from typing import Optional, Literal
from pydantic import BaseModel #pyright: ignore[reportMissingImports]

class BaseRequest(BaseModel):
    action: str