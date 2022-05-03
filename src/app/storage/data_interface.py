from typing import List, Protocol
from uuid import UUID

from pydantic import BaseModel, EmailStr

from .models import Base

DataObject = type(BaseModel)
DBObject = type(Base)


class DataInterface(Protocol):
    def read_by_id(self, id: int | UUID) -> DBObject:
        ...

    def read_all(self) -> List[DBObject]:
        ...

    def create(self, data: DBObject) -> DBObject:
        ...

    def update(self, id: int | UUID, data: DataObject) -> DBObject:
        ...

    def delete(self, id: int | UUID) -> None:
        ...


class DataUserInterface(DataInterface, Protocol):
    def read_by_email(self, email: EmailStr) -> DBObject:
        ...
