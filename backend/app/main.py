import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import apply_sqlite_patch
from app.routers import metrics, patients, export

apply_sqlite_patch()

app = FastAPI(title="HealthMetrics Pro API", version="1.0.0")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(export.router, prefix="/api/export", tags=["export"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "healthmetrics-pro"}
