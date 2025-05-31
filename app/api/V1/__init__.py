
# app/api/v1/__init__.py
from fastapi import APIRouter

from .user_routes import router as user_router
from .auth_routes import router as auth_router
from .scripts_route import router as scripts_router
# import any other routers here...

api_v1_router = APIRouter()
api_v1_router.include_router(user_router,    prefix="/users", tags=["Users"])
api_v1_router.include_router(auth_router,    prefix="/auth",  tags=["Auth"])
api_v1_router.include_router(scripts_router, prefix="/scripts", tags=["Scripts"])
# api_v1_router.include_router(other_router, prefix="/foo",   tags=["Foo"])
