from typing import List
from pydantic import BaseModel, Field, field_validator

class CreatePositionRequest(BaseModel):
    delay: int = Field(..., ge=100, le=1000)
    angles: List[int]
    movement_id: int

    @field_validator('angles', mode='before')
    def validate_angles(cls, value):
        if not isinstance(value, list):
            raise ValueError('Angles must be a list of integers.')
        if any(not 0 <= angle <= 180 for angle in value):
            raise ValueError('Each angle must be between 0 and 180.')
        return value
    
class UpdatePositionRequest(BaseModel):
    delay: int = Field(..., ge=100, le=1000)
    angles: List[int]

    @field_validator('angles', mode='before')
    def validate_angles(cls, value):
        if not isinstance(value, list):
            raise ValueError('Angles must be a list of integers.')
        if any(not 0 <= angle <= 180 for angle in value):
            raise ValueError('Each angle must be between 0 and 180.')
        return value
