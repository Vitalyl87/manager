from typing import Any

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDao:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[Any]:
        stmt = Select(cls.model).order_by(cls.model.id)
        result = await session.scalars(stmt)
        return result.all()
