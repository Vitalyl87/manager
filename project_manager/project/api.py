from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.config import settings
from project_manager.db_helper import db_helper
from project_manager.project.crud import ProjectCrud
from project_manager.project.schemas import ProjectRead

router = APIRouter(prefix=settings.prefix.project_prefix)


@router.get("/", status_code=200)
async def get_projects(
    session: AsyncSession = Depends(db_helper.get_session),
) -> list[ProjectRead]:
    return await ProjectCrud.get_all(session)
