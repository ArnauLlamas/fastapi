"""User Router"""
from typing import List
from fastapi import APIRouter, status, Depends
import fastapi
from sqlalchemy.orm import Session

from app.controllers.users import UsersController
from app.schemas.users import User
from app.dependencies import get_current_admin_user, get_current_user, get_db

router = APIRouter()


@router.get("/me", response_model=User)
def retrieve_users_info(current_user: User = Depends(get_current_user)):
    """Retrieves current user info"""
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: User = Depends(get_current_user), database: Session = Depends(get_db)
):
    """Deletes logged user"""
    await UsersController(database).delete_user(current_user)
    return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("", response_model=List[User])
async def retrieve_users(
    current_user: User = Depends(get_current_admin_user),
    database: Session = Depends(get_db),
):
    """Retrieves all users info"""
    return await UsersController(database).get_users(current_user)
