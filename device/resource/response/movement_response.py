from typing import Optional
from pydantic import BaseModel

from device.domain.model.coordinates_json import CoordinatesJson

class MovementResponse(BaseModel):
    id: int
    name: str
    coordinates: Optional[CoordinatesJson]
    
