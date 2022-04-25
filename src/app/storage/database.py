"""Database instantiation"""
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base

from app.settings import Settings


settings = Settings()

engine = sqlalchemy.create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
