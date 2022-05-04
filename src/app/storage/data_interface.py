from typing import Any, List, Protocol
from uuid import UUID

from pydantic import BaseModel

from .models import Base

DataObject = type(BaseModel)
DBObject = type(Base)


class DataInterface(Protocol):
    """
    Protocol on how to instantiate any Data Interface, such a DB Interface or others.
    """

    async def read_by_id(self, id: int | UUID) -> DBObject:
        ...

    async def read_by_field(self, field: str, field_valu: Any) -> DBObject:
        ...

    async def read_all(self) -> List[DBObject]:
        ...

    async def create(self, data: DBObject) -> DBObject:
        ...

    async def update(self, id: int | UUID, data: DataObject) -> DBObject:
        ...

    async def delete(self, id: int | UUID) -> None:
        ...
