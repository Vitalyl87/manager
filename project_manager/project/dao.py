from project_manager.base_dao import BaseDao
from project_manager.project.models import Project


class ProjectDao(BaseDao):
    model = Project
