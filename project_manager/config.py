from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import BaseModel
from pydantic import PostgresDsn


class ServerSettings(BaseModel):
    host: str
    port: int
    reload: bool


class DbSettings(BaseModel):
    url: PostgresDsn
    echo: bool


class Settings(BaseSettings):
    db: DbSettings
    server: ServerSettings
    model_config = SettingsConfigDict(case_sensitive=False,
                                      env_file=".env",
                                      env_nested_delimiter="__",
                                      env_prefix="APP_CONFIG__")


settings = Settings()
