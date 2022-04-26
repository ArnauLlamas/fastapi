from typing import List
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.schemas.crypt import Token, TokenData
from app.schemas.users import LoginUser, Role, SignupUser, User
from app.services.crypt import Crypt, DecodeTokenError
from app.services.users import DatabaseError, UsersService
from app.storage.models import UserModel


class UsersController:
    database: Session

    def __init__(self, database: Session):
        self.database = database

    async def login_user(self, login_attempt: LoginUser) -> Token:
        """Simple method to authenticate and encode an user"""

        user = await self.authenticate_user(login_attempt)
        return self.encode_user_into_jwt_token(user)

    async def authenticate_user(self, login_attempt: LoginUser) -> User:
        """Authenticate user against users service"""

        user_db: UserModel = await UsersService(self.database).get_user_by_email(
            login_attempt.email
        )
        if not user_db:
            raise UserNotCorrectlyAuthenticated

        passwords_match = Crypt().verify_password(login_attempt.password, str(user_db.password))
        if not passwords_match:
            raise UserNotCorrectlyAuthenticated

        return User(id=user_db.id, name=user_db.name, email=user_db.email, role=user_db.role)  # type: ignore

    @staticmethod
    def encode_user_into_jwt_token(user: User) -> Token:
        """Encodes a user public data into a standard JWT token"""
        return Crypt().create_access_token({"sub": str(user.id)})

    async def get_users(self, requesting_user: User) -> List[User]:
        """Retrieves all users in the database"""

        if requesting_user.role != Role.ADMIN:
            raise UserIsNotAuthorized

        users_db = await UsersService(self.database).get_users()
        users = []
        for user in users_db:
            users.append(User(id=user.id, name=user.name, email=user.email, role=user.role))  # type: ignore
        return users

    async def get_user_by_token(self, token: Token) -> User:
        """Returns user given JWT Token"""

        try:
            token_data: TokenData = Crypt().decode_access_token(token)
        except DecodeTokenError as exception:
            raise CryptError from exception

        return await self.get_user_by_id(token_data.id)

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Returns a user model given an user ID"""

        user_db = await UsersService(self.database).get_user_by_id(user_id)
        if not user_db:
            raise UserNotFoundError(user_id)

        return User(id=user_db.id, name=user_db.name, email=user_db.email, role=user_db.role)  # type: ignore

    async def create_user(self, user_to_create: SignupUser) -> User:
        """Creates a new user"""

        if await UsersService(self.database).get_user_by_email(user_to_create.email):
            raise UserAlreadyExistsError(user_to_create.email)

        hashed_password = Crypt().hash_password(user_to_create.password)
        user_db = UserModel(
            id=uuid4(),
            name=user_to_create.name,
            email=user_to_create.email,
            password=hashed_password,
            role=user_to_create.role,
        )
        try:
            await UsersService(self.database).add_user(user_db)
        except DatabaseError as exception:
            raise SomethingWrongHappened from exception

        return User(id=user_db.id, name=user_db.name, email=user_db.email, role=user_db.role)  # type: ignore

    async def delete_user(self, user_to_delete: User) -> None:
        """Deletes user"""
        user_model = await UsersService(self.database).get_user_by_id(user_to_delete.id)
        await UsersService(self.database).remove_user(user_model)


class SomethingWrongHappened(Exception):
    """General uncontrolled exception"""


class CryptError(Exception):
    """Error from crypt service"""


class UserIsNotAuthorized(Exception):
    """User tries to access to a restricted section"""


class UserNotCorrectlyAuthenticated(Exception):
    """User fails to authenticate exception"""


class UserNotFoundError(Exception):
    """User does not exist exception"""

    user_id: UUID

    def __init__(self, user_id, *args: object) -> None:
        super().__init__(*args)

        self.user_id = user_id


class UserAlreadyExistsError(Exception):
    """User already exists exception"""

    email: EmailStr

    def __init__(self, email, *args: object) -> None:
        super().__init__(*args)

        self.email = email
