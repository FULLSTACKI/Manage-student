from datetime import date
from src.utils.exceptions import ValidationError
from src.domain.services.compare_date_service import parse_date

class Registration:
    def __init__(self, student_id: str, course_id: str, registered_at: date = None):
        self.student_id = student_id
        self.course_id = course_id
        self.registered_at = registered_at
        self._validate_domain_invariants()

    def _validate_domain_invariants(self):
        # Quy tắc bất biến: student_id và course_id không được rỗng
        if not self.student_id or not self.course_id:
            raise ValidationError("REGISTRATION_INVALID", detail="student_id and course_id are required.")

    @classmethod
    def add(cls, student_id, course_id):
        try:
            reg_date = date.today()
        except Exception as e:
            raise ValidationError("DATE_FORMAT_INVALID", detail=str(e))
        new_registration = cls(student_id, course_id, reg_date)
        return new_registration