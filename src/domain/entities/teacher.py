from datetime import date
from src.domain.services import compute_age, parse_date

class Teacher:
    def __init__(self, teacher_id: str, teacher_name: str, email: str, birthday: date, age: int, sex: str, department_id: str):
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name
        self.email = email
        self.birthday = birthday
        self.age = age
        self.sex = sex
        self.department_id = department_id

    @classmethod
    def add(cls, teacher_id: str, teacher_name: str, email: str, birthday: date, sex: str, department_id: str):
        try:
            birthday = parse_date(birthday)
            age = compute_age(birthday)
            return cls(
                teacher_id=teacher_id,
                teacher_name=teacher_name,
                email=email,
                birthday=birthday,
                age=age,
                sex=sex,
                department_id=department_id
            )
        except Exception as e:
            raise e 