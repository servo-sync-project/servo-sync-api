from typing import List, Optional
from sqlmodel import select
from device.domain.model.movement import Movement
from core.database import getSession
from core.base_repository import BaseRepository
from device.domain.model.position import Position
from device.domain.model.robot import Robot
from security.domain.model.user import User  # Asegúrate de importar el BaseRepository

class MovementRepository(BaseRepository[Movement]):
    def __init__(self):
        super().__init__(Movement)  # Pasa el modelo Movement al BaseRepository
        
    def findAllByRobotId(self, robotId: int) -> List[Movement]:
        with getSession() as session:
            statement = select(Movement).where(Movement.robot_id == robotId)
            return session.exec(statement).all()
        
    def findByRobotIdAndName(self, robotId: int, movementName: str) -> Optional[Movement]:
        with getSession() as session:
            statement = select(Movement).where((Movement.robot_id == robotId) & 
                                               (Movement.name == movementName)).order_by(Movement.id)
            return session.exec(statement).first()
        
    def findByIdAndCoordinates(self, robotId: int, coordinates: str) -> Optional[Movement]:
        with getSession() as session:
            statement = select(Movement).where((Movement.robot_id == robotId) &
                                                (Movement.coordinates == coordinates))
            return session.exec(statement).first()

    # Metodos para obtener objetos padres    
    def findMyUserById(self, movementId: int) -> User:
        with getSession() as session:
            statement = (select(User)
                        .join(Robot, Robot.user_id == User.id)
                        .join(Movement, Movement.robot_id == Robot.id)
                        .where(Movement.id == movementId))
            return session.exec(statement).first()
        
    def findMyRobotById(self, movementId: int) -> Robot:
        with getSession() as session:
            statement = (select(Robot)
                        .join(Movement, Movement.robot_id == Robot.id)
                        .where(Movement.id == movementId))
            return session.exec(statement).first()