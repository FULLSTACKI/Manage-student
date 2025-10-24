from abc import ABC, abstractmethod
from src.domain.entities.course import Course
from typing import List

class IsCourseRepo(ABC):
    @abstractmethod
    def get_by_id(self, course_id:str) -> Course | None:
        pass
    @abstractmethod
    def get_filter_all(self) -> List[Course] | None:
        pass
    @abstractmethod
    def save(self, req_course: Course): 
        pass