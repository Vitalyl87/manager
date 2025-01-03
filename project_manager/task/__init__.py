from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.config import settings
from project_manager.db_helper import dp_helper
from project_manager.task.dao import get_all_tasks

router = APIRouter(prefix=settings.prefix.task_prefix)


@router.get("/")
async def get_tasks(session: AsyncSession = Depends(dp_helper.get_session)):
    return await get_all_tasks(session)
