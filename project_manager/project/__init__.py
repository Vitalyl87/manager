from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.config import settings
from project_manager.db_helper import dp_helper
from project_manager.project.dao import ProjectDao
from project_manager.project.schemas import ProjectRead

router = APIRouter(prefix=settings.prefix.project_prefix)


@router.get("/")
async def get_projects(
    session: AsyncSession = Depends(dp_helper.get_session),
) -> list[ProjectRead]:
    return await ProjectDao.get_all(session)
