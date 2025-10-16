from sqlalchemy.orm import Session
from src.infrastructure.persistence.models import Department as DepartmentModel
from src.domain.repositories import IsDepartmentRepo
from src.domain.entities import Department
from sqlalchemy.exc import IntegrityError
from typing import *
from sqlalchemy import text
from src.domain.entities.dtos import *

def _to_model(entity: Department) -> DepartmentModel:
    return DepartmentModel(
        department_id = entity.department_id,
        department_name = entity.department_name
    )
    
def _to_entity(model: DepartmentModel) -> Department:
    return Department(
        department_id = model.department_id,
        department_name = model.department_name
    )

class DepartmentRepo(IsDepartmentRepo):
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def get_total_student_sex_by_department(self) -> List[DepartmentStudentSexCountDTO]:
        try:
            query = text(
                """
                    SELECT
                        d.department_name, 
                        COUNT(CASE WHEN s.sex = 'M' THEN 1 END) AS total_M,
                        COUNT(CASE WHEN s.sex = 'F' THEN 1 END) AS total_F,
                        COUNT(s.sex) AS total_sex
                    FROM departments as d
                    JOIN students as s ON s.department_id = d.department_id
                    GROUP BY d.department_name
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [DepartmentStudentSexCountDTO(**data) for data in department_row]
        except Exception as e:
            raise f"Error: {e}" 
        
    def get_min_final_grade_by_department(self):
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        MIN(s.final_grade) as min_final_grade
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY min_final_grade
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [DepartmentCourseMaxGpaDTO(**data) for data in data_row]
        except Exception as e:
            raise  f"Error: {e}"
        
    def get_max_final_grade_by_department(self):
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        MAX(s.final_grade) as max_final_grade
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY max_final_grade DESC
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [DepartmentCourseMaxGpaDTO(**data) for data in data_row]
        except Exception as e:
            raise  f"Error: {e}"
        
    def get_total_course_by_department(self) -> List[DepartmentCourseCountDTO]:
        try:
            query = text(
                """
                    SELECT
                        d.department_name, 
                        COUNT(c.student_id) as total_courses
                    FROM departments as d
                    JOIN courses as c ON d.department_id = c.department_id
                    GROUP BY d.department_name
                    ORDER BY total_courses DESC
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            list_total_student_department = [DepartmentCourseCountDTO(**data) for data in department_row]
            return list_total_student_department
        except Exception as e:
            raise f"Error: {e}"
        
    def get_min_gpa_by_department(self) -> List[DepartmentCourseMinGpaDTO]:
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        MIN(s.gpa) as min_gpa
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY min_gpa 
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [DepartmentCourseMinGpaDTO(**data) for data in data_row]
        except Exception as e:
            raise  f"Error: {e}"
        
    def get_max_gpa_by_department(self) -> List[DepartmentCourseMaxGpaDTO]:
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        MAX(s.gpa) as max_gpa
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY max_gpa DESC
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [DepartmentCourseMaxGpaDTO(**data) for data in data_row]
        except Exception as e:
            raise  f"Error: {e}"
        
    def get_avg_gpa_by_department(self) -> List[DepartmentCourseAvgGpaDTO]:
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        AVG(s.gpa) as avg_gpa
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY avg_gpa DESC
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [DepartmentCourseAvgGpaDTO(**data) for data in data_row]
        except Exception as e:
            raise e
    
    def get_avg_final_grade_by_department(self) -> List[DepartmentCourseAvgFinalGradeDTO]:
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        AVG(s.final_grade) as avg_final_grade
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY avg_final_grade DESC
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [DepartmentCourseAvgFinalGradeDTO(**data) for data in data_row]
        except Exception as e:
            raise  f"Error: {e}"
        
    def get_all(self) -> List[Department]:
        try:
            query = text("SELECT * FROM departments")
            result = self.db.execute(query)
            department_row = result.mappings().all()
            list_department = [Department(**data) for data in department_row]
            return list_department
        except Exception as e:
            raise  f"Error: {e}"
    
    def get_by_id(self, Department_id: str) -> Department:
        data = self.db.query(DepartmentModel).filter(DepartmentModel.id == Department_id).first()
        if data:
            return _to_entity(data)
        return None
    
    def get_total_student_by_department(self) -> List[DepartmentStudentCountDTO]:
        try:
            query = text(
                """
                    SELECT
                        d.department_name, 
                        COUNT(s.student_id) as total_students
                    FROM departments as d
                    JOIN students as s ON d.department_id = s.department_id
                    GROUP BY d.department_name
                    ORDER BY total_students DESC
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            list_total_student_department = [DepartmentStudentCountDTO(**data) for data in department_row]
            return list_total_student_department
        except Exception as e:
            raise f"Error: {e}"
            

    def save(self, req_Department: Department) -> Department:
        existing = self.get_by_id(req_Department.id)
        
        save_Department = None 
        
        if existing:
            existing.department_name = req_Department.department_name
            save_Department = _to_model(existing)
        else: 
            save_Department = _to_model(req_Department)
            self.db.add(save_Department)
        try:
            self.db.commit()
            self.db.refresh(save_Department)
            return _to_entity(save_Department)
        except IntegrityError as e:
            errors = str(e)
            self.db.rollback()
            if "UNIQUE constraint failed: Department.name" in errors:
                raise ValueError("Name Department đã tồn tại.")
            else:
                raise ValueError(f"Lỗi lưu trữ dữ liệu: {errors}")
        except Exception as e:
            self.db.rollback()
            raise e
        
        