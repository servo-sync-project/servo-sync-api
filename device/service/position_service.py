import json
from fastapi import HTTPException, status
from device.domain.model.position import Position
from device.domain.persistence.position_repository import PositionRepository

class PositionService:
    def __init__(self, positionRepository: PositionRepository):
        self.repository = positionRepository

    def create(self, position: Position):
        if len(self.repository.findAllByMovementId(position.movement_id)) >= 16:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movement reached its limit with 16 positions")
        
        max_sequence = self.repository.findMaxSequenceByMovementId(position.movement_id)
        position.sequence = max_sequence + 1
        return self.repository.save(position)
    
    def validateAccess(self, userId: int, positionId: int):
        user = self.repository.findMyUserById(positionId)
        if userId != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return True

    def getById(self, positionId: int):
        position = self.repository.findById(positionId)
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
        return position
    
    def getAllByMovementId(self, movementId: int):
        position = self.repository.findAllByMovementId(movementId)
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No positions found")
        return position
    
    def updateById(self, positionId: int, newPosition: Position):
        positionToUpdate = self.getById(positionId)
        positionToUpdate.delay = newPosition.delay
        positionToUpdate.angles = newPosition.angles
        return self.repository.save(positionToUpdate)
    
    def deleteById(self, positionId: int):
        positionToDelete = self.getById(positionId)
        self.repository.deleteById(positionToDelete.id)
        self.repository.decrementSequenceAfter(positionToDelete)
        return True
    
    def increaseSequenceById(self, positionId: int):
        positionToIncrease = self.getById(positionId)
        max_sequence = self.repository.findMaxSequenceByMovementId(positionToIncrease.movement_id)

        if positionToIncrease.sequence < max_sequence:
            return self.repository.increaseSequence(positionToIncrease)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position is already at the maximum sequence")
    
    def decreaseSequenceById(self, positionId: int):
        positionToDecrease = self.getById(positionId)

        if positionToDecrease.sequence > 1:  # La secuencia mínima es 1
            return self.repository.decreaseSequence(positionToDecrease)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position is already at the minimum sequence")