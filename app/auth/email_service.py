"""
Real Agents - Email Service
خدمة إرسال البريد الإلكتروني
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional
import resend
import requests

# ============================================================================
# EMAIL CONFIGURATION - تكوين البريد
# ============================================================================

# Resend API (Recommended - Free 100 emails/month)
# Get your API key from: https://resend.com/api-keys
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

# SMTP Configuration (Gmail/Outlook/etc.)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Real Agents")

# Mailgun API (Free 5,000 emails/month)
# Get your API key from: https://mailgun.com
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "")
MAILGUN_BASE_URL = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net/v3")

# Brevo API (Free 300 emails/day)
# Get your API key from: https://www.brevo.com
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
BREVO_BASE_URL = "https://api.brevo.com"

# SendGrid API (Free 100 emails/day)
# Get your API key from: https://sendgrid.com
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_BASE_URL = "https://api.sendgrid.com/v3"

# Fallback email for testing
TEST_EMAIL = os.getenv("TEST_EMAIL", "test@example.com")

# ============================================================================
# EMAIL TEMPLATES - قوالب البريد
# ============================================================================

def get_verification_email_template(name: str, code: str) -> tuple:
    """قالب بريد التحقق من البريد"""
    subject = "🔐 رمز التحقق من منصة Real Agents"
    
    html_body = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #4F8EF7, #7C5CFC); padding: 40px; text-align: center; color: white; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .header p {{ margin: 10px 0 0; opacity: 0.9; }}
            .content {{ padding: 40px; text-align: center; }}
            .code-box {{ background: #f8f9fa; border: 2px dashed #4F8EF7; border-radius: 12px; padding: 30px; margin: 20px 0; }}
            .code {{ font-size: 48px; font-weight: bold; color: #4F8EF7; letter-spacing: 8px; direction: ltr; display: inline-block; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 8px; margin-top: 20px; text-align: right; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 التحقق من البريد الإلكتروني</h1>
                <p>منصة الوكلاء البرمجيين</p>
            </div>
            <div class="content">
                <p style="font-size: 18px; color: #333;">مرحباً <strong>{name}</strong>،</p>
                <p style="color: #666;">تم إنشاء حسابك في منصة Real Agents. استخدم الرمز التالي للتحقق من بريدك الإلكتروني:</p>
                
                <div class="code-box">
                    <div class="code">{code}</div>
                </div>
                
                <p style="color: #666;">هذا الرمز صالح لمدة <strong>10 دقائق</strong> فقط.</p>
                
                <div class="warning">
                    ⚠️ لا تشارك هذا الرمز مع أي شخص. فريقنا لن يطلب منك هذا الرمز أبداً.
                </div>
            </div>
            <div class="footer">
                <p>إذا لم تقم بإنشاء هذا الحساب، يرجى تجاهل هذه الرسالة.</p>
                <p>© 2024 منصة Real Agents - جميع الحقوق محفوظة</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    مرحباً {name}،
    
    تم إنشاء حسابك في منصة Real Agents.
    
    رمز التحقق: {code}
    
    هذا الرمز صالح لمدة 10 دقائق فقط.
    
    إذا لم تقم بإنشاء هذا الحساب، يرجى تجاهل هذه الرسالة.
    """
    
    return subject, html_body, text_body


