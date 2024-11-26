from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, List, Optional

from device.domain.model.servo_group import ServoGroup

if TYPE_CHECKING:
    from device.domain.model.movement import Movement
    from security.domain.model.user import User

class Robot(SQLModel, table=True):
    __tablename__ = "robots"

    id: Optional[int] = Field(primary_key=True)
    unique_uid: Optional[str] = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    botname: str = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    image_url: str = Field(nullable=False)
    description: str = Field(nullable=False)
    initial_position: str = Field(nullable=False)
    is_connected_broker: Optional[bool] = Field(nullable=False, default=False)
    user_id: Optional[int] = Field(foreign_key="users.id", nullable=False)
    
    
    # Relaciones
    user: Optional["User"] = Relationship(back_populates="robots")
    servo_groups: List["ServoGroup"] = Relationship(back_populates="robot")
    movements: List["Movement"] = Relationship(back_populates="robot")