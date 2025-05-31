from app.db.models import *
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from typing import List
from uuid import UUID


async def mark_article_as_read(article_id:UUID,current_user:user)->str:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Article).where(Article.id == article_id)
        )
        article = result.scalar_one_or_none()
        if not article:
            raise ValueError("Article not found")
        user_read_article = await session.execute(
            select(UserRead).where(
                UserRead.user_id == current_user.id,
                UserRead.article_id == article_id
            )
        )
        user_read = user_read_article.scalar_one_or_none()
        if user_read:
            return "Article already marked as read" 
        new_user_read = UserRead(
            user_id=current_user.id,
            article_id=article_id
        )   
        session.add(new_user_read)
        await session.commit()      
        return "Article marked as read successfully"
    

    
async def get_read_article_ids(current_user: User) -> List[UUID]:
    async with AsyncSessionLocal() as session:  
        result = await session.execute(
            select(UserRead.article_id)
            .where(UserRead.user_id == current_user.id)
        )
        read_ids: List[UUID] = result.scalars().all()
        return read_ids
    


    
        
        
     
