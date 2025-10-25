from src.infrastructure.persistence.models import DepartmentModel
from src.domain.entities import Department

def _to_model(entity: Department) -> DepartmentModel:
    return DepartmentModel(
        department_id = entity.department_id,
        department_name = entity.department_name
    )
    
def _to_entity(model: DepartmentModel) -> Department:
    return Department(
        department_id = model.department_id,
        department_name = model.department_name
    )