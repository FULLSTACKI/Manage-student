from src.infrastructure.persistence.models import StudentModel, CourseModel, DepartmentModel
from src.application.dtos import studentOut
from src.domain.entities import Student
from typing import List

class StudentMapper:
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
    def to_detail(model: StudentModel) -> studentOut:
        return studentOut(
            student_id=model.student_id,
            student_name=model.student_name,
            email=model.email,
            age=f"{model.age}",
            birthday=f"{model.birthday}",
            sex=model.sex,
            departments=model.department.department_name,
            birthplace=model.birthplace,
            address=model.address,
            phone=model.phone,
            ethnicity=model.ethnicity,
            religion=model.religion,
            id_card=model.id_card,
            issue_date=f"{model.issue_date}",
            issue_place=model.issue_place
        )
        
    @staticmethod
    def map_col(col: List[str]):
        column_map = {
            "student_id": StudentModel.student_id,
            "student_name": StudentModel.student_name,
            "email": StudentModel.email,
            "age": StudentModel.age,
            "birthday": StudentModel.birthday,
            "sex": StudentModel.sex,
            "departments": DepartmentModel.department_name,
            "courses": CourseModel.course_name,
            "birthplace": StudentModel.birthplace,
            "address": StudentModel.address,
            "phone": StudentModel.phone,
            "ethnicity": StudentModel.ethnicity,
            "religion": StudentModel.religion,
            "id_card": StudentModel.id_card,
            "issue_date": StudentModel.issue_date,
            "issue_place": StudentModel.issue_place,
        }
        return [column_map[c] for c in col if c in column_map]
