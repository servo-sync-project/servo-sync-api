from typing import Optional
from pydantic import BaseModel

from device.domain.model.position_json import PositionJson

class RobotResponse(BaseModel):
    id: int
    unique_uid: str
    botname: str
    description: str
    image_url: Optional[str]
    config_image_url: Optional[str]
    initial_position: Optional[PositionJson]
    current_position: Optional[PositionJson]
    is_connected_broker: bool

class RobotResponseForAll(BaseModel):
    id: int
    botname: str
    description: str
    image_url: Optional[str]
    is_connected_broker: bool
    
    