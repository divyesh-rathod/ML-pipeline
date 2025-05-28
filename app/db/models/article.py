from sqlalchemy import Column, Text, Boolean,text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base

class Article(Base):
    __tablename__ = 'articles'

  
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,                        
        server_default=func.gen_random_uuid(),     
        unique=True,
        index=True
    )

    title = Column(Text, nullable=False)
    link = Column(Text, nullable=False, unique=True)
    pub_date = Column(Text)
    description = Column(Text)
    categories = Column(ARRAY(Text))
    processed = Column(Boolean, server_default=text("false"), nullable=False)

    processed_article = relationship(
        "ProcessedArticle",
        back_populates="article",
        uselist=False
    )
