from pydantic import BaseModel, Field

class CreateMovementRequest(BaseModel):
    name: str
    coord_x: int = Field(..., ge=0, le=12)
    coord_y: int = Field(..., ge=0, le=6)
    robot_id: int

class UpdateMovementRequest(BaseModel):
    name: str
    coord_x: int = Field(..., ge=0, le=12)
    coord_y: int = Field(..., ge=0, le=6)

