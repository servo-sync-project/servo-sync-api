from typing import List, Optional
from sqlmodel import select
from core.base_repository import BaseRepository
from device.domain.model.movement import Movement
from device.domain.model.robot import Robot
from core.database import getSession
from security.domain.model.user import User

class RobotRepository(BaseRepository[Robot]):
    def __init__(self):
        super().__init__(Robot)  # Pasa el modelo Robot al BaseRepository

    def findByUniqueUid(self, uniqueUid: str) -> Optional[Robot]:
        with getSession() as session:
            statement = select(Robot).where(Robot.unique_uid == uniqueUid)
            return session.exec(statement).first()
        
    def findByBotname(self, botname: str) -> Optional[Robot]:
        with getSession() as session:
            statement = select(Robot).where(Robot.botname == botname)
            return session.exec(statement).first()
        
    def findAllByUserId(self, userId: int) -> list[Robot]:
        with getSession() as session:
            statement = select(Robot).where(Robot.user_id == userId)
            return session.exec(statement).all()
    
    # Metodos para obtener objetos padres    
    def findMyUserById(self, robotId: int) -> User:
        with getSession() as session:
            statement = (select(User)
                        .join(Robot, Robot.user_id == User.id)
                        .where(Robot.id == robotId))
            return session.exec(statement).first()