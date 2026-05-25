#!/usr/bin/env python3
"""
Database setup script for MNP AI Bot
"""

import sys
import os

# Add current directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

print(f"Project directory: {project_dir}")

try:
    from app.config import Config
    print("✓ Imported Config")
    from app.database import engine, Base
    print("✓ Imported Base from database")
    from app.models import UserOLM, MNPJourney, ApplicationLog
    print("✓ Imported models")
except Exception as e:
    print(f"❌ Import error: {e}")
    print(f"Files in app folder: {os.listdir(os.path.join(project_dir, 'app')) if os.path.exists(os.path.join(project_dir, 'app')) else 'app folder not found'}")
    sys.exit(1)

def setup_database():
    print("🔧 Setting up MNP AI Bot Database...")
    
    database_url = Config.DATABASE_URL
    print(f"Database URL: {database_url.split('@')[0].replace('://', '://***:***@') if '@' in database_url else 'configured'}")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Seed initial users
        from sqlalchemy.orm import Session
        db = Session(engine)
        from app.auth import seed_initial_users
        seed_initial_users(db)
        db.close()
        print("✅ Initial users seeded!")
        
        print("\n🎉 Setup complete! You can now run the bot:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is installed and running")
        print("2. Update .env file with correct database credentials")
        print("3. Database exists: CREATE DATABASE mnp_bot_db;")
        
        # Check if we can connect at all
        try:
            from sqlalchemy import create_engine, text
            test_engine = create_engine(database_url)
            with test_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✓ Database connection successful but table creation failed")
        except Exception as conn_err:
            print(f"✗ Cannot connect to database: {conn_err}")
        
        sys.exit(1)

if __name__ == "__main__":
    setup_database()