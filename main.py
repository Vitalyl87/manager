from fastapi import FastAPI
import uvicorn
from project_manager.config import settings


app = FastAPI()


@app.get("/")
async def hello():
    return "hello world"

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.server.host,
                port=settings.server.port,
                reload=settings.server.reload)
