from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.storage.models import Base

DBSession = sessionmaker(autocommit=False, autoflush=False)


def init_db(database_url) -> None:
    engine: Engine = create_engine(database_url)
    Base.metadata.bind = engine
    DBSession.bind = engine  # type: ignore


def get_session() -> Session:
    return DBSession()
