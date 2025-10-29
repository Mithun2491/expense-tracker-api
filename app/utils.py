from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional, Union
from app.core.config import settings

# ✅ Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt with security best practices.
    """
    password = password[:72]  # bcrypt limit
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version.
    """
    plain_password = plain_password[:72]  # ensure compatibility
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JWT access token.
    `subject` is usually the user ID or username.
    """
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": str(subject),
        "exp": expire
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    Returns payload if valid, None if expired/invalid.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
