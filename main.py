"""
main.py  —  FastAPI application entry point.

Run with:   uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.db import engine, Base
from database import models  # import so Base knows about ScanResult
from routes.pridect import router
import os

# ── Create all DB tables ────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Create FastAPI app ──────────────────────────────────────
app = FastAPI(
    title="PhishGuard — Phishing URL Detector",
    description="Scan any URL and detect if it's a phishing attempt using XGBoost ML.",
    version="1.0.0",
)

# ── Mount static files (CSS, JS, images) ────────────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ── Include API routes ──────────────────────────────────────
app.include_router(router)