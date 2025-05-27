# app/preprocessing/data.py

import re
import asyncio
import spacy
from bs4 import BeautifulSoup

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.db.models.article import Article
from app.db.models.processed_article import ProcessedArticle

nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    """
    Basic HTML stripping and whitespace normalization.
    """
    if not text:
        return ""

    soup = BeautifulSoup(text, "lxml")
    cleaned = soup.get_text(" ", strip=True)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned.lower()


async def process_articles() -> None:
    """
    Fetch all Article rows, clean and transform them, and
    write corresponding ProcessedArticle rows asynchronously.
    """
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        try:
            # 1) Load all articles
            result = await session.execute(select(Article))
            articles_to_process = result.scalars().all()

            for article in articles_to_process:
                cleaned_desc = clean_text(article.description)

                # Join categories into a single string
                categories_joined = (
                    ", ".join(article.categories) if article.categories else ""
                )

                # Combine description + categories for vector input
                vector_input = f"{cleaned_desc} {categories_joined}".strip().lower()

                p = ProcessedArticle(
                    article_id=article.id,
                    cleaned_text=cleaned_desc,
                    category_1=(article.categories[0] if article.categories else None),
                    category_2=vector_input,
                    embedding=None,
                )
                session.add(p)

                # Mark original article as processed
                article.processed = True

            # 2) Commit all changes
            await session.commit()
            print(f"Processed {len(articles_to_process)} articles.")
        except Exception as e:
            await session.rollback()
            print("Error processing articles:", e)


if __name__ == "__main__":
    asyncio.run(process_articles())

