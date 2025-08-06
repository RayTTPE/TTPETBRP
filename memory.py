from docx import Document

def get_prompt():
    """
    Reads system prompt from M1.docx for backup Memory.
    """
    try:
        doc = Document("M1.docx")
        prompt = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return prompt
    except Exception as e:
        return f"Error reading M1.docx: {e}"

