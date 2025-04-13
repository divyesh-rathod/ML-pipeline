# app/preprocessing/data.py

import re
import spacy
# If using nltk, import and setup as well
# import nltk
# nltk.download("stopwords")
# from nltk.corpus import stopwords

from app.db.session import SessionLocal
from app.db.models.article import Article
from app.db.models.processed_article import ProcessedArticle
from sqlalchemy.orm import Session

nlp = spacy.load("en_core_web_sm")  # small English model

def clean_text(text: str) -> str:
    """
    Cleans raw text using regex, spaCy, etc.
    Adjust steps according to your project’s needs.
    """
    if not text:
        return ""

    # 1) Remove HTML tags if needed
    # If you haven't stripped them already:
    # text = re.sub(r"<[^>]*>", "", text)

    # 2) Basic cleaning: remove extra whitespace, newlines
    text = re.sub(r"\s+", " ", text).strip()

    # 3) Use spaCy for tokenization, lemmatization (if desired):
    doc = nlp(text)
    # Build a cleaned string from lemmas, ignoring stopwords/punctuation, etc.
    tokens = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            # For advanced usage, you might check token.lemma_ vs. token.text
            tokens.append(token.lemma_.lower())

    cleaned_text = " ".join(tokens)
    return cleaned_text

def process_articles():
    """
    1) Fetch articles from the 'articles' table that need processing.
    2) Clean the text (title, description, etc.).
    3) Insert data into 'processed_articles'.
    4) Optionally mark article.processed = True.
    """
    db: Session = SessionLocal()
    try:
        # Step 1: Retrieve unprocessed articles
        articles_to_process = db.query(Article).filter(Article.processed == False).all()

        for article in articles_to_process:
            # Step 2: Clean the text
            cleaned_desc = clean_text(article.description)
            
            # If you want to treat title differently, you could do a separate function
            cleaned_title = clean_text(article.title)

            # Step 3: Insert (or update) record in processed_articles
            p = ProcessedArticle(
                article_id=article.id,
                cleaned_text=cleaned_desc,
                category_1=(article.categories[0] if article.categories else None),  
                category_2=None,  # Placeholder if you want to fill later with ML categories
                # processed_at will default to CURRENT_TIMESTAMP
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
