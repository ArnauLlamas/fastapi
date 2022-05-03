from __future__ import annotations

from typing import List
from uuid import UUID

from app.storage.data_interface import DataObject, DBObject
from app.storage.database import get_session


def exception_handling(function):
    """try except handling"""

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as exception:
            raise DatabaseError("Something wrong happened!") from exception

    return wrapper


class DBInterface:
    def __init__(self, db_class: DBObject):
        self.db_class = db_class

    @exception_handling
    async def read_by_id(self, id: int | UUID) -> DBObject:
        session = get_session()
        return session.query(self.db_class).get(id)

    @exception_handling
    async def read_all(self) -> List[DBObject]:
        session = get_session()
        return session.query(self.db_class).all()

    @exception_handling
    async def create(self, data: DBObject) -> DBObject:
        session = get_session()
        session.add(data)
        session.commit()
        session.refresh(data)
        return data

    @exception_handling
    async def update(self, id: int | UUID, data: DataObject) -> DBObject:
        session = get_session()
        result = session.query(self.db_class).get(id)
        for key, value in data.dict().items():  # type: ignore
            setattr(result, key, value)
        session.commit()
        session.refresh(result)
        return result

    @exception_handling
    async def delete(self, id: int | UUID) -> None:
        session = get_session()
        result = session.query(self.db_class).get(id)
        session.delete(result)
        session.commit()


class DatabaseError(Exception):
    """Fails to interact with the Database"""
