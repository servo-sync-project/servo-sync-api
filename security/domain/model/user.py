from datetime import datetime, timezone
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
    verification_uuid: Optional[str] = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    unique_token: Optional[str] = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    email: str = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    username: str = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    hashed_password: str = Field(nullable=False)
    email_verified_at: Optional[datetime] = Field(nullable=True)
    uuid_expires_at: Optional[datetime] = Field(nullable=False)
    token_expires_at: Optional[datetime] = Field(nullable=False)
    created_at: Optional[datetime] = Field(nullable=False, default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at: Optional[datetime] = Field(nullable=False, default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None), sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc).replace(tzinfo=None)})
    role: Optional[Role] = Field(nullable=False, default=Role.USER)

    robots: List["Robot"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    # ok, ahora tengo unique_uid  y email_verified_at para la habilitar la cuenta, ademas de verification_code para cambiar la contraseña, que otros nombres podria ponerles para que sean mas coherentes a su funcion?
    # unique_password_reset_uid: Optional[str] = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    # unique_email_verification_uid: Optional[str] = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})