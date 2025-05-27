# app/services/user_service.py

from app.db.session import SessionLocal
from app.db.models.user import User
from passlib.context import CryptContext
from app.schemas.user_schema import UserCreate
import datetime

# set up a password‐hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user_in: UserCreate) -> User:
    """
    :param user_in: Pydantic model with {name, email, phone_number, password}
    :returns: newly created User ORM object
    """
    db = SessionLocal()
    try:
        # hash the incoming password
        hashed_pw = pwd_context.hash(user_in.password)

        # build the User ORM object
        new_user = User(
            name=user_in.name,
            email=user_in.email,
            phone_number=user_in.phone_number,
            password=hashed_pw,
            # created_at / updated_at default handled by the model
        )

        # save
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    finally:
        db.close()

def get_user_by_email(email: str) -> User:
    """
    :param email: email address to search for
    :returns: User ORM object if found, else None
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    finally:
        db.close()
