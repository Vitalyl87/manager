from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.config import settings
from project_manager.db_helper import dp_helper
from project_manager.task.dao import TaskDao
from project_manager.task.schemas import TaskCreate, TaskRead
from project_manager.task.status import Status

router = APIRouter(prefix=settings.prefix.task_prefix)


@router.get("/")
async def get_tasks(
    session: AsyncSession = Depends(dp_helper.get_session),
) -> list[TaskRead]:
    return await TaskDao.get_all(session)


@router.get("/{project_id}")
async def get_task_by_project_id(
    project_id: int,
    status: Status = None,
    session: AsyncSession = Depends(dp_helper.get_session),
) -> list[TaskRead]:
    if status is None:
        return await TaskDao.get_task_by_project_id(
            session=session, project_id=project_id
        )
    return await TaskDao.get_task_by_project_id(
        session=session, project_id=project_id, status=status
    )


@router.post("/", status_code=200)
async def add_task_for_project(
    task_data: TaskCreate,
    session: AsyncSession = Depends(dp_helper.get_session),
) -> dict:
    await TaskDao.create_task_for_project_id(session=session, task=task_data)
    return {
        "message": f"Task for project (id={task_data.project_id}) added successfully"
    }


@router.delete("/{task_id}", status_code=200)
async def delete_task_by_id(
    task_id: int, session: AsyncSession = Depends(dp_helper.get_session)
) -> dict:
    await TaskDao.delete_by_id_or_404(session=session, id=task_id)
    return {"message": f"Task with id={task_id} was deleted successfully"}


@router.patch("/{task_id}/status")
async def update_task_status(
    task_id: int, status: Status, session: AsyncSession = Depends(dp_helper.get_session)
):
    await TaskDao.patch_by_id_or_404(session=session, id=task_id, status=status)
    return {"message": f"Task with id={task_id} was updated successfully"}
