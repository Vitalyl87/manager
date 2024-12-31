import uvicorn
from fastapi import FastAPI

from project_manager.config import settings
from project_manager.project import router as project_router
from project_manager.task import router as task_router

app = FastAPI()
app.include_router(project_router)
app.include_router(task_router)


@app.get("/")
async def hello():
    return "hello world"


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
    )
