from typing import List
from uuid import UUID, uuid4

from pydantic import EmailStr

from app.libs.crypt import crypt
from app.schemas.users import CreateUserData, Role, User
from app.services.db_interface import DatabaseError, DBInterface
from app.services.users import UsersInterface
from app.storage.models import DBUser


async def read_all(requesting_user: User, users_interface: UsersInterface) -> List[User]:
    """Retrieves all users in the database"""

    if requesting_user.role != Role.ADMIN:
        raise UserIsNotAuthorizedError

    users_db = await users_interface.read_all()
    users = []
    for user in users_db:
        users.append(User.from_orm(user))  # type: ignore
    return users


async def read_by_id(user_id: UUID, users_interface: DBInterface) -> User:
    """Returns a user model given an user ID"""

    user_db = await users_interface.read_by_id(user_id)
    if not user_db:
        raise UserNotFoundError(user_id)

    return User.from_orm(user_db)


async def create(user_to_create: CreateUserData, users_interface: UsersInterface) -> User:
    """Creates a new user"""

    if await users_interface.read_by_email(user_to_create.email):
        raise UserAlreadyExistsError(user_to_create.email)

    hashed_password = crypt.hash_password(user_to_create.password)
    user_db = DBUser(
        id=uuid4(),
        name=user_to_create.name,
        email=user_to_create.email,
        password=hashed_password,
        role=user_to_create.role,
    )
    try:
        await users_interface.create(user_db)
    except DatabaseError as exception:
        raise UnexpectedError from exception

    return User(id=user_db.id, name=user_db.name, email=user_db.email, role=user_db.role)  # type: ignore


async def delete(user_to_delete: User, users_interface: DBInterface) -> None:
    """Deletes user"""
    await users_interface.read_by_id(user_to_delete.id)
    await users_interface.delete(user_to_delete.id)


class UnexpectedError(Exception):
    """General uncontrolled exception"""


class UserIsNotAuthorizedError(Exception):
    """User tries to access to a restricted section"""


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
