from typing import Optional
from pydantic import BaseModel

class PositionResponse(BaseModel):
    id: int
    sequence: int
    delay: int
    angles: list[int]
