from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

from app.config.logger import setup_logging
from app.config.settings import settings
from app.api import routes, auth
from app.db.session import SessionLocal
from app.services.signal_dispatcher import SignalDispatcher
from app.services.recommendation_engine import RecommendationEngine

app = FastAPI()
setup_logging()

# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(routes.router, prefix="/api", tags=["signals"])

# Initialize DB session, dispatcher, engine
db = SessionLocal()
dispatcher = SignalDispatcher(db)
engine = RecommendationEngine(db, dispatcher, settings.symbols, settings.engine_interval)

@app.on_event("startup")
async def start_engine():
    # Launch the recommendation engine in background
    asyncio.create_task(engine.run())

@app.websocket("/ws/signals")
async def websocket_signals(websocket: WebSocket):
    await websocket.accept()
    dispatcher.register(websocket)
    try:
        while True:
            # Keep connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        dispatcher.unregister(websocket)

@app.get("/")
def root():
    return {"message": f"{settings.app_name} Running"}
