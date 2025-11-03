from pydantic import BaseModel
from typing import *
# from src.domain.entities import StudentDetail

class studentOut(BaseModel):
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[str] = None
    birthday: Optional[str] = None
    sex: Optional[str] = None 
    departments: Optional[str] = None
    courses: Optional[str] = None
    birthplace: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    ethnicity: Optional[str] = None
    religion: Optional[str] = None
    id_card: Optional[str] = None
    issue_date: Optional[str] = None
    issue_place: Optional[str] = None
    

# ======================================
# 🧩 DTO dùng khi upload thêm sinh viên
# ======================================
class UploadStudentRequest(BaseModel):
    id: str
    name: str
    email: str
    birthday: str
    age: Optional[str] = None
    sex: str
    department_id: str
    birthplace: Optional[str] 
    address: Optional[str] 
    phone: Optional[str] 
    ethnicity: Optional[str] 
    religion: Optional[str] 
    id_card: Optional[str] 
    issue_date: Optional[str] 
    issue_place: Optional[str] 


# =======================================
# 🧩 DTO trả kết quả phản hồi sau khi thêm
# =======================================
class StudentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: Optional[studentOut] = None
    
class ListStudentFileResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: List[Optional[studentOut]] = None


# ===============================
# 🧩 Option (dropdown selections)
# ===============================
class Option(BaseModel):
    id: str
    name: str


# ===========================
# 🧩 Bộ lọc danh sách Student
# ===========================
class StudentFilterOption(BaseModel):
    departments: Optional[List[Option]] = None
    courses: Optional[List[Option]] = None


# ===========================
# 🧩 Yêu cầu lấy chi tiết Student
# ===========================
class StudentDetailRequest(BaseModel):
    columns: List[str]
    department_id: Optional[List[str]] = None
    course_id: Optional[List[str]] = None
    