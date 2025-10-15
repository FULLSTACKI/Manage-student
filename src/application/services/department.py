from src.domain.entities.department.department import Department
from src.domain.entities.department.department_repo import IsDepartmentRepo
from src.models.schemas import UploadDepartmentRequest, UploadDepartmentResponse, departmentOut, GetDepartmentRequest, GetDepartmentResponse
from src.utils.validators import validate_id, validate_name
from src.utils.error.exceptions import ValidationError
from typing import *

class DepartmentManagement:
    def __init__(self, Department_repo: IsDepartmentRepo):
        self.Department_repo = Department_repo
        
        self._analytics_map: Dict[Tuple[str, str, str], Callable[[], List[Dict]]] = {
            ('department', 'course', 'count'): self.Department_repo.get_total_course_by_department,
            ('department', 'student', 'count'): self.Department_repo.get_total_student_by_department,
            ('department', 'sex', 'count'): self.Department_repo.get_total_student_sex_by_department,
            ('department', 'gpa','avg'): self.Department_repo.get_avg_gpa_by_department,
            ('department', 'gpa','min'): self.Department_repo.get_min_gpa_by_department,
            ('department', 'gpa','max'): self.Department_repo.get_max_gpa_by_department,
            ('department', 'final grade','avg'): self.Department_repo.get_avg_final_grade_by_department,
            ('department', 'final grade','min'): self.Department_repo.get_min_final_grade_by_department,
            ('department', 'final grade','max'): self.Department_repo.get_max_final_grade_by_department,
        }
        
    def upload(self, req: UploadDepartmentRequest) -> UploadDepartmentResponse:
        if not validate_id(req.id):
            raise ValidationError("INVALID_INPUT", detail=f"mã khoa {req.id} không hợp lệ")
        if not validate_name(req.name):
            raise ValidationError("INVALID_INPUT", detail=f"Tên khoa {req.name} không hợp lệ")
        try:
            Department_entity = Department.add(
                department_id=req.id,
                department_name=req.name,
            )
            
            Department_save = self.Department_repo.save(Department_entity)
        except Exception as e:
            # convert to app-level DB error
            raise ValidationError("DB_ERROR", detail=str(e))
    
        Department_out = departmentOut.from_entity(Department_save)
     
        return UploadDepartmentResponse(
            success=True,
            message="Department uploaded successfully",
            Department=Department_out
        )
        
    def get_by_id(self, Department_id: str) -> Department:
        if not validate_id(Department_id):
            raise ValidationError("INVALID_INPUT", detail="Department_id format is invalid")
        Department = self.Department_repo.get_by_id(Department_id)
        if not Department:
            raise ValidationError("NOT_FOUND",detail=f"Department {Department_id} not found")
        return Department
    
    def get_all(self) -> List[Department]:
        list_department = self.Department_repo.get_all()
        return list_department
    

    def view(self, req: GetDepartmentRequest) -> GetDepartmentResponse:
        Department_entity = self.get_by_id(req.id)
        Department_out = departmentOut.from_entity(Department_entity)
        return GetDepartmentResponse(
            success=True,
            message="Department retrieved successfully",
            Department=Department_out
        )