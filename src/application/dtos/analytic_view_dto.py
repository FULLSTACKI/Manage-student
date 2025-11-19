from pydantic import BaseModel
from typing import *

# # Analytics View 
# class DimensionDTO(BaseModel):
#     key: str
#     display: str
#     valid_metrics: List[str]
    
# class MetricDTO(BaseModel):
#     key: str
#     display: str
#     allowed_agg: List[str]
    
# class AnalyticsViewDTO(BaseModel):
#     display_name: str
#     dimensions: List[DimensionDTO]
#     metrics: List[MetricDTO]

# Analytics request
class AnalyticsRequest(BaseModel):
    dimension: Optional[str] = None
    metric: Optional[str] = None
    agg: Optional[str] = None
    
# class AnalyticsResponse(BaseModel):
#     column_categorical: Optional[str]
#     column_numerical: Optional[float]