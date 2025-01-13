from typing import Optional
from pydantic import BaseModel, Field

from device.domain.model.coordinates_json import CoordinatesJson

class CreateMovementRequest(BaseModel):
    name: str
    coordinates: Optional[CoordinatesJson]
    robot_id: int

class UpdateMovementRequest(BaseModel):
    name: str
    coordinates: Optional[CoordinatesJson]

    # coord_x: int = Field(..., ge=0, le=12)
    # coord_y: int = Field(..., ge=0, le=6)