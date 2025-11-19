from pydantic import BaseModel
from typing import *
from .student_query_dto import studentOut
from datetime import datetime

class StudentHistoryResp(BaseModel):
    user_email: Optional[str] = None
    action: Optional[str]
    change_at: Optional[datetime]
    detail: Optional[studentOut] = None
    old_val: Optional[str] = None
    new_val: Optional[str] = None