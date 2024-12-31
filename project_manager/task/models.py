from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_manager.base import Base
from project_manager.task.status import Status


class Task(Base):
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[Status] = mapped_column(
        default=Status.new, server_default="'new'", nullable=False
    )
    deadline: Mapped[date | None]

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
