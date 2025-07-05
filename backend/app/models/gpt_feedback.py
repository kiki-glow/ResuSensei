import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_feedback(resume_text):
    prompt = f"""
    Analyze the following resume and provide detailed feedback:
    
    {resume_text}
    
    Provide an ATS score (0-100) and suggest keyword optimizations.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]
