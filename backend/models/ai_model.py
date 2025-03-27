from transformers import pipeline

# Load AI model (BERT-based scoring)
resume_scoring_model = pipeline("text-classification", model="bert-base-uncased")

def analyze_resume_text(text):
    """Analyze resume text using AI model and return ATS score."""
    score = resume_scoring_model(text[:512])  # Use only first 512 tokens
    ats_score = min(100, int(score[0]["score"] * 100))
    return ats_score
