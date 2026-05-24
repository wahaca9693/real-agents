"""
Real Agents - Authentication API Routes
مسارات API المصادقة - مع تحسينات الأمان
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from .auth_system import (
    register_user,
    verify_user_email,
    login_user,
    resend_verification_code,
    request_password_reset,
    reset_password,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

# Import security functions
from app.security import (
    limiter,
    validate_password_strength,
    sanitize_input
)

# ============================================================================
# ROUTER - الموجه
# ============================================================================

router = APIRouter(prefix="/api/auth", tags=["المصادقة"])

# ============================================================================
# REQUEST MODELS - نماذج الطلب
# ============================================================================

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="اسم المستخدم")
    email: EmailStr = Field(..., description="البريد الإلكتروني")
    password: str = Field(..., min_length=8, max_length=100, description="كلمة المرور")
    phone: Optional[str] = Field(None, description="رقم الجوال")

class VerifyRequest(BaseModel):
    email: EmailStr = Field(..., description="البريد الإلكتروني")
    code: str = Field(..., min_length=6, max_length=6, description="رمز التحقق")

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="البريد الإلكتروني")
    password: str = Field(..., description="كلمة المرور")

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh Token")

class ResendCodeRequest(BaseModel):
    email: EmailStr = Field(..., description="البريد الإلكتروني")

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="البريد الإلكتروني")

class ResetPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="البريد الإلكتروني")
    code: str = Field(..., min_length=6, max_length=6, description="رمز التحقق")
    new_password: str = Field(..., min_length=8, max_length=100, description="كلمة المرور الجديدة")

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., description="كلمة المرور القديمة")
    new_password: str = Field(..., min_length=8, max_length=100, description="كلمة المرور الجديدة")

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_client_ip(request: Request) -> str:
    """الحصول على عنوان IP العميل"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

# ============================================================================
# PUBLIC ROUTES - المسارات العامة (مع Rate Limiting)
# ============================================================================

@router.post("/register", response_model=dict, summary="تسجيل حساب جديد")
@limiter.limit("5/minute")
async def register(request: Request, body: RegisterRequest):
    """
    تسجيل مستخدم جديد
    
    - يرسل رمز تحقق إلى البريد الإلكتروني
    - يجب تفعيل الحساب قبل أول تسجيل دخول
    - **Rate Limit**: 5 طلبات في الدقيقة
    """
    # التحقق من قوة كلمة المرور
    is_strong, message = validate_password_strength(body.password)
    if not is_strong:
        raise HTTPException(
            status_code=400,
            detail=f"كلمة المرور ضعيفة: {message}"
        )
    
    result = await register_user(
        name=sanitize_input(body.name),
        email=body.email.lower().strip(),
        password=body.password,
        phone=sanitize_input(body.phone) if body.phone else None
    )
    
    return {
        "success": True,
        "message": result["message"],
        "user": result["user"],
        "verification_code": result["verification_code"]  # للاختبار
    }


@router.post("/verify-email", response_model=dict, summary="تفعيل البريد الإلكتروني")
@limiter.limit("10/minute")
async def verify_email(request: Request, body: VerifyRequest):
    """
    التحقق من البريد الإلكتروني برمز التحقق
    
    - يرجع access_token و refresh_token عند نجاح التفعيل
    """
    result = await verify_user_email(body.email.lower().strip(), body.code)
    return {
        "success": True,
        "message": result["message"],
        "access_token": result["access_token"],
        "refresh_token": result.get("refresh_token", ""),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_expires_in": REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        "user": result["user"]
    }


@router.post("/login", response_model=dict, summary="تسجيل الدخول")
@limiter.limit("10/minute")
async def login(request: Request, body: LoginRequest):
    """
    تسجيل الدخول
    
    - يرجع access_token و refresh_token
    - يجب تفعيل الحساب أولاً
    """
    result = await login_user(body.email.lower().strip(), body.password)
    return {
        "success": True,
        "message": "تم تسجيل الدخول بنجاح",
        "access_token": result["access_token"],
        "refresh_token": result.get("refresh_token", ""),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_expires_in": REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        "user": result["user"]
    }


@router.post("/refresh-token", response_model=dict, summary="تحديث التوكن")
@limiter.limit("20/minute")
async def refresh_token(request: Request, body: RefreshTokenRequest):
    """
    تحديث Access Token باستخدام Refresh Token
    """
    from .auth_system import verify_refresh_token
    
    result = verify_refresh_token(body.refresh_token)
    if not result:
        raise HTTPException(
            status_code=401,
            detail="Refresh Token غير صالح أو منتهي الصلاحية"
        )
    
    return result


