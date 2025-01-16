from typing import List, Optional
from sqlmodel import select
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
            statement = select(ServoGroup).where(ServoGroup.robot_id == robotId).order_by(ServoGroup.column,
                                                                                          ServoGroup.sequence)
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

    def decrementSequenceAfter(self, servoGroup: ServoGroup):
        with getSession() as session:
            statement = select(ServoGroup).where((ServoGroup.robot_id == servoGroup.robot_id) & 
                                                 (ServoGroup.column == servoGroup.column) &
                                                 (ServoGroup.sequence > servoGroup.sequence))
            servoGroups = session.exec(statement).all()
            for existingServoGroup in servoGroups:
                existingServoGroup.sequence -= 1
                session.add(existingServoGroup)
            session.commit()

    def increaseSequence(self, servoGroup: ServoGroup) -> ServoGroup:
        with getSession() as session:
            statement = select(ServoGroup).where((ServoGroup.robot_id == servoGroup.robot_id) & 
                                                 (ServoGroup.column == servoGroup.column) &
                                                 (ServoGroup.sequence == servoGroup.sequence + 1))
            nextPosition = session.exec(statement).first()
            if nextPosition:
                nextPosition.sequence, servoGroup.sequence = servoGroup.sequence, nextPosition.sequence
                session.add(servoGroup)
                session.add(nextPosition)
                session.commit()
                session.refresh(servoGroup)
                session.refresh(nextPosition)
            return servoGroup

    def decreaseSequence(self, servoGroup: ServoGroup) -> ServoGroup:
        with getSession() as session:
            statement = select(ServoGroup).where((ServoGroup.robot_id == servoGroup.robot_id) & 
                                                 (ServoGroup.column == servoGroup.column) &
                                                 (ServoGroup.sequence == servoGroup.sequence - 1))
            prevPosition = session.exec(statement).first()
            if prevPosition:
                prevPosition.sequence, servoGroup.sequence = servoGroup.sequence, prevPosition.sequence
                session.add(servoGroup)
                session.add(prevPosition)
                session.commit()
                session.refresh(servoGroup)
                session.refresh(prevPosition)
            return servoGroup