"""
main.py — ResuSensei FastAPI Application (PostgreSQL Version)
Entry point. Run with: uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from pathlib import Path
import os
import sys
import logging
from datetime import datetime
from typing import Optional, List, Dict

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from werkzeug.utils import secure_filename
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

# ── Path setup (cross-platform: Windows / Mac / Linux) ────────────────────
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# ── Project imports ────────────────────────────────────────────────────────
from config.settings import (
    UPLOAD_FOLDER, MAX_FILE_SIZE,
    ALLOWED_EXTENSIONS, API_VERSION, API_TITLE, API_DESCRIPTION,
    ROLE_KEYWORDS,
)
from app.services.text_extraction import TextExtractionService
from app.services.scoring_service import ResumeScorer, RoleSpecificAnalyzer
from app.services.recommendation_engine import RecommendationEngine, generate_quick_tips

# ── Database imports (NEW - PostgreSQL) ────────────────────────────────────
from database import init_db, close_db, get_db, Resume, SuccessStory

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
        await init_db()
        logger.info("PostgreSQL connected and tables created.")
    except Exception as exc:
        logger.error(f"Database startup failed: {exc}")
        raise
    yield
    # SHUTDOWN
    await close_db()
    logger.info("PostgreSQL connection closed.")


# ── App ────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
)

# CORS
from os import getenv

frontend_origin = getenv("FRONTEND_ORIGIN", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
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
    resume_id: int
    filename: str
    target_role: Optional[str] = None
    overall_score: int
    grade: str
    score_breakdown: Dict[str, int]
    recommendations: List[Dict]
    quick_tips: List[str]
    role_analysis: Optional[Dict] = None
    analyzed_at: datetime

class SuccessStoryCreate(BaseModel):
    name: str
    job_title: str
    company: Optional[str] = None
    story: Optional[str] = None
    score_before: Optional[int] = None
    score_after: Optional[int] = None


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
    db: AsyncSession = Depends(get_db)
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

    # 7. Persist to PostgreSQL
    now = datetime.utcnow()
    resume_record = Resume(
        filename=filename,
        file_size_bytes=len(content),
        resume_text_preview=resume_text[:500],
        target_role=target_role,
        overall_score=score_data["overall_score"],
        grade=score_data["grade"],
        score_breakdown=score_data["breakdown"],
        recommendations=recommendations,
        quick_tips=quick_tips,
        role_analysis=role_analysis,
        analyzed_at=now,
        features=score_data["features"],
    )
    
    db.add(resume_record)
    await db.commit()
    await db.refresh(resume_record)
    
    resume_id = resume_record.id
    logger.info(f"Persisted analysis {resume_id} for {filename}")

    # 8. Delete temp file
    filepath.unlink(missing_ok=True)

    return {
        "resume_id": resume_id,
        "filename": filename,
        "target_role": target_role,
        "overall_score": score_data["overall_score"],
        "grade": score_data["grade"],
        "score_breakdown": score_data["breakdown"],
        "recommendations": recommendations,
        "quick_tips": quick_tips,
        "role_analysis": role_analysis,
        "analyzed_at": now,
    }


@app.get("/api/analysis/{resume_id}", tags=["Analysis"])
async def get_analysis(resume_id: int, db: AsyncSession = Depends(get_db)):
    """Fetch a single saved analysis by its ID."""
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(404, "Analysis not found.")
    
    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "target_role": resume.target_role,
        "overall_score": resume.overall_score,
        "grade": resume.grade,
        "score_breakdown": resume.score_breakdown,
        "recommendations": resume.recommendations,
        "quick_tips": resume.quick_tips,
        "role_analysis": resume.role_analysis,
        "analyzed_at": resume.analyzed_at,
    }


@app.delete("/api/analysis/{resume_id}", tags=["Analysis"])
async def delete_analysis(resume_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a saved analysis by ID."""
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(404, "Analysis not found.")
    
    await db.delete(resume)
    await db.commit()
    
    return {"deleted": resume_id}


