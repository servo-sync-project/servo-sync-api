from typing import List
from pydantic import BaseModel


class ServoGroupResponse(BaseModel):
    id: int
    name: str
    column: str
    sequence: int
    servo_angles: List[int]