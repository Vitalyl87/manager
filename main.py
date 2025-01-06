from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from project_manager.config import settings
from project_manager.project import router as project_router
from project_manager.task import router as task_router
from project_manager.data import router as data_router
from project_manager.db_helper import dp_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await dp_helper.dispose()

main_app = FastAPI(lifespan=lifespan)
main_app.include_router(project_router)
main_app.include_router(task_router)
main_app.include_router(data_router)


@main_app.get("/")
def hello():
    return "hello world"


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
    )
