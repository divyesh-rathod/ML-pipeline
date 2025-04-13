from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
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
