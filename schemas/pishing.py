"""
pishing.py  —  Pydantic schemas for request validation & response serialization.
"""

from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class URLInput(BaseModel):
    """What the user sends to the /scan endpoint."""
    url: str  # raw URL string


class ScanResponse(BaseModel):
    """What the API returns after scanning."""
    id: int
    url: str
    is_phishing: bool
    confidence: float
    scanned_at: datetime

    class Config:
        from_attributes = True  # allows creating from SQLAlchemy model


class HistoryItem(BaseModel):
    """Single row in scan history."""
    id: int
    url: str
    is_phishing: bool
    confidence: float
    scanned_at: datetime

    class Config:
        from_attributes = True
