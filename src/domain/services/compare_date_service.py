import pandas as pd
from datetime import datetime

def parse_date(date_str: str):
    try:    
        if not date_str or pd.isna(date_str):
            return None
        cleaned_str = date_str.replace("Ngày", "")
        cleaned_str = cleaned_str.replace("tháng", "")
        cleaned_str = cleaned_str.replace("năm", "")
        date_string = "-".join(cleaned_str.strip().split())
        if len(date_string) == 8 and date_string.isdigit():   
            try:
                # Định dạng: %d (ngày) %m (tháng) %Y (năm)
                return datetime.strptime(date_string, "%d%m%Y").date()
            except ValueError:
                # Thử định dạng YYYYMMDD nếu ở trên thất bại
                try:
                    return datetime.strptime(date_string, "%Y%m%d").date()
                except ValueError:
                    pass 

        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(date_string, fmt).date()
            except ValueError:
                continue
        
        print(f"Cảnh báo: Không thể parse ngày: '{date_string}'")
    except (ValueError, TypeError) as e:
        raise e