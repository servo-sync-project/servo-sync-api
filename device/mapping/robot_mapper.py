from device.domain.model.robot import Robot
from device.domain.model.position_json import loadPosition
from device.resource.request.robot_request import CreateRobotRequest
from device.resource.response.robot_response import RobotResponse, RobotResponseForAll

class RobotMapper:
    @staticmethod
    def createRequestToModel(request: CreateRobotRequest, currentUserId: int) -> Robot:
        return Robot(botname=request.botname,
                     description=request.description,
                     user_id=currentUserId)
    
    @staticmethod
    def modelToResponse(robot: Robot) -> RobotResponse:
        return RobotResponse(id=robot.id, 
                             unique_uid=robot.unique_uid,
                             botname=robot.botname, 
                             description=robot.description,
                             image_url=robot.image_url,
                             config_image_url=robot.config_image_url,
                             initial_position=robot.initial_position and loadPosition(robot.initial_position),
                             current_position=robot.current_position and loadPosition(robot.current_position),
                             is_connected_broker=robot.is_connected_broker)
    
    @staticmethod
    def modelToResponseForAll(robot: Robot) -> RobotResponse:
        return RobotResponseForAll(id=robot.id, 
                                   botname=robot.botname,
                                   description=robot.description,
                                   image_url=robot.image_url,
                                   is_connected_broker=robot.is_connected_broker)