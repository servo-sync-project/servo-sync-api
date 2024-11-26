from typing import List, Optional
from sqlmodel import select
from device.domain.model.movement import Movement
from core.database import getSession
from core.base_repository import BaseRepository
from device.domain.model.robot import Robot
from device.domain.model.servo_group import Column, ServoGroup
from security.domain.model.user import User  # Asegúrate de importar el BaseRepository

class ServoGroupRepository(BaseRepository[ServoGroup]):
    def __init__(self):
        super().__init__(ServoGroup)  # Pasa el modelo Movement al BaseRepository
        
    def findAllByRobotId(self, robotId: int) -> List[ServoGroup]:
        with getSession() as session:
            statement = select(ServoGroup).where(ServoGroup.robot_id == robotId)
            return session.exec(statement).all()
        
    def findByRobotIdAndName(self, robotId: int, servoGroupName: str) -> Optional[ServoGroup]:
        with getSession() as session:
            statement = select(ServoGroup).where((ServoGroup.robot_id == robotId) & 
                                                 (ServoGroup.name == servoGroupName))
            return session.exec(statement).first()
        
    # para ordenar secuencia
    def findMaxSequenceByRobotIdAndColumn(self, robotId: int, column: Column) -> int:
        with getSession() as session:
            statement = select(ServoGroup.sequence).where((ServoGroup.robot_id == robotId) &
                                                          (ServoGroup.column == column)).order_by(ServoGroup.sequence.desc()).limit(1)
            max_sequence = session.exec(statement).first()
            return max_sequence if max_sequence else 0

    def decrementSequenceAfter(self, position: ServoGroup):
        with getSession() as session:
            statement = select(ServoGroup).where(ServoGroup.sequence > position.sequence, ServoGroup.robot_id == position.robot_id)
            positions = session.exec(statement).all()
            for position in positions:
                position.sequence -= 1
                session.add(position)
            session.commit()

    def increaseSequence(self, position: Position) -> Position:
        with getSession() as session:
            nextPosition = session.exec(select(Position).where(Position.movement_id == position.movement_id, Position.sequence == position.sequence + 1)).first()
            if nextPosition:
                nextPosition.sequence, position.sequence = position.sequence, nextPosition.sequence
                session.add(position)
                session.add(nextPosition)
                session.commit()
                session.refresh(position)
                session.refresh(nextPosition)
            return position

    def decreaseSequence(self, position: Position) -> Position:
        with getSession() as session:
            prevPosition = session.exec(select(Position).where(Position.movement_id == position.movement_id, Position.sequence == position.sequence - 1)).first()
            if prevPosition:
                prevPosition.sequence, position.sequence = position.sequence, prevPosition.sequence
                session.add(position)
                session.add(prevPosition)
                session.commit()
                session.refresh(position)
                session.refresh(prevPosition)
            return position
        
    # Metodos para obtener objetos padres    
    def findMyUserById(self, servoGroupId: int) -> User:
        with getSession() as session:
            statement = (select(User)
                        .join(Robot, Robot.user_id == User.id)
                        .join(ServoGroup, ServoGroup.robot_id == Robot.id)
                        .where(ServoGroup.id == servoGroupId))
            return session.exec(statement).first()
        
    def findMyRobotById(self, servoGroupId: int) -> Robot:
        with getSession() as session:
            statement = (select(Robot)
                        .join(ServoGroup, ServoGroup.robot_id == Robot.id)
                        .where(ServoGroup.id == servoGroupId))
            return session.exec(statement).first()