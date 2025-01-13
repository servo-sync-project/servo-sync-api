from fastapi import UploadFile
from pydantic import BaseModel
from device.domain.model.position_json import PositionJson

class CreateRobotRequest(BaseModel):
    botname: str
    description: str

class UpdateRobotRequest(BaseModel):
    botname: str
    description: str

# class UpdateImageRequest(BaseModel):
#     image_file: UploadFile

# class UpdateConfigImageRequest(BaseModel):
#     config_image_file: UploadFile

class UpdateInitialPositionRequest(BaseModel):
    initial_position: PositionJson

class UpdateCurrentPositionRequest(BaseModel):
    current_position: PositionJson

