from typing import List
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.storage.models import UserModel


def exception_handling(function):
    """try except handling"""

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as exception:
            raise DatabaseError from exception

    return wrapper


class UsersService:
    database: Session

    def __init__(self, database: Session) -> None:
        self.database = database

    @exception_handling
    async def get_user_by_id(self, user_id: UUID) -> UserModel:
        return self.database.query(UserModel).filter(UserModel.id == user_id).first()

    @exception_handling
    async def get_user_by_email(self, email: EmailStr) -> UserModel:
        return self.database.query(UserModel).filter(UserModel.email == email).first()

    @exception_handling
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        return self.database.query(UserModel).offset(skip).limit(limit).all()

    @exception_handling
    async def add_user(self, user: UserModel) -> None:
        self.database.add(user)
        self.database.commit()
        self.database.refresh(user)

    @exception_handling
    async def remove_user(self, user: UserModel):
        self.database.delete(user)
        self.database.commit()


class DatabaseError(Exception):
    """Fails to interact with the Database"""
