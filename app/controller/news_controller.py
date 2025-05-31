from fastapi import HTTPException,status
from app.services.news_services import mark_article_as_read
from app.schemas.user_schema import UserResponse


async def mark_article_as_read_controller(article_id: str, current_user: UserResponse) -> str:
    try:
        result = await mark_article_as_read(article_id, current_user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
