import json
from fastapi import HTTPException, status
from device.domain.model.movement import Movement
from device.domain.model.servo_group import Column, ServoGroup
from device.domain.persistence.movement_repository import MovementRepository
from device.domain.persistence.servo_group_repository import ServoGroupRepository

class ServoGroupService:
    def __init__(self, servoGroupRepository: ServoGroupRepository):
        self.repository = servoGroupRepository
    
    def create(self, servoGroup: ServoGroup):
        # if self.repository.findByIdAndCoordinates(servoGroup.robot_id, servoGroup.coord_x, servoGroup.coord_y):
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot at these coordinates")
        
        # if self.repository.findByRobotIdAndName(servoGroup.robot_id, servoGroup.name):
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot")
        
        # if len(self.repository.findAllByRobotId(servoGroup.robot_id)) >= 10:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The robot reached its limit with 10 movements")
        
        return self.repository.save(servoGroup)
    
    def validateAccess(self, userId: int, servoGroupId: int):
        user = self.repository.findMyUserById(servoGroupId)
        if userId != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return True
    
    def getById(self, servoGroupId: int):
        servoGroup = self.repository.findById(servoGroupId)
        if not servoGroup:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servo group not found")
        return servoGroup
    
    def getAllByRobotId(self, servoGroupId: int):
        servoGroup = self.repository.findAllByRobotId(servoGroupId)
        if not servoGroup:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No servo groups found")
        return servoGroup
    
    def updateById(self, servoGroupId: int, newName: str, newColumn: Column, newSequence: int, newServoAngles: str):
        servoGroupToUpdate = self.getById(servoGroupId)

        # if self.repository.findByIdAndCoordinates(movementToUpdate.robot_id, newCoordX, newCoordY):
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot at these coordinates")
        
        # if newName != movementToUpdate.name and self.repository.findByRobotIdAndName(movementToUpdate.robot_id, newName):
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot")
        
        servoGroupToUpdate.name = newName
        servoGroupToUpdate.column = newColumn
        servoGroupToUpdate.sequence = newSequence
        servoGroupToUpdate.servo_angles = newServoAngles
        return self.repository.save(servoGroupToUpdate)
    
    def deleteById(self, servoGroupId: int):
        servoGroupToDelete = self.getById(servoGroupId)
        self.repository.deleteById(servoGroupToDelete.id)
        return True
    
    