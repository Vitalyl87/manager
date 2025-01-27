from typing import Any

from fastapi import HTTPException
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCrud:
    """Class for basic crud operations with database"""

    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[Any]:
        stmt = Select(cls.model).order_by(cls.model.id)
        result = await session.scalars(stmt)
        return result.all()

    @classmethod
    async def get_by_id_or_404(cls, session: AsyncSession, id: int) -> Any:
        item = await session.get(cls.model, id)
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"{cls.model} with id {id} was not found"
            )
        return item

    @classmethod
    async def delete_by_id_or_404(cls, session: AsyncSession, id: int) -> None:
        item = await cls.get_by_id_or_404(session=session, id=id)
        await session.delete(item)
        await session.commit()

    @classmethod
    async def patch_by_id_or_404(cls, session: AsyncSession, id: int, **values) -> None:
        await cls.get_by_id_or_404(session=session, id=id)
        stmt = update(cls.model).where(cls.model.id == id).values(**values)
        await session.execute(stmt)
        try:
            await session.commit()
        except Exception as ex:
            await session.rollback()
            raise HTTPException(status_code=422, detail=str(ex.orig))
