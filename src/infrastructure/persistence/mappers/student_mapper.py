from src.infrastructure.persistence.models import StudentModel, CourseModel, DepartmentModel
from src.domain.entities import StudentDetail, Student
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
            department_id = entity.department_id
        )

    @staticmethod
    def to_entity(model: StudentModel) -> Student:
        return Student(
            student_id=model.student_id,
            student_name=model.student_name,
            email=model.email,
            age=model.age,
            birthday=model.birthday,
            sex=model.sex,
            department_id=model.department_id
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
        }
        return [column_map[c] for c in col if c in column_map]