from sqlalchemy import Float, desc,asc
from sqlalchemy.orm import Session
from app.db.models.processed_article import ProcessedArticle
from app.ml_models.rerank import rerank_top_k

def get_top_50_cosine_similar_articles(db: Session, article_id: str):
 
      # Retrieve the source article's embedding.
    source_article = db.query(ProcessedArticle).filter(ProcessedArticle.article_id == article_id).first()
    if not source_article:
        raise ValueError(f"No article found with article_id: {article_id}")
    
    # Use an explicit check for None (or empty embedding)
    if source_article.embedding is None:
        raise ValueError(f"Article {article_id} does not have an embedding.")
    
    source_embedding = source_article.embedding
    
     # 2) build the distance expression and cast it to Float
    distance_expr = (
        ProcessedArticle.embedding
        .op("<->")(source_article.embedding)    # Euclidean on normalized → cosine
        .cast(Float)                    # ← tell SQLAlchemy this yields a float
        .label("distance")
    )
    
    # Query for articles excluding the source, ordering by cosine similarity (lower distance is better).
    query = (
        db.query(ProcessedArticle, distance_expr)
          .filter(ProcessedArticle.article_id != article_id)
          .order_by(asc(distance_expr))
          .limit(50)
          .all()
    )
    
    return query

# Example usage:
if __name__ == "__main__":
    from app.db.session import SessionLocal  # your session maker
    db = SessionLocal()
    try:
        example_article_id = "016d46e0-5e3e-441b-9bc2-ad21751483be"
        similar_articles = get_top_50_cosine_similar_articles(db, example_article_id)

        candidates = [art for art, _ in similar_articles]

    # 2) rerank those 50 with cross‑encoder
        query_text = db.query(ProcessedArticle).get(example_article_id).cleaned_text
        top5 = rerank_top_k(query_text, candidates, top_n=5)

        # 3) Print or return the final top‑5
        for art, score in top5:
            print(f"{art.article_id} → cross‑encoder score {score:.4f}")
        
        for article, distance in similar_articles:
            print(f"Article ID: {article.article_id}, Cosine Distance: {distance}")
    finally:
        db.close()
