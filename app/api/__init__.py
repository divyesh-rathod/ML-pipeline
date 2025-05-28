# app/api/__init__.py
from fastapi import APIRouter

from .V1 import api_v1_router    # your existing V1 router

api_router = APIRouter()
# Mount v1 under /v1
api_router.include_router(api_v1_router, prefix="/V1", tags=["V1"])

