from fastapi import FastAPI
from .api import api_router     

app = FastAPI(
    title="Smart News API",
    version="1.0.0",
)


app.include_router(api_router, prefix="/api")# uvicorn app.main:app --reload
