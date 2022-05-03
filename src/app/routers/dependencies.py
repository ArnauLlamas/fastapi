from typing import List

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.controllers import auth
from app.controllers.auth import CryptError
from app.controllers.users import UserNotFoundError
from app.libs.crypt.schemas import Token
from app.libs.responses import responses
from app.schemas.users import Role, User
from app.services.users import UsersInterface

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: Token = Depends(oauth2_scheme)) -> User:
    """Gets user based on JWT"""

    credentials_exception = responses.unauthorized_exception(
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    users_interface = UsersInterface()
    try:
        return await auth.read_user_by_token(token, users_interface)
    except (CryptError, UserNotFoundError) as exception:
        raise credentials_exception from exception


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """Check if current user is admin"""

    if current_user.role != Role.ADMIN:
        raise responses.forbidden_exception()
    return current_user


def get_responses(codes: List[int]) -> dict:
    """Helper function to return the expected dictionary of responses in routers"""

    code_responses = {}
    for code in codes:
        code_responses[code] = responses.predefined_responses[code]

    return code_responses
