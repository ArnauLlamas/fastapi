"""Database instantiation"""
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import settings

engine = sqlalchemy.create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
