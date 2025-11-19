from abc import ABC, abstractmethod
from src.config.settings import CONTENT_TYPE_CONFIG

class IsExportFile(ABC):
    def get_content_type(self, type: str) -> str:
        return CONTENT_TYPE_CONFIG.get(type)
    @abstractmethod
    def export(self, reports: dict):
        pass