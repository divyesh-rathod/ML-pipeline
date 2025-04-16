from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    link = Column(Text, nullable=False, unique=True)
    pub_date = Column(Text)
    description = Column(Text)
    # Categories stored as an array of text:
    categories = Column(ARRAY(Text))


    processed_article = relationship(
        "ProcessedArticle",
        back_populates="article",
        uselist=False  # ensures 1:1 instead of 1:many
    )