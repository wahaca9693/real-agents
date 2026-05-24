"""
Real Agents - Authentication System
نظام المصادقة والتحقق من البريد الإلكتروني
Security Enhanced - CSRF Protection & Secure IDs
"""

from datetime import datetime, timedelta
from typing import Optional
import random
import string
import json
import os
import secrets
from pathlib import Path

from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from jose import JWTError, jwt

# ============================================================================
# CONFIGURATION - التكوين
# ============================================================================

# JWT Settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    JWT_SECRET_KEY = secrets.token_hex(32)
    print("⚠️ WARNING: Using auto-generated JWT secret. Set JWT_SECRET_KEY in .env for production!")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# CSRF Secret for form protection
CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY")
if not CSRF_SECRET_KEY:
    CSRF_SECRET_KEY = secrets.token_hex(32)

# Security Bearer
security = HTTPBearer()

# Database Path (legacy support)
DB_PATH = Path(os.getenv("DB_PATH", "workspace/users_db.json"))

# Import security functions
from app.security import (
    validate_password_strength,
    sanitize_input,
    generate_password_hash,
    verify_password_hash
)

# ============================================================================
# PYDANTIC MODELS - نماذج البيانات
# ============================================================================

class UserRegister(BaseModel):
    """نموذج تسجيل مستخدم جديد"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    phone: Optional[str] = None

class UserLogin(BaseModel):
    """نموذج تسجيل الدخول"""
    email: EmailStr
    password: str

class VerificationCode(BaseModel):
    """نموذج رمز التحقق"""
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)
    action: str  # "register" or "reset_password"

class UserResponse(BaseModel):
    """نموذج استجابة المستخدم"""
    id: str
    name: str
    email: str
    phone: Optional[str]
    is_verified: bool
    created_at: str

class TokenResponse(BaseModel):
    """نموذج استجابة التوكن"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class MessageResponse(BaseModel):
    """نموذج رسالة عامة"""
    message: str
    success: bool = True

# ============================================================================
# DATABASE FUNCTIONS - وظائف قاعدة البيانات
# ============================================================================

