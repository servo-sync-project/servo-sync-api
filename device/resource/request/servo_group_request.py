from pydantic import BaseModel
from device.domain.model.servo_group import Column

class CreateServoGroupRequest(BaseModel):
    name: str
    num_servos: int
    column: Column
    robot_id: int
    
class UpdateServoGroupNumServosRequest(BaseModel):
    num_servos: int

class UpdateServoGroupNameRequest(BaseModel):
    name: str