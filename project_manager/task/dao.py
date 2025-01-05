from fastapi import HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.base_dao import BaseDao
from project_manager.task.models import Task
from project_manager.task.schemas import TaskCreate, TaskRead


class TaskDao(BaseDao):
    model = Task

    @classmethod
    async def get_task_by_project_id(
        cls, session: AsyncSession, project_id: int, **filter_by
    ) -> list[TaskRead]:
        print("DAO!")
        print(filter_by)
        stmt = (
            Select(cls.model)
            .where(cls.model.project_id == project_id)
            .filter_by(**filter_by)
            .order_by(cls.model.id)
        )
        result = await session.scalars(stmt)
        return result.all()

    @classmethod
    async def create_task_for_project_id(cls, session: AsyncSession, task: TaskCreate):
        data = task.model_dump()
        new_task = Task(**data)
        session.add(new_task)
        try:
            await session.commit()
        except Exception as ex:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(ex.orig))
