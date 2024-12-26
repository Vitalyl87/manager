from enum import Enum


class Status(str, Enum):
    new = "new"
    in_progress = "in_progress"
    completed = "completed"
