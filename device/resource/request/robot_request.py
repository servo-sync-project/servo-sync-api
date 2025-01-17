from pydantic import BaseModel
from device.domain.model.position_json import PositionJson

class CreateRobotRequest(BaseModel):
    botname: str
    description: str

class UpdateRobotRequest(BaseModel):
    botname: str
    description: str

class UpdateInitialPositionRequest(BaseModel):
    initial_position: PositionJson

class UpdateCurrentPositionRequest(BaseModel):
    current_position: PositionJson

