import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { User, Plus, Check, X, Star, Trash2, Settings } from 'lucide-react'
import { useToast } from '../components/Toast'

const settingsNav = [
  { icon: User, label: 'الملف الشخصي', path: '/app/settings/profile' },
  { icon: User, label: 'النماذج', path: '/app/settings/models' },
  { icon: User, label: 'المظهر', path: '/app/settings/appearance' },
  { icon: User, label: 'الدردشة', path: '/app/settings' },
  { icon: User, label: 'الأمان', path: '/app/settings' },
]

const savedModels = [
  { id: 1, name: 'GPT-4o', provider: 'OpenAI', status: 'connected', isDefault: true },
  { id: 2, name: 'Claude 3', provider: 'Anthropic', status: 'disconnected', isDefault: false },
]

export default function ModelsSettings() {
  const location = useLocation()
  const { success, error: showError } = useToast()
  const [models, setModels] = useState(savedModels)
  const [showAddModal, setShowAddModal] = useState(false)
  const [testingConnection, setTestingConnection] = useState(false)
  const [testResult, setTestResult] = useState(null)

  const handleTestConnection = async () => {
    setTestingConnection(true)
    setTestResult(null)
    await new Promise(resolve => setTimeout(resolve, 2000))
    setTestResult(true)
    setTestingConnection(false)
    success('الاتصال ناجح!')
  }

  const handleSetDefault = (id) => {
    setModels(models.map(m => ({
      ...m,
      isDefault: m.id === id
    })))
    success('تم تعيين النموذج كافتراضي')
  }

  const handleDelete = (id) => {
    setModels(models.filter(m => m.id !== id))
    success('تم حذف النموذج')
  }

  return (
    <div className="flex min-h-screen bg-bg-primary">
      <Sidebar />
      
      <main className="flex-1 mr-[280px] p-8">
        <div className="mb-8">
          <h1 className="font-syne font-bold text-3xl mb-2">النماذج</h1>
          <p className="text-text-secondary">إدارة نماذج الذكاء الاصطناعي المرتبطة</p>
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

          {/* Models Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Current Model */}
            <div className="card">
              <h2 className="font-syne font-semibold text-xl mb-4">النموذج الحالي</h2>
              <div className="flex items-center justify-between p-4 rounded-xl bg-success/10 border border-success/30">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-success/20 flex items-center justify-center">
                    <span className="w-3 h-3 rounded-full bg-success animate-pulse" />
                  </div>
                  <div>
                    <div className="font-syne font-semibold">GPT-4o</div>
                    <div className="text-xs text-text-muted">متصل — OpenAI API</div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button className="px-4 py-2 rounded-lg border border-border hover:bg-bg-hover text-sm">
                    تغيير
                  </button>
                  <button className="px-4 py-2 rounded-lg border border-border hover:bg-bg-hover text-sm text-danger">
                    فصل
                  </button>
                </div>
              </div>
            </div>

            {/* Saved Models */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-syne font-semibold text-xl">النماذج المحفوظة</h2>
                <button 
                  onClick={() => setShowAddModal(true)}
                  className="btn-primary flex items-center gap-2 text-sm py-2"
                >
                  <Plus size={16} />
                  <span>إضافة نموذج</span>
                </button>
              </div>

              <div className="space-y-3">
                {models.map(model => (
                  <div 
                    key={model.id}
                    className="flex items-center justify-between p-4 rounded-xl bg-bg-hover"
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${
                        model.status === 'connected' ? 'bg-success' : 'bg-text-muted'
                      }`} />
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-medium">{model.name}</span>
                          {model.isDefault && (
                            <span className="badge badge-info text-xs">
                              <Star size={10} />
                              <span>افتراضي</span>
                            </span>
                          )}
                        </div>
                        <div className="text-xs text-text-muted">{model.provider}</div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      {!model.isDefault && (
                        <button 
                          onClick={() => handleSetDefault(model.id)}
                          className="px-3 py-1.5 rounded-lg text-xs border border-border hover:bg-bg-card"
                        >
                          تعيين كافتراضي
                        </button>
                      )}
                      <button 
                        onClick={() => handleDelete(model.id)}
                        className="p-2 rounded-lg text-danger hover:bg-danger/10"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Add Model Modal */}
            {showAddModal && (
              <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
                <div className="bg-bg-secondary border border-border rounded-2xl p-6 w-full max-w-md">
                  <h2 className="font-syne font-bold text-xl mb-6">إضافة نموذج جديد</h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm text-text-secondary mb-2">المزود</label>
                      <select className="input-field">
                        <option>OpenAI</option>
                        <option>Anthropic</option>
                        <option>Google Gemini</option>
                        <option>Custom</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm text-text-secondary mb-2">مفتاح API</label>
                      <input 
                        type="password" 
                        placeholder="sk-..." 
                        className="input-field font-mono"
                        dir="ltr"
                      />
                    </div>

                    <div>
                      <label className="block text-sm text-text-secondary mb-2">النموذج</label>
                      <select className="input-field">
                        <option>GPT-4o</option>
                        <option>GPT-4-turbo</option>
                        <option>GPT-3.5-turbo</option>
                      </select>
                    </div>

                    <div className="flex gap-3 pt-4">
                      <button 
                        onClick={() => setShowAddModal(false)}
                        className="flex-1 py-3 rounded-xl border border-border"
                      >
                        إلغاء
                      </button>
                      <button 
                        onClick={handleTestConnection}
                        disabled={testingConnection}
                        className="flex-1 py-3 rounded-xl border border-border hover:bg-bg-hover flex items-center justify-center gap-2"
                      >
                        {testingConnection ? (
                          <span className="animate-spin">⟳</span>
                        ) : testResult === true ? (
                          <Check size={18} className="text-success" />
                        ) : testResult === false ? (
                          <X size={18} className="text-danger" />
                        ) : null}
                        <span>اختبار الاتصال</span>
                      </button>
                    </div>

                    <button className="w-full btn-primary py-3">
                      حفظ
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}