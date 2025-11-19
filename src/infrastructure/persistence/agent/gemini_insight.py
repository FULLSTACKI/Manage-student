from src.config.settings import GEMINI_KEY
import google.generativeai as genai
from src.domain.repositories.gemini_repo import IsInsightService
from src.config.settings import DATA_DIR
import traceback
import json

class GeminiInsightService(IsInsightService):
    def __init__(self):
        self.api_key = GEMINI_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash") 
    
    async def generate_insight_from_data_analytic(self, data_analytic: list[dict]) -> str:
        try:
            prompt = f"""
                Phân tích biểu đồ này như một nhà phân tích dữ liệu cho hệ thống quản lý sinh viên.
                Đưa ra 3 gạch đầu dòng nhận xét chính (insights) mà biểu đồ này thể hiện.
                Viết ngắn gọn, tối đa 100 từ.
                Dữ liệu:
                {data_analytic}
            """
            response = self.model.generate_content(prompt)
            bot_response = response.text.replace("*", "")
            return bot_response
        except Exception as e:
            print(f"Lỗi: {traceback.print_exc()}")
            raise ValueError(f"Lỗi: Không thể tạo nhận xét ({e})")
    
    # def save_insight(self, history=None):
    #     with open(file=DATA_DIR/"insight_history.json", mode="w", encoding="utf-8") as f:
    #         json.dump(history,ensure_ascii=False)