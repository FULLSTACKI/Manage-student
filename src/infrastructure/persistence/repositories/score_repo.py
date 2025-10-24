from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.repositories import IsScoreRepo
from src.infrastructure.persistence.models import ScoreModel
from src.domain.entities import Score


def _to_model(entity: Score) -> ScoreModel:
    return ScoreModel(
        student_id=entity.student_id,
        course_id=entity.course_id,
        coursework_grade=entity.coursework_grade,
        midterm_grade=entity.midterm_grade,
        final_grade=entity.final_grade,
        gpa=entity.gpa
    )
    
def _to_entity(model: ScoreModel) -> Score:
    return Score(
        student_id=model.student_id,
        course_id=model.course_id,
        coursework_grade=model.coursework_grade,
        midterm_grade=model.midterm_grade,
        final_grade=model.final_grade,
        gpa=model.gpa
    )

class ScoreRepo(IsScoreRepo):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, student_id: str, course_id: str) -> Score:
        score = self.db.query(ScoreModel).filter(
            ScoreModel.student_id == student_id,
            ScoreModel.course_id == course_id
        ).first()
        if score:
            return _to_entity(score)
        return None
    
    # def get_avg_gpa_all(self) -> float:
    #     try:
    #         query = """
    #             SELECT 
    #                 AVG(s.gpa) as avg_gpa
    #             FROM scores as s
    #         """
    #         result = self.db.execute(query)
    #         return result
    #     except Exception as e:
    #         raise e

    def save(self,req_score: Score) -> Score:
        existing = self.get_by_id(req_score.student_id, req_score.course_id)

        if existing:
            existing.coursework_grade = req_score.coursework_grade
            existing.midterm_grade = req_score.midterm_grade
            existing.final_grade = req_score.final_grade
            existing.gpa = req_score.gpa
            save_score = _to_model(existing)
        else:
            save_score = _to_model(req_score)

        try:
            persistent_obj = self.db.merge(save_score)
            self.db.commit()
            self.db.refresh(persistent_obj)
            return _to_entity(persistent_obj)
        except IntegrityError as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            raise e
        