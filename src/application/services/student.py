from src.domain.repositories import IsStudentRepo, IsDepartmentRepo, IsCourseRepo
from src.application.dtos.student_dto import *
from src.utils.exceptions import ValidationError
from src.domain.entities import  Student, CoverLetterProcessor
from src.utils.validators import validate_upload_student_request, validate_id, validate_sex
from fastapi import UploadFile
import shortuuid
import traceback

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
        
        return StudentResponse(
            success=True,
            message="Chỉnh sửa Sinh viên thành công",
            student=student_out
        )
    
    def delete(self, student_id: str) -> Student:
        if not validate_id(student_id):
            raise ValidationError("INVALID_INPUT", detail="Định dạng student_id không hợp lệ")

        try:
            student_out = self.student_repo.deleted(student_id)
            
            if student_out is None:
                raise f"Không tìm thấy sinh viên với ID: {student_id}"

            return StudentResponse(
                success=True,
                message=f"Đã xóa thành công sinh viên ID: {student_id}",
                student=student_out
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
        return [student for student in list_student]
        
    def get_by_id(self, student_id: str) -> studentOut:
        if not validate_id(student_id):
            raise ValidationError("INVALID_INPUT", detail="student_id format is invalid")
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValidationError("NOT_FOUND",detail=f"student {student_id} not found")
        return StudentResponse(
            success=True,
            message="Đã tìm thấy Sinh viên",
            student=student
        )
        
    async def import_students_from_docx(self, files: List[UploadFile], pattern: dict = None) -> List[StudentResponse]:
        if not pattern: 
            raise ValueError("Lỗi cấu hình: Không mở được file json")
        
        list_file_docx = [file for file in files if file.filename and file.filename.lower().endswith(".docx")]
        
        try:
            coverLetter = CoverLetterProcessor(files=list_file_docx, pattern=pattern)

            list_text = await coverLetter.save_info() 
            
            if not list_text:
                raise ValueError("Không trích xuất được văn bản nào từ file.")

            students_entity = [] 
            
            for text in list_text:
                new_id = f"S{shortuuid.uuid()[:8].upper()}"
                new_email = f"{new_id}@gmail.com" 
                dept_id = text.get("department_id", "D001")

                entity = Student.add(
                    id=new_id,
                    name=text.get("student_name"),
                    email=new_email,
                    birthday=text.get("birthday"),
                    sex=text.get("sex") if validate_sex(text.get("sex")) else "M",
                    birthplace = text.get("birthplace"),
                    address = text.get("address"),
                    phone = text.get("phone"),
                    ethnicity = text.get("ethnicity"),
                    religion = text.get("religion"),
                    id_card = text.get("id_card"),
                    issue_date = text.get("issue_date"),
                    issue_place = text.get("issue_place"),
                    department_id=dept_id
                )
                students_entity.append(entity)
            
            if not students_entity:
                raise ValueError("Error mapper: Không trích xuất được entity nào")
            
            list_student_saved = []
            for student_ent in students_entity:
                student_save = self.student_repo.save(student_ent)
                list_student_saved.append(student_save)
                
            return ListStudentFileResponse(
                success=True,
                message=f"Thêm {len(list_student_saved)} Sinh viên thành công.",
                student=list_student_saved
            )
        except Exception as e: 
            print("❌ LỖI TRONG import_students_from_docx ❌")
            traceback.print_exc()
            raise e
        
        