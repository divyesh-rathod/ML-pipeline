# app/preprocessing/data.py

import re
import spacy
from bs4 import BeautifulSoup


from app.db.session import SessionLocal
from app.db.models.article import Article
from app.db.models.processed_article import ProcessedArticle
from sqlalchemy.orm import Session

nlp = spacy.load("en_core_web_sm")  

def clean_text(text: str) -> str:
    """
    
    """
    if not text:
        return ""

 
    soup = BeautifulSoup(text, "lxml")
    text = soup.get_text(" ", strip=True)
    # 2) Basic cleaning: remove extra whitespace, newlines
    text = re.sub(r"\s+", " ", text).strip()
    text=text.lower();



    return text;

def process_articles():

    db: Session = SessionLocal()
    try:

        articles_to_process = db.query(Article).all()

        for article in articles_to_process:

            cleaned_desc = clean_text(article.description)
            
            # Join all categories (if any) into a single string with a comma separator
            categories_joined = ", ".join(article.categories) if article.categories else ""
            
            # Create a single combined string: description and categories together.
            # You can adjust the delimiter (here a space is used) to your needs.
            vector_input = f"{cleaned_desc} {categories_joined}".strip().lower()
              
            p = ProcessedArticle(
                article_id=article.id,
                cleaned_text=cleaned_desc,
                category_1=(article.categories[0] if article.categories else None),  
                category_2=vector_input, 
               
            )
            db.add(p)

            # Step 4: Optionally mark the original article as processed
            article.processed = True

        db.commit()
        print(f"Processed {len(articles_to_process)} articles.")
    except Exception as e:
        db.rollback()
        print("Error processing articles:", e)
    finally:
        db.close()

if __name__ == "__main__":
    process_articles()
