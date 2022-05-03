"""General responses helper controller"""
from typing import Any

from fastapi import HTTPException, status

from .schemas import BadRequest, Forbidden, NotFound, Unauthorized


def already_exists_detail(parameter: str, value: Any) -> str:
    """Helper function to build the the already_exists error detail"""
    return f"User with {parameter}: {value} already exists"


def bad_request_exception(**kwargs) -> HTTPException:
    """Helper function to return an exception when user already exists"""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, **kwargs)


def unauthorized_detail() -> str:
    """Helper function to build the the forbidden error detail"""
    return "Could not validate credentials"


def unauthorized_exception(**kwargs) -> HTTPException:
    """Helper function to return an exception when user fails authenticate"""
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, **kwargs)


def forbidden_detail() -> str:
    """Helper function to build the the forbidden error detail"""
    return "Incorrect email or password"


def forbidden_exception(**kwargs) -> HTTPException:
    """Helper function to return an exception when user fails authenticate"""
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, **kwargs)


def not_found_detail(parameter: str, value: Any) -> str:
    """Helper function to build the the not_found error detail"""
    return f"User with {parameter}: {value} not found"


def not_found_exception(**kwargs) -> HTTPException:
    """Helper function to return an exception when user does not exist"""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, **kwargs)


predefined_responses = {
    404: {
        "model": NotFound,
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": not_found_detail("id", "765bdd21-71bc-4869-9b31-bd37ef84284c"),
                }
            }
        },
    },
    403: {
        "model": Forbidden,
        "description": "Authentication failed",
        "content": {
            "application/json": {
                "example": {
                    "detail": forbidden_detail(),
                }
            }
        },
    },
    401: {
        "model": Unauthorized,
        "description": "Invalid JWT",
        "content": {"application/json": {"example": {"detail": unauthorized_detail()}}},
    },
    400: {
        "model": BadRequest,
        "description": "User already exists",
        "content": {
            "application/json": {
                "example": {
                    "detail": already_exists_detail("email", "test@example.com"),
                }
            }
        },
    },
}
