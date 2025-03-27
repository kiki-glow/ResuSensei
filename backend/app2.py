from flask import Flask, request, jsonify
import os
import pymongo
from werkzeug.utils import secure_filename
from flask_cors import CORS
from services.extract_text import extract_text  # Import the text extraction function
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch MongoDB details from .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "ResuSenseiDB")  # Default to "resumeAI" if not set

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing in the .env file!")

# Initialize MongoDB connection
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["resumes"]

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# File upload configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "rtf"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_resume():
    """Upload and analyze a resume."""
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

    # Placeholder AI Scoring (Replace with real AI model)
    ats_score = len(resume_text) % 100  # Dummy score based on text length
    recommendations = [
        "Use more action verbs.",
        "Add measurable achievements.",
        "Optimize formatting for ATS systems."
    ]

    # Store in MongoDB
    analysis_result = {
        "filename": filename,
        "filepath": filepath,
        "resume_text": resume_text[:500],  # Store only part of the text
        "ats_score": ats_score,
        "recommendations": recommendations
    }
    collection.insert_one(analysis_result)

    return jsonify({
        "message": "File uploaded and analyzed successfully",
        "ats_score": ats_score,
        "recommendations": recommendations
    })

@app.route("/results", methods=["GET"])
def get_results():
    """Retrieve all stored resume analysis results."""
    results = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB `_id` field
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
