"""Dependencies"""
from typing import List
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import app.schemas.responses

from app.controllers.responses import ResponsesController
from app.controllers.users import CryptError, UserNotFoundError, UsersController
from app.storage.database import SessionLocal
from app.schemas.users import Role, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    """Get database session"""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(get_db),
) -> User:
    """Gets user based on JWT"""

    credentials_exception = ResponsesController().unauthorized_exception(
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return await UsersController(database).get_user_by_token(token)
    except (CryptError, UserNotFoundError) as exception:
        raise credentials_exception from exception


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """Check if current user is admin"""

    if current_user.role != Role.ADMIN:
        raise ResponsesController().forbidden_exception()
    return current_user


def get_responses(codes: List[int]) -> dict:
    """Helper function to return the expected dictionary of responses in routers"""

    code_responses = {}
    for code in codes:
        code_responses[code] = app.schemas.responses.responses[code]

    return code_responses
