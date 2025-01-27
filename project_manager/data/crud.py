from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.project.models import Project
from project_manager.project.schemas import ProjectCreate
from project_manager.task.models import Task
from project_manager.task.schemas import TaskCreate
from project_manager.task.status import Status

fake = Faker("ru_RU")


class DataCrud:
    """Crud actions for generate app data"""

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        data: TaskCreate | ProjectCreate,
        entity: Project | Task,
    ) -> int:
        data = data.model_dump()
        new_entity = entity(**data)
        session.add(new_entity)
        try:
            await session.commit()
            await session.refresh(new_entity)
        except Exception as e:
            await session.rollback()
            raise e
        return new_entity.id

    @classmethod
    async def generate_data(
        cls, session: AsyncSession, prj_count: int, task_count: int
    ) -> None:
        for prj in range(prj_count):
            prj_create = ProjectCreate(
                name=fake.company(), description=fake.sentence(nb_words=5)
            )
            proj_id = await cls.create(session=session, data=prj_create, entity=Project)

            for tsk in range(task_count):
                tsk_create = TaskCreate(
                    title=fake.sentence(nb_words=3),
                    status=Status.new,
                    deadline=fake.date_this_year(),
                    project_id=proj_id,
                )
                await cls.create(session=session, data=tsk_create, entity=Task)
