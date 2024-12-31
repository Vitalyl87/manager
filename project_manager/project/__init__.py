from fastapi import APIRouter

from project_manager.config import settings

router = APIRouter(prefix=settings.prefix.project_prefix)


@router.get("/")
async def get_tasks():
    return "projects"