@router.post("/resend-code", response_model=dict, summary="إعادة إرسال رمز التحقق")
@limiter.limit("5/minute")
async def resend_code(request: Request, body: ResendCodeRequest):
    """
    إعادة إرسال رمز التحقق إلى البريد الإلكتروني
    """
    result = await resend_verification_code(body.email.lower().strip())
    return {
        "success": True,
        "message": result["message"],
        "verification_code": result.get("verification_code")  # للاختبار
    }


@router.post("/forgot-password", response_model=dict, summary="نسيت كلمة المرور")
@limiter.limit("3/minute")
async def forgot_password(request: Request, body: ForgotPasswordRequest):
    """
    طلب إعادة تعيين كلمة المرور
    
    - يرسل رمز تحقق إذا كان البريد مسجلاً
    """
    result = await request_password_reset(body.email.lower().strip())
    return {
        "success": True,
        "message": result["message"]
    }


@router.post("/reset-password", response_model=dict, summary="إعادة تعيين كلمة المرور")
@limiter.limit("5/minute")
async def reset_pwd(request: Request, body: ResetPasswordRequest):
    """
    إعادة تعيين كلمة المرور بالرمز المرسل إلى البريد
    """
    # التحقق من قوة كلمة المرور الجديدة
    is_strong, message = validate_password_strength(body.new_password)
    if not is_strong:
        raise HTTPException(
            status_code=400,
            detail=f"كلمة المرور الجديدة ضعيفة: {message}"
        )
    
    result = await reset_password(
        body.email.lower().strip(),
        body.code,
        body.new_password
    )
    return {
        "success": True,
        "message": result["message"]
    }


# ============================================================================
# PROTECTED ROUTES - المسارات المحمية
# ============================================================================

@router.get("/me", response_model=dict, summary="معلومات المستخدم الحالي")
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    الحصول على معلومات المستخدم الحالي
    
    - يتطلب توكن وصول صالح
    """
    return {
        "success": True,
        "user": current_user
    }


@router.put("/profile", response_model=dict, summary="تحديث الملف الشخصي")
async def update_profile(
    body: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    تحديث معلومات المستخدم
    
    - يتطلب توكن وصول صالح
    """
    from .auth_system import update_user
    
    updates = {}
    if body.name:
        updates["name"] = sanitize_input(body.name)
    if body.phone is not None:
        updates["phone"] = sanitize_input(body.phone) if body.phone else None
    
    if updates:
        updated_user = update_user(current_user["id"], updates)
        updated_user.pop("password", None)
        return {
            "success": True,
            "message": "تم تحديث الملف الشخصي",
            "user": updated_user
        }
    
    return {
        "success": True,
        "message": "لم يتم تغيير أي بيانات",
        "user": current_user
    }


@router.post("/change-password", response_model=dict, summary="تغيير كلمة المرور")
async def change_password(
    body: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    تغيير كلمة المرور للمستخدم الحالي
    
    - يتطلب كلمة المرور القديمة
    - يتطلب توكن وصول صالح
    """
    from .auth_system import verify_password, hash_password, load_db, save_db
    
    # التحقق من كلمة المرور القديمة
    db = load_db()
    for u in db["users"]:
        if u["id"] == current_user["id"]:
            if not verify_password(body.old_password, u["password"]):
                raise HTTPException(
                    status_code=400,
                    detail="كلمة المرور القديمة غير صحيحة"
                )
            
            # التحقق من قوة كلمة المرور الجديدة
            is_strong, message = validate_password_strength(body.new_password)
            if not is_strong:
                raise HTTPException(
                    status_code=400,
                    detail=f"كلمة المرور الجديدة ضعيفة: {message}"
                )
            
            # تحديث كلمة المرور
            u["password"] = hash_password(body.new_password)
            u["updated_at"] = datetime.now().isoformat()
            save_db(db)
            break
    
    return {
        "success": True,
        "message": "تم تغيير كلمة المرور بنجاح"
    }


@router.post("/logout", response_model=dict, summary="تسجيل الخروج")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    تسجيل الخروج
    
    - يتطلب توكن وصول صالح
    """
    return {
        "success": True,
        "message": "تم تسجيل الخروج بنجاح"
    }


# ============================================================================
# DEBUG/HEALTH ROUTES - مسارات التصحيح
# ============================================================================

@router.get("/health", response_model=dict, summary="فحص حالة المصادقة")
async def auth_health():
    """
    فحص حالة نظام المصادقة
    """
    from .auth_system import init_database
    
    try:
        init_database()
        return {
            "status": "healthy",
            "auth_system": "active",
            "security_features": {
                "rate_limiting": True,
                "password_strength_check": True,
                "jwt_access_tokens": True,
                "jwt_refresh_tokens": True,
                "input_sanitization": True
            },
            "features": [
                "user_registration",
                "email_verification",
                "login",
                "password_reset",
                "profile_management"
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }