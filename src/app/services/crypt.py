from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas.crypt import Token, TokenData
from app.settings import settings


class Crypt:
    pwd_context: CryptContext

    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hashes a plain text password"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_text_password: str, hashed_password: str) -> bool:
        """Verifies if a plain text password matches a hashed one"""
        return self.pwd_context.verify(plain_text_password, hashed_password)

    @staticmethod
    def create_access_token(
        data: dict, min_expire: int = settings.access_token_expire_minutes
    ) -> Token:
        """Encodes and returns a JWT"""

        to_encode = data.copy()
        now = datetime.utcnow()
        expire = now + timedelta(minutes=min_expire)
        to_encode.update({"exp": expire, "iat": now})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

        return Token(access_token=encoded_jwt, token_type="bearer")

    @staticmethod
    def decode_access_token(token: Token) -> TokenData:
        """Decodes a JWT and returns the stored UUID"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

            user_id: UUID = payload.get("sub")
            if not user_id:
                raise DecodeTokenError

            return TokenData(id=user_id)

        except JWTError:
            raise DecodeTokenError from JWTError


class DecodeTokenError(Exception):
    """Exception when cannot decode a JWT or it is expired"""
