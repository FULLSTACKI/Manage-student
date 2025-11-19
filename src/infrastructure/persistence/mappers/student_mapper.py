from src.infrastructure.persistence.models import StudentModel
from src.domain.entities import Student

class StudentCommandMapper:
    @staticmethod
    def to_model(entity: Student) -> StudentModel:
        return StudentModel(
            student_id=entity.student_id,
            student_name=entity.student_name,
            email=entity.email,
            birthday=entity.birthday,
            age=entity.age,
            sex=entity.sex,
            department_id=entity.department_id,
            birthplace=entity.birthplace,
            address=entity.address,
            phone=entity.phone,
            ethnicity=entity.ethnicity,
            religion=entity.religion,
            id_card=entity.id_card,
            issue_date=entity.issue_date,
            issue_place=entity.issue_place
        )
        
    @staticmethod
    def to_entity(model: StudentModel) -> Student:
        return Student(
            student_id=model.student_id,
            student_name=model.student_name,
            email=model.email,
            birthday=model.birthday,
            age=model.age,
            sex=model.sex,
            department_id=model.department_id,
            birthplace=model.birthplace,
            address=model.address,
            phone=model.phone,
            ethnicity=model.ethnicity,
            religion=model.religion,
            id_card=model.id_card,
            issue_date=model.issue_date,
            issue_place=model.issue_place
        )