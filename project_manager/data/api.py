from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.config import settings
from project_manager.data.crud import DataCrud
from project_manager.db_helper import db_helper

router = APIRouter(prefix=settings.prefix.data_prefix)


@router.post("/", status_code=201)
async def create_projects_with_tasks(
    prj_count: int,
    task_count: int,
    session: AsyncSession = Depends(db_helper.get_session),
) -> dict:
    await DataCrud.generate_data(
        session=session, prj_count=prj_count, task_count=task_count
    )
    return {"message": "Projects and tasks were generated successfully"}
