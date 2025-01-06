from datetime import date

from pydantic import BaseModel, Field

from project_manager.task.status import Status


class TaskBase(BaseModel):
    title: str = Field(max_length=200)
    status: Status
    deadline: date | None


class TaskRead(TaskBase):
    pass


class TaskCreate(TaskBase):
    project_id: int
