"""General responses helper models"""
from pydantic import BaseModel

from app.controllers.responses import ResponsesController


class BaseResponse(BaseModel):
    """Base response"""

    detail: str


class BadRequest(BaseResponse):
    """Bad request response"""


class Unauthorized(BaseResponse):
    """Unauthorized response"""


class Forbidden(BaseResponse):
    """Forbidden response"""


class NotFound(BaseResponse):
    """Not found response"""


responses = {
    404: {
        "model": NotFound,
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": ResponsesController().not_found_detail(
                        "id", "765bdd21-71bc-4869-9b31-bd37ef84284c"
                    ),
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
                    "detail": ResponsesController().forbidden_detail(),
                }
            }
        },
    },
    401: {
        "model": Unauthorized,
        "description": "Invalid JWT",
        "content": {
            "application/json": {"example": {"detail": ResponsesController().unauthorized_detail()}}
        },
    },
    400: {
        "model": BadRequest,
        "description": "User already exists",
        "content": {
            "application/json": {
                "example": {
                    "detail": ResponsesController().already_exists_detail(
                        "email", "test@example.com"
                    ),
                }
            }
        },
    },
}
