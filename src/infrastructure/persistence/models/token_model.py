from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime, timedelta
from src.infrastructure.persistence.db import Base

class SessionTokenModel(Base):
    __tablename__ = "session_tokens"

    token = Column(String, primary_key=True, unique=True, index=True)
    username = Column(String, ForeignKey("accounts.username"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False)

