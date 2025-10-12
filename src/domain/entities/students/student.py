from datetime import date
from src.utils.error.exceptions import ValidationError
from src.app.service.compare_date_service import parse_date
from src.app.service.age_service import compute_age
class Student:
    def __init__(self, id: str, name: str, email: str, birthday: date, age: int, sex: str):
        self.id = id
        self.name = name
        self.email = email
        self.birthday = birthday
        self.sex = sex
        self.age = age
        self._validate_domain_invariants()
    
    def _validate_domain_invariants(self):
        # Quy tắc bất biến
        if self.age < 16:
            raise ValidationError("AGE_INVALID")
        
    @classmethod
    def add(cls, id, name, email, birthday:str, sex):
        try:
            birthday = parse_date(birthday)
            age = compute_age(birthday)
        except Exception as e:
            raise ValidationError("DATE_FORMAT_INVALID", detail=str(e))
        
        new_student = cls(id, name, email, birthday, age, sex)
        return new_student