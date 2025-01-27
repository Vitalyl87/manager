from enum import Enum


class Status(str, Enum):
    """Task statuses"""

    new = "new"
    in_progress = "in_progress"
    completed = "completed"
