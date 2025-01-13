import json
import logging
from typing import Optional
from fastapi import HTTPException, status
from device.domain.model.movement import Movement
from crosscutting.mqtt_client import mqttClient
from device.domain.persistence.movement_repository import MovementRepository
from device.domain.persistence.position_repository import PositionRepository

logger = logging.getLogger(__name__)

class MovementService:
    def __init__(self, movementRepository: MovementRepository, positionRepository: PositionRepository):
        self.repository = movementRepository
        self.positionRepository = positionRepository
    
    def create(self, movement: Movement):
        if movement.coordinates:
            if self.repository.findByIdAndCoordinates(movement.robot_id, movement.coordinates):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movement coordinates already exists for this robot")
            
        if self.repository.findByRobotIdAndName(movement.robot_id, movement.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movement already exists for this robot")
        
        if len(self.repository.findAllByRobotId(movement.robot_id)) >= 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The robot reached its limit with 10 movements")
        
        return self.repository.save(movement)
    
    def validateAccess(self, userId: int, movementId: int):
        user = self.repository.findMyUserById(movementId)
        if userId != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return True
    
    def getById(self, movementId: int):
        movement = self.repository.findById(movementId)
        if not movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
        return movement
    
    def getAllByRobotId(self, robotId: int):
        return self.repository.findAllByRobotId(robotId)
    
    def updateById(self, movementId: str, newName: str, newCoordinates: Optional[str]):
        movementToUpdate = self.getById(movementId)
        # if newCoordinates:
        #     if (loadCoordinates(newCoordinates).coord_x != loadCoordinates(movementToUpdate.coordinates).coord_x or loadCoordinates(newCoordinates).coord_y != loadCoordinates(movementToUpdate.coordinates).coord_y) and self.repository.findByIdAndCoordinates(movementToUpdate.robot_id, newCoordX, newCoordY):
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt coordinate already exists for this robot")

        if newCoordinates and newCoordinates != movementToUpdate.coordinates:
            if self.repository.findByIdAndCoordinates(movementToUpdate.robot_id, newCoordinates):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movement coordinates already exists for this robot")
        
        if newName != movementToUpdate.name and self.repository.findByRobotIdAndName(movementToUpdate.robot_id, newName):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt name already exists for this robot")
        
        movementToUpdate.name = newName
        movementToUpdate.coordinates=newCoordinates
        return self.repository.save(movementToUpdate)
    
    def deleteById(self, movementId: int):
        movementToDelete = self.getById(movementId)
        self.repository.deleteById(movementToDelete.id)
        return True
    
    # ---------------- METODOS TRANSACCIONALES PARA EL ALMACENAMIENTO LOCAL DEL ROBOT-----------------
    def saveMovementInLocalById(self, movementId: int):
        movement = self.getById(movementId)

        robot = self.repository.findMyRobotById(movementId)
        
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
     
    def deleteMovementInLocalById(self, movementId: int):
        movement = self.getById(movementId)

        robot = self.repository.findMyRobotById(movementId)

        message = { "name": movement.name }

        topic = f"robot/{robot.unique_uid}/access/storage/delete-movement"
        mqttClient.publish(topic, json.dumps(message))
        logger.info(f"Data sent to topic {topic}")

        return True