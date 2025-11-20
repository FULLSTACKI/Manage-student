from src.domain.entities import Registration
from src.infrastructure.persistence.models import RegistrationModel

class RegistrationMapper:
    @staticmethod
    def _to_model(entity: Registration) -> RegistrationModel:
        return RegistrationModel(
            student_id=entity.student_id,
            course_id=entity.course_id,
            registered_at=entity.registered_at
        )
    @staticmethod
    def _to_entity(model: RegistrationModel) -> Registration:
        return Registration(
            student_id=model.student_id,
            course_id=model.course_id,
            registered_at=model.registered_at
        )