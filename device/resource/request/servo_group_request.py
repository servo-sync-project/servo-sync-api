from typing import List
from pydantic import BaseModel, Field, field_validator

from device.domain.model.servo_group import Column


class CreateServoGroupRequest(BaseModel):
    name: str
    servo_angles: List[int]
    column: Column

    @field_validator('servo_angles', mode='before')
    def validate_angles(cls, value):
        if not isinstance(value, list):
            raise ValueError('Servo Angles must be a list of integers.')
        if any(not 0 <= angle <= 180 for angle in value):
            raise ValueError('Each servo angle must be between 0 and 180.')
        return value
    
class UpdateServoGroupRequest(BaseModel):
    name: str
    servo_angles: List[int]

    @field_validator('servo_angles', mode='before')
    def validate_angles(cls, value):
        if not isinstance(value, list):
            raise ValueError('Servo Angles must be a list of integers.')
        if any(not 0 <= angle <= 180 for angle in value):
            raise ValueError('Each servo angle must be between 0 and 180.')
        return value