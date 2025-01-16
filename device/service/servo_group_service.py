import json
from fastapi import HTTPException, status
from device.domain.model.servo_group import ServoGroup
from device.domain.persistence.servo_group_repository import ServoGroupRepository
from security.domain.persistence.user_repository import UserRepository

class ServoGroupService:
    def __init__(self, servoGroupRepository: ServoGroupRepository):
        self.repository = servoGroupRepository
    
    def create(self, servoGroup: ServoGroup):
        if self.repository.findByRobotIdAndName(servoGroup.robot_id, servoGroup.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The servo group already exists for this robot")

        if sum(existingServoGroup.num_servos
               for existingServoGroup in self.repository.findAllByRobotId(servoGroup.robot_id)) >= 24:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The robot reached its limit with 24 Servo Angles")
        
        max_sequence = self.repository.findMaxSequenceByRobotIdAndColumn(servoGroup.robot_id, servoGroup.column)
        servoGroup.sequence = max_sequence + 1
        return self.repository.save(servoGroup)
    
    def getById(self, servoGroupId: int):
        servoGroup = self.repository.findById(servoGroupId)
        if not servoGroup:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servo group not found")
        return servoGroup
    
    def getAllByRobotId(self, servoGroupId: int):
        return self.repository.findAllByRobotId(servoGroupId)
    
    def updateNumServos(self, servoGroupToUpdate: ServoGroup, newNumServos: int):
        servoGroupToUpdate.num_servos = newNumServos
        return self.repository.save(servoGroupToUpdate)
    
    def updateName(self, servoGroupToUpdate: ServoGroup, newName: str):
        if newName != servoGroupToUpdate.name and self.repository.findByRobotIdAndName(servoGroupToUpdate.robot_id, newName):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The servo group already exists for this robot")
        
        servoGroupToUpdate.name = newName
        return self.repository.save(servoGroupToUpdate)
    
    def increaseSequence(self, servoGroupToIncrease: ServoGroup):
        max_sequence = self.repository.findMaxSequenceByRobotIdAndColumn(servoGroupToIncrease.robot_id, servoGroupToIncrease.column)

        if servoGroupToIncrease.sequence >= max_sequence:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position is already at the maximum sequence")
        
        return self.repository.increaseSequence(servoGroupToIncrease)
    
    def decreaseSequence(self, servoGroupToDecrease: ServoGroup):
        if servoGroupToDecrease.sequence <= 1:  # La secuencia mínima es 1
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position is already at the minimum sequence")
            
        return self.repository.decreaseSequence(servoGroupToDecrease)
            
    def delete(self, servoGroupToDelete: ServoGroup):
        self.repository.deleteById(servoGroupToDelete.id)
        self.repository.decrementSequenceAfter(servoGroupToDelete)
        return True

        