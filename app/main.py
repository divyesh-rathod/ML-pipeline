# app/main.py - Complete CORS setup

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router

app = FastAPI(
    title="Smart News API",
    version="1.0.0",
)

# CORS middleware must be added BEFORE including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers AFTER CORS middleware
app.include_router(api_router, prefix="/api")