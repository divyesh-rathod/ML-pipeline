
from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserResponse, UpdateUserSchema
from app.controller.user_controller import update_user_controller
from app.utils.auth import get_current_user

router = APIRouter(
    tags=["Users"],
    dependencies=[Depends(get_current_user)],    # protect every endpoint here
)

@router.put("/update", response_model=UserResponse)
async def update_user(user_details: UpdateUserSchema, current_user: UserResponse = Depends(get_current_user)):
    return await update_user_controller(user_details, current_user)




