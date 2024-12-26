from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from project_manager.config import settings


class Db_hepler:
    def __init__(self, url: str, echo: bool) -> None:
        self.engine: AsyncEngine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(bind=self.engine,
                                                  autoflush=False,
                                                  expire_on_commit=False)

    async def get_session(self):
        async with self.session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self.engine.dispose()


dp_hepler = Db_hepler(url=str(settings.db.url), echo=settings.db.echo)
