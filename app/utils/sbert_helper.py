from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from app.db.models.processed_article import ProcessedArticle
import numpy as np

# Load model once (singleton-style)
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> list[float]:
    """
    Generate SBERT embedding from a cleaned text string.
    """
    if not text:
        return None
    embedding = model.encode(text)
    norm = np.linalg.norm(embedding)
    if norm == 0:  
        return embedding.tolist()
    normalized_embedding = embedding / norm
    return normalized_embedding.tolist()



def embed_articles(db: Session, batch_size: int = 100):
    """
    Loop through articles with null embeddings and generate them.
    """
    articles = db.query(ProcessedArticle).filter(ProcessedArticle.embedding == None).limit(batch_size).all()

    for article in articles:
        if article.category_2:
            article.embedding = generate_embedding(article.category_2)

    db.commit()
    return f"{len(articles)} articles embedded and saved."
