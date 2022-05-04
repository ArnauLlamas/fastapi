from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, ValidationError

from app.controllers import auth, users
from app.controllers.auth import UserNotCorrectlyAuthenticatedError
from app.controllers.users import UserAlreadyExistsError
from app.libs.crypt.schemas import Token
from app.libs.responses import responses
from app.schemas.users import CreateUserData, LoginUserData
from app.services.db_interface import DBInterface
from app.storage.models import DBUser

from .dependencies import get_responses

router = APIRouter()


@router.post("/login", response_model=Token, responses=get_responses([403]))
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """Logins user with email + password and returns a JWT with user's ID"""

    users_interface = DBInterface(DBUser)
    try:
        login_attempt = LoginUserData(
            email=EmailStr(form_data.username), password=form_data.password
        )
        return await auth.login_user(login_attempt, users_interface)

    except UserNotCorrectlyAuthenticatedError as exception:
        raise responses.forbidden_exception() from exception

    except ValidationError as exception:
        raise responses.bad_request_exception(detail="Not a valid email") from exception


@router.post("/signup", status_code=status.HTTP_201_CREATED, responses=get_responses([400]))
async def signup_user(new_user: CreateUserData):
    """Creates a new user into the system"""

    users_interface = DBInterface(DBUser)
    try:
        await users.create(new_user, users_interface)

    except UserAlreadyExistsError as exception:
        raise responses.bad_request_exception(
            detail=responses.already_exists_detail("email", exception.email)
        ) from exception

    return Response(status_code=status.HTTP_201_CREATED)
