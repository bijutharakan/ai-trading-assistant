from fastapi import FastAPI
from app.api import routes, auth
from app.config.logger import setup_logging

app = FastAPI()
setup_logging()

# Include auth and signal routers
app.include_router(auth.router, tags=["auth"])
app.include_router(routes.router, prefix="/api", tags=["signals"])
