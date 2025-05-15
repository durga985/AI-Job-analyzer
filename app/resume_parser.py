import os
import pdfplumber
import docx

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {e}")

def extract_text_from_docx(file_path):
    """
    Extracts text from a DOCX file using python-docx.
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to read DOCX: {e}")

def extract_text(file_path):
    """
    Detects the file type based on extension and extracts text accordingly.
    Supports PDF, DOCX, and TXT formats.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"Failed to read TXT: {e}")
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported types are PDF, DOCX, and TXT.")
