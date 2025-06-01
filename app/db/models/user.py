from sqlalchemy import Column, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class User(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    name = Column(Text,      nullable=False)
    email = Column(Text,     nullable=False, unique=True, index=True)
    phone_number = Column(Text, nullable=False, unique=True, index=True)
    password = Column(Text,  nullable=False)
    profile_picture = Column(Text, nullable=True)
    is_blocked = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    feed_position = relationship("UserFeedPosition", back_populates="user", uselist=False)