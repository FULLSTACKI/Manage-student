from pydantic import BaseModel
from typing import Optional
from datetime import datetime 

class TokenDTO(BaseModel):  
    access_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    username: Optional[str] = None
    created_at: Optional[datetime] = None