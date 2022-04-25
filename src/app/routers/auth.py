"""Authentication router"""
from fastapi import APIRouter, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.schemas.crypt import Token
from app.schemas.users import LoginUser, SignupUser
from app.controllers.users import UsersController
from app.controllers.users import UserAlreadyExistsError, UserNotCorrectlyAuthenticated
from app.controllers.responses import ResponsesController
from app.dependencies import get_db, get_responses

router = APIRouter()


@router.post("/login", response_model=Token, responses=get_responses([403]))
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database: Session = Depends(get_db),
) -> Token:
    """Logins user with email + password and returns a JWT with user's ID"""

    try:
        login_attempt = LoginUser(email=form_data.username, password=form_data.password)
        return await UsersController(database).login_user(login_attempt)

    except UserNotCorrectlyAuthenticated as exception:
        raise ResponsesController().forbidden_exception() from exception

    except ValidationError as exception:
        raise ResponsesController().bad_request_exception(detail="Not a valid email") from exception


@router.post("/signup", status_code=status.HTTP_201_CREATED, responses=get_responses([400]))
async def signup_user(new_user: SignupUser, database: Session = Depends(get_db)) -> None:
    """Creates a new user into the system"""

    try:
        await UsersController(database).create_user(new_user)

    except UserAlreadyExistsError as exception:
        raise ResponsesController().bad_request_exception(
            detail=ResponsesController().already_exists_detail("email", exception.email)
        ) from exception

    return Response(status_code=status.HTTP_201_CREATED)
