from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from project_manager.project.models import Project
from project_manager.project.schemas import ProjectRead


async def get_all_projects(session: AsyncSession) -> list[ProjectRead]:
    stmt = Select(Project).order_by(Project.id)
    result = await session.scalars(stmt)
    return result.all()
