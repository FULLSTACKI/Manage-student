from src.domain.repositories import IsStudentCommandRepo
from src.application.dtos.student_command_dto import *
from src.domain.entities import  Student
from src.infrastructure.persistence.read import CoverLetterProcessor
from src.utils.validators import validate_sex
from src.utils.exceptions import ValidationError
from fastapi import UploadFile
from src.config import DOCX_CONFIG
from typing import List
import shortuuid
import traceback

class StudentImportFileManagement:
    def __init__(self, student_repo: IsStudentCommandRepo):
        self.student_repo = student_repo
        self.pattern = DOCX_CONFIG
        
    async def import_students_from_docx(self, files: List[UploadFile]) -> StudentCommandResponse:
        if not self.pattern: 
            raise ValueError("Lỗi cấu hình: Không mở được file json")
        
        list_file_docx = [file for file in files if file.filename and file.filename.lower().endswith(".docx")]
        
        try:
            coverLetter = CoverLetterProcessor(files=list_file_docx, pattern=self.pattern)

            list_text = await coverLetter.save_info() 
            
            if not list_text:
                raise ValueError("Không trích xuất được văn bản nào từ file.")

            students_entity = []
            errors = []
            
            for index, row in list_text:
                try:
                    new_id = f"S{shortuuid.uuid()[:8].upper()}"
                    new_email = f"{new_id}@gmail.com" 
                    dept_id = row.get("department_id", "D001")

                    entity = Student.add(
                        name=row.get("student_name"),
                        email=new_email,
                        birthday=row.get("birthday"),
                        sex=row.get("sex") if validate_sex(row.get("sex")) else "M",
                        birthplace = row.get("birthplace"),
                        address = row.get("address"),
                        phone = row.get("phone"),
                        ethnicity = row.get("ethnicity"),
                        religion = row.get("religion"),
                        id_card = row.get("id_card"),
                        issue_date = row.get("issue_date"),
                        issue_place = row.get("issue_place"),
                        department_id=dept_id
                    )
                    students_entity.append(entity)
                except ValidationError as e:
                    error_detail = {
                        "row_index": index + 1,  # Dòng thứ mấy trong file
                        "student_name": row.get("student_name", "Unknown"),
                        "reason": str(e) # Lỗi gì (ví dụ: AGE_INVALID)
                    }
                    errors.append(error_detail)
            
            list_student_saved = []
            for student_ent in students_entity:
                student_save = self.student_repo.save(student_ent)
                list_student_saved.append(student_save)
                
            return StudentCommandResponse(
                success=True,
                message=f"Thêm {len(list_student_saved)} Sinh viên thành công."
            )
        except Exception as e: 
            print("❌ LỖI TRONG import_students_from_docx ❌")
            traceback.print_exc()
            raise e