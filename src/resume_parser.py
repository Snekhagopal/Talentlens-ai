"""Extract plain text from PDF, DOCX and TXT resumes."""
import io
from pathlib import Path

from docx import Document
from pypdf import PdfReader

from src.config import SUPPORTED_EXTENSIONS


class UnsupportedFileError(ValueError):
    pass


def extract_text_from_pdf(data: bytes) -> str:
    reader = PdfReader(io.BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_text_from_docx(data: bytes) -> str:
    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text(data: bytes, filename: str) -> str:
    """Return cleaned text from a resume file's bytes, dispatching on extension."""
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileError(f"Unsupported file type: {ext or '(none)'}")

    if ext == ".pdf":
        text = extract_text_from_pdf(data)
    elif ext == ".docx":
        text = extract_text_from_docx(data)
    else:
        text = data.decode("utf-8", errors="ignore")

    return clean_text(text)


def clean_text(text: str) -> str:
    lines = (line.strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)
