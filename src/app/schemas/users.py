"""User Models"""
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Role

    class Config:
        orm_mode = True


class User(UserBase):
    """Standard model to serve"""

    id: UUID

    class Config:
        schema_extra = {
            "example": {
                "id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
                "name": "Foo",
                "email": "foo@example.com",
                "role": "admin",
            }
        }


class CreateUserData(UserBase):
    """Model expected when a new user signups"""

    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "email": "foo@example.com",
                "role": "admin",
                "password": "a-super-secret-password",
            }
        }


class LoginUserData(BaseModel):
    """Model expected when a user logins"""

    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "foo@example.com",
                "password": "a-super-secret-password",
            }
        }


class UpdateUserData(BaseModel):
    """Model expected when modifying a user"""

    name: str | None
    email: EmailStr | None
    password: str | None
    role: Role | None

    class Config:
        schema_extra = {
            "example": {
                "email": "bar@example.com",
            }
        }
