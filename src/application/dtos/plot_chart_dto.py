from pydantic import BaseModel
from typing import Optional, List
# from .analytic_view_dto import AnalyticsResponse

class PlotChartColRequest(BaseModel):
    data: List[dict]
    chart_type: Optional[str]
    x_col: str
    y_col: str