from datetime import date
from src.utils.exceptions import ValidationError
from src.domain.services.compare_date_service import parse_date
from src.domain.services.age_service import compute_age
class Student:
    def __init__(
        self,
        student_id: str,
        student_name: str,
        email: str,
        birthday: date,
        age: int,
        sex: str,
        department_id: str,
        birthplace: str ,
        address: str ,
        phone: str ,
        ethnicity: str ,
        religion: str ,
        id_card: str ,
        issue_date: date ,
        issue_place: str 
    ):
        self.student_id = student_id
        self.student_name = student_name
        self.email = email
        self.birthday = birthday
        self.sex = sex
        self.age = age
        self.department_id = department_id
        self.birthplace = birthplace
        self.address = address
        self.phone = phone
        self.ethnicity = ethnicity
        self.religion = religion
        self.id_card = id_card
        self.issue_date = issue_date
        self.issue_place = issue_place

        self._validate_domain_invariants()

    def _validate_domain_invariants(self):
        """Quy tắc bất biến"""
        if self.age < 10:
            raise ValidationError("AGE_INVALID")
        return None

    @classmethod
    def add(
        cls,
        id,
        name,
        email,
        birthday,
        sex,
        department_id,
        birthplace,
        address,
        phone,
        ethnicity,
        religion,
        id_card,
        issue_date,
        issue_place
    ):
        try:
            birthday = parse_date(birthday)
            age = compute_age(birthday)
            if issue_date:
                issue_date = parse_date(issue_date)
        except Exception as e:
            raise ValidationError("DATE_FORMAT_INVALID", detail=str(e))

        new_student = cls(
            id,
            name,
            email,
            birthday,
            age,
            sex,
            department_id,
            birthplace,
            address,
            phone,
            ethnicity,
            religion,
            id_card,
            issue_date,
            issue_place
        )
        return new_student