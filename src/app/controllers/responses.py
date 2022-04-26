"""General responses helper controller"""
from typing import Any

from fastapi import HTTPException, status


class ResponsesController:
    """Helper class to manage responses"""

    @staticmethod
    def already_exists_detail(parameter: str, value: Any) -> str:
        """Helper function to build the the already_exists error detail"""
        return f"User with {parameter}: {value} already exists"

    @staticmethod
    def bad_request_exception(**kwargs) -> HTTPException:
        """Helper function to return an exception when user already exists"""
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, **kwargs)

    @staticmethod
    def unauthorized_detail() -> str:
        """Helper function to build the the forbidden error detail"""
        return "Could not validate credentials"

    @staticmethod
    def unauthorized_exception(**kwargs) -> HTTPException:
        """Helper function to return an exception when user fails authenticate"""
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, **kwargs)

    @staticmethod
    def forbidden_detail() -> str:
        """Helper function to build the the forbidden error detail"""
        return "Incorrect email or password"

    @staticmethod
    def forbidden_exception(**kwargs) -> HTTPException:
        """Helper function to return an exception when user fails authenticate"""
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, **kwargs)

    @staticmethod
    def not_found_detail(parameter: str, value: Any) -> str:
        """Helper function to build the the not_found error detail"""
        return f"User with {parameter}: {value} not found"

    @staticmethod
    def not_found_exception(**kwargs) -> HTTPException:
        """Helper function to return an exception when user does not exist"""
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, **kwargs)
