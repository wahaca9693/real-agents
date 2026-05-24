import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Eye, EyeOff, Mail, Lock, User, Loader2, Check } from 'lucide-react'
import api from '../services/api'

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [verificationEmail, setVerificationEmail] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess(false)

    if (form.password !== form.confirmPassword) {
      setError('كلمات المرور غير متطابقة')
      return
    }

    if (form.password.length < 8) {
      setError('كلمة المرور يجب أن تكون 8 أحرف على الأقل')
      return
    }

    setLoading(true)

    try {
      const data = await api.register(form.name, form.email, form.password)

      if (data.success) {
        setSuccess(true)
        setVerificationEmail(form.email)
        // Navigate to verification page after 3 seconds
        setTimeout(() => {
          navigate('/verify-email', { state: { email: form.email } })
        }, 3000)
      } else {
        setError(data.detail || 'حدث خطأ أثناء التسجيل')
      }
    } catch (err) {
      setError(err.message || 'تعذر الاتصال بالخادم')
    }

    setLoading(false)
  }

  const passwordRequirements = [
    { test: form.password.length >= 8, text: '8 أحرف على الأقل' },
    { test: /[A-Z]/.test(form.password), text: 'حرف كبير واحد' },
    { test: /[0-9]/.test(form.password), text: 'رقم واحد' },
  ]

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
              <h2 className="font-syne font-bold text-xl mb-2">تم إنشاء الحساب!</h2>
              <p className="text-text-secondary mb-4">
                تم إرسال رمز التحقق إلى بريدك الإلكتروني
              </p>
              <p className="text-sm text-text-muted mb-4">
                {verificationEmail}
              </p>
              <Link 
                to="/verify-email" 
                state={{ email: verificationEmail }}
                className="btn-primary inline-block px-8 py-3"
              >
                تحقق من البريد
              </Link>
            </div>
          ) : (
            <>
              <h1 className="font-syne font-bold text-2xl text-center mb-2">إنشاء حساب جديد</h1>
              <p className="text-text-secondary text-center mb-8">
                انضم إلينا وابدأ رحلتك مع الوكلاء البرمجيين
              </p>

              {error && (
                <div className="mb-6 p-4 rounded-xl bg-danger/10 border border-danger/30 text-danger text-sm">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Name */}
                <div>
                  <label className="block text-sm text-text-secondary mb-2">الاسم الكامل</label>
                  <div className="relative">
                    <User size={20} className="absolute right-4 top-1/2 -translate-y-1/2 text-text-muted" />
                    <input
                      type="text"
                      value={form.name}
                      onChange={(e) => setForm({ ...form, name: e.target.value })}
                      placeholder="أحمد محمد"
                      required
                      className="input-field pr-12"
                    />
                  </div>
                </div>

                {/* Email */}
                <div>
                  <label className="block text-sm text-text-secondary mb-2">البريد الإلكتروني</label>
                  <div className="relative">
                    <Mail size={20} className="absolute right-4 top-1/2 -translate-y-1/2 text-text-muted" />
                    <input
                      type="email"
                      value={form.email}
                      onChange={(e) => setForm({ ...form, email: e.target.value })}
                      placeholder="example@email.com"
                      required
                      className="input-field pr-12"
                    />
                  </div>
                </div>

                {/* Password */}
                <div>
                  <label className="block text-sm text-text-secondary mb-2">كلمة المرور</label>
                  <div className="relative">
                    <Lock size={20} className="absolute right-4 top-1/2 -translate-y-1/2 text-text-muted" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={form.password}
                      onChange={(e) => setForm({ ...form, password: e.target.value })}
                      placeholder="••••••••"
                      required
                      className="input-field pr-12 pl-12"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-secondary"
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                  
                  {/* Password Strength */}
                  {form.password && (
                    <div className="mt-3 space-y-1">
                      {passwordRequirements.map((req, i) => (
                        <div key={i} className="flex items-center gap-2 text-xs">
                          <Check size={14} className={req.test ? 'text-success' : 'text-text-muted'} />
                          <span className={req.test ? 'text-success' : 'text-text-muted'}>
                            {req.text}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Confirm Password */}
                <div>
                  <label className="block text-sm text-text-secondary mb-2">تأكيد كلمة المرور</label>
                  <div className="relative">
                    <Lock size={20} className="absolute right-4 top-1/2 -translate-y-1/2 text-text-muted" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={form.confirmPassword}
                      onChange={(e) => setForm({ ...form, confirmPassword: e.target.value })}
                      placeholder="••••••••"
                      required
                      className="input-field pr-12"
                    />
                  </div>
                </div>

                {/* Terms */}
                <div className="flex items-start gap-3">
                  <input
                    type="checkbox"
                    id="terms"
                    required
                    className="mt-1 w-4 h-4 rounded border-border text-accent-primary focus:ring-accent-primary"
                  />
                  <label htmlFor="terms" className="text-sm text-text-secondary">
                    أوافق على{' '}
                    <button type="button" className="text-accent-primary hover:underline">
                      شروط الاستخدام
                    </button>{' '}
                    و{' '}
                    <button type="button" className="text-accent-primary hover:underline">
                      سياسة الخصوصية
                    </button>
                  </label>
                </div>

                {/* Submit */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full btn-primary py-4 flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <Loader2 size={20} className="animate-spin" />
                  ) : (
                    'إنشاء الحساب'
                  )}
                </button>
              </form>

              {/* Login Link */}
              <p className="text-center mt-6 text-text-secondary">
                لديك حساب بالفعل؟{' '}
                <Link to="/login" className="text-accent-primary hover:underline">
                  سجل دخولك
                </Link>
              </p>
            </>
          )}
        </div>
      </motion.div>
    </div>
  )
}