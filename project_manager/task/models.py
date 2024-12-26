from project_manager.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional
from sqlalchemy import String
from datetime import date
from project_manager.task.status import Status


class Task(Base):
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[Status] = mapped_column(default=Status.new,
                                           server_default="'new'",
                                           nullable=False)
    deadline: Mapped[Optional[date]]

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project",
                                              back_populates="tasks")
