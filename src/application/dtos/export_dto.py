from pydantic import BaseModel
from typing import *

class ReportDTO(BaseModel):
    dimension: Optional[str]
    metric: Optional[str]
    agg: Optional[str]
    chart_type: Optional[str]
    type: str