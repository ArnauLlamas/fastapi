"""Users database schema"""
from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.users import Role

from .database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(Role, nullable=False, values_callable=lambda obj: [e.value for e in obj]))
