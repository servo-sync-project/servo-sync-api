from device.domain.model.movement import Movement
from device.resource.request.movement_request import CreateMovementRequest, UpdateMovementRequest
from device.resource.response.movement_response import MovementResponse

class MovementMapper:
    @staticmethod
    def createRequestToModel(request: CreateMovementRequest) -> Movement:
        return Movement(name=request.name, 
                        coord_x=request.coord_x,
                        coord_y=request.coord_y,
                        robot_id=request.robot_id)
    
    @staticmethod
    def modelToResponse(request: Movement) -> MovementResponse:
        return Movement(id=request.id, 
                        name=request.name,
                        coord_x=request.coord_x,
                        coord_y=request.coord_y)
