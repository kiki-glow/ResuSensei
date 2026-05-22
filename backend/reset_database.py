"""
Run this to reset the database tables
Usage: python reset_database.py
"""

import asyncio
from database import Base, engine, init_db


async def reset_database():
    print("Dropping existing tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Tables dropped successfully!")
    
    print("\nCreating new tables...")
    await init_db()
    print("Database reset complete!")
    
    print("\nTables created:")
    print("  - resumes")
    print("  - success_stories")


if __name__ == "__main__":
    asyncio.run(reset_database())
