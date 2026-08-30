import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load variables from .env
load_dotenv()

# Get PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")

# Create PostgreSQL engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Provides a database session for application code.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Test database connection
if __name__ == "__main__":
    try:
        with engine.connect():
            print("✅ PostgreSQL connection opened successfully!")

    except Exception as e:
        print("❌ PostgreSQL connection failed!")
        print(e)