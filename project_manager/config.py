from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseModel):
    host: str
    port: int
    reload: bool


class DbSettings(BaseModel):
    url: PostgresDsn
    echo: bool


class AppSettings(BaseModel):
    project_prefix: str = "/projects"
    task_prefix: str = "/tasks"
    data_prefix: str = "/add_data"


class TestSettings(BaseModel):
    db: str


class Settings(BaseSettings):
    """Settings for application"""

    db: DbSettings
    prefix: AppSettings = AppSettings()
    server: ServerSettings
    test: TestSettings
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


settings = Settings()
