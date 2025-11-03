import os
from docx import Document 
file_path = "D:/CS_DATA_9/Buoi6/Data/cover_letters/le_van_c.docx"
doc = Document(file_path)
text = [para.text for para in doc.paragraphs]
print(text)