import logging
from fastapi import WebSocket
from sqlalchemy.orm import Session
from app.db.repository.signal_repo import create_signal
from app.schemas.signal import SignalCreate

logger = logging.getLogger("trading_ai")

class SignalDispatcher:
    """
    Dispatches signals: persists to DB and broadcasts via WebSocket.
    """
    def __init__(self, db: Session):
        self.db = db
        self.connections: set[WebSocket] = set()

    async def dispatch(self, signal_data: dict):
        # Persist signal
        sig_in = SignalCreate(**signal_data)
        created = create_signal(self.db, sig_in)
        logger.info(f"Created signal: {created.id} for {created.instrument}")
        # Broadcast to all connected websockets
        for ws in list(self.connections):
            try:
                await ws.send_json(created.dict())
            except Exception as e:
                logger.warning(f"WebSocket send failed: {e}")

    def register(self, websocket: WebSocket):
        self.connections.add(websocket)

    def unregister(self, websocket: WebSocket):
        self.connections.discard(websocket)
