from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
from sqlalchemy import text
from model import predict_risk
from pydantic import BaseModel

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── REQUEST MODEL ─────────────────────────────────

class PredictRequest(BaseModel):
    rainfall: float
    slope: float
    soil_moisture: float
    temperature: float

# ── BASIC ROUTES ──────────────────────────────────

@app.get("/")
def home():
    return {
        "message": "GeoShield Nepal Backend Running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# ── SHELTERS ──────────────────────────────────────

@app.get("/api/shelters")
def get_shelters(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT id, name, capacity,
               ST_X(location::geometry) AS longitude,
               ST_Y(location::geometry) AS latitude
        FROM shelters
    """))
    rows = result.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "capacity": row[2],
            "longitude": row[3],
            "latitude": row[4]
        }
        for row in rows
    ]

# ── HOSPITALS ─────────────────────────────────────

@app.get("/api/hospitals")
def get_hospitals(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT id, name, contact,
               ST_X(location::geometry) AS longitude,
               ST_Y(location::geometry) AS latitude
        FROM hospitals
    """))
    rows = result.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "contact": row[2],
            "longitude": row[3],
            "latitude": row[4]
        }
        for row in rows
    ]

# ── RISK ZONES ────────────────────────────────────

@app.get("/api/risk-zones")
def get_risk_zones(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT id, zone_name, risk_level
        FROM risk_zones
    """))
    rows = result.fetchall()
    return [
        {
            "id": row[0],
            "zone_name": row[1],
            "risk_level": row[2]
        }
        for row in rows
    ]

# ── USERS ─────────────────────────────────────────

@app.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, name, email FROM users"))
    rows = result.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2]
        }
        for row in rows
    ]

# ── AI PREDICTION ─────────────────────────────────

@app.post("/predict")
def predict(request: PredictRequest):
    result = predict_risk(
        request.rainfall,
        request.slope,
        request.soil_moisture,
        request.temperature
    )
    return result