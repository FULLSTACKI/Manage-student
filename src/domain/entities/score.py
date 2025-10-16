from src.utils.exceptions import ValidationError
from src.domain.services.gpa_service import compute_gpa

class Score:
    def __init__(self, student_id: str, course_id: str, coursework_grade: float, midterm_grade: float, final_grade: float, gpa:float):
        self.student_id = student_id
        self.course_id = course_id
        self.coursework_grade = coursework_grade
        self.midterm_grade = midterm_grade
        self.final_grade = final_grade
        self.gpa = gpa
        self._validate_domain_invariants()

    def _validate_domain_invariants(self):
        # Quy tắc bất biến: điểm phải từ 0 đến 10
        for grade, name in [
            (self.coursework_grade, "coursework_grade"),
            (self.midterm_grade, "midterm_grade"),
            (self.final_grade, "final_grade"),
        ]:
            if not (0.0 <= grade <= 10.0):
                raise ValidationError("SCORE_INVALID", detail=f"{name} must be between 0 and 10.")

    @classmethod
    def add(cls, student_id, course_id, coursework_grade, midterm_grade, final_grade):
        try:
            coursework_grade = float(coursework_grade)
            midterm_grade = float(midterm_grade)
            final_grade = float(final_grade)
            gpa = compute_gpa(coursework_grade, midterm_grade, final_grade)
        except Exception as e:
            raise ValidationError("GRADE_FORMAT_INVALID", detail=str(e))
        new_score = cls(student_id, course_id, coursework_grade, midterm_grade, final_grade, gpa)
        return new_score