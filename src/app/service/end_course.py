from datetime import date, timedelta

def compute_end_course(start_course: date, duration_weeks: int = 16) -> date:
    try:
        # Mỗi tuần có 7 ngày
        delta = timedelta(weeks=duration_weeks)
        end_course = start_course + delta
        return end_course
    except Exception as e:
        raise ValueError(f"Lỗi tính ngày: {e}")
