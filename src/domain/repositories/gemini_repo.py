from abc import ABC, abstractmethod

class IsInsightService(ABC):
    @abstractmethod
    def generate_insight_from_data_analytic(self, chart_path, chart_name) -> str:
        pass