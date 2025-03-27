import pdfplumber
import docx
import pypandoc

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_rtf(rtf_path):
    """Extract text from an RTF file using Pandoc."""
    return pypandoc.convert_file(rtf_path, "plain")

def extract_text(filepath):
    """Extract text based on file type."""
    file_ext = filepath.rsplit(".", 1)[1].lower()

    if file_ext == "pdf":
        return extract_text_from_pdf(filepath)
    elif file_ext == "docx":
        return extract_text_from_docx(filepath)
    elif file_ext == "rtf":
        return extract_text_from_rtf(filepath)
    else:
        raise ValueError("Unsupported file type. Only PDF, DOCX, and RTF are allowed.")