def get_welcome_email_template(name: str) -> tuple:
    """قالب بريد الترحيب"""
    subject = "🎉 مرحباً بك في منصة Real Agents!"
    
    html_body = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #4F8EF7, #7C5CFC); padding: 40px; text-align: center; color: white; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .content {{ padding: 40px; }}
            .feature {{ background: #f8f9fa; border-radius: 12px; padding: 20px; margin: 15px 0; }}
            .feature h3 {{ color: #4F8EF7; margin-top: 0; }}
            .cta {{ text-align: center; margin-top: 30px; }}
            .cta a {{ background: linear-gradient(135deg, #4F8EF7, #7C5CFC); color: white; padding: 15px 40px; border-radius: 8px; text-decoration: none; display: inline-block; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 مرحباً بك!</h1>
                <p>فريق تطوير كامل بين يديك</p>
            </div>
            <div class="content">
                <p style="font-size: 18px;">مرحباً <strong>{name}</strong>،</p>
                <p>تم تفعيل حسابك بنجاح! يمكنك الآن الاستفادة من خدمات منصة Real Agents:</p>
                
                <div class="feature">
                    <h3>🧠 6 وكلاء ذكيين</h3>
                    <p>فريق من الوكلاء المتخصصين يعملون معاً لتنفيذ مشاريعك</p>
                </div>
                
                <div class="feature">
                    <h3>⚡ سرعة فائقة</h3>
                    <p>إنجاز المهام المعقدة في دقائق بدلاً من ساعات</p>
                </div>
                
                <div class="feature">
                    <h3>🔒 أمان عالي</h3>
                    <p>حماية متقدمة لبياناتك ورمزك المصدري</p>
                </div>
                
                <div class="cta">
                    <a href="#">ابدأ مشروعك الأول</a>
                </div>
            </div>
            <div class="footer">
                <p>© 2024 منصة Real Agents - جميع الحقوق محفوظة</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    مرحباً {name}،
    
    تم تفعيل حسابك بنجاح!
    
    يمكنك الآن الاستفادة من خدمات منصة Real Agents:
    - 6 وكلاء ذكيين
    - سرعة فائقة
    - أمان عالي
    
    ابدأ مشروعك الأول الآن!
    """
    
    return subject, html_body, text_body


def get_password_reset_email_template(name: str, code: str) -> tuple:
    """قالب بريد إعادة تعيين كلمة المرور"""
    subject = "🔑 طلب إعادة تعيين كلمة المرور - Real Agents"
    
    html_body = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #EF4444, #DC2626); padding: 40px; text-align: center; color: white; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .content {{ padding: 40px; text-align: center; }}
            .code-box {{ background: #f8f9fa; border: 2px dashed #EF4444; border-radius: 12px; padding: 30px; margin: 20px 0; }}
            .code {{ font-size: 48px; font-weight: bold; color: #EF4444; letter-spacing: 8px; direction: ltr; display: inline-block; }}
            .warning {{ background: #fee2e2; border-left: 4px solid #EF4444; padding: 15px; border-radius: 8px; margin-top: 20px; text-align: right; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔑 إعادة تعيين كلمة المرور</h1>
                <p>منصة Real Agents</p>
            </div>
            <div class="content">
                <p style="font-size: 18px; color: #333;">مرحباً <strong>{name}</strong>،</p>
                <p style="color: #666;">طلبنا إعادة تعيين كلمة المرور لحسابك. استخدم الرمز التالي:</p>
                
                <div class="code-box">
                    <div class="code">{code}</div>
                </div>
                
                <div class="warning">
                    ⚠️ إذا لم تطلب إعادة تعيين كلمة المرور، تجاهل هذه الرسالة فوراً.
                </div>
                
                <p style="color: #666; margin-top: 20px;">هذا الرمز صالح لمدة <strong>10 دقائق</strong> فقط.</p>
            </div>
            <div class="footer">
                <p>© 2024 منصة Real Agents - جميع الحقوق محفوظة</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    مرحباً {name}،
    
    طلب إعادة تعيين كلمة المرور.
    
    رمز التحقق: {code}
    
    هذا الرمز صالح لمدة 10 دقائق فقط.
    
    إذا لم تطلب ذلك، تجاهل هذه الرسالة.
    """
    
    return subject, html_body, text_body


def get_password_changed_email_template(name: str) -> tuple:
    """قالب بريد تأكيد تغيير كلمة المرور"""
    subject = "✅ تم تغيير كلمة المرور بنجاح - Real Agents"
    
    html_body = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #22C55E, #16A34A); padding: 40px; text-align: center; color: white; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .content {{ padding: 40px; text-align: center; }}
            .success-icon {{ font-size: 80px; margin-bottom: 20px; }}
            .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; border-radius: 8px; margin-top: 20px; text-align: right; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ تم تغيير كلمة المرور</h1>
                <p>منصة Real Agents</p>
            </div>
            <div class="content">
                <div class="success-icon">✓</div>
                <p style="font-size: 18px;">مرحباً <strong>{name}</strong>،</p>
                <p style="color: #666;">تم تغيير كلمة المرور لحسابك بنجاح.</p>
                
                <div class="warning">
                    ⚠️ إذا لم تقم أنت بهذا التغيير، تواصل معنا فوراً.
                </div>
            </div>
            <div class="footer">
                <p>© 2024 منصة Real Agents - جميع الحقوق محفوظة</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    مرحباً {name}،
    
    تم تغيير كلمة المرور لحسابك بنجاح.
    
    إذا لم تقم أنت بهذا التغيير، تواصل معنا فوراً.
    """
    
    return subject, html_body, text_body


# ============================================================================
# EMAIL SENDING FUNCTIONS - وظائف إرسال البريد
# ============================================================================

def send_email_smtp(to_email: str, subject: str, html_body: str, text_body: str) -> bool:
    """إرسال بريد باستخدام SMTP"""
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"⚠️ SMTP not configured. Email to {to_email} not sent.")
        print(f"   Subject: {subject}")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = f"{SMTP_FROM_NAME} <{SMTP_USER}>"
        msg['To'] = to_email
        
        # إضافة الإصدارات
        msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        # الاتصال والإرسال
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False


def send_email_resend(to_email: str, subject: str, html_body: str) -> bool:
    """إرسال بريد باستخدام Resend API"""
    if not RESEND_API_KEY:
        print(f"⚠️ Resend API not configured. Email to {to_email} not sent.")
        return False
    
    try:
        resend.api_key = RESEND_API_KEY
        
        r = resend.Emails.send({
            "from": f"Real Agents <onboarding@resend.dev>",
            "to": to_email,
            "subject": subject,
            "html": html_body
        })
        
        print(f"✅ Email sent via Resend to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email via Resend to {to_email}: {e}")
        return False


def send_email_mailgun(to_email: str, subject: str, html_body: str, text_body: str) -> bool:
    """إرسال بريد باستخدام Mailgun API"""
    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        print(f"⚠️ Mailgun not configured. Email to {to_email} not sent.")
        return False
    
    try:
        response = requests.post(
            f"{MAILGUN_BASE_URL}/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Real Agents <mailgun@{MAILGUN_DOMAIN}>",
                "to": to_email,
                "subject": subject,
                "html": html_body,
                "text": text_body
            }
        )
        
        if response.status_code == 200:
            print(f"✅ Email sent via Mailgun to {to_email}")
            return True
        else:
            print(f"❌ Mailgun error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send email via Mailgun to {to_email}: {e}")
        return False


def send_email_brevo(to_email: str, subject: str, html_body: str, text_body: str) -> bool:
    """إرسال بريد باستخدام Brevo API (Sendinblue)"""
    if not BREVO_API_KEY:
        print(f"⚠️ Brevo not configured. Email to {to_email} not sent.")
        return False
    
    try:
        response = requests.post(
            f"{BREVO_BASE_URL}/v3/smtp/email",
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "sender": {"name": "Real Agents", "email": "noreply@realagents.com"},
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html_body,
                "textContent": text_body
            }
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Email sent via Brevo to {to_email}")
            return True
        else:
            print(f"❌ Brevo error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send email via Brevo to {to_email}: {e}")
        return False


def send_email_sendgrid(to_email: str, subject: str, html_body: str, text_body: str) -> bool:
    """إرسال بريد باستخدام SendGrid API"""
    if not SENDGRID_API_KEY:
        print(f"⚠️ SendGrid not configured. Email to {to_email} not sent.")
        return False
    
    try:
        response = requests.post(
            f"{SENDGRID_BASE_URL}/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": "noreply@realagents.com", "name": "Real Agents"},
                "subject": subject,
                "content": [
                    {"type": "text/plain", "value": text_body},
                    {"type": "text/html", "value": html_body}
                ]
            }
        )
        
        if response.status_code in [200, 201, 202]:
            print(f"✅ Email sent via SendGrid to {to_email}")
            return True
        else:
            print(f"❌ SendGrid error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send email via SendGrid to {to_email}: {e}")
        return False


def get_available_email_services() -> list:
    """التحقق من خدمات البريد المتاحة"""
    services = []
    
    if RESEND_API_KEY:
        services.append("resend")
    if SMTP_USER and SMTP_PASSWORD:
        services.append("smtp")
    if MAILGUN_API_KEY and MAILGUN_DOMAIN:
        services.append("mailgun")
    if BREVO_API_KEY:
        services.append("brevo")
    if SENDGRID_API_KEY:
        services.append("sendgrid")
    
    return services


async def send_email_with_fallback(to_email: str, subject: str, html_body: str, text_body: str) -> bool:
    """إرسال بريد مع fallback بين الخدمات المتاحة"""
    services = get_available_email_services()
    
    # محاولة كل خدمة متاحة
    if "resend" in services:
        if send_email_resend(to_email, subject, html_body):
            return True
    
    if "mailgun" in services:
        if send_email_mailgun(to_email, subject, html_body, text_body):
            return True
    
    if "brevo" in services:
        if send_email_brevo(to_email, subject, html_body, text_body):
            return True
    
    if "sendgrid" in services:
        if send_email_sendgrid(to_email, subject, html_body, text_body):
            return True
    
    if "smtp" in services:
        if send_email_smtp(to_email, subject, html_body, text_body):
            return True
    
    # إذا لم تعمل أي خدمة، اطبع في الكونسول
    print(f"\n" + "="*60)
    print(f"📧 EMAIL (Fallback)")
    print(f"="*60)
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(f"="*60 + "\n")
    return True


async def send_verification_email(to_email: str, name: str, code: str) -> bool:
    """إرسال بريد التحقق"""
    subject, html_body, text_body = get_verification_email_template(name, code)
    return await send_email_with_fallback(to_email, subject, html_body, text_body)


async def send_welcome_email(to_email: str, name: str) -> bool:
    """إرسال بريد الترحيب"""
    subject, html_body, text_body = get_welcome_email_template(name)
    return await send_email_with_fallback(to_email, subject, html_body, text_body)


async def send_password_reset_email(to_email: str, name: str, code: str) -> bool:
    """إرسال بريد إعادة تعيين كلمة المرور"""
    subject, html_body, text_body = get_password_reset_email_template(name, code)
    return await send_email_with_fallback(to_email, subject, html_body, text_body)


async def send_password_changed_notification(to_email: str, name: str) -> bool:
    """إرسال إشعار تغيير كلمة المرور"""
    subject, html_body, text_body = get_password_changed_email_template(name)
    return await send_email_with_fallback(to_email, subject, html_body, text_body)


def get_email_service_status() -> dict:
    """التحقق من حالة خدمات البريد"""
    return {
        "resend": bool(RESEND_API_KEY),
        "mailgun": bool(MAILGUN_API_KEY and MAILGUN_DOMAIN),
        "brevo": bool(BREVO_API_KEY),
        "sendgrid": bool(SENDGRID_API_KEY),
        "smtp": bool(SMTP_USER and SMTP_PASSWORD),
        "active_services": get_available_email_services()
    }