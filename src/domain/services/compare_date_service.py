import pandas as pd
from datetime import datetime

def parse_date(date_str: str):
    try:
        if not date_str or pd.isna(date_str):
            return None
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None