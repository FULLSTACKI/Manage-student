from src.domain.repositories.export_file import IsExportFile
import pandas as pd
import os
import io

class ExcelExportFile(IsExportFile):
    def export(self, reports: dict) -> io.BytesIO:
        try:
            df = pd.DataFrame(reports.get("data_table"))
            output_buffer = io.BytesIO()
            with pd.ExcelWriter(output_buffer, engine='xlsxwriter') as writer:
                sheet_name = "overview"
                
                # --- 1. GHI BẢNG DỮ LIỆU (DATA TABLE) ---
                # Ghi DataFrame vào sheet, bắt đầu từ ô A1
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                # Lấy worksheet và workbook để tùy chỉnh
                worksheet = writer.sheets[sheet_name]
                workbook = writer.book
                
                # (Tùy chọn) Thêm định dạng cho tiêu đề
                header_format = workbook.add_format({'bold': True, 'font_size': 12})
                
                
                # --- 2. XÁC ĐỊNH VỊ TRÍ HÀNG TRỐNG TIẾP THEO ---
                # Hàng 0 là Header. Hàng 1 -> len(df) là dữ liệu.
                # Hàng trống tiếp theo là len(df) + 1.
                # Thêm 2 hàng đệm (padding) cho đẹp.
                current_row = len(df) + 3 # Index bắt đầu từ 0
                
                # --- 3. GHI BIỂU ĐỒ (CHART) ---
                chart_path = reports.get("chart_path")
                if chart_path and os.path.exists(chart_path):
                    worksheet.write("H1", "Biểu đồ Phân tích:", header_format)
                    # Chèn ảnh vào hàng bên dưới
                    worksheet.insert_image("H3",chart_path, {"x_scale": 0.5, "y_scale": 0.5})
                    
                # --- 4. GHI NHẬN XÉT (INSIGHT) ---
                insight_text = reports.get("response")
                if insight_text:
                    # (Tùy chọn) Gộp ô để văn bản dài hiển thị đẹp hơn
                    cell_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
                    worksheet.merge_range(f'A{current_row + 1}:F{current_row + 10}', insight_text, cell_format)
            output_buffer.seek(0)
            return output_buffer
        except Exception as e:
            raise e