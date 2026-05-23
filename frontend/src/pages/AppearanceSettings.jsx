import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { User, Check } from 'lucide-react'
import { useToast } from '../components/Toast'

const settingsNav = [
  { icon: User, label: 'الملف الشخصي', path: '/app/settings/profile' },
  { icon: User, label: 'النماذج', path: '/app/settings/models' },
  { icon: User, label: 'المظهر', path: '/app/settings/appearance' },
  { icon: User, label: 'الدردشة', path: '/app/settings' },
  { icon: User, label: 'الأمان', path: '/app/settings' },
]

const themes = [
  { id: 'dark', name: 'داكن', emoji: '🌙', colors: ['#0A0D12', '#111520', '#4F8EF7'] },
  { id: 'light', name: 'فاتح', emoji: '☀️', colors: ['#FFFFFF', '#F8FAFC', '#3B82F6'] },
  { id: 'blue', name: 'أزرق', emoji: '💙', colors: ['#0F172A', '#1E293B', '#3B82F6'] },
  { id: 'green', name: 'أخضر', emoji: '🌿', colors: ['#052E16', '#166534', '#22C55E'] },
]

const fontSizes = [
  { id: 'small', name: 'صغير', size: '14px' },
  { id: 'medium', name: 'متوسط', size: '16px' },
  { id: 'large', name: 'كبير', size: '18px' },
]

export default function AppearanceSettings() {
  const location = useLocation()
  const { success } = useToast()
  const [selectedTheme, setSelectedTheme] = useState('dark')
  const [selectedFontSize, setSelectedFontSize] = useState('medium')

  const handleSave = () => {
    success('تم حفظ إعدادات المظهر!')
  }

  return (
    <div className="flex min-h-screen bg-bg-primary">
      <Sidebar />
      
      <main className="flex-1 mr-[280px] p-8">
        <div className="mb-8">
          <h1 className="font-syne font-bold text-3xl mb-2">المظهر</h1>
          <p className="text-text-secondary">تخصيص شكل المنصة</p>
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
                  </Link>
                ))}
              </nav>
            </div>
          </div>

          {/* Appearance Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Theme Selection */}
            <div className="card">
              <h2 className="font-syne font-semibold text-xl mb-4">السمة</h2>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {themes.map(theme => (
                  <button
                    key={theme.id}
                    onClick={() => setSelectedTheme(theme.id)}
                    className={`relative p-4 rounded-xl border transition-all ${
                      selectedTheme === theme.id
                        ? 'border-accent-primary bg-accent-primary/10'
                        : 'border-border hover:border-accent-primary/30'
                    }`}
                  >
                    {/* Color Preview */}
                    <div className="flex gap-1 mb-3">
                      {theme.colors.map((color, i) => (
                        <div
                          key={i}
                          className="w-6 h-6 rounded-md"
                          style={{ backgroundColor: color }}
                        />
                      ))}
                    </div>
                    <div className="text-2xl mb-1">{theme.emoji}</div>
                    <div className="text-sm font-medium">{theme.name}</div>
                    
                    {selectedTheme === theme.id && (
                      <div className="absolute top-2 left-2 w-6 h-6 rounded-full bg-accent-primary flex items-center justify-center">
                        <Check size={14} className="text-white" />
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Font Size */}
            <div className="card">
              <h2 className="font-syne font-semibold text-xl mb-4">حجم الخط</h2>
              <div className="flex gap-4">
                {fontSizes.map(font => (
                  <button
                    key={font.id}
                    onClick={() => setSelectedFontSize(font.id)}
                    className={`flex-1 p-4 rounded-xl border transition-all ${
                      selectedFontSize === font.id
                        ? 'border-accent-primary bg-accent-primary/10'
                        : 'border-border hover:border-accent-primary/30'
                    }`}
                  >
                    <div 
                      className="mb-2" 
                      style={{ fontSize: font.size }}
                    >
                      نص تجريبي
                    </div>
                    <div className="text-sm font-medium">{font.name}</div>
                    <div className="text-xs text-text-muted font-mono">{font.size}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Compact Mode */}
            <div className="card">
              <h2 className="font-syne font-semibold text-xl mb-4">العرض</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium mb-1">الوضع المدمج</h3>
                    <p className="text-sm text-text-muted">تقليل المسافات بين العناصر</p>
                  </div>
                  <button className="toggle" />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium mb-1">عرض.compact للرسائل</h3>
                    <p className="text-sm text-text-muted">عرض الرسائل بشكل مدمج</p>
                  </div>
                  <button className="toggle active" />
                </div>
              </div>
            </div>

            {/* Save Button */}
            <div className="flex justify-end">
              <button onClick={handleSave} className="btn-primary px-8">
                حفظ التغييرات
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}