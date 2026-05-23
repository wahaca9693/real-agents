import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Eye, EyeOff, Mail, Lock, Loader2 } from 'lucide-react'
import { useAuth } from '../App'

const API_URL = 'http://localhost:8000/api/auth'

export default function Login() {
  const navigate = useNavigate()
  const { setIsAuthenticated } = useAuth()
  const [form, setForm] = useState({ email: '', password: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: form.email,
          password: form.password
        })
      })

      const data = await response.json()

      if (data.success) {
        localStorage.setItem('auth_token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        setIsAuthenticated(true)
        navigate('/app')
      } else {
        setError(data.detail || 'البريد أو كلمة المرور غير صحيحة')
      }
    } catch (err) {
      setError('تعذر الاتصال بالخادم')
    }

    setLoading(false)
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
          <h1 className="font-syne font-bold text-2xl text-center mb-2">مرحباً بعودتك!</h1>
          <p className="text-text-secondary text-center mb-8">
            سجل دخولك للمتابعة إلى لوحة التحكم
          </p>

          {error && (
            <div className="mb-6 p-4 rounded-xl bg-danger/10 border border-danger/30 text-danger text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
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
            </div>

            {/* Forgot Password */}
            <div className="text-left">
              <button type="button" className="text-sm text-accent-primary hover:underline">
                نسيت كلمة المرور؟
              </button>
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
                'تسجيل الدخول'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="flex items-center gap-4 my-6">
            <div className="flex-1 h-px bg-border" />
            <span className="text-text-muted text-sm">أو</span>
            <div className="flex-1 h-px bg-border" />
          </div>

          {/* Google */}
          <button className="w-full py-4 rounded-xl border border-border hover:bg-bg-hover transition-colors flex items-center justify-center gap-3">
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <span className="text-text-secondary">تسجيل بـ Google</span>
          </button>

          {/* Register Link */}
          <p className="text-center mt-6 text-text-secondary">
            ليس لديك حساب؟{' '}
            <Link to="/register" className="text-accent-primary hover:underline">
              سجل الآن
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}