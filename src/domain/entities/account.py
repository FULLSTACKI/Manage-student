from src.config.settings import Role 
import bcrypt
from ..services.hash import _hash_password

class Account:
    def __init__(self, username: str, password: str, role: Role, student_id: str = None, teacher_id: str = None):
        self.username = username
        self.password = password
        self.role = role
        self.student_id = student_id
        self.teacher_id = teacher_id
    
    @classmethod
    def create(cls, username: str, password: str, role: Role):
        hashed_password = cls._hash_password(password)
        return cls(username=username, password_hash=hashed_password, role=role)

    def verify_password(self, req_pass: str) -> bool:
        return bcrypt.checkpw(
            req_pass.encode('utf-8'), 
            self.password.encode('utf-8')
        )