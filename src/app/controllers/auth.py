from app.controllers import users
from app.libs.crypt import crypt
from app.libs.crypt.crypt import DecodeTokenError
from app.libs.crypt.schemas import Token, TokenData
from app.schemas.users import LoginUserData, User
from app.services.users import UsersInterface
from app.settings import settings
from app.storage.models import DBUser


async def login_user(login_attempt: LoginUserData, users_interface: UsersInterface) -> Token:
    """Simple method to authenticate and encode an user"""

    user = await authenticate_user(login_attempt, users_interface)
    return encode_user_into_jwt_token(user)


async def authenticate_user(login_attempt: LoginUserData, users_interface: UsersInterface) -> User:
    """Authenticate user against users service"""

    user_db: DBUser = await users_interface.read_by_email(login_attempt.email)
    if not user_db:
        raise UserNotCorrectlyAuthenticatedError

    passwords_match = crypt.verify_password(login_attempt.password, str(user_db.password))
    if not passwords_match:
        raise UserNotCorrectlyAuthenticatedError

    return User.from_orm(user_db)


def encode_user_into_jwt_token(user: User) -> Token:
    """Encodes a user public data into a standard JWT token"""
    return crypt.create_access_token(
        {"sub": str(user.id)},
        settings.access_token_expire_minutes,
        settings.secret_key,
        settings.algorithm,
    )


async def read_user_by_token(token: Token, users_interface: UsersInterface) -> User:
    """Returns user given JWT Token"""

    try:
        token_data: TokenData = crypt.decode_access_token(
            token, settings.secret_key, [settings.algorithm]
        )
    except DecodeTokenError as exception:
        raise CryptError from exception

    return await users.read_by_id(token_data.id, users_interface)


class CryptError(Exception):
    """Error from crypt service"""


class UserNotCorrectlyAuthenticatedError(Exception):
    """User fails to authenticate exception"""
