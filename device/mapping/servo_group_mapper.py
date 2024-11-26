import json
from device.domain.model.servo_group import ServoGroup
from device.resource.request.servo_group_request import CreateServoGroupRequest
from device.resource.response.position_response import PositionResponse
from device.resource.response.servo_group_response import ServoGroupResponse

class ServoGroupMapper:
    @staticmethod
    def createRequestToModel(request: CreateServoGroupRequest) -> ServoGroup:        
        return ServoGroup(name=request.name,
                          servo_angles=json.dumps(request.servo_angles), 
                          column=request.column)
    
    @staticmethod
    def modelToResponse(servoGroup: ServoGroup) -> PositionResponse:
        return ServoGroupResponse(id=servoGroup.id, 
                                  name=servoGroup.name, 
                                  column=servoGroup.column.value, 
                                  sequence=servoGroup.sequence,
                                  servo_angles=json.loads(servoGroup.servo_angles))