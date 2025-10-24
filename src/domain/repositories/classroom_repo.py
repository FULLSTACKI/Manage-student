from abc import ABC, abstractmethod
from src.domain.entities import Classroom
from typing import List

class IsClassroomRepo(ABC):
    @abstractmethod
    def get_by_id(self, classroom_id: str) -> Classroom:
        pass 
    
    @abstractmethod
    def get_all(self) -> List[Classroom]:
        pass 
    
    @abstractmethod
    def save(self, teacher_id: str) -> Classroom:
        pass
     