@app.get("/api/history", tags=["Analysis"])
async def get_history(
    limit: int = 10, 
    skip: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Paginated history of all analyses, newest first.
    - limit: results per page (max 50)
    - skip:  offset for pagination
    """
    limit = min(limit, 50)
    
    # Get total count
    count_result = await db.execute(select(func.count(Resume.id)))
    total = count_result.scalar()
    
    # Get paginated results
    result = await db.execute(
        select(Resume)
        .order_by(desc(Resume.analyzed_at))
        .offset(skip)
        .limit(limit)
    )
    resumes = result.scalars().all()
    
    analyses = [
        {
            "resume_id": r.id,
            "filename": r.filename,
            "target_role": r.target_role,
            "overall_score": r.overall_score,
            "grade": r.grade,
            "analyzed_at": r.analyzed_at,
        }
        for r in resumes
    ]
    
    return {"total": total, "skip": skip, "limit": limit, "analyses": analyses}


@app.get("/api/stats", tags=["Stats"])
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """Aggregated platform statistics."""
    
    # Total analyses
    count_result = await db.execute(select(func.count(Resume.id)))
    total = count_result.scalar()
    
    # Score statistics
    stats_result = await db.execute(
        select(
            func.avg(Resume.overall_score).label("avg_overall"),
            func.max(Resume.overall_score).label("max_score"),
            func.min(Resume.overall_score).label("min_score"),
        )
    )
    stats = stats_result.one()
    
    # Role distribution
    role_result = await db.execute(
        select(Resume.target_role, func.count(Resume.id).label("count"))
        .where(Resume.target_role.isnot(None))
        .group_by(Resume.target_role)
        .order_by(desc("count"))
    )
    role_dist = [{"_id": row[0], "count": row[1]} for row in role_result.all()]
    
    # Grade distribution
    grade_result = await db.execute(
        select(Resume.grade, func.count(Resume.id).label("count"))
        .group_by(Resume.grade)
        .order_by(Resume.grade)
    )
    grade_dist = [{"_id": row[0], "count": row[1]} for row in grade_result.all()]
    
    return {
        "total_analyses": total,
        "score_stats": {
            "avg_overall": float(stats[0]) if stats[0] else 0,
            "max_score": stats[1] or 0,
            "min_score": stats[2] or 0,
        },
        "role_distribution": role_dist,
        "grade_distribution": grade_dist,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Success Stories Endpoints
# ═══════════════════════════════════════════════════════════════════════════

@app.post("/api/success-story", tags=["Success Stories"])
async def submit_success_story(
    story: SuccessStoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Submit a success story from a user who got hired"""
    try:
        story_record = SuccessStory(
            name=story.name,
            job_title=story.job_title,
            company=story.company,
            story=story.story,
            score_before=story.score_before,
            score_after=story.score_after,
            submitted_at=datetime.utcnow(),
            approved=False,
            featured=False
        )
        
        db.add(story_record)
        await db.commit()
        await db.refresh(story_record)
        
        logger.info(f"Success story submitted: {story.name} - {story.job_title}")
        
        return {
            "message": "Thank you for sharing your success! We'll review and feature your story soon.",
            "story_id": story_record.id
        }
        
    except Exception as e:
        logger.error(f"Error submitting success story: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit success story")


@app.get("/api/success-stories", tags=["Success Stories"])
async def get_success_stories(
    limit: int = 10,
    featured_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """Get approved success stories to display on the homepage"""
    try:
        query = select(SuccessStory).where(SuccessStory.approved == True)
        
        if featured_only:
            query = query.where(SuccessStory.featured == True)
        
        query = query.order_by(desc(SuccessStory.submitted_at)).limit(limit)
        
        result = await db.execute(query)
        stories = result.scalars().all()
        
        formatted_stories = [
            {
                "id": s.id,
                "name": s.name,
                "jobTitle": s.job_title,
                "company": s.company,
                "story": s.story,
                "scoreBefore": s.score_before,
                "scoreAfter": s.score_after,
                "submittedAt": s.submitted_at.isoformat()
            }
            for s in stories
        ]
        
        return {"stories": formatted_stories, "total": len(formatted_stories)}
        
    except Exception as e:
        logger.error(f"Error fetching success stories: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch success stories")


@app.patch("/api/admin/success-story/{story_id}/approve", tags=["Admin"])
async def approve_success_story(
    story_id: int,
    featured: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """ADMIN ONLY: Approve a success story for display"""
    try:
        result = await db.execute(select(SuccessStory).where(SuccessStory.id == story_id))
        story = result.scalar_one_or_none()
        
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")
        
        story.approved = True
        story.featured = featured
        story.approved_at = datetime.utcnow()
        
        await db.commit()
        
        return {"message": "Success story approved", "featured": featured}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error approving success story: {e}")
        raise HTTPException(status_code=500, detail="Failed to approve success story")


@app.get("/api/admin/success-stories/pending", tags=["Admin"])
async def get_pending_success_stories(db: AsyncSession = Depends(get_db)):
    """ADMIN ONLY: Get all pending (unapproved) success stories"""
    try:
        result = await db.execute(
            select(SuccessStory)
            .where(SuccessStory.approved == False)
            .order_by(desc(SuccessStory.submitted_at))
        )
        stories = result.scalars().all()
        
        formatted_stories = [
            {
                "id": s.id,
                "name": s.name,
                "jobTitle": s.job_title,
                "company": s.company,
                "story": s.story,
                "scoreBefore": s.score_before,
                "scoreAfter": s.score_after,
                "submittedAt": s.submitted_at.isoformat()
            }
            for s in stories
        ]
        
        return {"pending": formatted_stories, "total": len(formatted_stories)}
        
    except Exception as e:
        logger.error(f"Error fetching pending stories: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch pending stories")


# ── Global error handlers ──────────────────────────────────────────────────

@app.exception_handler(HTTPException)
async def http_exc_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def unhandled_exc_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.url}: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal server error."})


# ── Dev entrypoint ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)