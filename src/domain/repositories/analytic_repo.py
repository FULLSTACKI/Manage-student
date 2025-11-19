from abc import ABC, abstractmethod
from typing import List
# from src.application.dtos.analytic_view_dto import AnalyticsResponse

class IsAnalyticRepo(ABC):
    @abstractmethod
    def analytic(self, dimensions: str, metrics: str, agg: str) -> List[dict]:
        pass