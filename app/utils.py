from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from app.core.config import settings

# ✅ Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt. Trims to 72 characters due to bcrypt limitation.
    """
    password = password[:72]  # Prevent bcrypt errors if password is too long
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify hashed password against plain password.
    """
    plain = plain[:72]  # Ensure same bcrypt limit
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT token with expiration.
    """
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "exp": expire,
        "sub": str(subject)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def decode_token(token: str):
    """
    Decode JWT token safely with error handling.
    """
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_data
    except JWTError:
        return None  # Token invalid or expired
