from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import pymongo
from config import UPLOAD_FOLDER, MONGO_URI, DB_NAME
from services.extract_text import extract_text_from_pdf
from models.ai_model import analyze_resume_text

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["resumes"]

api = Blueprint("api", __name__)

# Allowed file types
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route("/upload", methods=["POST"])
def upload_resume():
    """Upload a resume file."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        return jsonify({"message": "File uploaded successfully", "filepath": file_path})
    
    return jsonify({"error": "Invalid file format"}), 400

@api.route("/analyze", methods=["POST"])
def analyze_resume():
    """Analyze a resume and return ATS score + recommendations."""
    data = request.json
    filepath = data.get("filepath")

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "Invalid file path"}), 400

    # Extract text from PDF
    resume_text = extract_text_from_pdf(filepath)

    # AI analysis
    ats_score = analyze_resume_text(resume_text)

    # Sample recommendations
    recommendations = [
        "Use more action verbs.",
        "Add measurable achievements.",
        "Optimize formatting for ATS."
    ]

    # Save results to MongoDB
    analysis_result = {
        "filepath": filepath,
        "ats_score": ats_score,
        "recommendations": recommendations
    }
    collection.insert_one(analysis_result)

    return jsonify(analysis_result)

@api.route("/results", methods=["GET"])
def get_results():
    """Get all past resume analysis results."""
    results = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    return jsonify(results)
