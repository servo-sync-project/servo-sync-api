from fastapi import HTTPException, status
from security.domain.persistence.user_repository import UserRepository
from security.service.auth_service import pwd_context

class UserService:
    def __init__(self, userRepository: UserRepository):
        self.repository = userRepository
    
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
    
    def updateById(self, userId: int, newUsername:str):
        userToUpdate = self.getById(userId)

        if newUsername != userToUpdate.username and self.repository.findByUsername(newUsername):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        
        userToUpdate.username = newUsername
        return self.repository.save(userToUpdate)

    def deleteById(self, userId: int):
        userToDelete = self.getById(userId)
        self.repository.deleteById(userToDelete.id)
        return True
