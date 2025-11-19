from src.domain.repositories.plot_chart_repo import IsChartService
from src.infrastructure.persistence.mappers import ChartMapper
import os
from src.config.paths import CHART_DIR
import pandas as pd 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime 

class SeabornChartService(IsChartService):
    def __init__(self):
        self.save_dir = CHART_DIR
        os.makedirs(self.save_dir, exist_ok=True)
        
    def _get_path_chart(self, chart_name: str):
        return os.path.join(self.save_dir, chart_name)
        
    async def plot_chart(self, data: list[dict], chart_type, x_col, y_col) -> tuple[str, str]:
        if not data: 
            raise ValueError("Lỗi data không tồn tại!")
        df = pd.DataFrame(data)
        fig, ax = plt.subplots(figsize=(20, 10))
        try:
            # 1. Lấy "chiến lược vẽ" từ Mapper
            plot_function = ChartMapper._get_chart_type(chart_type)
            
            if plot_function is None: 
                raise ValueError("Lỗi mapper!")
            
            # 2. Thực thi chiến lược đó
            chart = plot_function(df, x_col, y_col, ax)
            
            # 3. Lưu chart name với datetime
            timestamp = datetime.now().strftime("%Y-%m-%d")
            chart_fig = chart.get_figure()
            chart_name = f"{chart_type}_{x_col}_by_{y_col}_at_{timestamp}.png"
            chart_path = self._get_path_chart(chart_name)
            
            # 4. Tùy chỉnh chung
            ax.set_title(f"{chart_type.upper()}: {y_col.upper()} BY {x_col.upper()}", pad=10)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            if chart_path is None:
                raise ValueError("Join lỗi")
            chart_fig.savefig(chart_path)
            plt.close(fig)
            
            return chart_path, chart_name
        except Exception as e:
            plt.close(fig)
            raise e
        
    def remove_chart(self, chart_path):
        return os.remove(chart_path)