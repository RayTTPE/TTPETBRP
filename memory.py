import docx
import os
from docx import Document
#ใช้ไลบารี่นี้เปิดไฟล์ .docxเสริมความจำของget_prompt

def read_docx_files_from_folder(file_path):
    """
    นี้คือความจำก่อนที่เล้งจะสร้างไบร์ทขึ้นมา
    """
    combined_text = ""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} is not a valid file.")
    
    doc = Document(file_path)  # เปิดไฟล์ .docx
    for paragraph in doc.paragraphs:  # อ่านเนื้อหาในแต่ละย่อหน้า
        combined_text += paragraph.text + "\n"
    return combined_text

def get_prompt():
     """
     คืนค่าข้อความ prompt สำหรับระบบ โดยรวมความจำจากไฟล์ .docx ในโฟลเดอร์
     """
     file_path = "/workspaces/TTPETBRP/M1.docx"

     base_prompt = (
        "เล้งอยากให้ไบร์ทเป็นเพื่อนเเละผู้ช่วยของทุกๆคน\n"
     )

     memory_from_files = read_docx_files_from_folder(file_path)
     return base_prompt + memory_from_files + "\n"
