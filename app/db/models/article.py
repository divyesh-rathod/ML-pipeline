from sqlalchemy import Boolean, Column, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY
import uuid
from app.db.base import Base
from sqlalchemy.orm import relationship
import sqlalchemy as sa

class Article(Base):
    __tablename__ = 'articles'
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default="gen_random_uuid()"
    )
    title = Column(Text, nullable=False)
    link = Column(Text, nullable=False, unique=True)
    pub_date = Column(Text)
    description = Column(Text)
    categories = Column(ARRAY(Text))
    processed = Column(Boolean, nullable=False, server_default=sa.text("false"))


    processed_article = relationship("ProcessedArticle",back_populates="article",uselist=False)


