import { useState } from 'react'
import Sidebar from '../components/Sidebar'
import { User, Camera, Save, ChevronLeft } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { useToast } from '../components/Toast'

const settingsNav = [
  { icon: User, label: 'الملف الشخصي', path: '/app/settings/profile' },
  { icon: User, label: 'النماذج', path: '/app/settings/models' },
  { icon: User, label: 'المظهر', path: '/app/settings/appearance' },
  { icon: User, label: 'الدردشة', path: '/app/settings' },
  { icon: User, label: 'الأمان', path: '/app/settings' },
]

export default function ProfileSettings() {
  const location = useLocation()
  const { success } = useToast()
  const [form, setForm] = useState({
    name: 'أحمد محمد',
    email: 'ahmed@example.com',
    username: 'ahmed_dev',
    bio: 'مطور ويب شغوف بالتقنية والذكاء الاصطناعي'
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    await new Promise(resolve => setTimeout(resolve, 1000))
    setLoading(false)
    success('تم حفظ التغييرات بنجاح!')
  }

  return (
    <div className="flex min-h-screen bg-bg-primary">
      <Sidebar />
      
      <main className="flex-1 mr-[280px] p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-syne font-bold text-3xl mb-2">الملف الشخصي</h1>
          <p className="text-text-secondary">إدارة معلوماتك الشخصية</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Settings Navigation */}
          <div className="lg:col-span-1">
            <div className="card">
              <h2 className="font-syne font-semibold mb-4">الإعدادات</h2>
              <nav className="space-y-1">
                {settingsNav.map((item, i) => (
                  <Link
                    key={i}
                    to={item.path}
                    className={`nav-item ${
                      location.pathname === item.path ? 'active' : ''
                    }`}
                  >
                    <item.icon size={18} />
                    <span>{item.label}</span>
                    <ChevronLeft size={16} className="mr-auto text-text-muted" />
                  </Link>
                ))}
              </nav>
            </div>
          </div>

          {/* Profile Content */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit} className="card space-y-6">
              {/* Avatar */}
              <div className="flex items-center gap-6">
                <div className="relative">
                  <div className="w-24 h-24 rounded-2xl bg-bg-hover flex items-center justify-center text-4xl">
                    👤
                  </div>
                  <button
                    type="button"
                    className="absolute -bottom-2 -left-2 w-8 h-8 rounded-full bg-accent-primary flex items-center justify-center text-white hover:bg-accent-secondary transition-colors"
                  >
                    <Camera size={14} />
                  </button>
                </div>
                <div>
                  <h3 className="font-syne font-semibold">صورة الملف الشخصي</h3>
                  <p className="text-sm text-text-muted">PNG, JPG حتى 2MB</p>
                </div>
              </div>

              {/* Name */}
              <div>
                <label className="block text-sm text-text-secondary mb-2">الاسم الكامل</label>
                <input
                  type="text"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="input-field"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm text-text-secondary mb-2">البريد الإلكتروني</label>
                <input
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className="input-field"
                  disabled
                />
                <p className="text-xs text-text-muted mt-1">البريد الإلكتروني غير قابل للتعديل</p>
              </div>

              {/* Username */}
              <div>
                <label className="block text-sm text-text-secondary mb-2">اسم المستخدم</label>
                <input
                  type="text"
                  value={form.username}
                  onChange={(e) => setForm({ ...form, username: e.target.value })}
                  className="input-field font-mono"
                  dir="ltr"
                />
              </div>

              {/* Bio */}
              <div>
                <label className="block text-sm text-text-secondary mb-2">نبذة عنك</label>
                <textarea
                  value={form.bio}
                  onChange={(e) => setForm({ ...form, bio: e.target.value })}
                  rows={3}
                  className="input-field resize-none"
                />
              </div>

              {/* Submit */}
              <div className="flex items-center justify-between pt-4 border-t border-border">
                <p className="text-xs text-text-muted">آخر تحديث: منذ ساعة</p>
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary flex items-center gap-2"
                >
                  {loading ? (
                    <span className="animate-spin">⟳</span>
                  ) : (
                    <Save size={18} />
                  )}
                  <span>حفظ التغييرات</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  )
}