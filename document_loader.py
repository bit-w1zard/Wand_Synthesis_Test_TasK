import os
from pathlib import Path
from utils import sentence_split
from typing import List
from docx import Document

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

"""
Helper functions for loading different Doc Types
"""

def load_text_from_pdf(file_path: str) -> str:
    """
    Args: file_path (Path of the Input Document File)
    """
    if pdfplumber is None:
        raise ImportError("Module not found: pip install pdfplumber to parse PDFs")
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def load_text_from_txt(file_path: str) -> str:
    """
    Args: file_path (Path of the Input Document File)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_text_from_docx(file_path: str) -> str:
    """
    Args: file_path (Path of the Input Document File)
    """
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

def load_document(file_path: str) -> str:
    """
    Function to Detect and Standardize Documents to Plain Text
    Args: file_path (Path of the Input Document File)
    """
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return load_text_from_pdf(file_path)
    elif ext == ".txt":
        return load_text_from_txt(file_path)
    elif ext == ".docx":
        return load_text_from_docx(file_path)
    else:
        raise ValueError(f"Unidentified file type: {ext}")

def extract_claims_from_file(file_path: str) -> List[str]:
    """
    Pipeline: read → split → return claim list
    Args: file_path (Path of the Input Document File)
    """
    raw_text = load_document(file_path)
    return sentence_split(raw_text)

