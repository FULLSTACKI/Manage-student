from sqlalchemy.orm import Session
from src.infrastructure.persistence.models import DepartmentModel
from src.domain.repositories import IsDepartmentRepo
from src.domain.entities import Department
from sqlalchemy.exc import IntegrityError
from typing import *
from sqlalchemy import text

def _to_model(entity: Department) -> DepartmentModel:
    return DepartmentModel(
        department_id = entity.department_id,
        department_name = entity.department_name
    )
    
def _to_entity(model: DepartmentModel) -> Department:
    return Department(
        department_id = model.department_id,
        department_name = model.department_name
    )

class DepartmentRepo(IsDepartmentRepo):
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def get_filter_all(self) -> List[Department]:
        try:
            query = text("SELECT * FROM departments")
            result = self.db.execute(query)
            department_row = result.mappings().all()
            list_department = [Department(**data) for data in department_row]
            return list_department
        except Exception as e:
            raise  e
    
    def get_by_id(self, Department_id: str) -> Department:
        data = self.db.query(DepartmentModel).filter(DepartmentModel.id == Department_id).first()
        if data:
            return _to_entity(data)
        return None

    def save(self, req_Department: Department) -> Department:
        existing = self.get_by_id(req_Department.id)
        
        save_Department = None 
        
        if existing:
            existing.department_name = req_Department.department_name
            save_Department = _to_model(existing)
        else: 
            save_Department = _to_model(req_Department)
            self.db.add(save_Department)
        try:
            self.db.commit()
            self.db.refresh(save_Department)
            return _to_entity(save_Department)
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
        
        