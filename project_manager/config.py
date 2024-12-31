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


class Settings(BaseSettings):
    db: DbSettings
    prefix: AppSettings = AppSettings()
    server: ServerSettings
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


settings = Settings()
