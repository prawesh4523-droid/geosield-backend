from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ── Change these to match your PostgreSQL setup ──
DB_USER     = "postgres"
DB_PASSWORD = "12345678"   # ← your PostgreSQL password
DB_HOST     = "localhost"
DB_PORT     = "5432"
DB_NAME     = "geoshield"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency — use this in your routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()