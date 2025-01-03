from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(max_length=100)


class ProjectRead(ProjectBase):
    id: int


class ProjectCreate(ProjectBase):
    name: str = Field(max_length=100)
    description: str | None
