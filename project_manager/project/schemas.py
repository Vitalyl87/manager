from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(max_length=100)


class ProjectRead(UserBase):
    id: int


class ProjectCreate(UserBase):
    name: str = Field(max_length=100)
    description: str | None
