from typing import Optional
from sqlmodel import select
from device.domain.model.robot import Robot
from security.domain.model.user import User
from core.database import getSession
from core.base_repository import BaseRepository  # Importa el BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)  # Pasa el modelo User al BaseRepository

    def findByUsername(self, username: str) -> Optional[User]:
        with getSession() as session:
            statement = select(User).where(User.username == username)
            return session.exec(statement).first()
        
    def findByEmail(self, email: str) -> Optional[User]:
        with getSession() as session:
            statement = select(User).where(User.email == email)
            return session.exec(statement).first()
