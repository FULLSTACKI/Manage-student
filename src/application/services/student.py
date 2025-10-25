from src.domain.repositories import IsStudentRepo, IsDepartmentRepo, IsCourseRepo
from src.application.dtos.student_dto import *
from src.utils.exceptions import ValidationError
from src.domain.entities.student import Student
from src.utils.validators import validate_upload_student_request, validate_id

class StudentManagement:
    def __init__(self, student_repo: IsStudentRepo, course_repo: IsCourseRepo, department_repo: IsDepartmentRepo):
        self.student_repo = student_repo
        self.department_repo = department_repo
        self.course_repo = course_repo

    def upload(self, req: UploadStudentRequest) -> UploadStudentResponse:
        errors = validate_upload_student_request(
            id = req.id,
            name = req.name,
            email = req.email,
            birthday = req.birthday,
            sex = req.sex,
            department_id=req.department_id
        )
        if errors:
            raise ValidationError("INVALID_INPUT", detail=errors)
        try:
            student_entity = Student.add(
                id = req.id,
                name = req.name,
                email = req.email,
                birthday = req.birthday,
                sex = req.sex,
                department_id=req.department_id
            )
            student_save = self.student_repo.save(student_entity)
        except Exception as e:
            raise ValidationError("DB_ERROR", detail=str(e))
        
        student_out = studentOut.from_entity(student_save)
        
        return UploadStudentResponse(
            success=True,
            message="Student uploaded successfully",
            student=student_out
        )
        
    def get_filter_options(self, columns: List[str]):
        departments = []
        courses = []

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

        return StudentFilterOption(
            departments=departments,
            courses=courses
        )
    
    def get_detail_students(self, req: StudentDetailRequest) -> List[StudentDetailResponse]:
        list_student = self.student_repo.get_list_detail_student(req.columns,req.department_id,req.course_id)
        return [StudentDetailResponse(
            student_id=student.student_id,
            student_name=student.student_name,
            email=student.email,
            birthday=f"student.birthday",
            departments=student.department_name,
            courses=student.course_name
        ) for student in list_student]
        
    def get_by_id(self, student_id: str) -> Student:
        if not validate_id(student_id):
            raise ValidationError("INVALID_INPUT", detail="student_id format is invalid")
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValidationError("NOT_FOUND",detail=f"student {student_id} not found")
        return student

    def view(self, student_id: str) -> GetStudentResponse:   
        student_entity = self.get_by_id(student_id)
        student_out = studentOut.from_entity(student_entity)
        return GetStudentResponse(
            success=True,
            message="Student retrieved successfully",
            student=student_out
        )
        
    