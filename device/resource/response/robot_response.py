from pydantic import BaseModel

from device.domain.model.position_json import PositionJson

class RobotResponse(BaseModel):
    id: int
    unique_uid: str
    image_url: str
    botname: str
    is_connected_broker: bool
    description: str
    initial_position: PositionJson
    

class RobotResponseForAll(BaseModel):
    id: int
    image_url: str
    botname: str
    is_connected_broker: bool
    num_servos: int
    description: str
    