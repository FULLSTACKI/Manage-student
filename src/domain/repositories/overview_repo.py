from abc import ABC, abstractmethod
from src.domain.entities.dtos import OverviewTopStudent, OverviewKpi

class IsOverviewKpiRepo(ABC):
    @abstractmethod
    def get_all_kpi(self) -> OverviewKpi | None:
        pass
    @abstractmethod
    def get_top3_student(self) -> OverviewTopStudent | None:
        pass