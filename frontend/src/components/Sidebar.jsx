import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  MessageSquare, 
  Plus, 
  Settings, 
  ChevronDown,
  MoreHorizontal,
  Edit3,
  Lock,
  Trash2,
  LogOut,
  User,
  Users,
  Home
} from 'lucide-react'

const mockChats = [
  { id: 1, name: 'مشروع الموقع', status: 'active', lastMessage: 'تم إنشاء الملفات...' },
  { id: 2, name: 'تطبيق الجوال', status: 'working', lastMessage: 'جارٍ التطوير...' },
  { id: 3, name: 'API Backend', status: 'closed', lastMessage: 'تم الاكتمال' },
  { id: 4, name: 'قاعدة البيانات', status: 'closed', lastMessage: 'تم الإنشاء' },
]

export default function Sidebar() {
  const location = useLocation()
  const [chats, setChats] = useState(mockChats)
  const [activeChat, setActiveChat] = useState(null)
  const [showNewChat, setShowNewChat] = useState(false)
  const [newChatName, setNewChatName] = useState('')
  const [user, setUser] = useState(null)

  useEffect(() => {
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    }
  }, [])

  const handleNewChat = () => {
    if (!newChatName.trim()) return
    const newChat = {
      id: Date.now(),
      name: newChatName,
      status: 'active',
      lastMessage: 'محادثة جديدة'
    }
    setChats([newChat, ...chats])
    setNewChatName('')
    setShowNewChat(false)
  }

  const handleDeleteChat = (id) => {
    setChats(chats.filter(c => c.id !== id))
  }

  const statusColors = {
    active: 'bg-success',
    working: 'bg-warning',
    closed: 'bg-text-muted'
  }

  return (
    <aside className="sidebar flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center">
            <span className="text-xl">🧠</span>
          </div>
          <div>
            <h1 className="font-syne font-bold text-lg gradient-text">Real Agents</h1>
            <p className="text-xs text-text-muted">منصة الوكلاء البرمجيين</p>
          </div>
        </div>

        {/* Navigation Links */}
        <div className="mb-4 space-y-1">
          <Link
            to="/app"
            className={`flex items-center gap-3 px-3 py-2 rounded-xl transition-all ${
              location.pathname === '/app' ? 'bg-accent-primary/20 text-accent-primary' : 'hover:bg-bg-hover'
            }`}
          >
            <Home size={18} />
            <span className="text-sm font-medium">الرئيسية</span>
          </Link>
          <Link
            to="/app/team"
            className={`flex items-center gap-3 px-3 py-2 rounded-xl transition-all ${
              location.pathname === '/app/team' ? 'bg-accent-primary/20 text-accent-primary' : 'hover:bg-bg-hover'
            }`}
          >
            <Users size={18} />
            <span className="text-sm font-medium">فريق العمل</span>
          </Link>
        </div>

        {/* New Chat Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setShowNewChat(true)}
          className="w-full py-3 px-4 rounded-xl font-medium text-white flex items-center justify-center gap-2"
          style={{
            background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))'
          }}
        >
          <Plus size={20} />
          <span>+ مشروع جديد</span>
        </motion.button>
      </div>

      {/* New Chat Modal */}
      <AnimatePresence>
        {showNewChat && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="modal-backdrop"
            onClick={() => setShowNewChat(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={e => e.stopPropagation()}
              className="bg-bg-secondary border border-border rounded-2xl p-6 w-full max-w-md mx-4"
            >
              <h2 className="font-syne font-bold text-xl mb-4">مشروع جديد</h2>
              <input
                type="text"
                value={newChatName}
                onChange={e => setNewChatName(e.target.value)}
                placeholder="اسم المشروع..."
                className="input-field mb-4"
                autoFocus
                onKeyDown={e => e.key === 'Enter' && handleNewChat()}
              />
              <div className="flex gap-3">
                <button
                  onClick={() => setShowNewChat(false)}
                  className="flex-1 py-3 rounded-xl border border-border text-text-secondary hover:bg-bg-hover transition-colors"
                >
                  إلغاء
                </button>
                <button
                  onClick={handleNewChat}
                  className="flex-1 btn-primary"
                >
                  بدء
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chats List */}
      <div className="flex-1 overflow-y-auto p-3">
        <div className="flex items-center justify-between mb-3 px-2">
          <span className="text-sm text-text-muted font-medium">المحادثات</span>
          <span className="text-xs text-text-muted">{chats.length}</span>
        </div>

        <div className="space-y-1">
          {chats.map(chat => (
            <motion.div
              key={chat.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="group relative"
            >
              <Link
                to={`/app/chat/${chat.id}`}
                className={`flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-150 ${
                  location.pathname === `/app/chat/${chat.id}`
                    ? 'bg-bg-card border-r-3 border-accent-primary'
                    : 'hover:bg-bg-hover'
                }`}
              >
                <div className="relative">
                  <MessageSquare size={18} className="text-text-secondary" />
                  <span className={`absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full ${statusColors[chat.status]} ${
                    chat.status === 'active' ? 'animate-pulse' : ''
                  }`} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-sm truncate">{chat.name}</span>
                    {chat.status === 'closed' && <Lock size={12} className="text-text-muted" />}
                  </div>
                  <p className="text-xs text-text-muted truncate">{chat.lastMessage}</p>
                </div>
                
                {/* Actions Menu */}
                <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                  <div className="relative">
                    <button className="p-1.5 rounded-lg hover:bg-bg-card">
                      <MoreHorizontal size={16} className="text-text-secondary" />
                    </button>
                    
                    {/* Dropdown */}
                    <div className="hidden group-hover:block absolute left-0 top-full mt-1 bg-bg-card border border-border rounded-xl shadow-xl py-1 min-w-[140px] z-10">
                      <button className="w-full flex items-center gap-2 px-3 py-2 text-sm text-text-secondary hover:bg-bg-hover">
                        <Edit3 size={14} />
                        <span>إعادة التسمية</span>
                      </button>
                      <button className="w-full flex items-center gap-2 px-3 py-2 text-sm text-text-secondary hover:bg-bg-hover">
                        <Lock size={14} />
                        <span>إغلاق</span>
                      </button>
                      <button 
                        onClick={() => handleDeleteChat(chat.id)}
                        className="w-full flex items-center gap-2 px-3 py-2 text-sm text-danger hover:bg-bg-hover"
                      >
                        <Trash2 size={14} />
                        <span>حذف</span>
                      </button>
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Footer - User Profile */}
      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-accent-primary/20 flex items-center justify-center">
            <User size={20} className="text-accent-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-medium text-sm truncate">{user?.name || 'مستخدم'}</p>
            <p className="text-xs text-text-muted truncate">{user?.email || ''}</p>
          </div>
          <Link
            to="/app/settings"
            className="p-2 rounded-lg hover:bg-bg-hover transition-colors"
          >
            <Settings size={20} className="text-text-secondary" />
          </Link>
        </div>
      </div>
    </aside>
  )
}