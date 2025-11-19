from src.domain.repositories import IsStudentQueryRepo, IsDepartmentRepo, IsCourseRepo
from ..dtos.student_query_dto import *
from src.utils.exceptions import ValidationError
from src.utils.validators import validate_id

class StudentQueryManagement:
    def __init__(self, student_query_repo: IsStudentQueryRepo, course_repo: IsCourseRepo, department_repo: IsDepartmentRepo):
        self.student_repo = student_query_repo
        self.course_repo = course_repo
        self.department_repo = department_repo
    
    def get_filter_options(self, columns: List[str]) -> StudentFilterOption:
        departments = []
        courses = []
        try:
            if "departments" in columns:
                deps = self.department_repo.get_filter_all()
                if deps:
                    departments = [{"id": d.id, "name": d.name} for d in deps]
                else:
                    departments = []

            # Lấy courses nếu cần
            if "courses" in columns:
                crs = self.course_repo.get_filter_all()
                if crs:
                    courses = [{"id": c.id, "name": c.name} for c in crs]
                else:
                    courses = []
        except Exception as e:
            raise e
        return StudentFilterOption(
            departments=departments,
            courses=courses
        )
    
    def get_detail_students(self, req: StudentDetailRequest) -> List[studentOut]:
        try:
            list_student = self.student_repo.get_list_detail_student(req.columns,req.department_id,req.course_id)
            if not list_student:
                raise ValidationError("NOT_FOUND", detail="No students found with the given criteria")
            return [student for student in list_student]
        except Exception as e:
            raise e

    def get_by_id(self, student_id: str) -> studentOut:
        try:
            if not validate_id(student_id):
                raise ValidationError("INVALID_INPUT", detail="student_id format is invalid")
                 
            student = self.student_repo.get_by_id(student_id)
            
            if not student:
                raise ValidationError("NOT_FOUND",detail=f"student {student_id} not found")
        except Exception as e:
            raise e
        return StudentResponse(
            success=True,
            message=f"Đã tìm thấy Sinh viên ID: {student.student_id}",
            student=student
        )        