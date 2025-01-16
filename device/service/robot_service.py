import json
import logging
import uuid
from fastapi import HTTPException, UploadFile, status
from crosscutting.service.cloudinary_service import CloudinaryService
from device.domain.model.movement import Movement
from device.domain.model.position import Position
from device.domain.persistence.movement_repository import MovementRepository
from device.domain.persistence.position_repository import PositionRepository
from device.domain.persistence.robot_repository import RobotRepository
from device.domain.model.robot import Robot
from crosscutting.mqtt_client import mqttClient
from device.domain.model.position_json import PositionJson, loadPosition
from security.domain.model.user import User
from security.domain.persistence.user_repository import UserRepository

logger = logging.getLogger(__name__)

class RobotService:
    def __init__(self, robotRepository: RobotRepository, 
                 movementRepository: MovementRepository,
                 positionRepository: PositionRepository,
                 cloudinaryService: CloudinaryService):
        self.repository = robotRepository
        self.movementRepository = movementRepository
        self.positionRepository = positionRepository
        self.cloudinaryService = cloudinaryService
    
    def create(self, robot: Robot):                        
        if self.repository.findByBotname(robot.botname):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Robot already exists")
        
        if len(self.repository.findAllByUserId(robot.user_id)) >= 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user reached its limit with 2 robots")
        
        uniqueUuid = str(uuid.uuid4())
        while self.repository.findByUniqueUid(uniqueUuid):
            uniqueUuid = str(uuid.uuid4())
        
        robot.unique_uid = uniqueUuid
        return self.repository.save(robot)
    
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
        return self.repository.findAllByUserId(userId)

    def getAll(self):
        return self.repository.findAll()
    
    def update(self, robotToUpdate: Robot, newBotname: str, newDescription: str): 
        if newBotname != robotToUpdate.botname and self.repository.findByBotname(newBotname):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Robot already exists")
        
        robotToUpdate.botname=newBotname
        robotToUpdate.description=newDescription
        return self.repository.save(robotToUpdate)
    
    def updateImage(self, robotToUpdate: Robot, newImageFile: UploadFile):
        robotToUpdate.image_url = self.cloudinaryService.uploadImage("robots/image", robotToUpdate.unique_uid, newImageFile)
        return self.repository.save(robotToUpdate)

    def updateConfigImage(self, robotToUpdate: Robot, newConfigImageFile: UploadFile):
        robotToUpdate.config_image_url = self.cloudinaryService.uploadImage("robots/config-image", robotToUpdate.unique_uid, newConfigImageFile)
        return self.repository.save(robotToUpdate)

    def updateInitialPosition(self, robotToUpdate: Robot, newInitialPosition: str):
        robotToUpdate.initial_position = newInitialPosition
        return self.repository.save(robotToUpdate)

    def updateCurrentPosition(self, robotToUpdate: Robot, newCurrentPosition: str): 
        robotToUpdate.current_position = newCurrentPosition
        return self.repository.save(robotToUpdate)
    
    def updateConnectionStatusByUUID(self, uniqueUid: int, isConnected: bool):
        robot = self.repository.findByUniqueUid(uniqueUid)
        if robot:
            robot.is_connected_broker = isConnected
            self.repository.save(robot)
    
    def delete(self, robotToDelete: Robot):
        self.repository.deleteById(robotToDelete.id)
        return True
    
    def moveToInitialPosition(self, robot: Robot):
        if not robot.initial_position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
        
        initialPosition = loadPosition(robot.initial_position)
        
        message = [{"delay": initialPosition.delay, "angles": initialPosition.angles}]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        # Actualizar la posición actual del robot en la base de datos
        self.updateCurrentPosition(robot, robot.initial_position)
        return True
    
    def updateAndmoveToInitialPosition(self, robot: Robot, newInitialPosition: str):
        robot = self.updateInitialPosition(robot, newInitialPosition)
        
        initialPosition = loadPosition(robot.initial_position)

        message = [{"delay": initialPosition.delay, "angles": initialPosition.angles}]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        # Actualizar la posición actual del robot en la base de datos
        robot = self.updateCurrentPosition(robot, robot.initial_position)
        return robot
    
    def updateAndMoveToCurrentPosition(self, robot: Robot, newCurrentPosition: str):
        robot = self.updateCurrentPosition(robot, newCurrentPosition)

        currentPosition = loadPosition(robot.current_position)

        message = [{"delay": currentPosition.delay, "angles": currentPosition.angles}]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")

        return robot
    
    # ejecutar movimmientos por su nombre
    def executeMovementById(self, robot: Robot, movementId: int): #robotId: int, movementName: str):            
        positions = self.positionRepository.findAllByMovementId(movementId) 
        if not positions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No positions found")

        message = [{"delay": position.delay, "angles": json.loads(position.angles)} for position in positions]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        self.updateCurrentPosition(robot, PositionJson(delay=positions[-1].delay, angles=json.loads(positions[-1].angles)).model_dump_json())

        return True
    
    # ejecutar movimmientos por su nombre
    def moveToPositionById(self, robot: Robot, positionId: int): #robotId: int, movementName: str, positionSequence: int):
        position = self.positionRepository.findById(positionId)
        
        message = [{"delay": position.delay, "angles": json.loads(position.angles)}]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        self.updateCurrentPosition(robot, PositionJson(delay=position.delay, angles=json.loads(position.angles)).model_dump_json())

        return True
    
    # ---------------- METODOS TRANSACCIONALES PARA EL ALMACENAMIENTO LOCAL DEL ROBOT-----------------
    def saveMovementInLocal(self, robot: Robot, movementId: int):
        movement = self.movementRepository.findById(movementId)
        
        positions = self.positionRepository.findAllByMovementId(movement.id) 
        if not positions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No positions found")
        
        positions_data = [
            {"delay": position.delay, "angles": json.loads(position.angles)} for position in positions
        ]

        message = {
            "name": movement.name, 
            "positions": positions_data
        }

        topic = f"robot/{robot.unique_uid}/access/storage/save-movement"
        mqttClient.publish(topic, json.dumps(message))
        logger.info(f"Data sent to topic {topic}")

        return True
     
    def deleteMovementInLocal(self, robot: Robot, movementId: int):
        movement = self.movementRepository.findById(movementId)

        message = { "name": movement.name }

        topic = f"robot/{robot.unique_uid}/access/storage/delete-movement"
        mqttClient.publish(topic, json.dumps(message))
        logger.info(f"Data sent to topic {topic}")

        return True
    
    #{60, 150, 30, 30, 120, 30, 150, 150, 90, 90, 0, 90, 90, 180, 90, 90}
    def saveInitialPositionInLocal(self, robot: Robot):
        if not robot.initial_position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Initial position not found")
        
        message = loadPosition(robot.initial_position).model_dump()

        topic = f"robot/{robot.unique_uid}/access/storage/save-initial-position"
        mqttClient.publish(topic, json.dumps(message))
        logger.info(f"Data sent to topic {topic}")

        return True
    
    def clearLocalStorage(self, robot: Robot):
        topic = f"robot/{robot.unique_uid}/access/storage/clear"
        mqttClient.publish(topic)
        logger.info(f"Data sent to topic {topic}")

        return True
    
    def validateMovementAccess(self, robotId: int, movementId: int):
        robot = self.repository.findByMovementId(movementId)
        if not robot or robotId != robot.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return robot
        
    def validatePositionAccess(self, robotId: int, positionId: int):
        robot = self.repository.findByPositionId(positionId)
        if not robot or robotId != robot.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return robot
    
# robot -> movement -> position
# position -> movement -> robot
