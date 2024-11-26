import json
from typing import List
from device.domain.model.movement import Movement
from device.domain.model.robot import Robot
from device.domain.model.position_json import loadPosition
from device.domain.model.servo_group import ServoGroup
from device.mapping.servo_group_mapper import ServoGroupMapper
from device.resource.request.robot_request import CreateRobotRequest
from device.resource.response.robot_response import RobotResponse, RobotResponseForAll

class RobotMapper:
    @staticmethod
    def createRequestToModel(request: CreateRobotRequest, currentUserId: int) -> Robot:
        # initial_position_angles = []
        # servoGroups = []
        # for servoGroup in request.initial_servo_groups:
        #     servoGroups.append(ServoGroup(name=servoGroup.name,
        #                               servo_angles=json.dumps(servoGroup.servo_angles),  # Convertir a JSON si es necesario
        #                               column=servoGroup.column))
        #     for angle in servoGroup.servo_angles:
        #         initial_position_angles.append(angle)

        return Robot(
            image_url=request.image_url,
            botname=request.botname,
            description=request.description,
            initial_position=json.dumps(request.initial_position),
            user_id=currentUserId
        )
        
        # return robot, servoGroups
    
    @staticmethod
    def modelToResponse(robot: Robot) -> RobotResponse:
        return RobotResponse(id=robot.id, 
                             unique_uid=robot.unique_uid,
                             image_url=robot.image_url,
                             botname=robot.botname, 
                             is_connected_broker=robot.is_connected_broker,
                             description=robot.description,
                             initial_position=loadPosition(robot.initial_position))
    
    @staticmethod
    def modelToResponseForAll(robot: Robot) -> RobotResponse:
        return RobotResponseForAll(id=robot.id, 
                                   image_url=robot.image_url,
                                   botname=robot.botname,
                                   is_connected_broker=robot.is_connected_broker,
                                   num_servos=len(loadPosition(robot.initial_position)),
                                   description=robot.description)