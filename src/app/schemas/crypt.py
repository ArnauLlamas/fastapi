"""JWT Models"""
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    """JWT Token Model"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT Token Data Model"""

    id: UUID
