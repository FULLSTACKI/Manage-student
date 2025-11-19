from src.domain.repositories import IsAnalyticRepo, IsChartService, IsInsightService, IsExportFile
from src.application.dtos import *
from src.utils import ValidationError, HTTPException
import asyncio
from typing import *

class AnalyticManagement:
    def __init__(self, analytic_repo: IsAnalyticRepo, chart_service: IsChartService, insight_service: IsInsightService, export_service: dict[str,IsExportFile]):
        self.analytic_repo = analytic_repo
        self.chart_service = chart_service
        self.insight_service = insight_service
        self.export_service = export_service
        
    def get_analytic(self, dimension: str, metric: str, agg: str) -> list[dict]:
        try:
            query = self.analytic_repo.analytic(dimension, metric, agg)
            if not query:
                raise HTTPException(status_code=404, detail="No data found for the given parameters.")
            return query
        except ValidationError as e:
            raise e
        except Exception as e:
            raise e
        
    async def plot_chart(self,data: list[dict], chart_type: str, x_col: str, y_col: str) -> Tuple[str, str]:
        try:
            chart_path, chart_name = await self.chart_service.plot_chart(data, chart_type, x_col, y_col)
            if not (chart_path or chart_name):
                raise ValueError(f"Tác vụ vẽ lỗi!")
            return chart_path, chart_name
        except Exception as e:
            raise e
        
    async def generate_insight(self, data: list[dict]) -> str:
        try:
            response = await self.insight_service.generate_insight_from_data_analytic(data)
            if not response:
                raise ValueError("Tác vụ nhận xét lỗi!")
            return response
        except Exception as e:
            raise e
        
    async def export_file(self, req: ReportDTO):
        try:
            # ---------------------------------------------------------
            # BƯỚC 1: Lấy dữ liệu nền (Tuần tự)
            # ---------------------------------------------------------
            data = self.get_analytic(req.dimension, req.metric, req.agg)
            if not data:
                raise ValueError("Lỗi phân tích dữ liệu!")

            # ---------------------------------------------------------
            # BƯỚC 2 & 3: Chạy SONG SONG (Parallel) - Chart & Insight
            # Đây chính là "Parallel Gateway" trong BPMN
            # ---------------------------------------------------------
            
            # Định nghĩa 2 task nhưng chưa await lẻ tẻ
            task_plot = self.plot_chart(data, req.chart_type, x_col=req.dimension, y_col=req.metric)
            task_insight = self.generate_insight(data)

            # Dùng asyncio.gather để chạy cả 2 cùng lúc và đợi kết quả
            results = await asyncio.gather(task_plot, task_insight)

            # Giải nén kết quả (Unpack) theo thứ tự đã đưa vào gather
            (chart_path, chart_name) = results[0] # Kết quả của task_plot
            insight_response = results[1]         # Kết quả của task_insight

            # ---------------------------------------------------------
            # BƯỚC 4: Export File (Gộp luồng - Merge Gateway)
            # ---------------------------------------------------------
            req_report= {
                "data_table": data,
                "chart_path": chart_path,
                "response": insight_response
            }
            
            # Chọn Strategy Export phù hợp
            export_worker = self.export_service.get(req.type)
            if not export_worker:
                raise ValueError(f"Loại file '{req.type}' không được hỗ trợ.")

            # Thực thi export
            content_type = export_worker.get_content_type(req.type)
            file_bytes = export_worker.export(reports=req_report) # req giờ đã đủ data, chart, insight
            
            file_name_full = f"Report.{req.type}" # Format lại tên file cho chuẩn
            
            return file_bytes, content_type, file_name_full

        except Exception as e:
            # Log lỗi ở đây nếu cần
            raise e