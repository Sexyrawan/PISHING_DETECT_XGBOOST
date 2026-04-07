"""
pridect.py  —  FastAPI route endpoints.

Endpoints:
    GET  /              →  Render the homepage (scan form)
    POST /scan          →  Accept a URL, predict, save to DB, return result
    GET  /history       →  Return all past scan results
    GET  /api/history   →  JSON API for scan history
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import ScanResult
from model.pridect import predict_url
from schemas.pishing import ScanResponse

import os

router = APIRouter()

# Templates directory
_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "tampletes")
templates = Jinja2Templates(directory=_TEMPLATE_DIR)


# ── GET /  —  Homepage ──────────────────────────────────────
@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ── POST /scan  —  Scan a URL ───────────────────────────────
@router.post("/scan", response_class=HTMLResponse)
async def scan_url(request: Request, url: str = Form(...), db: Session = Depends(get_db)):
    """
    1. Receive the URL from the form
    2. Run through XGBoost model
    3. Save result to the database
    4. Show the result page
    """
    # ── Predict ──
    result = predict_url(url)

    # ── Save to DB ──
    scan = ScanResult(
        url=result["url"],
        is_phishing=result["is_phishing"],
        confidence=result["confidence"],
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)  # get the auto-generated id & scanned_at

    # ── Render result ──
    return templates.TemplateResponse("result.html", {
        "request": request,
        "scan": scan,
        "features": result["features"],
    })


# ── GET /history  —  Scan History Page ──────────────────────
@router.get("/history", response_class=HTMLResponse)
async def history_page(request: Request, db: Session = Depends(get_db)):
    scans = db.query(ScanResult).order_by(ScanResult.scanned_at.desc()).all()
    return templates.TemplateResponse("history.html", {
        "request": request,
        "scans": scans,
    })


# ── GET /api/history  —  JSON History ───────────────────────
@router.get("/api/history")
async def history_json(db: Session = Depends(get_db)):
    scans = db.query(ScanResult).order_by(ScanResult.scanned_at.desc()).all()
    return [
        ScanResponse.model_validate(s).model_dump()
        for s in scans
    ]
