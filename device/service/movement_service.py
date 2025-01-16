import logging
from typing import Optional
from fastapi import HTTPException, status
from device.domain.model.movement import Movement
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
    
    def getById(self, movementId: int):
        movement = self.repository.findById(movementId)
        if not movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
        return movement
    
    def getAllByRobotId(self, robotId: int):
        return self.repository.findAllByRobotId(robotId)
    
    def update(self, movementToUpdate: Movement, newName: str, newCoordinates: Optional[str]):
        if newCoordinates and newCoordinates != movementToUpdate.coordinates:
            if self.repository.findByIdAndCoordinates(movementToUpdate.robot_id, newCoordinates):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movement coordinates already exists for this robot")
        
        if newName != movementToUpdate.name and self.repository.findByRobotIdAndName(movementToUpdate.robot_id, newName):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt name already exists for this robot")
        
        movementToUpdate.name = newName
        movementToUpdate.coordinates=newCoordinates
        return self.repository.save(movementToUpdate)
    
    def delete(self, movementToDelete: Movement):
        self.repository.deleteById(movementToDelete.id)
        return True