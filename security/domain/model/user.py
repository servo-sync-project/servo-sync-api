from sqlmodel import Relationship, SQLModel, Field
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from device.domain.model.robot import Robot

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(primary_key=True)
    image_url: str = Field(nullable=False)
    email: str = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    username: str = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    full_name: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    enabled: Optional[bool] = Field(default=False)
    role: Optional[Role] = Field(default=Role.USER)

    robots: List["Robot"] = Relationship(back_populates="user")