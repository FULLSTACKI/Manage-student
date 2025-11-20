from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.entities import Registration
from src.infrastructure.persistence.models import RegistrationModel
from src.infrastructure.persistence.mappers import RegistrationMapper
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
            return RegistrationMapper._to_entity(reg)
        return None

    def save(self, req: Registration) -> Registration:
        existing = self.db.query(RegistrationModel).filter(RegistrationModel.course_id == req.course_id and RegistrationModel.student_id == req.student_id).first()
        try:
            if not existing:
                save_regis = RegistrationMapper._to_model(req)
                persistent = self.db.merge(save_regis)
                self.db.commit()
                self.db.refresh(persistent)
                return  req
        except IntegrityError as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            raise e