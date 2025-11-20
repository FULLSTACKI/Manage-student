import re 
from docx import Document 
import io

class CoverLetterProcessor:
    def __init__(self, files, pattern): 
        self.pattern = pattern
        self.files = files
        
    # đọc file docx
    async def read_file_docx(self, file):
        try:
            file_content = await file.read()
            
            file_stream = io.BytesIO(file_content)
            
            doc = Document(file_stream)
            
            return '\n'.join(para.text for para in doc.paragraphs)
        except FileNotFoundError as e:
            raise e
        
    # trích xuất dữ liệu từ file docx
    def extract_info(self, text):
        info = {}
        for key,val in self.pattern.items():
            match = re.search(val, text, re.MULTILINE)
            if match:
                info[key] = match.group(1).strip()
        return info 
    
    # lưu dữ liệu vào sheet 
    async def save_info(self):
        list_text = []
        for file in self.files:
            docx = await self.read_file_docx(file)
            text = self.extract_info(docx)
            list_text.append(text)
        return list_text