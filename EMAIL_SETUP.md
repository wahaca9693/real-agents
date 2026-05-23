# 📧 Real Agents - Email Service Setup Guide

## 🎯 Overview
This system supports multiple email services with automatic fallback. You can configure one or more services.

---

## 🆓 FREE Email Services (No Credit Card Required)

### 1. Resend ⭐ RECOMMENDED
**Free Tier:** 100 emails/month

1. Go to: https://resend.com/signup
2. Sign up with email (GitHub/Google)
3. Go to: https://resend.com/api-keys
4. Click "Create API Key"
5. Copy the key

**Config:**
```bash
RESEND_API_KEY=re_xxxxx_your_key_here
```

---

### 2. Mailgun
**Free Tier:** 5,000 emails/month

1. Go to: https://www.mailgun.com/signup/
2. Sign up (no credit card needed for trial)
3. Go to: https://app.mailgun.com/app/domains
4. Click "Add Domain" (use sandbox for testing)
5. Copy API key from: https://app.mailgun.com/app/account/security

**Config:**
```bash
MAILGUN_API_KEY=key-xxxxx
MAILGUN_DOMAIN=your-domain.mailgun.org
MAILGUN_BASE_URL=https://api.mailgun.net/v3
```

---

### 3. Brevo (Sendinblue)
**Free Tier:** 300 emails/day

1. Go to: https://www.brevo.com/signup
2. Sign up with email
3. Go to: https://app.brevo.com/developers/api-key
4. Copy your API key

**Config:**
```bash
BREVO_API_KEY=your_api_key_here
```

---

### 4. SendGrid (Twilio)
**Free Tier:** 100 emails/day

1. Go to: https://signup.sendgrid.com/
2. Choose "Free" plan
3. Verify email
4. Go to: https://app.sendgrid.com/settings/api_keys
5. Create API Key
6. Verify sender (add domain or single sender)

**Config:**
```bash
SENDGRID_API_KEY=SG.xxxxx
```

---

### 5. Gmail SMTP (No API needed!)
**Free:** Unlimited (with restrictions)

1. Enable 2FA on your Gmail account
2. Go to: https://myaccount.google.com/security
3. Click "App passwords"
4. Select "Mail" and "Other (Custom name)"
5. Enter "Real Agents" and generate
6. Copy the 16-character password

**Config:**
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=xxxx_xxxx_xxxx_xxxx
SMTP_FROM_NAME=Real Agents
```

---

## 🚀 Quick Setup

### For Testing (No Setup Required)
The system will print emails to console by default!

### For Production

1. Create `.env` file in project root:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API key:
```bash
# Choose one (or multiple for fallback)
RESEND_API_KEY=re_your_key
```

3. Restart the server:
```bash
python main.py
```

---

## 🔄 Automatic Fallback

The system tries services in this order:
1. Resend
2. Mailgun
3. Brevo
4. SMTP
5. Console (fallback)

If one fails, it automatically tries the next!

---

## 📊 Check Status

```bash
curl http://localhost:8000/api/health
```

---

## 🛠️ Troubleshooting

### Email not sending?
1. Check API key is correct
2. Check the service is active
3. Check spam folder
4. For Gmail, make sure "Less secure apps" is OFF (use App Password instead)

### Need to test?
```bash
# Test email service status
python -c "from app.auth.email_service import get_email_service_status; print(get_email_service_status())"
```

---

## 📋 Summary of Services

| Service | Free Tier | Daily Limit | Credit Card |
|---------|-----------|-------------|-------------|
| Resend | 100/month | ~3/day | No |
| Mailgun | 5,000/month | ~166/day | No (trial) |
| Brevo | 300/day | 300/day | No |
| SendGrid | 100/day | 100/day | No |
| Gmail SMTP | Unlimited | 500/day | No |

---

## ⚠️ Important Notes

1. **Test Mode:** Without any API key, emails print to console
2. **Rate Limits:** Free tiers have limits - don't spam!
3. **Verification:** Some services require domain/email verification
4. **Spam:** Don't send unsolicited emails