
from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserResponse
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)],    # protect every endpoint here
)