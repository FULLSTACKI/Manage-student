from pydantic import BaseModel
from typing import Optional
from .token_dto import TokenDTO

class AccountLoginRequest(BaseModel):
    username: str
    password: str

class AccountResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    access_token: Optional[str] = None
    role: Optional[str] = None
    student_id: Optional[str] = None