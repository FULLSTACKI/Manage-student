from abc import ABC, abstractmethod
from src.application.dtos.overview_dto import OverviewKpiResponse, OverviewTopStudent
class IsOverviewKpiRepo(ABC):
    @abstractmethod
    def get_all_kpi(self) -> OverviewKpiResponse | None:
        pass
    @abstractmethod
    def get_top3_student(self) -> OverviewTopStudent | None:
        pass