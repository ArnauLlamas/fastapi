"""Users service"""
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
    """Users Service class"""

    database: Session

    def __init__(self, database: Session) -> None:
        self.database = database

    @exception_handling
    async def get_user_by_id(self, user_id: UUID) -> UserModel:
        """Retrieve user by ID from Database"""
        return self.database.query(UserModel).filter(UserModel.id == user_id).first()

    @exception_handling
    async def get_user_by_email(self, email: EmailStr) -> UserModel:
        """Retrieve user by email from Database"""
        return self.database.query(UserModel).filter(UserModel.email == email).first()

    @exception_handling
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Retrieves all users from the Database (max 100 by default)"""
        return self.database.query(UserModel).offset(skip).limit(limit).all()

    @exception_handling
    async def add_user(self, user: UserModel) -> None:
        """Inserts an user into the Database"""

        self.database.add(user)
        self.database.commit()
        self.database.refresh(user)

    @exception_handling
    async def remove_user(self, user: UserModel):
        """Removes the user from the Database"""
        self.database.delete(user)
        self.database.commit()


class DatabaseError(Exception):
    """Fails to interact with the Database"""
