import { useState, useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Mail, Lock, Loader2, Check, AlertCircle } from 'lucide-react'
import api from '../services/api'

export default function VerifyEmail() {
  const location = useLocation()
  const navigate = useNavigate()
  const [email, setEmail] = useState(location.state?.email || '')
  const [code, setCode] = useState(['', '', '', '', '', ''])
  const [loading, setLoading] = useState(false)
  const [resendLoading, setResendLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [token, setToken] = useState('')

  // Auto-focus first input
  useEffect(() => {
    const input = document.querySelector('input[data-index="0"]')
    if (input) input.focus()
  }, [])

  const handleCodeChange = (index, value) => {
    if (value.length > 1) {
      // Handle paste
      const chars = value.slice(0, 6).split('')
      const newCode = [...code]
      chars.forEach((char, i) => {
        if (index + i < 6) {
          newCode[index + i] = char
        }
      })
      setCode(newCode)
      // Focus last filled or next empty
      const nextEmpty = newCode.findIndex((c, i) => i >= index && !c)
      const focusIndex = nextEmpty === -1 ? 5 : nextEmpty
      document.querySelector(`input[data-index="${focusIndex}"]`)?.focus()
    } else {
      const newCode = [...code]
      newCode[index] = value
      setCode(newCode)
      // Auto-advance
      if (value && index < 5) {
        document.querySelector(`input[data-index="${index + 1}"]`)?.focus()
      }
    }
  }

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      document.querySelector(`input[data-index="${index - 1}"]`)?.focus()
    }
  }

  const handleVerify = async () => {
    const verificationCode = code.join('')
    if (verificationCode.length !== 6) {
      setError('يرجى إدخال الرمز كاملاً')
      return
    }

    setLoading(true)
    setError('')

    try {
      const data = await api.verifyEmail(email, verificationCode)

      if (data.success) {
        setSuccess(true)
        setToken(data.access_token)
        // Save token to localStorage
        localStorage.setItem('auth_token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        // Redirect to dashboard after 2 seconds
        setTimeout(() => {
          navigate('/app')
        }, 2000)
      } else {
        setError(data.detail || 'الرمز غير صحيح')
      }
    } catch (err) {
      setError(err.message || 'تعذر الاتصال بالخادم')
    }

    setLoading(false)
  }

  const handleResendCode = async () => {
    setResendLoading(true)
    setError('')

    try {
      const response = await fetch('/api/auth/resend-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })

      const data = await response.json()

      if (data.success) {
        setError('')
        // Show success message
        alert('تم إعادة إرسال الرمز!')
      } else {
        setError(data.detail || 'حدث خطأ')
      }
    } catch (err) {
      setError('تعذر الاتصال بالخادم')
    }

    setResendLoading(false)
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-bg-primary bg-gradient-radial">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center">
              <span className="text-2xl">🧠</span>
            </div>
            <span className="font-syne font-bold text-2xl gradient-text">Real Agents</span>
          </Link>
        </div>

        {/* Form Card */}
        <div className="glass border border-border rounded-2xl p-8">
          {success ? (
            <div className="text-center">
              <div className="w-16 h-16 bg-success/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Check size={32} className="text-success" />
              </div>
              <h2 className="font-syne font-bold text-xl mb-2">تم تفعيل الحساب!</h2>
              <p className="text-text-secondary mb-4">
                مرحباً بك في منصة Real Agents
              </p>
              <div className="animate-pulse text-text-muted">
                جاري التحويل إلى لوحة التحكم...
              </div>
            </div>
          ) : (
            <>
              <div className="text-center mb-8">
                <div className="w-16 h-16 bg-accent-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Mail size={32} className="text-accent-primary" />
                </div>
                <h1 className="font-syne font-bold text-2xl mb-2">التحقق من البريد</h1>
                <p className="text-text-secondary">
                  أدخل الرمز المكون من 6 أرقام المرسل إلى
                </p>
                <p className="text-accent-primary font-bold mt-1">{email}</p>
              </div>

              {error && (
                <div className="mb-6 p-4 rounded-xl bg-danger/10 border border-danger/30 text-danger text-sm flex items-center gap-2">
                  <AlertCircle size={18} />
                  {error}
                </div>
              )}

              {/* Code Input */}
              <div className="flex justify-center gap-3 mb-8" dir="ltr">
                {code.map((digit, index) => (
                  <input
                    key={index}
                    type="text"
                    data-index={index}
                    maxLength={6}
                    value={digit}
                    onChange={(e) => handleCodeChange(index, e.target.value)}
                    onKeyDown={(e) => handleKeyDown(index, e)}
                    className="w-12 h-14 text-center text-2xl font-bold bg-bg-secondary border border-border rounded-xl focus:border-accent-primary focus:outline-none transition-colors"
                    disabled={loading}
                  />
                ))}
              </div>

              {/* Verify Button */}
              <button
                onClick={handleVerify}
                disabled={loading || code.join('').length !== 6}
                className="w-full btn-primary py-4 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 size={20} className="animate-spin" />
                    جاري التحقق...
                  </>
                ) : (
                  <>
                    <Check size={20} />
                    تحقق من الرمز
                  </>
                )}
              </button>

              {/* Resend Code */}
              <div className="text-center mt-6">
                <p className="text-text-secondary text-sm mb-2">
                  لم تستلم الرمز؟
                </p>
                <button
                  onClick={handleResendCode}
                  disabled={resendLoading}
                  className="text-accent-primary hover:underline text-sm disabled:opacity-50"
                >
                  {resendLoading ? 'جاري الإرسال...' : 'إعادة إرسال الرمز'}
                </button>
              </div>

              {/* Change Email */}
              <div className="text-center mt-4">
                <Link to="/register" className="text-text-muted hover:text-text-secondary text-sm">
                  استخدام بريد إلكتروني آخر
                </Link>
              </div>
            </>
          )}
        </div>
      </motion.div>
    </div>
  )
}