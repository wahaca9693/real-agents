"""
Real Agents - Security Module
وحدة الأمان
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
import re


# Rate Limiter
limiter = Limiter(key_func=get_remote_address)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware لإضافة Security Headers"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


def validate_password_strength(password: str) -> tuple[bool, str]:
    """التحقق من قوة كلمة المرور"""
    errors = []
    
    if len(password) < 8:
        errors.append("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
    
    if not re.search(r"[A-Z]", password):
        errors.append("يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل")
    
    if not re.search(r"[a-z]", password):
        errors.append("يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل")
    
    if not re.search(r"[0-9]", password):
        errors.append("يجب أن تحتوي كلمة المرور على رقم واحد على الأقل")
    
    if errors:
        return False, "; ".join(errors)
    
    return True, "كلمة المرور قوية ✓"


def sanitize_input(text: str) -> str:
    """تنظيف المدخلات"""
    if not text:
        return ""
    
    # إزالة HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # إزالة SQL injection patterns
    dangerous_patterns = [
        r"(\b)SELECT(\b)",
        r"(\b)INSERT(\b)",
        r"(\b)UPDATE(\b)",
        r"(\b)DELETE(\b)",
        r"(\b)DROP(\b)",
        r"(\b)UNION(\b)",
        r"(\b)EXEC(\b)",
        r"--",
        r"/\*",
        r"\*/",
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    
    return text.strip()


def generate_password_hash(password: str) -> str:
    """تشفير كلمة المرور"""
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password_hash(password: str, hashed: str) -> bool:
    """التحقق من كلمة المرور"""
    import bcrypt
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False


def generate_tokens(user_id: str, email: str) -> dict:
    """توليد Access و Refresh Tokens"""
    import secrets
    from datetime import datetime, timedelta
    from jose import jwt
    
    JWT_SECRET = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    
    # Access Token (15 دقيقة)
    access_payload = {
        "sub": user_id,
        "email": email,
        "type": "access",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    access_token = jwt.encode(access_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    # Refresh Token (7 أيام)
    refresh_token = secrets.token_hex(32)
    refresh_hash = secrets.hash_token(refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 900  # 15 دقيقة بالثواني
    }


def verify_access_token(token: str) -> dict:
    """التحقق من Access Token"""
    from jose import jwt, JWTError
    
    JWT_SECRET = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise JWTError("Invalid token type")
        return payload
    except JWTError:
        return None


import os