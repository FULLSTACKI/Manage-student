from src.infrastructure.persistence.models import StudentModel, CourseModel, DepartmentModel
from src.application.dtos import studentOut
from typing import List
from sqlalchemy import func

class StudentQueryMapper:
    @staticmethod
    def to_detail(model: StudentModel) -> studentOut:
        return studentOut(
            student_id=model.student_id,
            student_name=model.student_name,
            email=model.email,
            age=model.age,
            birthday=model.birthday,
            sex=model.sex,
            departments=model.department.department_name,
            birthplace=model.birthplace,
            address=model.address,
            phone=model.phone,
            ethnicity=model.ethnicity,
            religion=model.religion,
            id_card=model.id_card,
            issue_date=model.issue_date,
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
            "departments": DepartmentModel.department_name.label("departments"),
            "courses": CourseModel.course_name.label("courses"),
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
    

