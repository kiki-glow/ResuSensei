from fastapi import APIRouter, File, UploadFile, HTTPException
import joblib
import pdfplumber
import docx
import os
import tempfile
import tika
from app.models.gpt_feedback import generate_feedback

router = APIRouter()

model = joblib.load("app/models/resume_model/model.pkl")
vectorizer = joblib.load("app/models/resume_model/vectorizer.pkl")

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".rtf"}

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()]).strip()

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def extract_text_from_rtf(rtf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".rtf") as temp_rtf:
        temp_rtf.write(rtf_file.read())
        temp_rtf_path = temp_rtf.name
    text = tika.process(temp_rtf_path, extension="rtf").decode("utf-8")
    os.remove(temp_rtf_path)
    return text.strip()

@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, and RTF are supported.")

    # Extract text based on file type
    if file_ext == ".pdf":
        text = extract_text_from_pdf(file.file)
    elif file_ext == ".docx":
        text = extract_text_from_docx(file.file)
    elif file_ext == ".rtf":
        text = extract_text_from_rtf(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    if not text:
        raise HTTPException(status_code=400, detail="Unable to extract text from the file.")

    text_vectorized = vectorizer.transform([text])
    score = model.predict(text_vectorized)[0]

    feedback = generate_feedback(text)

    return {"score": score, "feedback": feedback}
