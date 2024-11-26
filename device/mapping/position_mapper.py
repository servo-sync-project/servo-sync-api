import json
from device.domain.model.position import Position
from device.resource.request.position_request import CreatePositionRequest, UpdatePositionRequest
from device.resource.response.position_response import PositionResponse

class PositionMapper:
    @staticmethod
    def createRequestToModel(request: CreatePositionRequest) -> Position:
        return Position(delay=request.delay, 
                        angles=json.dumps(request.angles), 
                        movement_id=request.movement_id)
    
    @staticmethod
    def updateRequestToModel(request: UpdatePositionRequest) -> Position:
        return Position(delay=request.delay, 
                        angles=json.dumps(request.angles))
    
    @staticmethod
    def modelToResponse(position: Position) -> PositionResponse:
        return PositionResponse(id=position.id, 
                                sequence=position.sequence, 
                                delay=position.delay, 
                                angles=json.loads(position.angles))
