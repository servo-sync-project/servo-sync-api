from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select
from core.database import getSession  # Asegúrate de que esto es el método para obtener la sesión de tu base de datos.

T = TypeVar('T', bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def findById(self, id: int) -> Optional[T]:
        with getSession() as session:
            return session.get(self.model, id)

    def findAll(self) -> List[T]:
        with getSession() as session:
            statement = select(self.model)
            return session.exec(statement).all()

    def save(self, obj: T) -> T:
        with getSession() as session:
            try:
                session.add(obj)
                session.commit()
                session.refresh(obj)
                return obj
            except IntegrityError as e:
                session.rollback()
                raise ValueError(self.ParseIntegrityError(e))

    def deleteById(self, id: int) -> None:
        with getSession() as session:
            obj = session.get(self.model, id)
            if obj:
                session.delete(obj)
                session.commit()

    def ParseIntegrityError(self, error: IntegrityError) -> str:
        orig_msg = str(error.orig)
        err_msg = orig_msg.split(':')[-1].replace('\n', '').strip()

        parts = err_msg.split('.')
        if len(parts) >= 2:
            table, column = parts[-2], parts[-1]
            return f"Duplicate entry for {column} in {table}. Please choose a different value."
        else:
            return "An error occurred while processing your request."
