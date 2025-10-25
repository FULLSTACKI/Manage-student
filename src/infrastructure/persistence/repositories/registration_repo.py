from sqlalchemy.orm import Session
from src.domain.entities import Registration
from src.infrastructure.persistence.models import RegistrationModel
from src.domain.repositories import IsRegistrationRepo

class RegistrationRepo(IsRegistrationRepo):
    def __init__(self, db_session: Session=None):
        self.db = db_session
        
    def get_by_id(self, student_id: str, course_id: str):
        reg = self.db.query(RegistrationModel).filter(
            RegistrationModel.student_id == student_id,
            RegistrationModel.course_id == course_id
        ).first()
        if reg:
            return _to_entity(reg)
        return None

    def save(self, reg: Registration) -> Registration:
        existing = self.get_by_id(reg.student_id, reg.course_id)
        if not existing:
            self.db.add(_to_model(reg))
            self.db.commit()
            self.db.refresh(_to_model(reg))
            return reg
        return None 