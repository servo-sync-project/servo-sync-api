from typing import Optional
from sqlmodel import select
from core.base_repository import BaseRepository
from device.domain.model.movement import Movement
from device.domain.model.position import Position
from core.database import getSession
from device.domain.model.robot import Robot
from security.domain.model.user import User

class PositionRepository(BaseRepository[Position]):
    def __init__(self):
        super().__init__(Position)  # Pasa el modelo Position al BaseRepository
    
    # def findByMovementIdAndSequence(self, movementId: int, sequence: int) -> Optional[Position]:
    #     with getSession() as session:
    #         statement = select(Position).where((Position.movement_id == movementId)&
    #                                            (Position.sequence == sequence))
    #         return session.exec(statement).first()
        
    def findAllByMovementId(self, movementId: int) -> list[Position]:
        with getSession() as session:
            statement = select(Position).where(Position.movement_id == movementId).order_by(Position.sequence)
            return session.exec(statement).all()
        
    def findMaxSequenceByMovementId(self, movementId: int) -> int:
        with getSession() as session:
            statement = select(Position.sequence).where(Position.movement_id == movementId).order_by(Position.sequence.desc()).limit(1)
            max_sequence = session.exec(statement).first()
            return max_sequence if max_sequence else 0

    def decrementSequenceAfter(self, position: Position):
        with getSession() as session:
            statement = select(Position).where(Position.sequence > position.sequence, Position.movement_id == position.movement_id)
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
    def findMyUserById(self, positionId: int) -> User:
        with getSession() as session:
            statement = (select(User)
                        .join(Robot, Robot.user_id == User.id)
                        .join(Movement, Movement.robot_id == Robot.id)
                        .join(Position, Position.movement_id == Movement.id)
                        .where(Position.id == positionId))
            return session.exec(statement).first()
        
    def findMyRobotById(self, positionId: int) -> Robot:
        with getSession() as session:
            statement = (select(Robot)
                        .join(Movement, Movement.robot_id == Robot.id)
                        .join(Position, Position.movement_id == Movement.id)
                        .where(Position.id == positionId))
            return session.exec(statement).first()