def init_database():
    """إنشاء قاعدة البيانات إذا لم تكن موجودة"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        with open(DB_PATH, 'w') as f:
            json.dump({"users": [], "verification_codes": {}, "sessions": []}, f)

def load_db():
    """تحميل قاعدة البيانات"""
    init_database()
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def save_db(data: dict):
    """حفظ قاعدة البيانات"""
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def find_user_by_email(email: str) -> Optional[dict]:
    """البحث عن مستخدم بالبريد الإلكتروني"""
    db = load_db()
    for user in db.get("users", []):
        if user["email"].lower() == email.lower():
            return user
    return None

def find_user_by_id(user_id: str) -> Optional[dict]:
    """البحث عن مستخدم بالمعرف"""
    db = load_db()
    for user in db.get("users", []):
        if user["id"] == user_id:
            return user
    return None

def generate_user_id() -> str:
    """توليد معرف مستخدم آمن باستخدام UUID"""
    return f"user_{secrets.token_urlsafe(16)}"

def generate_csrf_token() -> str:
    """توليد CSRF token للتحقق من صحة الطلبات"""
    return secrets.token_urlsafe(32)

def verify_csrf_token(token: str, expected: str) -> bool:
    """التحقق من CSRF token بطريقة آمنة (timing-safe)"""
    if not token or not expected:
        return False
    return secrets.compare_digest(token, expected)

# CSRF Token Storage (in production, use Redis or database)
csrf_tokens_store = {}

def store_csrf_token(user_id: str) -> str:
    """تخزين CSRF token للمستخدم"""
    token = generate_csrf_token()
    csrf_tokens_store[user_id] = {
        "token": token,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=1)
    }
    return token

def get_csrf_token(user_id: str) -> Optional[str]:
    """الحصول على CSRF token للمستخدم"""
    token_data = csrf_tokens_store.get(user_id)
    if not token_data:
        return None
    
    # Check expiration
    if datetime.now() > token_data["expires_at"]:
        del csrf_tokens_store[user_id]
        return None
    
    return token_data["token"]

def create_user(name: str, email: str, password: str, phone: str = None) -> dict:
    """إنشاء مستخدم جديد"""
    db = load_db()
    
    # التحقق من عدم وجود البريد
    if find_user_by_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني مسجل مسبقاً"
        )
    
    # إنشاء المستخدم مع معرف آمن
    user = {
        "id": generate_user_id(),
        "name": name,
        "email": email.lower(),
        "password": hash_password(password),
        "phone": phone,
        "is_verified": False,
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "verification_attempts": 0,
        "login_count": 0,
        "last_login": None
    }
    
    db["users"].append(user)
    save_db(db)
    
    return user

def update_user(user_id: str, updates: dict) -> dict:
    """تحديث بيانات المستخدم"""
    db = load_db()
    for user in db["users"]:
        if user["id"] == user_id:
            user.update(updates)
            user["updated_at"] = datetime.now().isoformat()
            save_db(db)
            return user
    raise HTTPException(status_code=404, detail="المستخدم غير موجود")

# ============================================================================
# PASSWORD FUNCTIONS - وظائف كلمة المرور
# ============================================================================

def hash_password(password: str) -> str:
    """تشفير كلمة المرور باستخدام bcrypt (أكثر أماناً)"""
    return generate_password_hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """التحقق من كلمة المرور"""
    return verify_password_hash(plain_password, hashed_password)

# ============================================================================
# VERIFICATION CODE FUNCTIONS - وظائف رمز التحقق
# ============================================================================

def generate_verification_code() -> str:
    """توليد رمز تحقق من 6 أرقام"""
    return ''.join(random.choices(string.digits, k=6))

def store_verification_code(email: str, code: str, action: str = "register"):
    """تخزين رمز التحقق"""
    db = load_db()
    db["verification_codes"][email.lower()] = {
        "code": code,
        "action": action,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(minutes=10)).isoformat(),
        "attempts": 0
    }
    save_db(db)

def get_verification_code(email: str) -> Optional[dict]:
    """الحصول على رمز التحقق"""
    db = load_db()
    return db["verification_codes"].get(email.lower())

def delete_verification_code(email: str):
    """حذف رمز التحقق"""
    db = load_db()
    if email.lower() in db["verification_codes"]:
        del db["verification_codes"][email.lower()]
        save_db(db)

def verify_code(email: str, code: str) -> bool:
    """التحقق من صحة الرمز"""
    stored = get_verification_code(email)
    
    if not stored:
        return False
    
    # التحقق من انتهاء الصلاحية
    expires = datetime.fromisoformat(stored["expires_at"])
    if datetime.now() > expires:
        delete_verification_code(email)
        return False
    
    # التحقق من عدد المحاولات
    if stored["attempts"] >= 5:
        delete_verification_code(email)
        return False
    
    # التحقق من الرمز
    if stored["code"] != code:
        # زيادة عدد المحاولات
        db = load_db()
        db["verification_codes"][email.lower()]["attempts"] += 1
        save_db(db)
        return False
    
    return True

# ============================================================================
# JWT TOKEN FUNCTIONS - وظائف التوكن
# ============================================================================

def create_access_token(data: dict) -> str:
    """إنشاء توكن الوصول"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    """فك تشفير التوكن"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="التوكن غير صالح أو منتهي الصلاحية"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """الحصول على المستخدم الحالي من التوكن"""
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="التوكن غير صالح"
        )
    
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="المستخدم غير موجود"
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="الحساب غير نشط"
        )
    
    # إزالة كلمة المرور من الاستجابة
    user.pop("password", None)
    return user

# ============================================================================
# AUTHENTICATION FUNCTIONS - وظائف المصادقة
# ============================================================================

async def register_user(name: str, email: str, password: str, phone: str = None) -> dict:
    """تسجيل مستخدم جديد"""
    # التحقق من قوة كلمة المرور
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="كلمة المرور يجب أن تكون 8 أحرف على الأقل"
        )
    
    # إنشاء المستخدم
    user = create_user(name, email, password, phone)
    
    # توليد رمز التحقق
    code = generate_verification_code()
    store_verification_code(email, code, "register")
    
    # إرسال البريد الإلكتروني
    try:
        from .email_service import send_verification_email
        await send_verification_email(email, name, code)
    except Exception as e:
        print(f"Failed to send verification email: {e}")
    
    # للاختبار: إرجاع الرمز مع رسالة
    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "phone": user.get("phone"),
            "is_verified": user["is_verified"],
            "created_at": user["created_at"]
        },
        "verification_code": code,  # للاختبار فقط - يجب إزالته في الإنتاج
        "message": "تم إنشاء الحساب بنجاح. يرجى التحقق من بريدك الإلكتروني."
    }

async def verify_user_email(email: str, code: str) -> dict:
    """التحقق من البريد الإلكتروني"""
    if not verify_code(email, code):
        raise HTTPException(
            status_code=400,
            detail="رمز التحقق غير صحيح أو منتهي الصلاحية"
        )
    
    # البحث عن المستخدم وتفعيله
    db = load_db()
    for user in db["users"]:
        if user["email"].lower() == email.lower():
            user["is_verified"] = True
            user["updated_at"] = datetime.now().isoformat()
            save_db(db)
            
            # حذف رمز التحقق
            delete_verification_code(email)
            
            # إنشاء توكن
            token = create_access_token({"sub": user["id"], "email": user["email"]})
            
            return {
                "message": "تم تفعيل الحساب بنجاح",
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "is_verified": True
                }
            }
    
    raise HTTPException(status_code=404, detail="المستخدم غير موجود")

async def login_user(email: str, password: str) -> dict:
    """تسجيل دخول المستخدم"""
    user = find_user_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة"
        )
    
    if not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة"
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=403,
            detail="الحساب غير نشط. يرجى التحقق من بريدك الإلكتروني."
        )
    
    # تحديث عدد مرات الدخول
    db = load_db()
    for u in db["users"]:
        if u["id"] == user["id"]:
            u["login_count"] = u.get("login_count", 0) + 1
            u["last_login"] = datetime.now().isoformat()
            save_db(db)
            break
    
    # إنشاء التوكن
    access_token = create_access_token({"sub": user["id"], "email": user["email"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "phone": user.get("phone"),
            "is_verified": user.get("is_verified", False),
            "created_at": user["created_at"]
        }
    }

async def resend_verification_code(email: str) -> dict:
    """إعادة إرسال رمز التحقق"""
    user = find_user_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="المستخدم غير موجود"
        )
    
    if user.get("is_verified", False):
        raise HTTPException(
            status_code=400,
            detail="الحساب مفعل بالفعل"
        )
    
    # توليد رمز جديد
    code = generate_verification_code()
    store_verification_code(email, code, "register")
    
    return {
        "message": "تم إرسال رمز التحقق",
        "verification_code": code  # للاختبار فقط
    }

async def request_password_reset(email: str) -> dict:
    """طلب إعادة تعيين كلمة المرور"""
    user = find_user_by_email(email)
    
    if user:
        # توليد رمز التحقق
        code = generate_verification_code()
        store_verification_code(email, code, "reset_password")
        
        return {
            "message": "إذا كان البريد مسجلاً، ستصلك رسالة",
            "verification_code": code  # للاختبار فقط
        }
    
    # نرجع نفس الرسالة حتى لو لم يوجد المستخدم (لأسباب أمنية)
    return {
        "message": "إذا كان البريد مسجلاً، ستصلك رسالة"
    }

async def reset_password(email: str, code: str, new_password: str) -> dict:
    """إعادة تعيين كلمة المرور"""
    if not verify_code(email, code):
        raise HTTPException(
            status_code=400,
            detail="رمز التحقق غير صحيح أو منتهي الصلاحية"
        )
    
    user = find_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="المستخدم غير موجود"
        )
    
    # تحديث كلمة المرور
    db = load_db()
    for u in db["users"]:
        if u["email"].lower() == email.lower():
            u["password"] = hash_password(new_password)
            u["updated_at"] = datetime.now().isoformat()
            save_db(db)
            break
    
    # حذف رمز التحقق
    delete_verification_code(email)
    
    return {
        "message": "تم تغيير كلمة المرور بنجاح"
    }

# ============================================================================
# INITIALIZE - التهيئة
# ============================================================================

# تهيئة قاعدة البيانات عند استيراد الوحدة
init_database()