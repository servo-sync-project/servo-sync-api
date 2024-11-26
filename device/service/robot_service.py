import json
from typing import List
import uuid
from fastapi import HTTPException, status
from device.domain.model.movement import Movement
from device.domain.model.servo_group import ServoGroup
from device.domain.persistence.movement_repository import MovementRepository
from device.domain.persistence.position_repository import PositionRepository
from device.domain.persistence.robot_repository import RobotRepository
from device.domain.model.robot import Robot
from crosscutting.mqtt_client import mqttClient
from device.domain.model.position_json import loadPosition
from device.domain.persistence.servo_group_repository import ServoGroupRepository
from security.domain.persistence.user_repository import UserRepository

class RobotService:
    def __init__(self, robotRepository: RobotRepository, 
                 servoGroupRepository: ServoGroupRepository,
                 movementRepository: MovementRepository, 
                 positionRepository: PositionRepository):
        self.repository = robotRepository
        self.servoGroupRepository = servoGroupRepository
        self.movementRepository = movementRepository
        self.positionRepository = positionRepository
    
    def create(self, robot: Robot, servoGroups: List[ServoGroup]):                        
        if self.repository.findByBotname(robot.botname):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Robot already exists")
        
        if len(self.repository.findAllByUserId(robot.user_id)) >= 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user reached its limit with 2 robots")
        
        uniqueUuid = str(uuid.uuid4())
        while self.repository.findByUniqueUid(uniqueUuid):
            uniqueUuid = str(uuid.uuid4())
        
        robot.unique_uid = uniqueUuid
        robotCreated = self.repository.save(robot)
        for servoGroup in servoGroups:
            servoGroup.robot_id=robotCreated.id
            max_sequence = self.servoGroupRepository.findMaxSequenceByRobotIdAndColumn(servoGroup.robot_id, servoGroup.column)
            servoGroup.sequence = max_sequence + 1
            self.servoGroupRepository.save(servoGroup)
        return robotCreated
    
    def validateAccess(self, userId: int, robotId: int):
        user = self.repository.findMyUserById(robotId)
        if userId != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return True
    
    def getById(self, robotId: int):
        robot = self.repository.findById(robotId)
        if not robot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
        return robot
    
    def getByUniqueUid(self, uniqueUid: str):
        robot = self.repository.findByUniqueUid(uniqueUid)
        if not robot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
        return robot
    
    def getByBotname(self, botname: str):
        robot = self.repository.findByBotname(botname)
        if not robot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
        return robot
    
    def getAllByUserId(self, userId: int):
        robots = self.repository.findAllByUserId(userId)
        if not robots:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No robots were found for this user")
        return robots

    def getAll(self):
        robots = self.repository.findAll()
        if not robots:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No robots found")
        return robots
    
    def updateById(self, robotId: str, newBotname: str, newImageUrl: str,  newDescription: str): 
        robotToUpdate = self.getById(robotId) 

        if newBotname != robotToUpdate.botname and self.repository.findByBotname(newBotname):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Robot already exists")
        
        robotToUpdate.image_url=newImageUrl
        robotToUpdate.botname=newBotname
        robotToUpdate.description=newDescription
        return self.repository.save(robotToUpdate)
    
    def updateInitialPositionById(self, robotId: int, newInitialPosition: str):
        robotToUpdate = self.getById(robotId)
        robotToUpdate.initial_position = newInitialPosition
        return self.repository.save(robotToUpdate)

    def updateCurrentPositionById(self, robotId: int, newCurrentPosition: str):
        robotToUpdate = self.getById(robotId)        
        # robotToUpdate.current_position = newCurrentPosition
        return self.repository.save(robotToUpdate)
    
    def updateConnectionStatus(self, robotId: int, isConnected: bool):
        robot = self.getById(robotId)
        robot.is_connected_broker = isConnected
        return self.repository.save(robot)
    
    def deleteById(self, robotId: int):
        robotToDelete = self.getById(robotId)
        self.repository.deleteById(robotToDelete.id)
        return True
    
    def moveToInitialPositionById(self, robotId: int):
        # Verificar si el robot está conectado
        robot = self.getById(robotId)

        message = {
            "positions": [{"delay": loadPosition(robot.initial_position).delay, "angles": loadPosition(robot.initial_position).angles}]  # Duración estimada para alcanzar la posición inicial
        }

        topic = f"robot/{robot.botname}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        # Actualizar la posición actual del robot en la base de datos
        self.updateCurrentPositionById(robot.id, robot.initial_position)
        return True
    
    def updateAndMoveToCurrentPositionById(self, robotId: int, newCurrentPosition: str):
        robot = self.updateCurrentPositionById(robotId, newCurrentPosition)

        message = {
            "positions": [{"delay": loadPosition(robot.current_position).delay, "angles": loadPosition(robot.current_position).angles}]
        }

        topic = f"robot/{robot.botname}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")

        return True
    
    def sendPositionByIdAndMovementName(self, robotId: int, movementName: str):
        movement = self.movementRepository.findByRobotIdAndName(robotId, movementName)
        if not movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
        
        positions = self.positionRepository.findAllByMovementId(movement.id) 
        if not positions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No positions found")
        
        robot = self.getById(movement.robot_id)

        message = {
            "positions": [{"delay": position.delay, "angles": json.loads(position.angles)} for position in positions]
        }

        topic = f"robot/{robot.botname}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")

        self.updateCurrentPositionById(robot.id, positions[-1].angles)
        return True
    
    #{60, 150, 30, 30, 120, 30, 150, 150, 90, 90, 0, 90, 90, 180, 90, 90}
    def saveDataByIdAndMovementName(self, robotId: int, movementName: str):
        movement = self.movementRepository.findByRobotIdAndName(robotId, movementName)
        if not movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
        
        positions = self.positionRepository.findAllByMovementId(movement.id) 
        if not positions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No positions found")
        
        robot = self.getById(movement.robot_id)

        positions_data = [
            {"delay": position.delay, "angles": json.loads(position.angles)} for position in positions
        ]

        message = {
            "initial_position": json.loads(robot.initial_position),
            "movement": {"name": movement.name, "positions": positions_data}
        }

        topic = f"robot/{robot.botname}/access/save"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")

        return True
    
# robot -> movement -> position
# position -> movement -> robot
