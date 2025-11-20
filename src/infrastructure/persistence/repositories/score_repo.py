from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.repositories import IsScoreRepo
from src.infrastructure.persistence.models import ScoreModel
from src.infrastructure.persistence.mappers import ScoreMapper
from src.domain.entities import Score

class ScoreRepo(IsScoreRepo):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, student_id: str, course_id: str) -> Score:
        score = self.db.query(ScoreModel).filter(
            ScoreModel.student_id == student_id,
            ScoreModel.course_id == course_id
        ).first()
        if score:
            return ScoreMapper._to_entity(score)
        return None

    def save(self,req_score: Score) -> Score:
        existing = self.db.query(ScoreModel).filter(ScoreModel.course_id == req_score.course_id and ScoreModel.student_id == req_score.student_id).first()
        try:
            if not existing:
                save_score = ScoreMapper._to_model(req_score)
                persistent = self.db.merge(save_score)
                self.db.commit()
                self.db.refresh(persistent)
                return  req_score
        except IntegrityError as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            raise e
        