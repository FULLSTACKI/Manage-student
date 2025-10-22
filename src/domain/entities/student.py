from datetime import date
from src.utils.exceptions import ValidationError
from src.domain.services.compare_date_service import parse_date
from src.domain.services.age_service import compute_age
class Student:
    def __init__(self, student_id: str, student_name: str, email: str, birthday: date, age: int, sex: str, department_id:str):
        self.student_id = student_id
        self.student_name = student_name
        self.email = email
        self.birthday = birthday
        self.sex = sex
        self.age = age
        self.department_id = department_id 
        self._validate_domain_invariants()
    
    def _validate_domain_invariants(self):
        # Quy tắc bất biến
        if self.age < 16:
            raise ValidationError("AGE_INVALID")
        
    @classmethod
    def add(cls, id, name, email, birthday, sex, department_id):
        try:
            birthday = parse_date(birthday)
            age = compute_age(birthday)
        except Exception as e:
            raise ValidationError("DATE_FORMAT_INVALID", detail=str(e))
        
        new_student = cls(id, name, email, birthday, age, sex, department_id)
        return new_student