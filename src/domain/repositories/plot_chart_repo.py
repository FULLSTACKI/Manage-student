from abc import ABC, abstractmethod

class IsChartService(ABC):
    @abstractmethod
    def plot_chart(self, data, chart_type, x_col, y_col) -> tuple[str, str]:
        pass
    @abstractmethod
    def remove_chart(self, chart_path):
        pass