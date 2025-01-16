from typing import Optional
from sqlmodel import select
from core.base_repository import BaseRepository
from device.domain.model.movement import Movement
from device.domain.model.position import Position
from device.domain.model.robot import Robot
from core.database import getSession
from device.domain.model.servo_group import ServoGroup
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
            statement = select(Robot).where(Robot.user_id == userId).order_by(Robot.id)
            return session.exec(statement).all()
    
    # Metodos para obtener padre por hijos       
    def findByServoGroupId(self, servoGroupId: int) -> Optional[Robot]:
        with getSession() as session:
            statement = (select(Robot)
                        .join(ServoGroup, ServoGroup.robot_id == Robot.id)
                        .where(ServoGroup.id == servoGroupId))
            return session.exec(statement).first()
             
    def findByMovementId(self, movementId: int) -> Optional[Robot]:
        with getSession() as session:
            statement = (select(Robot)
                        .join(Movement, Movement.robot_id == Robot.id)
                        .where(Movement.id == movementId))
            return session.exec(statement).first()
        
    def findByPositionId(self, positionId: int) -> Optional[Robot]:
        with getSession() as session:
            statement = (select(Robot)
                        .join(Movement, Movement.robot_id == Robot.id)
                        .join(Position, Position.movement_id == Movement.id)
                        .where(Position.id == positionId))
            return session.exec(statement).first()
    
