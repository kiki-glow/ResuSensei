"""
database.py - PostgreSQL database configuration
Location: backend/database.py
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from datetime import datetime
import os
from dotenv import load_dotenv
from config.settings import DATABASE_URL

load_dotenv()

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


# ═══════════════════════════════════════════════════════════════════════════
# Database Models
# ═══════════════════════════════════════════════════════════════════════════

class Resume(Base):
    """Resume analysis records"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_size_bytes = Column(Integer)
    resume_text_preview = Column(Text)
    target_role = Column(String(100), index=True)
    
    # Scores
    overall_score = Column(Integer, nullable=False)
    grade = Column(String(2), nullable=False)
    score_breakdown = Column(JSON)  # Stores the 6-dimension scores as JSON
    
    # Analysis results
    recommendations = Column(JSON)  # Array of recommendations
    quick_tips = Column(JSON)  # Array of quick tips
    role_analysis = Column(JSON, nullable=True)  # Role-specific keyword analysis
    features = Column(JSON, nullable=True)  # Additional features/metadata
    
    # Timestamps
    analyzed_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SuccessStory(Base):
    """User success stories"""
    __tablename__ = "success_stories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    story = Column(Text, nullable=True)
    
    # Scores
    score_before = Column(Integer, nullable=True)
    score_after = Column(Integer, nullable=True)
    
    # Moderation
    approved = Column(Boolean, default=False, index=True)
    featured = Column(Boolean, default=False, index=True)
    
    # Timestamps
    submitted_at = Column(DateTime, default=datetime.utcnow, index=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════
# Database Dependency
# ═══════════════════════════════════════════════════════════════════════════

async def get_db():
    """Dependency to get database session"""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Drop all tables (for development - remove in production)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database tables created successfully!")


async def close_db():
    """Close database connection"""
    await engine.dispose()
    print("Database connection closed")