from typing import List

import fastapi
from fastapi import APIRouter, Depends, status

from app.controllers import users
from app.schemas.users import User
from app.services.users import UsersInterface

from .dependencies import get_current_admin_user, get_current_user

router = APIRouter()


@router.get("/me", response_model=User)
async def retrieve_users_info(current_user: User = Depends(get_current_user)):
    """Retrieves current user info"""
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user: User = Depends(get_current_user)):
    """Deletes logged user"""
    users_interface = UsersInterface()
    await users.delete(current_user, users_interface)
    return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("", response_model=List[User])
async def retrieve_users(current_user: User = Depends(get_current_admin_user)):
    """Retrieves all users info"""
    users_interface = UsersInterface()
    return await users.read_all(current_user, users_interface)
