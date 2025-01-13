import json
from device.domain.model.servo_group import ServoGroup
from device.resource.request.servo_group_request import CreateServoGroupRequest
from device.resource.response.position_response import PositionResponse
from device.resource.response.servo_group_response import ServoGroupResponse

class ServoGroupMapper:
    @staticmethod
    def createRequestToModel(request: CreateServoGroupRequest) -> ServoGroup:        
        return ServoGroup(name=request.name,
                          num_servos=request.num_servos, 
                          column=request.column,
                          robot_id=request.robot_id)
    
    @staticmethod
    def modelToResponse(servoGroup: ServoGroup) -> PositionResponse:
        return ServoGroupResponse(id=servoGroup.id, 
                                  name=servoGroup.name, 
                                  num_servos=servoGroup.num_servos,
                                  column=servoGroup.column.value, 
                                  sequence=servoGroup.sequence)