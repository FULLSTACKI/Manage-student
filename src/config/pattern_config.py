import json
from src.config import PATTERN_DIR
from src.utils import HTTPException
from functools import lru_cache
import os

@lru_cache
def load_pattern(name: str, folder_path=PATTERN_DIR):
    path = folder_path / f"{name}.json"
    if not os.path.exists(path):
        try:
            # Dùng 'w' (write) để tạo file
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default=[]) # Ghi dữ liệu mặc định vào
        except Exception as e:
            print(f"Không thể tạo file: {e}")
    try:
        with open(path,mode="r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # 3. Bắt lỗi cụ thể hơn
        raise HTTPException(status_code=500, detail="Error decoding configuration file.")
    except Exception as e:
        # Bắt các lỗi khác
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
