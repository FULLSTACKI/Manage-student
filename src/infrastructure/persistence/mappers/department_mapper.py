from src.infrastructure.persistence.models import DepartmentModel
from src.domain.entities import Department

class DepartmentMapper:
    @staticmethod
    def _to_model(entity: Department) -> DepartmentModel:
        return DepartmentModel(
            department_id = entity.department_id,
            department_name = entity.department_name
        )
    @staticmethod
    def _to_entity(model: DepartmentModel) -> Department:
        return Department(
            department_id = model.department_id,
            department_name = model.department_name
        )