from pydantic import EmailStr

from app.services.db_interface import DBInterface, exception_handling
from app.storage.database import get_session
from app.storage.models import DBUser


class UsersInterface(DBInterface):
    def __init__(self) -> None:
        super().__init__(DBUser)

    @exception_handling
    async def read_by_email(self, email: EmailStr) -> DBUser:
        session = get_session()
        result = session.query(DBUser).filter(DBUser.email == email).first()
        return result
