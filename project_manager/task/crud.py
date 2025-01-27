from fastapi import HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.crud import BaseCrud
from project_manager.task.models import Task
from project_manager.task.schemas import TaskCreate, TaskRead


class TaskCrud(BaseCrud):
    """Crud operations for tasks"""

    model = Task

    @classmethod
    async def get_task_by_project_id(
        cls, session: AsyncSession, project_id: int, **filter_by
    ) -> list[TaskRead]:
        stmt = (
            Select(cls.model)
            .where(cls.model.project_id == project_id)
            .filter_by(**filter_by)
            .order_by(cls.model.id)
        )
        result = await session.scalars(stmt)
        res = result.all()
        if len(res) == 0:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Tasks with project id={project_id} was not found"
                    if not filter_by
                    else f"Tasks with project id={project_id} and status={filter_by['status'].value} was not found"
                ),
            )
        return res

    @classmethod
    async def create_task_for_project_id(
        cls, session: AsyncSession, task: TaskCreate
    ) -> int:
        data = task.model_dump()
        new_task = Task(**data)
        session.add(new_task)
        try:
            await session.commit()
            await session.refresh(new_task)
        except Exception as ex:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(ex.orig))
        return new_task.id
