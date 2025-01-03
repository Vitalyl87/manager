from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.task.models import Task


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    stmt = Select(Task).order_by(Task.id)
    result = await session.scalars(stmt)
    return result.all()
