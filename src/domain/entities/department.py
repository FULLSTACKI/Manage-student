from src.utils.exceptions import ValidationError

class Department:
    def __init__(self, department_id: str, department_name: str):
        self.department_id = department_id
        self.department_name = department_name
        self._validate_domain_invariants()
        
    def _validate_domain_invariants(self):
        # Quy tắc bất biến: student_id và course_id không được rỗng
        if not self.department_id:
            raise ValidationError("NOT_FOUND", detail= f"ID department {self.department_id} không tồn tại")
    
    @classmethod
    def add(cls, department_id, department_name):
        return cls(department_id, department_name)
    
    