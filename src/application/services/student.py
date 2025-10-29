from src.domain.repositories import IsStudentRepo, IsDepartmentRepo, IsCourseRepo
from src.application.dtos.student_dto import *
from sqlalchemy.exc import IntegrityError
from src.utils.exceptions import ValidationError
from src.domain.entities import StudentDetail, Student
from src.utils.validators import validate_upload_student_request, validate_id

class StudentManagement:
    def __init__(self, student_repo: IsStudentRepo, course_repo: IsCourseRepo, department_repo: IsDepartmentRepo):
        self.student_repo = student_repo
        self.department_repo = department_repo
        self.course_repo = course_repo

    def upload(self, req: UploadStudentRequest) -> StudentResponse:
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
            if not student_save:
                raise ValidationError("ALREADY_EXISTS")
        except Exception as e:
            raise ValidationError("DB_ERROR", detail=str(e))
        
        student_out = studentOut.from_entity(student_save)
        
        return StudentResponse(
            success=True,
            message="Thêm Sinh viên thành công",
            student=student_out
        )
    
    def update(self, req: UploadStudentRequest) -> StudentResponse:
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
            student_save = self.student_repo.update(student_entity)
            if not student_save:
                raise ValidationError("ALREADY_EXISTS", detail="Student đã tồn tại")
        except Exception as e:
            raise ValidationError("DB_ERROR", detail=str(e))
        
        student_out = studentOut.from_entity(student_save)
        
        return StudentResponse(
            success=True,
            message="Chỉnh sửa Sinh viên thành công",
            student=student_out
        )
    
    def delete_student(self, student_id: str) -> Student:
        if not validate_id(student_id):
            raise ValidationError("INVALID_INPUT", detail="Định dạng student_id không hợp lệ")

        try:
            deleted_student_entity = self.student_repo.deleted(student_id)
            
            if deleted_student_entity is None:
                raise f"Không tìm thấy sinh viên với ID: {student_id}"
            
            student_out_dto = studentOut.from_entity(deleted_student_entity) 

            return StudentResponse(
                success=True,
                message=f"Đã xóa thành công sinh viên ID: {student_id}",
                student=student_out_dto
            )
        except Exception as e:
            raise e
              
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
    
    def get_detail_students(self, req: StudentDetailRequest) -> List[studentOut]:
        list_student = self.student_repo.get_list_detail_student(req.columns,req.department_id,req.course_id)
        return [studentOut.from_entity(student) for student in list_student]
        
    def get_by_id(self, student_id: str) -> StudentDetail:
        if not validate_id(student_id):
            raise ValidationError("INVALID_INPUT", detail="student_id format is invalid")
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValidationError("NOT_FOUND",detail=f"student {student_id} not found")
        return student

    def view(self, student_id: str) -> StudentResponse:   
        student_entity = self.get_by_id(student_id)
        student_out = studentOut.from_entity(student_entity)
        return StudentResponse(
            success=True,
            message="Đã tìm thấy Sinh viên",
            student=student_out
        )
        
    