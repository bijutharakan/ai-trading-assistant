from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Any

class SignalBase(BaseModel):
    instrument: str
    action: str
    entry: float
    sl: float
    target: float
    confidence: float
    rationale: str

class SignalCreate(SignalBase):
    metadata: Optional[Any] = None

class Signal(SignalBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
