from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from .schemas import Token, TokenData


def __get_pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes a plain text password"""
    return __get_pwd_context().hash(password)


def verify_password(plain_text_password: str, hashed_password: str) -> bool:
    """Verifies if a plain text password matches a hashed one"""
    return __get_pwd_context().verify(plain_text_password, hashed_password)


def create_access_token(data: dict, min_expire: int, secret_key: str, algorithm: str) -> Token:
    """Encodes and returns a JWT"""

    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=min_expire)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return Token(access_token=encoded_jwt, token_type="bearer")


def decode_access_token(token: Token, secret_key, algorithms: list[str]) -> TokenData:
    """Decodes a JWT and returns the stored UUID"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)

        user_id: UUID = payload.get("sub")
        if not user_id:
            raise DecodeTokenError

        return TokenData(id=user_id)

    except JWTError:
        raise DecodeTokenError from JWTError


class DecodeTokenError(Exception):
    """Exception when cannot decode a JWT or it is expired"""
