from sqlalchemy import Column, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserFeedPosition(Base):
    __tablename__ = "user_feed_position"

    user_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    last_read_date = Column(DateTime(timezone=True), nullable=True)
    cursor        = Column(DateTime(timezone=True), nullable=True, default=None)
    updated_at     = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="feed_position", uselist=False)
