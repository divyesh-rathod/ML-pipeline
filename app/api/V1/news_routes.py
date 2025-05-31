from fastapi import APIRouter, Depends
from app.controller.news_controller import mark_article_as_read_controller
from app.schemas.user_schema import UserResponse   
from app.utils.auth import get_current_user 

router = APIRouter(
    tags=["News"],
    dependencies=[Depends(get_current_user)],  # protect every endpoint here
)

@router.post("/mark-as-read/{article_id}", response_model=str)
async def mark_article_as_read(article_id: str, current_user: UserResponse = Depends(get_current_user)):
 
    return await mark_article_as_read_controller(article_id, current_user)  

