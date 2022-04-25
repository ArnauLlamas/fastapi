"""User Models"""
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    """Model for a user's role"""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserBase(BaseModel):
    """Class used as model for other class models. Do not use implement it directly"""

    name: str
    email: EmailStr
    role: Role


class User(UserBase):
    """Standard model to serve"""

    id: UUID


class SignupUser(UserBase):
    """Model expected when a new user signups"""

    password: str


class LoginUser(BaseModel):
    """Model expected when a user logins"""

    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    """Model expected when modifying a user"""

    name: str | None
    email: EmailStr | None
    password: str | None
    role: Role | None
