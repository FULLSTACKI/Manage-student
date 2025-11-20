from sqlalchemy.orm import Session
from src.domain.repositories import IsAnalyticRepo
from src.infrastructure.persistence.mappers.analytic_mapper import AnalyticMapper
from src.infrastructure.persistence.auto.build_query import BuildQueryModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from typing import List

class AnalyticRepo(IsAnalyticRepo):
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def analytic(self, dimensions: str, metrics: str, agg: str) -> List[dict]:
        try:
            dimension = AnalyticMapper.map_dimension(dimensions)
            metric  = AnalyticMapper.map_metric(metrics)
            agg = AnalyticMapper.map_agg(agg)
            metric_val = getattr(func, agg)(metric)
            stmt = (
                select(
                    dimension.label(dimensions),
                    metric_val.label(metrics)
                )
            )
            stmt = BuildQueryModel.apply_joins(stmt, dimension, metric)
            stmt = (
                stmt
                .group_by(dimension)
                .order_by(metric_val.desc())
            )
            result_query = self.db.execute(stmt).mappings().all()
            return result_query
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise e