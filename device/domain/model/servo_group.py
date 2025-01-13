from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from device.domain.model.robot import Robot

class Column(str, Enum):
    RIGHT = "right"
    MIDDLE = "middle"
    LEFT = "left"

class ServoGroup(SQLModel, table=True):
    __tablename__ = "servo_groups"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False)
    num_servos: int = Field(nullable=False)
    column: Column = Field(nullable=False)
    sequence: Optional[int] = Field(nullable=False)
    robot_id: Optional[int] = Field(foreign_key="robots.id", nullable=False)

    # Relaciones
    robot: Optional["Robot"] = Relationship(back_populates="servo_groups")

# servo_angles: str = Field(nullable=False)

