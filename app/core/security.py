from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configure bcrypt to auto-truncate passwords to 72 bytes
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False  # Auto-truncate instead of raising error
)
ALGORITHM = settings.JWT_ALGORITHM

def create_access_token(subject: Union[str, Any], role: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "role": role}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Encode and truncate password to 72 bytes for bcrypt 5.0.0 compatibility
    password_bytes = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(password_bytes, hashed_password)

def get_password_hash(password: str) -> str:
    # Bcrypt 5.0.0 requires passwords to be 72 bytes or less
    # Encode to bytes and truncate to ensure compatibility
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes)
