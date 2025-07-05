from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pymongo
from werkzeug.utils import secure_filename
from services.extract_text import extract_text  # Import text extraction
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Fetch MongoDB details from .env
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "ResuSenseiDB")

# Initialize MongoDB connection
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["resumes"]

# File upload configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "rtf"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_recommendations(resume_text):
    """Generate AI-driven recommendations based on resume content."""
    recommendations = []

    # **1. Check for Action Verbs**
    action_verbs = ["achieved", "implemented", "managed", "developed", "optimized"]
    if not any(verb in resume_text.lower() for verb in action_verbs):
        recommendations.append("Use strong action verbs (e.g., 'Led', 'Executed', 'Innovated') to describe achievements.")

    # **2. Check for Measurable Achievements**
    if "%" not in resume_text and "$" not in resume_text and "increased" not in resume_text.lower():
        recommendations.append("Include measurable results (e.g., 'Increased sales by 20%', 'Reduced costs by $50K').")

    # **3. Ensure ATS-Friendly Formatting**
    if "•" not in resume_text and "-" not in resume_text:
        recommendations.append("Use bullet points for readability and ATS optimization.")

    # **4. Check for Industry Keywords**
    industry_keywords = ["teamwork", "leadership", "communication", "Python", "data analysis"]
    missing_keywords = [word for word in industry_keywords if word.lower() not in resume_text.lower()]
    if missing_keywords:
        recommendations.append(f"Consider adding relevant industry keywords: {', '.join(missing_keywords[:3])}.")

    # **5. Check Length of Resume**
    word_count = len(resume_text.split())
    if word_count < 200:
        recommendations.append("Your resume might be too short. Ensure you fully describe your skills and experience.")
    elif word_count > 1000:
        recommendations.append("Your resume might be too long. Keep it concise and under two pages.")

    # **6. Check for Missing Sections**
    if "education" not in resume_text.lower():
        recommendations.append("Ensure you include an 'Education' section.")
    if "experience" not in resume_text.lower():
        recommendations.append("Ensure you include a 'Work Experience' section.")

    # Ensure at least 3 recommendations
    if len(recommendations) < 3:
        recommendations.append("Your resume is well-optimized, but always tailor it for each job.")

    return recommendations

@app.route("/upload", methods=["POST"])
def upload_resume():
    """Upload and analyze a resume."""
    print("Requested files: ", request.files)

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Only PDF, DOCX, and RTF are allowed."}), 400

    # Save file securely
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        # Extract text from the resume
        resume_text = extract_text(filepath)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Calculate ATS Score
    ats_score = min(100, len(resume_text) % 100)

    # Get dynamic recommendations
    recommendations = generate_recommendations(resume_text)

    # Score breakdown
    breakdown = {
        "ATS Compatibility": min(100, ats_score + 5),
        "Content Quality": max(0, ats_score - 5),
        "Format & Structure": min(100, ats_score + 2),
    }

    # Store in MongoDB
    analysis_result = {
        "filename": filename,
        "resume_text": resume_text[:500],  # Store only part of the text for database efficiency
        "ats_score": ats_score,
        "recommendations": recommendations,
        "breakdown": breakdown
    }
    result = collection.insert_one(analysis_result)

    # Return response with resume_id
    return jsonify({
        "message": "Resume analyzed successfully",
        "resume_id": str(result.inserted_id),  # MongoDB document ID
        "ats_score": ats_score,
        "recommendations": recommendations,
        "breakdown": breakdown
    })

@app.route("/results", methods=["GET"])
def get_results():
    """Retrieve stored resume analysis results."""
    results = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's _id field
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)