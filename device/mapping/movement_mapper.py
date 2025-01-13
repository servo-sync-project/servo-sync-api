from device.domain.model.coordinates_json import loadCoordinates
from device.domain.model.movement import Movement
from device.resource.request.movement_request import CreateMovementRequest, UpdateMovementRequest
from device.resource.response.movement_response import MovementResponse

class MovementMapper:
    @staticmethod
    def createRequestToModel(request: CreateMovementRequest) -> Movement:
        return Movement(name=request.name, 
                        coordinates=request.coordinates and request.coordinates.model_dump_json(),
                        robot_id=request.robot_id)
    
    @staticmethod
    def modelToResponse(request: Movement) -> MovementResponse:
        return MovementResponse(id=request.id, 
                                name=request.name,
                                coordinates=request.coordinates and loadCoordinates(request.coordinates))
