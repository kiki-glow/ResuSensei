"""
main.py — ResuSensei FastAPI Application
Entry point. Run with: uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from pathlib import Path
import os
import sys
import logging
from datetime import datetime
from typing import Optional, List, Dict

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from werkzeug.utils import secure_filename
from bson import ObjectId
from bson.errors import InvalidId

# ── Path setup (cross-platform: Windows / Mac / Linux) ────────────────────
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# ── Project imports ────────────────────────────────────────────────────────
from config.settings import (
    MONGO_URI, DB_NAME, UPLOAD_FOLDER, MAX_FILE_SIZE,
    ALLOWED_EXTENSIONS, API_VERSION, API_TITLE, API_DESCRIPTION,
    ROLE_KEYWORDS,
)
from app.services.text_extraction import TextExtractionService
from app.services.scoring_service import ResumeScorer, RoleSpecificAnalyzer
from app.services.recommendation_engine import RecommendationEngine, generate_quick_tips

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ── Services ───────────────────────────────────────────────────────────────
text_extractor = TextExtractionService()
scorer         = ResumeScorer()
role_analyzer  = RoleSpecificAnalyzer()
rec_engine     = RecommendationEngine()


# ── Lifespan (replaces deprecated @app.on_event) ──────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    try:
        app.mongodb_client = AsyncIOMotorClient(MONGO_URI)
        app.mongodb = app.mongodb_client[DB_NAME]
        await app.mongodb.resumes.create_index([("analyzed_at", -1)])
        await app.mongodb.resumes.create_index([("target_role", 1)])
        logger.info("MongoDB connected and indexes ensured.")
    except Exception as exc:
        logger.error(f"MongoDB startup failed: {exc}")
        raise
    yield
    # SHUTDOWN
    app.mongodb_client.close()
    logger.info("MongoDB connection closed.")


# ── App ────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic response models ───────────────────────────────────────────────
class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime

class RoleListResponse(BaseModel):
    available_roles: List[Dict]
    total_roles: int

class AnalysisResponse(BaseModel):
    resume_id: str
    filename: str
    target_role: Optional[str] = None
    overall_score: int
    grade: str
    score_breakdown: Dict[str, int]
    recommendations: List[Dict]
    quick_tips: List[str]
    role_analysis: Optional[Dict] = None
    analyzed_at: datetime


# ── Helper ─────────────────────────────────────────────────────────────────
def _serialize(doc: dict) -> dict:
    """Replace MongoDB _id ObjectId with a plain string resume_id."""
    doc["resume_id"] = str(doc.pop("_id"))
    return doc


# ── Routes ─────────────────────────────────────────────────────────────────

@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """Health-check — confirms the API is up."""
    return {"status": "running", "version": API_VERSION, "timestamp": datetime.utcnow()}


@app.get("/api/roles", response_model=RoleListResponse, tags=["Roles"])
async def get_available_roles():
    """All supported target roles and their keyword counts."""
    roles = [
        {
            "key": key,
            "name": value["name"],
            "essential_keywords_count": len(value.get("essential_keywords", [])),
            "preferred_keywords_count": len(value.get("preferred_keywords", [])),
        }
        for key, value in ROLE_KEYWORDS.items()
    ]
    return {"available_roles": roles, "total_roles": len(roles)}


@app.post("/api/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_resume(
    file: UploadFile = File(..., description="PDF, DOCX, or RTF resume"),
    target_role: Optional[str] = Form(None, description="Role key from GET /api/roles"),
):
    """
    Analyze a resume. Returns:
    - ATS score + letter grade
    - 6-dimension score breakdown
    - Prioritised recommendations
    - Role-specific keyword gap analysis (when target_role provided)
    """
    # 1. Validate file extension
    if not file.filename:
        raise HTTPException(400, "No file provided.")
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported type '{ext}'. Use: {', '.join(ALLOWED_EXTENSIONS)}")

    # 2. Validate role
    if target_role and target_role not in ROLE_KEYWORDS:
        raise HTTPException(400, f"Unknown role '{target_role}'. See GET /api/roles.")

    # 3. Read and size-check
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        mb = len(content) / 1_048_576
        raise HTTPException(413, f"File too large ({mb:.1f} MB). Limit: {MAX_FILE_SIZE // 1_048_576} MB.")

    # 4. Save temporarily
    filename = secure_filename(file.filename)
    filepath = Path(UPLOAD_FOLDER) / filename
    filepath.write_bytes(content)
    logger.info(f"Saved upload: {filename} ({len(content):,} bytes)")

    # 5. Extract text
    try:
        resume_text = text_extractor.extract_text(str(filepath))
        logger.info(f"Extracted {len(resume_text):,} chars from {filename}")
    except ValueError as exc:
        filepath.unlink(missing_ok=True)
        raise HTTPException(422, str(exc))

    # 6. Score + analyse
    score_data   = scorer.calculate_overall_score(resume_text, target_role)
    role_analysis = role_analyzer.analyze_for_role(resume_text, target_role) if target_role else None
    recommendations = rec_engine.generate_recommendations(
        resume_text, score_data["breakdown"], role_analysis, target_role
    )
    quick_tips = generate_quick_tips(score_data["breakdown"], target_role)

    # 7. Persist to MongoDB
    now = datetime.utcnow()
    record = {
        "filename":            filename,
        "file_size_bytes":     len(content),
        "resume_text_preview": resume_text[:500],
        "target_role":         target_role,
        "overall_score":       score_data["overall_score"],
        "grade":               score_data["grade"],
        "score_breakdown":     score_data["breakdown"],
        "recommendations":     recommendations,
        "quick_tips":          quick_tips,
        "role_analysis":       role_analysis,
        "analyzed_at":         now,
        "features":            score_data["features"],
    }
    result    = await app.mongodb.resumes.insert_one(record)
    resume_id = str(result.inserted_id)
    logger.info(f"Persisted analysis {resume_id} for {filename}")

    # 8. Delete temp file
    filepath.unlink(missing_ok=True)

    return {**record, "resume_id": resume_id}


@app.get("/api/analysis/{resume_id}", tags=["Analysis"])
async def get_analysis(resume_id: str):
    """Fetch a single saved analysis by its ID."""
    try:
        oid = ObjectId(resume_id)
    except InvalidId:
        raise HTTPException(400, f"'{resume_id}' is not a valid analysis ID.")

    doc = await app.mongodb.resumes.find_one({"_id": oid})
    if not doc:
        raise HTTPException(404, "Analysis not found.")
    return _serialize(doc)


@app.delete("/api/analysis/{resume_id}", tags=["Analysis"])
async def delete_analysis(resume_id: str):
    """Delete a saved analysis by ID."""
    try:
        oid = ObjectId(resume_id)
    except InvalidId:
        raise HTTPException(400, f"'{resume_id}' is not a valid analysis ID.")

    result = await app.mongodb.resumes.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(404, "Analysis not found.")
    return {"deleted": resume_id}


@app.get("/api/history", tags=["Analysis"])
async def get_history(limit: int = 10, skip: int = 0):
    """
    Paginated history of all analyses, newest first.
    - limit: results per page (max 50)
    - skip:  offset for pagination
    """
    limit  = min(limit, 50)
    cursor = (
        app.mongodb.resumes
        .find({}, {"resume_text_preview": 0, "features": 0})   # exclude heavy fields
        .sort("analyzed_at", -1)
        .skip(skip)
        .limit(limit)
    )
    docs  = await cursor.to_list(length=limit)
    total = await app.mongodb.resumes.count_documents({})
    return {"total": total, "skip": skip, "limit": limit, "analyses": [_serialize(d) for d in docs]}


@app.get("/api/stats", tags=["Stats"])
async def get_statistics():
    """Aggregated platform statistics."""
    total = await app.mongodb.resumes.count_documents({})

    score_pipeline = [{"$group": {
        "_id":         None,
        "avg_overall": {"$avg": "$overall_score"},
        "avg_ats":     {"$avg": "$score_breakdown.ats_compatibility"},
        "avg_content": {"$avg": "$score_breakdown.content_quality"},
        "avg_keywords":{"$avg": "$score_breakdown.keyword_optimization"},
        "max_score":   {"$max": "$overall_score"},
        "min_score":   {"$min": "$overall_score"},
    }}]
    score_agg = await app.mongodb.resumes.aggregate(score_pipeline).to_list(1)

    role_pipeline = [
        {"$match": {"target_role": {"$ne": None}}},
        {"$group": {"_id": "$target_role", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    role_dist = await app.mongodb.resumes.aggregate(role_pipeline).to_list(20)

    grade_pipeline = [
        {"$group": {"_id": "$grade", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    grade_dist = await app.mongodb.resumes.aggregate(grade_pipeline).to_list(10)

    return {
        "total_analyses":   total,
        "score_stats":      score_agg[0] if score_agg else {},
        "role_distribution":role_dist,
        "grade_distribution":grade_dist,
    }


# ── Global error handlers ──────────────────────────────────────────────────

@app.exception_handler(HTTPException)
async def http_exc_handler(request: Request, exc: HTTPException):
    return JSONResponse(exc.status_code, {"error": exc.detail})

@app.exception_handler(Exception)
async def unhandled_exc_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.url}: {exc}")
    return JSONResponse(500, {"error": "Internal server error."})


# ── Dev entrypoint ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)