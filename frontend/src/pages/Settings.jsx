import { Link, useLocation } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { User, Brain, Palette, MessageSquare, Shield, ChevronLeft } from 'lucide-react'

const settingsNav = [
  { icon: User, label: 'الملف الشخصي', path: '/app/settings/profile' },
  { icon: Brain, label: 'النماذج', path: '/app/settings/models' },
  { icon: Palette, label: 'المظهر', path: '/app/settings/appearance' },
  { icon: MessageSquare, label: 'الدردشة', path: '/app/settings' },
  { icon: Shield, label: 'الأمان', path: '/app/settings' },
]

export default function Settings() {
  const location = useLocation()

  return (
    <div className="flex min-h-screen bg-bg-primary">
      <Sidebar />
      
      <main className="flex-1 mr-[280px] p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-syne font-bold text-3xl mb-2">الإعدادات</h1>
          <p className="text-text-secondary">إدارة حسابك وتفضيلاتك</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Settings Navigation */}
          <div className="lg:col-span-1">
            <div className="card">
              <h2 className="font-syne font-semibold mb-4">القائمة</h2>
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

          {/* Settings Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Chat Settings */}
            <div className="card">
              <h2 className="font-syne font-semibold text-xl mb-6">إعدادات الدردشة</h2>
              
              <div className="space-y-6">
                {/* Save Conversations */}
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium mb-1">حفظ المحادثات</h3>
                    <p className="text-sm text-text-muted">حفظ جميع محادثاتك تلقائياً</p>
                  </div>
                  <button className="toggle active" />
                </div>

                {/* Show Timestamps */}
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium mb-1">عرض الوقت</h3>
                    <p className="text-sm text-text-muted">عرض وقت كل رسالة</p>
                  </div>
                  <button className="toggle active" />
                </div>

                {/* Sound Notifications */}
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium mb-1">إشعارات صوتية</h3>
                    <p className="text-sm text-text-muted">تنبيه عند اكتمال المهام</p>
                  </div>
                  <button className="toggle" />
                </div>
              </div>
            </div>

            {/* Delete All Data */}
            <div className="card border-danger/30">
              <h2 className="font-syne font-semibold text-xl mb-4 text-danger">خطر</h2>
              <p className="text-sm text-text-secondary mb-4">
                هذا الإجراء يحذف جميع محادثاتك نهائياً ولا يمكن التراجع عنه.
              </p>
              <button className="px-6 py-2.5 rounded-xl bg-danger/10 text-danger border border-danger/30 hover:bg-danger/20 transition-colors">
                حذف كل المحادثات
              </button>
            </div>

            {/* Restore */}
            <div className="card">
              <h2 className="font-syne font-semibold text-xl mb-4">استعادة</h2>
              <p className="text-sm text-text-secondary mb-4">
                استعادة محادثات محذوفة خلال آخر 30 يوماً
              </p>
              <button className="px-6 py-2.5 rounded-xl border border-border hover:bg-bg-hover transition-colors">
                عرض المحذوفات
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}