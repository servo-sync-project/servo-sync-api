import json
from fastapi import HTTPException, status
from device.domain.model.movement import Movement
from device.domain.persistence.movement_repository import MovementRepository

class MovementService:
    def __init__(self, movementRepository: MovementRepository):
        self.repository = movementRepository
    
    def create(self, movement: Movement):
        if self.repository.findByIdAndCoordinates(movement.robot_id, movement.coord_x, movement.coord_y):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot at these coordinates")
        
        if self.repository.findByRobotIdAndName(movement.robot_id, movement.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot")
        
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
        movements = self.repository.findAllByRobotId(robotId)
        if not movements:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No robots found")
        return movements
    
    def updateById(self, movementId: str, newName: str, newCoordX: int, newCoordY: int):
        movementToUpdate = self.getById(movementId)

        if self.repository.findByIdAndCoordinates(movementToUpdate.robot_id, newCoordX, newCoordY):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot at these coordinates")
        
        if newName != movementToUpdate.name and self.repository.findByRobotIdAndName(movementToUpdate.robot_id, newName):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot")
        
        movementToUpdate.name = newName
        movementToUpdate.coord_x = newCoordX
        movementToUpdate.coord_y = newCoordY
        return self.repository.save(movementToUpdate)
    
    def deleteById(self, movementId: int):
        movementToDelete = self.getById(movementId)
        self.repository.deleteById(movementToDelete.id)
        return True
    
    