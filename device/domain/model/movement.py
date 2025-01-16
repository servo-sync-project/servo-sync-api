from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Relationship

if TYPE_CHECKING:
    from device.domain.model.robot import Robot
    from device.domain.model.position import Position

class Movement(SQLModel, table=True):
    __tablename__ = "movements"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False)
    coordinates: Optional[str] = Field(nullable=True)
    robot_id: Optional[int] = Field(foreign_key="robots.id", nullable=False)

    # Relaciones
    robot: Optional["Robot"] = Relationship(back_populates="movements")
    positions: List["Position"] = Relationship(back_populates="movement", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    # coord_x: Optional[int] = Field(nullable=False, default=0)
    # coord_y: Optional[int] = Field(nullable=False, default=0)