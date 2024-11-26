from typing import List
from pydantic import BaseModel, Field, model_validator
from device.domain.model.position_json import PositionJson
from device.resource.request.servo_group_request import CreateServoGroupRequest, UpdateServoGroupRequest

class CreateRobotRequest(BaseModel):
    image_url: str
    botname: str
    description: str
    initial_position: PositionJson
    # initial_position_delay: int = Field(..., ge=100, le=1000)
    # initial_servo_groups: List[CreateServoGroupRequest]
    
    # @model_validator(mode="before")
    # def validate_and_sort_servo_groups(cls, values):
    #     initial_servo_groups: List[CreateServoGroupRequest] = values.get("initial_servo_groups", [])
        
    #     # Validar que los nombres sean únicos
    #     names = [servo_group.name for servo_group in initial_servo_groups]
    #     if len(names) != len(set(names)):
    #         raise ValueError("Servo group names must be unique.")
        
    #     # Ordenar los grupos de servos por columna y secuencia
    #     sorted_initial_servo_groups = sorted(
    #         initial_servo_groups,
    #         key=lambda sg: (["right", "middle", "left"].index(sg.column))
    #     )
        
    #     # Actualizar los valores con los grupos ordenados
    #     values["initial_servo_groups"] = sorted_initial_servo_groups
    #     return values

class UpdateRobotRequest(BaseModel):
    botname: str
    image_url: str
    description: str

    # initial_position: PositionJson
    # initial_position_delay: int = Field(..., ge=100, le=1000)
    # initial_servo_groups: List[UpdateServoGroupRequest]
    
class UpdateInitialPositionRequest(BaseModel):
    initial_position: PositionJson

# class UpdateCurrentPositionRequest(BaseModel):
#     current_position: PositionJson

