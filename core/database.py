from sqlmodel import Session, create_engine
from contextlib import contextmanager
from core.config import settings

engine = create_engine(settings.database_url)

@contextmanager
def getSession():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
