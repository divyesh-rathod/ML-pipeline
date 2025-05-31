# app/db/models/user_read.py
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class UserRead(Base):
    __tablename__ = "user_reads"
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), primary_key=True)
    read_at    = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
