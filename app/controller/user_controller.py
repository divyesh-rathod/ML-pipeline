# app/controllers/user_controller.py
from fastapi import HTTPException, status
from app.schemas.user_schema import UpdateUserSchema, UserResponse
from app.services.user_services import update_user




async def update_user_controller(user_details: UpdateUserSchema,current_user:UserResponse) -> UserResponse:
    try:
        user = await update_user(user_details,current_user)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

