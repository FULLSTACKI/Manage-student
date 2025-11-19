from src.domain.repositories import IsStudentCommandRepo
from ..dtos.student_command_dto import *
from src.utils.exceptions import ValidationError
from src.domain.entities import  Student
from src.utils.validators import validate_upload_student_request, validate_id

class StudentCommandManagement:
    def __init__(self, student_repo: IsStudentCommandRepo):
        self.student_repo = student_repo

    def upload(self, req: CreateStudentRequest) -> StudentCommandResponse:
        errors = validate_upload_student_request(
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
                birthplace = req.birthplace,
                address = req.address,
                phone = req.phone,
                ethnicity = req.ethnicity,
                religion = req.religion,
                id_card = req.id_card,
                issue_date = req.issue_date,
                issue_place = req.issue_place,
                department_id=req.department_id
            )
            student_out = self.student_repo.save(student_entity)
            if not student_out:
                raise ValidationError("ALREADY_EXISTS")
        except Exception as e:
            raise ValidationError("DB_ERROR", detail=str(e))
        
        return StudentCommandResponse(
            success=True,
            message=f"Thêm thành công Sinh viên ID: {student_out.student_id}"
        )
    
    def update(self, req: UpdateStudentRequest) -> StudentCommandResponse:
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
            student_entity = Student.update(
                id = req.id,
                name = req.name,
                email = req.email,
                birthday = req.birthday,
                sex = req.sex,
                birthplace = req.birthplace,
                address = req.address,
                phone = req.phone,
                ethnicity = req.ethnicity,
                religion = req.religion,
                id_card = req.id_card,
                issue_date = req.issue_date,
                issue_place = req.issue_place,
                department_id=req.department_id
            )
            student_out = self.student_repo.update(student_entity)
            if not student_out:
                raise ValidationError("ALREADY_EXISTS", detail="Student đã tồn tại")
        except Exception as e:
            raise ValidationError("DB_ERROR", detail=str(e))
        
        return StudentCommandResponse(
            success=True,
            message=f"Chỉnh sửa thành công Sinh viên ID: {student_out.student_id}"
        )
    
    def delete(self, student_id: str) -> StudentCommandResponse:
        if not validate_id(student_id):
            raise ValidationError("INVALID_INPUT", detail="Định dạng student_id không hợp lệ")

        try:
            student_out = self.student_repo.deleted(student_id)
            
            if student_out is None:
                raise f"Không tìm thấy sinh viên với ID: {student_id}"
        except Exception as e:
            raise e
        
        return StudentCommandResponse(
            success=True,
            message=f"Đã xóa thành công Sinh viên ID: {student_out}"
        )
              