from docx import Document

def get_prompt():
    """
    อ่านpromptจาก M1.docx แล้วนำค่ากลับมาใช้วนระบบกับผู้ใช้
    """
    try:
        doc = Document("M1.docx")
        prompt = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return prompt
    except Exception as e:
        return f"Error reading M1.docx: {e}"

