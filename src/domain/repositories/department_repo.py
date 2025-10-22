from abc import ABC, abstractmethod
from src.domain.entities.department import Department
from src.domain.entities.dtos import *
from typing import List

class IsDepartmentRepo(ABC):
    @abstractmethod
    def get_by_id(self, department_id:str) -> Department | None:
        pass
    @abstractmethod
    def get_all(self) -> List[Department] | None:
        pass
    @abstractmethod
    def save(self, req_department: Department) -> Department | None: 
        pass
    