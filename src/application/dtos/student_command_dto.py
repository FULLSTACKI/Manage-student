from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    birthday: str 
    age: Optional[str] = None
    sex: str
    department_id: str
    birthplace: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    ethnicity: Optional[str] = None
    religion: Optional[str] = None
    id_card: Optional[str] = None
    issue_date: Optional[str] = None
    issue_place: Optional[str] = None

# --- 2. DTO cho việc Tạo (Create) ---
class CreateStudentRequest(StudentBase):
    pass

# --- 3. DTO cho việc Cập nhật (Update) ---
class UpdateStudentRequest(StudentBase):
    pass

class StudentCommandResponse(BaseModel):
    success: bool
    message: Optional[str] = None