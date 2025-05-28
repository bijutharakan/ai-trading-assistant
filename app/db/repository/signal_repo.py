from sqlalchemy.orm import Session
from app.models.signal_model import Signal as SignalModel
from app.schemas.signal import SignalCreate

def create_signal(db: Session, signal: SignalCreate):
    db_signal = SignalModel(**signal.dict())
    db.add(db_signal)
    db.commit()
    db.refresh(db_signal)
    return db_signal

def get_signals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SignalModel).offset(skip).limit(limit).all()
