from fastapi import HTTPException, status
from security.domain.model.user import User
from security.domain.persistence.user_repository import UserRepository
from security.service.auth_service import pwd_context

class UserService:
    def __init__(self, userRepository: UserRepository):
        self.repository = userRepository
    
    def getByVerificationUUID(self, verificationUuid: str):
        user = self.repository.findByVerificationUuid(verificationUuid)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    def getByUniqueToken(self, uniqueToken: str):
        user = self.repository.findByUniqueToken(uniqueToken)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    def getByEmail(self, email: str):
        user = self.repository.findByEmail(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    def getByUsername(self, username: str):
        user = self.repository.findByUsername(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    def getById(self, userId: int):
        user = self.repository.findById(userId)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    def getAll(self):
        users = self.repository.findAll()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return users
    
    def update(self, userToUpdate: User, newUsername:str):
        if newUsername != userToUpdate.username and self.repository.findByUsername(newUsername):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        
        userToUpdate.username = newUsername
        return self.repository.save(userToUpdate)

    def delete(self, userToDelete: User):
        self.repository.deleteById(userToDelete.id)
        return True
    
    def validateRobotAccess(self, userId: int, robotId: int):
        user = self.repository.findByRobotId(robotId)
        if not user or userId != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return user
        
    def validateServoGroupAccess(self, userId: int, servoGroupId: int):
        user = self.repository.findByServoGroupId(servoGroupId)
        if not user or userId != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return user
        
    def validateMovementAccess(self, userId: int, movementId: int):
        user = self.repository.findByMovementId(movementId)
        if not user or userId != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return user
        
    def validatePositionAccess(self, userId: int, positionId: int):
        user = self.repository.findByPositionId(positionId)
        if not user or userId != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to resource")
        return user
