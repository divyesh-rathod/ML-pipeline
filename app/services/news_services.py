from app.db.models import *
from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy import insert, update
from sqlalchemy import select, desc, and_
from app.db.session import AsyncSessionLocal
from app.schemas.news_schema import UnseenProcessedArticle, UnseenArticlesResponse, UnseenArticlesQuery,ToggleLikeResponse,ArticleScore
from app.ml_models.retrieve import main
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
      
async def get_unseen_processed_articles_for_user(
    current_user: User,
    params: UnseenArticlesQuery
) -> UnseenArticlesResponse:
    async with AsyncSessionLocal() as session:
     
        feed_pos = await session.get(UserFeedPosition, current_user.id)
        if not feed_pos:
        
            feed_pos = UserFeedPosition(user_id=current_user.id)
            session.add(feed_pos)
            await session.flush()  
            

        current_cursor: Optional[datetime] = feed_pos.cursor

        PA = ProcessedArticle
        A  = Article
        UR = UserRead

        stmt = (
            select(PA)
            .join(A, PA.article_id == A.id)
            .outerjoin(
                UR,
                and_(UR.article_id == A.id,
                     UR.user_id    == current_user.id)
            )
            .where(UR.article_id.is_(None))  # only unread
        )

        if current_cursor is None:

            stmt = stmt.order_by(A.pub_date.desc())
        else:
         
            stmt = stmt.order_by(
                (A.pub_date > current_cursor).desc(),
                A.pub_date.desc()
            )

 
        stmt = stmt.limit(params.limit).offset(params.offset or 0)

        result = await session.execute(stmt)
        processed_articles: List[ProcessedArticle] = result.scalars().all()

   
        if len(processed_articles) == params.limit:
            next_cursor = processed_articles[-1].article.pub_date
        else:
            next_cursor = None

       
        if feed_pos.cursor != next_cursor:
            feed_pos.cursor = next_cursor
            await session.commit()
        else:
    
            await session.rollback()

        return UnseenArticlesResponse(
            results     = processed_articles,
            next_cursor = next_cursor
        )

       
       
    
async def set_last_read_date(current_user: User, explicit_date: datetime | None = None) -> str:
  
    async with AsyncSessionLocal() as session:  
        # Check if row exists
        row = await session.get(UserFeedPosition, current_user.id)
        if row:
            new_date = explicit_date or datetime.utcnow()
            stmt = (
                update(UserFeedPosition)
                .where(UserFeedPosition.user_id == current_user.id)
                .values(last_read_date=new_date, updated_at=datetime.utcnow())
            )
            await session.execute(stmt)
        else:
            new_date = explicit_date or datetime.utcnow()
            new_row = UserFeedPosition(user_id=current_user.id, last_read_date=new_date)
            session.add(new_row)



        await session.commit()
        return "Last read date updated successfully"
    


async def toggle_article_like(
    article_id: UUID,
    current_user: User
) -> ToggleLikeResponse:
    async with AsyncSessionLocal() as session:
        # 1) Ensure the article exists
        # result = await session.execute(
        #     select(Article).where(Article.id == article_id)
        # )
        # article = result.scalar_one_or_none()
        # if not article:
        #     raise ValueError("Article not found")

        # 2) Check if a Like row already exists
        result = await session.execute(
            select(Like).where(
                Like.article_id == article_id,
                Like.user_id    == current_user.id
            )
        )
        existing_like = result.scalar_one_or_none()

        if existing_like:
            # 3A) Flip the 0/1 integer in Python, re‐add, and commit
            existing_like.is_liked = existing_like.is_liked ^ 1
            session.add(existing_like)
            await session.commit()

            # If it was 1 → becomes 0, we treat that as “Like removed”
            if existing_like.is_liked == 0:
                return "Like removed", False,[], []
            else:
                top5, similar = await main(str(article_id))
                return "Article liked", True, top5, similar

        else:
            # 3B) No row yet → create a new one with is_liked=1
            new_like = Like(
                user_id    = current_user.id,
                article_id = article_id,
                is_liked   = 1
            )
            session.add(new_like)
            await session.commit()

            top5, similar = await main(str(article_id))


            return "Article liked", True, top5, similar
        

def serialize_article_scores(raw: list[tuple[ProcessedArticle, float]]) -> list[ArticleScore]:
    """
    Convert List[(ProcessedArticle, float)] into List[ArticleScore] (or dicts).
    """
    results: list[ArticleScore] = []
    for art_obj, score in raw:
        # We can either pass an ORM object and let Pydantic read .article_id etc.
        results.append(ArticleScore(
            article_id=art_obj.article_id,
            cleaned_text=art_obj.cleaned_text,
            category_1=art_obj.category_1,
            category_2=art_obj.category_2,
            score=score
        ))
    return results


    

    

        
     
