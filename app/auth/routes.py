"""
Real Agents - Authentication API Routes
مسارات API المصادقة
"""

from fastapi import APIRouter, HTTPException, Depends, Body
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
    UserResponse,
    TokenResponse,
    MessageResponse
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
# PUBLIC ROUTES - المسارات العامة
# ============================================================================

@router.post("/register", response_model=dict, summary="تسجيل حساب جديد")
async def register(request: RegisterRequest):
    """
    تسجيل مستخدم جديد
    
    - يرسل رمز تحقق إلى البريد الإلكتروني
    - يجب تفعيل الحساب قبل أول تسجيل دخول
    """
    result = await register_user(
        name=request.name,
        email=request.email,
        password=request.password,
        phone=request.phone
    )
    return {
        "success": True,
        "message": result["message"],
        "user": result["user"],
        "verification_code": result["verification_code"]  # للاختبار
    }


@router.post("/verify-email", response_model=dict, summary="تفعيل البريد الإلكتروني")
async def verify_email(request: VerifyRequest):
    """
    التحقق من البريد الإلكتروني برمز التحقق
    
    - يرجع توكن الدخول عند نجاح التفعيل
    """
    result = await verify_user_email(request.email, request.code)
    return {
        "success": True,
        "message": result["message"],
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user": result["user"]
    }


@router.post("/login", response_model=dict, summary="تسجيل الدخول")
async def login(request: LoginRequest):
    """
    تسجيل الدخول
    
    - يرجع توكن للوصول إلى المسارات المحمية
    - يجب تفعيل الحساب أولاً
    """
    result = await login_user(request.email, request.password)
    return {
        "success": True,
        "message": "تم تسجيل الدخول بنجاح",
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user": result["user"]
    }


@router.post("/resend-code", response_model=dict, summary="إعادة إرسال رمز التحقق")
async def resend_code(request: ResendCodeRequest):
    """
    إعادة إرسال رمز التحقق إلى البريد الإلكتروني
    """
    result = await resend_verification_code(request.email)
    return {
        "success": True,
        "message": result["message"],
        "verification_code": result.get("verification_code")  # للاختبار
    }


@router.post("/forgot-password", response_model=dict, summary="نسيت كلمة المرور")
async def forgot_password(request: ForgotPasswordRequest):
    """
    طلب إعادة تعيين كلمة المرور
    
    - يرسل رمز تحقق إذا كان البريد مسجلاً
    """
    result = await request_password_reset(request.email)
    return {
        "success": True,
        "message": result["message"]
    }


@router.post("/reset-password", response_model=dict, summary="إعادة تعيين كلمة المرور")
async def reset_pwd(request: ResetPasswordRequest):
    """
    إعادة تعيين كلمة المرور بالرمز المرسل إلى البريد
    """
    result = await reset_password(
        request.email,
        request.code,
        request.new_password
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
    request: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    تحديث معلومات المستخدم
    
    - يتطلب توكن وصول صالح
    """
    from .auth_system import update_user
    
    updates = {}
    if request.name:
        updates["name"] = request.name
    if request.phone is not None:
        updates["phone"] = request.phone
    
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
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    تغيير كلمة المرور للمستخدم الحالي
    
    - يتطلب كلمة المرور القديمة
    - يتطلب توكن وصول صالح
    """
    from .auth_system import verify_password, hash_password, load_db, save_db
    
    # التحقق من كلمة المرور القديمة
    user = current_user
    db = load_db()
    for u in db["users"]:
        if u["id"] == current_user["id"]:
            if not verify_password(request.old_password, u["password"]):
                raise HTTPException(
                    status_code=400,
                    detail="كلمة المرور القديمة غير صحيحة"
                )
            
            # تحديث كلمة المرور
            u["password"] = hash_password(request.new_password)
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
    - ملاحظة: في التطبيق الحقيقي، يجب إضافة التوكن إلى قائمة الرفض
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