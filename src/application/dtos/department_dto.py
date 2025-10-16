from pydantic import BaseModel
from typing import *
from src.domain.entities import Department

#define department data models
class departmentOut(BaseModel):
    id: str
    name: str
    
    def from_entity(department: Department):
        
        return departmentOut(
            id = department.department_id,
            name = department.department_name,
        )
        
class UploadDepartmentRequest(BaseModel):
    id: str
    name: str

class UploadDepartmentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    department: Optional[departmentOut] = None
    
class GetDepartmentRequest(BaseModel):
    id: str

class GetDepartmentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    department: Optional[departmentOut] = None