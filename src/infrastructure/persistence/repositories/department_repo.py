from sqlalchemy.orm import Session
from src.infrastructure.persistence.mappers import DepartmentMapper
from src.infrastructure.persistence.models import DepartmentModel
from src.domain.repositories import IsDepartmentRepo
from src.domain.entities import Department
from src.application.dtos import Option
from sqlalchemy.exc import IntegrityError
from typing import *
from sqlalchemy import text

class DepartmentRepo(IsDepartmentRepo):
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def get_filter_all(self) -> List[Department]:
        try:
            query = text("SELECT * FROM departments")
            result = self.db.execute(query)
            department_row = result.mappings().all()
            list_department = [Option(id=data.department_id,name=data.department_name) for data in department_row]
            return list_department
        except Exception as e:
            raise  e
    
    def get_by_id(self, Department_id: str) -> Department:
        data = self.db.query(DepartmentModel).filter(DepartmentModel.id == Department_id).first()
        if data:
            return DepartmentMapper._to_entity(data)
        return None

    def save(self, req_Department: Department) -> Department:
        existing = self.db.query(DepartmentModel).filter(DepartmentModel.department_id == req_Department.department_id).first()
        try:
            if not existing:
                save_department = DepartmentMapper._to_model(req_Department)
                persistent = self.db.merge(save_department)
                self.db.commit()
                self.db.refresh(persistent)
                return req_Department
        except IntegrityError as e:
            errors = str(e)
            self.db.rollback()
            if "UNIQUE constraint failed: Department.name" in errors:
                raise ValueError("Name Department đã tồn tại.")
            else:
                raise ValueError(f"Lỗi lưu trữ dữ liệu: {errors}")
        except Exception as e:
            self.db.rollback()
            raise e
        
        