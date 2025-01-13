import json
from pydantic import BaseModel, Field


class CoordinatesJson(BaseModel):
    coord_x: int = Field(..., ge=1, le=9)
    coord_y: int = Field(..., ge=1, le=4)

def loadCoordinates(coordinates: str) -> CoordinatesJson:
    return CoordinatesJson(**json.loads(coordinates))