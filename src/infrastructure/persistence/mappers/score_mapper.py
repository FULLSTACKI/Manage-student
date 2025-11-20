from src.infrastructure.persistence.models import ScoreModel
from src.domain.entities import Score

class ScoreMapper:
    @staticmethod
    def _to_model(entity: Score) -> ScoreModel:
        return ScoreModel(
            student_id=entity.student_id,
            course_id=entity.course_id,
            coursework_grade=entity.coursework_grade,
            midterm_grade=entity.midterm_grade,
            final_grade=entity.final_grade,
            gpa=entity.gpa
        )
    @staticmethod
    def _to_entity(model: ScoreModel) -> Score:
        return Score(
            student_id=model.student_id,
            course_id=model.course_id,
            coursework_grade=model.coursework_grade,
            midterm_grade=model.midterm_grade,
            final_grade=model.final_grade,
            gpa=model.gpa
        )