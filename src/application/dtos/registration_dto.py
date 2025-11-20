from pydantic import BaseModel
from typing import Optional

class RegistrationResponse(BaseModel):
    success: bool
    message: Optional[str]