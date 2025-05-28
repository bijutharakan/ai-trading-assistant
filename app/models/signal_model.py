from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.db.base import Base
import datetime

class Signal(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True, index=True)
    instrument = Column(String, index=True, nullable=False)
    action = Column(String, nullable=False)
    entry = Column(Float, nullable=False)
    sl = Column(Float, nullable=False)
    target = Column(Float, nullable=False)
    confidence = Column(Float)
    rationale = Column(String)
    metadata = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
