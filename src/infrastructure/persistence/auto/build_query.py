from src.infrastructure.persistence.db import Base
from src.infrastructure.persistence.models import *

class BuildQueryModel:
    @staticmethod
    def _get_model_from_col(col: str):
        try:
            # Trường hợp 1: Cột thông thường (StudentModel.age)
            if hasattr(col, 'class_'):
                return col.class_
                
            # Trường hợp 2: Cột đã qua hàm aggregate (func.avg(ScoreModel.gpa))
            elif hasattr(col, 'element'):
                # Đào sâu vào biểu thức để tìm bảng gốc
                for child in col.element.get_children():
                    if hasattr(child, 'table'):
                        # Tìm trong registry của SQLAlchemy để lấy Model class từ Table object
                        # (Cần truyền Base model của bạn vào để tra cứu)
                        for mapper in Base.registry.mappers:
                            if mapper.local_table == child.table:
                                return mapper.class_
        except Exception as e:
            raise e
        return None
    
    @staticmethod
    def _path_to_target_model(models: set):
        try: 
            if ScoreModel in models and DepartmentModel in models and not CourseModel in models: 
                models.add(StudentModel)
                models.add(RegistrationModel)
            elif not DepartmentModel in models and CourseModel in models and StudentModel in models: 
                models.add(RegistrationModel)
        except Exception as e: 
            ValueError(f"Lỗi nối đường đi: {e}")
    
    @staticmethod
    def apply_joins(stmt, dimension, metric):
        try: 
            visited_model = []
            needed_model = {
                BuildQueryModel._get_model_from_col(dimension),
                BuildQueryModel._get_model_from_col(metric)
            }
            needed_model.discard(None)
            # Chọn đường đi ngắn nhất cho model cần thiết 
            BuildQueryModel._path_to_target_model(needed_model)
            print(needed_model)
            # chọn base model (ưu tiên StudentModel)
            if StudentModel in needed_model:
                stmt = stmt.select_from(StudentModel)
                visited_model.append(StudentModel)
            elif CourseModel in needed_model: 
                stmt = stmt.select_from(CourseModel)
                visited_model.append(CourseModel)
            # join bảng tự động 
            for item in list(needed_model):
                if item not in visited_model: 
                    stmt = stmt.join(item)
                    visited_model.append(item)
            return stmt
        except Exception as e: 
            raise ValueError(f"Lỗi join tự động: {e}")