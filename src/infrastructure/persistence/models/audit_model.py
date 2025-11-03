from sqlalchemy import Column, Integer, String, DateTime, JSON
from src.infrastructure.persistence.db import Base

class AuditBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String, nullable=False)         # UPDATE | DELETE
    changed_at = Column(DateTime, nullable=False)
    old_val = Column(JSON, nullable=True)
    new_val = Column(JSON, nullable=True)
    
    