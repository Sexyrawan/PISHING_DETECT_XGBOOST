from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func
from database.db import Base

class ScanResult(Base):
    __tablename__ = "PHISHING_HISTORY"  
    id          = Column(Integer, primary_key=True, index=True)
    url         = Column(String(2000), nullable=False)
    is_phishing = Column(Boolean, nullable=False)
    confidence  = Column(Float, nullable=False)
    scanned_at  = Column(DateTime, default=func.now())
