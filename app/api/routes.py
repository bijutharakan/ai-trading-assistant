from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.signal import Signal, SignalCreate
from app.db.repository.signal_repo import create_signal, get_signals
from app.core.dependencies import get_db

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/signals/", response_model=Signal)
def create_new_signal(signal: SignalCreate, db: Session = Depends(get_db)):
    return create_signal(db, signal)

@router.get("/signals/", response_model=list[Signal])
def read_signals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_signals(db, skip=skip, limit=limit)
