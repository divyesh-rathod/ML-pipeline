from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import your models so they are registered with the Base
from app.db.models import article  # etc.