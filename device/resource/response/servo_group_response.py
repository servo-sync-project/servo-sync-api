from typing import List
from pydantic import BaseModel


class ServoGroupResponse(BaseModel):
    id: int
    name: str
    num_servos: int
    column: str
    sequence: int
    