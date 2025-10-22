from src.domain.repositories.student_repo import IsStudentRepo
from src.application.dtos.student_dto import *
from src.utils.exceptions import ValidationError
from src.domain.entities.student import Student 
from src.utils.validators import validate_upload_student_request, validate_id

class StudentManagement:
    def __init__(self, student_repo: IsStudentRepo):
        self.student_repo = student_repo

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
        
    def get_all(self) -> List[studentOut]:
        list_student = self.student_repo.get_all()
        if not list_student:
            raise ValidationError("NOT_FOUND",detail="student not exist")
        try:
            return [studentOut(
                id = student.student_id,
                name = student.student_name,
                email = student.email,
                birthday = f"{student.birthday}",
                age = f"{student.age}",
                sex = student.sex,
                department_id=student.department_id
            )
            for student in list_student]
        except Exception as e:
            raise e
        
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