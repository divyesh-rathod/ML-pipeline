
# app/api/v1/__init__.py
from fastapi import APIRouter

from .user_routes import router as user_router
# import any other routers here...

api_v1_router = APIRouter()
api_v1_router.include_router(user_router,    prefix="/users", tags=["Users"])
# api_v1_router.include_router(other_router, prefix="/foo",   tags=["Foo"])
