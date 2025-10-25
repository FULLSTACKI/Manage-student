from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.repositories import IsStudentRepo
from src.infrastructure.persistence.models import StudentModel, DepartmentModel, CourseModel, RegistrationModel
from src.domain.entities import Student, StudentDetail
from src.infrastructure.persistence.mappers import StudentMapper
from sqlalchemy import select
from typing import List

class StudentRepo(IsStudentRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_by_id(self, student_id:str) -> Student:
        db_model = self.db_session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
        if db_model:
            return StudentMapper.to_entity(db_model)
        return None
    
    def get_list_detail_student(self, col: List[str], department_id:List[str] = None, course_id:List[str] = None):
        try: 
            columns = StudentMapper.map_col(col)

            stmt = (
                select(*columns)
                .select_from(StudentModel)
                .join(DepartmentModel)
                .join(RegistrationModel)
                .join(CourseModel)
            )
            
            if "departments" in col and department_id:
                stmt = stmt.where(StudentModel.department_id.in_(department_id))
            if "courses" in col and course_id:
                stmt = stmt.where(RegistrationModel.course_id.in_(course_id))

            data_row = self.db_session.execute(stmt).mappings().all()

            return [StudentDetail(
                student_id=data.student_id,
                student_name=data.student_name,
                email=data.email,
                birthday=data.birthday,
                department_name=data.department_name,
                course_name=data.course_name
            ) for data in data_row]
        except Exception as e:
            raise e 
        except IntegrityError as e:
            raise e
    
    def save(self, req_student: Student) -> Student:
        existing = self.get_by_id(req_student.student_id)
        
        save_student = None 
        
        if existing:
            existing.student_name = req_student.student_name
            existing.email = req_student.email
            existing.age = req_student.age 
            existing.birthday = req_student.birthday
            existing.sex = req_student.sex
            existing.department_id = req_student.department_id
            save_student = StudentMapper.to_model(existing)
        else: 
            save_student = StudentMapper.to_model(req_student)
        try:
            persistent = self.db_session.merge(save_student)
            self.db_session.commit()
            self.db_session.refresh(persistent)
            return StudentMapper.to_entity(persistent)
        except IntegrityError as e:
            errors = str(e)
            self.db_session.rollback()
            if "UNIQUE constraint failed: students.email" in errors:
                raise ValueError("Email đã tồn tại. Vui lòng sử dụng một địa chỉ email khác.")
            else:
                # Chuyển đổi lỗi kỹ thuật thành lỗi có ý nghĩa hơn cho Application Layer
                raise ValueError(f"Lỗi lưu trữ dữ liệu: {errors}")
        except Exception as e:
            self.db_session.rollback()
            raise e
        
if __name__ == "__main__":
    list = ["student_id","student_name","email","departments","courses"]
    data = StudentRepo.get_list_detail_student(list)
    print(data)
        