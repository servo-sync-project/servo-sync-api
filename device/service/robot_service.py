import json
import logging
import uuid
from fastapi import HTTPException, UploadFile, status
from crosscutting.service.cloudinary_service import CloudinaryService
from device.domain.persistence.movement_repository import MovementRepository
from device.domain.persistence.position_repository import PositionRepository
from device.domain.persistence.robot_repository import RobotRepository
from device.domain.model.robot import Robot
from crosscutting.mqtt_client import mqttClient
from device.domain.model.position_json import PositionJson, loadPosition

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
        return self.repository.findAllByUserId(userId)

    def getAll(self):
        return self.repository.findAll()
    
    def updateById(self, robotId: str, newBotname: str, newDescription: str): 
        robotToUpdate = self.getById(robotId) 

        if newBotname != robotToUpdate.botname and self.repository.findByBotname(newBotname):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Robot already exists")
        
        robotToUpdate.botname=newBotname
        robotToUpdate.description=newDescription
        return self.repository.save(robotToUpdate)
    
    def updateImageById(self, robotId: int, newImageFile: UploadFile):
        robotToUpdate = self.getById(robotId)
        robotToUpdate.image_url = self.cloudinaryService.uploadImage("robots/image", robotToUpdate.unique_uid, newImageFile)
        return self.repository.save(robotToUpdate)

    def updateConfigImageById(self, robotId: int, newConfigImageFile: UploadFile):
        robotToUpdate = self.getById(robotId)
        robotToUpdate.config_image_url = self.cloudinaryService.uploadImage("robots/config-image", robotToUpdate.unique_uid, newConfigImageFile)
        return self.repository.save(robotToUpdate)

    def updateInitialPositionById(self, robotId: int, newInitialPosition: str):
        robotToUpdate = self.getById(robotId)
        robotToUpdate.initial_position = newInitialPosition
        return self.repository.save(robotToUpdate)

    def updateCurrentPositionById(self, robotId: int, newCurrentPosition: str):
        robotToUpdate = self.getById(robotId)        
        robotToUpdate.current_position = newCurrentPosition
        return self.repository.save(robotToUpdate)
    
    def updateConnectionStatusByUUID(self, uniqueUid: int, isConnected: bool):
        # robot = self.getByUniqueUid(uniqueUid)
        robot = self.repository.findByUniqueUid(uniqueUid)
        if robot:
            robot.is_connected_broker = isConnected
            self.repository.save(robot)
    
    def deleteById(self, robotId: int):
        robotToDelete = self.getById(robotId)
        self.repository.deleteById(robotToDelete.id)
        return True
    
    def moveToInitialPositionById(self, robotId: int):
        robot = self.getById(robotId)
        if not robot.initial_position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
        
        initialPosition = loadPosition(robot.initial_position)
        
        message = [{"delay": initialPosition.delay, "angles": initialPosition.angles}]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        # Actualizar la posición actual del robot en la base de datos
        self.updateCurrentPositionById(robot.id, robot.initial_position)
        return True
    
    def updateAndmoveToInitialPositionById(self, robotId: int, newInitialPosition: str):
        robot = self.updateInitialPositionById(robotId, newInitialPosition)
        
        initialPosition = loadPosition(robot.initial_position)

        message = [{"delay": initialPosition.delay, "angles": initialPosition.angles}]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        # Actualizar la posición actual del robot en la base de datos
        robot = self.updateCurrentPositionById(robot.id, robot.initial_position)
        return robot
    
    def updateAndMoveToCurrentPositionById(self, robotId: int, newCurrentPosition: str):
        robot = self.updateCurrentPositionById(robotId, newCurrentPosition)

        currentPosition = loadPosition(robot.current_position)

        message = [{"delay": currentPosition.delay, "angles": currentPosition.angles}]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")

        return robot
    
    # ejecutar movimmientos por su nombre
    def executeMovementByIdAndYourId(self, robotId: int, movementId: int): #robotId: int, movementName: str):
        movement = self.movementRepository.findById(movementId)
        if not movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
        
        positions = self.positionRepository.findAllByMovementId(movement.id) 
        if not positions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No positions found")
        
        # robot = self.getById(movement.robot_id)

        robot = self.movementRepository.findMyRobotById(movementId) 
        if not robot or robot.id != robotId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="robot not found or not access")

        message = [{"delay": position.delay, "angles": json.loads(position.angles)} for position in positions]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        self.updateCurrentPositionById(robot.id, PositionJson(delay=positions[-1].delay, angles=json.loads(positions[-1].angles)).model_dump_json())

        return True
    
    # ejecutar movimmientos por su nombre
    def moveToPositionByIdAndYourId(self, robotId: int, positionId: int): #robotId: int, movementName: str, positionSequence: int):
        position = self.positionRepository.findById(positionId) 
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
        
        # robot = self.getById(movement.robot_id)

        robot = self.positionRepository.findMyRobotById(positionId) 
        if not robot or robot.id != robotId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="robot not found or not access")
        
        message = [{"delay": position.delay, "angles": json.loads(position.angles)}]

        topic = f"robot/{robot.unique_uid}/access/positions"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        self.updateCurrentPositionById(robot.id, PositionJson(delay=position.delay, angles=json.loads(position.angles)).model_dump_json())

        return True
    
    # ---------------- METODOS TRANSACCIONALES PARA EL ALMACENAMIENTO LOCAL DEL ROBOT-----------------
    #{60, 150, 30, 30, 120, 30, 150, 150, 90, 90, 0, 90, 90, 180, 90, 90}
    def saveInitialPositionInLocalById(self, robotId: int):
        robot = self.getById(robotId)
        if not robot.initial_position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
        
        message = loadPosition(robot.initial_position).model_dump()

        topic = f"robot/{robot.unique_uid}/access/storage/save-initial-position"
        mqttClient.publish(topic, json.dumps(message))
        logger.info(f"Data sent to topic {topic}")

        return True
    
    def clearLocalStorageById(self, robotId: int):
        robot = self.getById(robotId)

        topic = f"robot/{robot.unique_uid}/access/storage/clear"
        mqttClient.publish(topic)
        logger.info(f"Data sent to topic {topic}")

        return True
    
# robot -> movement -> position
# position -> movement -> robot
