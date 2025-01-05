from project_manager.project.models import Project
from project_manager.base_dao import BaseDao


class ProjectDao(BaseDao):
    model = Project
