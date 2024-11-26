from typing import Optional
from pydantic import BaseModel

class MovementResponse(BaseModel):
    id: int
    coord_x: int
    coord_y: int
    name: str
