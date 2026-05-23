import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import Sidebar from '../components/Sidebar'
import { Bot, TrendingUp, Clock, Activity, ArrowLeft, Play } from 'lucide-react'

const recentProjects = [
  { 
    id: 1, 
    name: 'مشروع الموقع', 
    status: 'active',
    progress: 75,
    agent: 'developer',
    lastUpdate: 'منذ 5 دقائق'
  },
  { 
    id: 2, 
    name: 'تطبيق الجوال', 
    status: 'working',
    progress: 45,
    agent: 'designer',
    lastUpdate: 'منذ ساعة'
  },
  { 
    id: 3, 
    name: 'API Backend', 
    status: 'completed',
    progress: 100,
    agent: 'deployer',
    lastUpdate: 'أمس'
  },
]

const stats = [
  { icon: Bot, label: 'مهام منجزة', value: '147', color: 'text-accent-primary' },
  { icon: Clock, label: 'ساعات العمل', value: '23', color: 'text-warning' },
  { icon: TrendingUp, label: 'نسبة النجاح', value: '98%', color: 'text-success' },
  { icon: Activity, label: 'الوكلاء النشطون', value: '6', color: 'text-accent-secondary' },
]

const quickActions = [
  { emoji: '👨‍💻', label: 'مشروع Python', action: 'ابني مشروع Python جديد' },
  { emoji: '🌐', label: 'موقع ويب', action: 'أنشئ موقع ويب بسيط' },
  { emoji: '📱', label: 'تطبيق جوال', action: 'صمم تطبيق جوال' },
  { emoji: '🗄️', label: 'قاعدة بيانات', action: 'أنشئ قاعدة بيانات' },
]

export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-bg-primary">
      <Sidebar />
      
      <main className="flex-1 mr-[280px] p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-syne font-bold text-3xl mb-2">مرحباً، أحمد 👋</h1>
          <p className="text-text-secondary">كيف يمكن للوكلاء مساعدتك اليوم؟</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {stats.map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="card"
            >
              <stat.icon size={24} className={stat.color} />
              <div className="mt-3">
                <div className="font-syne font-bold text-2xl">{stat.value}</div>
                <div className="text-sm text-text-muted">{stat.label}</div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="font-syne font-semibold text-xl mb-4">إجراءات سريعة</h2>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action, i) => (
              <motion.button
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ scale: 1.02 }}
                className="card-hover text-right"
              >
                <div className="text-3xl mb-2">{action.emoji}</div>
                <div className="font-medium">{action.label}</div>
                <div className="text-xs text-text-muted mt-1">{action.action}</div>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Recent Projects */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-syne font-semibold text-xl">المشاريع الأخيرة</h2>
            <button className="text-sm text-accent-primary hover:underline">
              عرض الكل
            </button>
          </div>
          
          <div className="grid lg:grid-cols-3 gap-4">
            {recentProjects.map((project, i) => (
              <motion.div
                key={project.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <Link
                  to={`/app/chat/${project.id}`}
                  className="block card-hover"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-syne font-semibold">{project.name}</h3>
                    <span className={`badge ${
                      project.status === 'active' ? 'badge-success' :
                      project.status === 'working' ? 'badge-warning' :
                      'badge-info'
                    }`}>
                      {project.status === 'active' && 'نشط'}
                      {project.status === 'working' && 'قيد العمل'}
                      {project.status === 'completed' && 'مكتمل'}
                    </span>
                  </div>
                  
                  {project.status !== 'completed' && (
                    <div className="mb-3">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-text-muted">التقدم</span>
                        <span className="text-accent-primary font-mono">{project.progress}%</span>
                      </div>
                      <div className="progress-bar">
                        <div className="progress-bar-fill" style={{ width: `${project.progress}%` }} />
                      </div>
                    </div>
                  )}
                  
                  <div className="flex items-center justify-between text-xs text-text-muted">
                    <span>{project.lastUpdate}</span>
                    <div className="flex items-center gap-1">
                      <Play size={12} />
                      <span>متابعة</span>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Agents Status */}
        <div className="mt-8">
          <h2 className="font-syne font-semibold text-xl mb-4">حالة الوكلاء</h2>
          <div className="grid grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { emoji: '🧠', name: 'المدير', status: 'idle' },
              { emoji: '👨‍💻', name: 'المطور', status: 'working' },
              { emoji: '🎨', name: 'المصمم', status: 'idle' },
              { emoji: '🔬', name: 'الباحث', status: 'idle' },
              { emoji: '🧪', name: 'الفاحص', status: 'idle' },
              { emoji: '🚀', name: 'الناشر', status: 'idle' },
            ].map((agent, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                className="card text-center"
              >
                <div className="relative inline-block mb-2">
                  <span className="text-3xl">{agent.emoji}</span>
                  <span className={`absolute -top-1 -right-1 w-3 h-3 rounded-full ${
                    agent.status === 'working' ? 'bg-warning animate-pulse' : 'bg-success'
                  }`} />
                </div>
                <div className="text-sm font-medium">{agent.name}</div>
                <div className="text-xs text-text-muted">
                  {agent.status === 'working' ? 'يعمل' : 'متاح'}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}