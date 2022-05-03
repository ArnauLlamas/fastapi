"""General responses helper models"""
from pydantic import BaseModel


class BaseResponse(BaseModel):
    detail: str


class BadRequest(BaseResponse):
    """Bad request response"""


class Unauthorized(BaseResponse):
    """Unauthorized response"""


class Forbidden(BaseResponse):
    """Forbidden response"""


class NotFound(BaseResponse):
    """Not found response"""
