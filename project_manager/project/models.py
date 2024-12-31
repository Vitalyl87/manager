from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text

from project_manager.base import Base


class Project(Base):
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project")
