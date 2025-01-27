from project_manager.crud import BaseCrud
from project_manager.project.models import Project


class ProjectCrud(BaseCrud):
    """Crud operations for projects"""

    model = Project
