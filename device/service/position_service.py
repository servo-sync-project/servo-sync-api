import json
from fastapi import HTTPException, status
from device.domain.model.position import Position
from device.domain.persistence.position_repository import PositionRepository
from security.domain.persistence.user_repository import UserRepository

class PositionService:
    def __init__(self, positionRepository: PositionRepository):
        self.repository = positionRepository

    def create(self, position: Position):
        if len(self.repository.findAllByMovementId(position.movement_id)) >= 16:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movement reached its limit with 16 positions")
        
        max_sequence = self.repository.findMaxSequenceByMovementId(position.movement_id)
        position.sequence = max_sequence + 1
        return self.repository.save(position)

    def getById(self, positionId: int):
        position = self.repository.findById(positionId)
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
        return position
    
    def getAllByMovementId(self, movementId: int):
        return self.repository.findAllByMovementId(movementId)
    
    def update(self, positionToUpdate: Position, newDelay: int, newAngles: str):
        positionToUpdate.delay = newDelay
        positionToUpdate.angles = newAngles
        return self.repository.save(positionToUpdate)
        
    def increaseSequence(self, positionToIncrease: Position):
        max_sequence = self.repository.findMaxSequenceByMovementId(positionToIncrease.movement_id)

        if positionToIncrease.sequence >= max_sequence:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position is already at the maximum sequence")
        
        return self.repository.increaseSequence(positionToIncrease)        
    
    def decreaseSequence(self, positionToDecrease: Position):
        if positionToDecrease.sequence <= 1:  # La secuencia mínima es 1
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position is already at the minimum sequence")
        
        return self.repository.decreaseSequence(positionToDecrease)
    
    def delete(self, positionToDelete: Position):
        self.repository.deleteById(positionToDelete.id)
        self.repository.decrementSequenceAfter(positionToDelete)
        return True
    

            