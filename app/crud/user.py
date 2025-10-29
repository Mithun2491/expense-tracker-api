from sqlalchemy.orm import Session
from app.models.user import User
from app.utils import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    """
    Fetch a user by email.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str, full_name: str):
    """
    Create a new user and hash the password.
    """
    hashed_password = get_password_hash(password)
    db_user = User(email=email, hashed_password=hashed_password, full_name=full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    """
    Check if user exists and verify password.
    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
