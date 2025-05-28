from fastapi import FastAPI
from app.api import routes
from app.config.logger import setup_logging

app = FastAPI()
setup_logging()

@app.get('/')
def root():
    return {'message': 'Trading AI Recommendation Engine Running'}
