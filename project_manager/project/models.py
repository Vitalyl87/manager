from project_manager.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy.types import Text


class Project(Base):
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)

    tasks: Mapped[list["Task"]] = relationship("Task",
                                               back_populates="project")
