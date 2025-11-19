from fastapi import HTTPException, status
from src.config import Role

class AuthorizationService:
    def __init__(self):
        pass
    
    def check_permission_role(self, account, allowed_roles,student_id = None):
        if account.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập tài nguyên này"
            )
        if student_id != account.student_id and account.role == Role.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập tài nguyên này"
            )
        return 
    
