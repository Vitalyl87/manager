from fastapi import APIRouter

from project_manager.config import settings

router = APIRouter(prefix=settings.prefix.task_prefix)


@router.get("/")
async def get_tasks():
    return "tasks"
