from src.domain.repositories import IsStudentCommandRepo
from ..dtos.student_command_dto import *
from src.domain.entities import  Student, CoverLetterProcessor
from src.utils.validators import validate_sex
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
            
            for text in list_text:
                new_id = f"S{shortuuid.uuid()[:8].upper()}"
                new_email = f"{new_id}@gmail.com" 
                dept_id = text.get("department_id", "D001")

                entity = Student.add(
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
                
            return StudentCommandResponse(
                success=True,
                message=f"Thêm {len(list_student_saved)} Sinh viên thành công."
            )
        except Exception as e: 
            print("❌ LỖI TRONG import_students_from_docx ❌")
            traceback.print_exc()
            raise e