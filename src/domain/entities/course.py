from datetime import date
from src.utils.exceptions import ValidationError
from src.domain.services.compare_date_service import parse_date
from src.domain.services.end_course import compute_end_course
class Course:
    def __init__(self, course_id: str, course_name: str, credits: int, start_course: date, end_course: date, department_id: str):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.start_course = start_course
        self.end_course = end_course
        self.department_id = department_id
        self._validate_domain_invariants()

    def _validate_domain_invariants(self):
        # Quy tắc bất biến: ngày bắt đầu phải trước ngày kết thúc
        if self.start_course and self.end_course and self.start_course > self.end_course:
            raise ValidationError("COURSE_DATE_INVALID", detail="Start date must be before end date.")

    @classmethod
    def add(cls, id, name, credits, start_course, department_id):
        try:
            start_course = parse_date(start_course)
            end_course = compute_end_course(start_course)
        except Exception as e:
            raise ValidationError("DATE_FORMAT_INVALID", detail=str(e))
        new_course = cls(id, name, int(credits), start_course, end_course, department_id)
        return new_course