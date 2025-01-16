from typing import Optional
from sqlmodel import select
from device.domain.model.movement import Movement
from device.domain.model.position import Position
from device.domain.model.robot import Robot
from device.domain.model.servo_group import ServoGroup
from security.domain.model.user import User
from core.database import getSession
from core.base_repository import BaseRepository  # Importa el BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)  # Pasa el modelo User al BaseRepository

    def findByUniqueToken(self, uniqueToken: str) -> Optional[User]:
        with getSession() as session:
            statement = select(User).where(User.unique_token == uniqueToken)
            return session.exec(statement).first()
        
    def findByVerificationUuid(self, verificationUuid: str) -> Optional[User]:
        with getSession() as session:
            statement = select(User).where(User.verification_uuid == verificationUuid)
            return session.exec(statement).first()
        
    def findByUsername(self, username: str) -> Optional[User]:
        with getSession() as session:
            statement = select(User).where(User.username == username)
            return session.exec(statement).first()
        
    def findByEmail(self, email: str) -> Optional[User]:
        with getSession() as session:
            statement = select(User).where(User.email == email)
            return session.exec(statement).first()
    
    # Metodos para obtener padre por hijos   
    def findByRobotId(self, robotId: int) -> Optional[User]:
        with getSession() as session:
            statement = (select(User)
                        .join(Robot, Robot.user_id == User.id)
                        .where(Robot.id == robotId))
            return session.exec(statement).first()
    
    def findByServoGroupId(self, servoGroupId: int) -> Optional[User]:
        with getSession() as session:
            statement = (select(User)
                        .join(Robot, Robot.user_id == User.id)
                        .join(ServoGroup, ServoGroup.robot_id == Robot.id)
                        .where(ServoGroup.id == servoGroupId))
            return session.exec(statement).first()
        
    def findByMovementId(self, movementId: int) -> Optional[User]:
        with getSession() as session:
            statement = (select(User)
                        .join(Robot, Robot.user_id == User.id)
                        .join(Movement, Movement.robot_id == Robot.id)
                        .where(Movement.id == movementId))
            return session.exec(statement).first()
        
    def findByPositionId(self, positionId: int) -> Optional[User]:
        with getSession() as session:
            statement = (select(User)
                        .join(Robot, Robot.user_id == User.id)
                        .join(Movement, Movement.robot_id == Robot.id)
                        .join(Position, Position.movement_id == Movement.id)
                        .where(Position.id == positionId))
            return session.exec(statement).first()
        