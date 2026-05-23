import { useState, useEffect } from 'react'
import Sidebar from '../components/Sidebar'
import { motion } from 'framer-motion'
import { Users, Plus, TrendingUp, Trophy, CheckCircle, Clock, AlertCircle } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const roleLabels = {
  coordinator: 'منسق',
  developer: 'مطور',
  designer: 'مصمم',
  researcher: 'باحث',
  deployer: 'ناشر',
  tester: 'مختبر',
  security: 'أمني',
  communicator: 'مترجم'
}

const roleColors = {
  coordinator: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  developer: 'bg-green-500/20 text-green-400 border-green-500/30',
  designer: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  researcher: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  deployer: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  tester: 'bg-pink-500/20 text-pink-400 border-pink-500/30',
  security: 'bg-red-500/20 text-red-400 border-red-500/30',
  communicator: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30'
}

const taskTypeLabels = {
  development: 'تطوير',
  design: 'تصميم',
  research: 'بحث',
  deployment: 'نشر',
  testing: 'اختبار',
  security: 'أمان',
  documentation: 'وثائق',
  full_stack: 'كامل',
  complex: 'معقد'
}

export default function Team() {
  const [team, setTeam] = useState(null)
  const [agents, setAgents] = useState([])
  const [stats, setStats] = useState(null)
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [showNewTask, setShowNewTask] = useState(false)
  const [newTask, setNewTask] = useState({ title: '', description: '', task_type: 'development', priority: 1 })
  const [creating, setCreating] = useState(false)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [teamRes, agentsRes, statsRes, tasksRes] = await Promise.all([
        fetch(`${API_URL}/team/team`),
        fetch(`${API_URL}/team/list`),
        fetch(`${API_URL}/team/stats`),
        fetch(`${API_URL}/team/tasks/list`)
      ])
      
      const teamData = await teamRes.json()
      const agentsData = await agentsRes.json()
      const statsData = await statsRes.json()
      const tasksData = await tasksRes.json()
      
      setTeam(teamData.team)
      setAgents(agentsData.agents)
      setStats(statsData.stats)
      setTasks(tasksData.tasks || [])
    } catch (error) {
      console.error('Error fetching team data:', error)
    } finally {
      setLoading(false)
    }
  }

  const createTask = async () => {
    if (!newTask.title || !newTask.description) return
    
    try {
      setCreating(true)
      const res = await fetch(`${API_URL}/team/tasks/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTask)
      })
      
      if (res.ok) {
        const task = await res.json()
        setTasks(prev => [task, ...prev])
        setShowNewTask(false)
        setNewTask({ title: '', description: '', task_type: 'development', priority: 1 })
        fetchData() // Refresh stats
      }
    } catch (error) {
      console.error('Error creating task:', error)
    } finally {
      setCreating(false)
    }
  }

  const getStatusBadge = (status) => {
    const styles = {
      idle: 'bg-gray-500/20 text-gray-400',
      working: 'bg-blue-500/20 text-blue-400',
      completed: 'bg-green-500/20 text-green-400',
      failed: 'bg-red-500/20 text-red-400'
    }
    const labels = {
      idle: 'متاح',
      working: 'يعمل',
      completed: 'منتهي',
      failed: 'فشل'
    }
    return (
      <span className={`px-2 py-1 rounded-full text-xs ${styles[status]}`}>
        {labels[status]}
      </span>
    )
  }

  if (loading) {
    return (
      <div className="flex min-h-screen bg-bg-primary">
        <Sidebar />
        <main className="flex-1 mr-[280px] p-8 flex items-center justify-center">
          <div className="animate-spin w-12 h-12 border-4 border-accent-primary border-t-transparent rounded-full"></div>
        </main>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen bg-bg-primary">
      <Sidebar />
      
      <main className="flex-1 mr-[280px] p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="font-syne font-bold text-3xl mb-2 flex items-center gap-3">
              <Users className="text-accent-primary" />
              فريق العمل
            </h1>
            <p className="text-text-secondary">فريق من الوكلاء المتخصصين يعملون معاً لتنفيذ مهامك</p>
          </div>
          
          <button
            onClick={() => setShowNewTask(true)}
            className="flex items-center gap-2 px-4 py-2 bg-accent-primary text-white rounded-xl hover:bg-accent-primary/80 transition-colors"
          >
            <Plus size={20} />
            مهمة جديدة
          </button>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-4 gap-4 mb-8">
            <div className="bg-bg-secondary rounded-2xl p-4 border border-border">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-blue-500/20 flex items-center justify-center">
                  <CheckCircle className="text-blue-400" size={20} />
                </div>
                <div>
                  <div className="text-2xl font-bold">{stats.completed}</div>
                  <div className="text-text-muted text-sm">مهام منجزة</div>
                </div>
              </div>
            </div>
            
            <div className="bg-bg-secondary rounded-2xl p-4 border border-border">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-yellow-500/20 flex items-center justify-center">
                  <Clock className="text-yellow-400" size={20} />
                </div>
                <div>
                  <div className="text-2xl font-bold">{stats.in_progress}</div>
                  <div className="text-text-muted text-sm">قيد التنفيذ</div>
                </div>
              </div>
            </div>
            
            <div className="bg-bg-secondary rounded-2xl p-4 border border-border">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-green-500/20 flex items-center justify-center">
                  <TrendingUp className="text-green-400" size={20} />
                </div>
                <div>
                  <div className="text-2xl font-bold">{stats.completion_rate}</div>
                  <div className="text-text-muted text-sm">نسبة الإنجاز</div>
                </div>
              </div>
            </div>
            
            <div className="bg-bg-secondary rounded-2xl p-4 border border-border">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-purple-500/20 flex items-center justify-center">
                  <Users className="text-purple-400" size={20} />
                </div>
                <div>
                  <div className="text-2xl font-bold">{stats.available_agents}/{stats.agents_count}</div>
                  <div className="text-text-muted text-sm">وكلاء متاحين</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Agents Grid */}
        <div className="mb-8">
          <h2 className="font-syne font-bold text-xl mb-4">الوكلاء</h2>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {agents.map((agent, i) => (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="bg-bg-secondary rounded-2xl p-4 border border-border hover:border-accent-primary/50 transition-colors"
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-12 h-12 rounded-xl bg-accent-primary/20 flex items-center justify-center text-2xl">
                    {agent.icon}
                  </div>
                  <div>
                    <div className="font-bold">{agent.name}</div>
                    <div className="text-sm text-text-muted">{roleLabels[agent.role] || agent.role}</div>
                  </div>
                </div>
                
                <p className="text-sm text-text-secondary mb-3 line-clamp-2">{agent.description}</p>
                
                <div className="flex items-center justify-between">
                  {getStatusBadge(agent.status)}
                  <div className="flex items-center gap-1 text-sm">
                    <TrendingUp size={14} className="text-green-400" />
                    <span className="text-green-400">{agent.performance}%</span>
                  </div>
                </div>
                
                <div className="mt-3 pt-3 border-t border-border text-xs text-text-muted">
                  {agent.completed_tasks} مهمة منجزة
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Tasks List */}
        <div>
          <h2 className="font-syne font-bold text-xl mb-4">المهام الأخيرة</h2>
          <div className="space-y-3">
            {tasks.length === 0 ? (
              <div className="text-center py-8 text-text-muted">
                لا توجد مهام حتى الآن
              </div>
            ) : (
              tasks.slice(0, 5).map((task, i) => (
                <motion.div
                  key={task.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="bg-bg-secondary rounded-xl p-4 border border-border flex items-center justify-between"
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                      task.status === 'completed' ? 'bg-green-500/20' :
                      task.status === 'in_progress' ? 'bg-blue-500/20' :
                      task.status === 'failed' ? 'bg-red-500/20' : 'bg-gray-500/20'
                    }`}>
                      {task.status === 'completed' ? <CheckCircle className="text-green-400" size={20} /> :
                       task.status === 'in_progress' ? <Clock className="text-blue-400" size={20} /> :
                       task.status === 'failed' ? <AlertCircle className="text-red-400" size={20} /> :
                       <Clock className="text-gray-400" size={20} />}
                    </div>
                    <div>
                      <div className="font-medium">{task.title}</div>
                      <div className="text-sm text-text-muted">
                        {taskTypeLabels[task.type] || task.type} • {task.assigned_agents?.join(', ') || 'غير معين'}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      task.priority >= 4 ? 'bg-red-500/20 text-red-400' :
                      task.priority >= 3 ? 'bg-orange-500/20 text-orange-400' :
                      'bg-gray-500/20 text-gray-400'
                    }`}>
                      أولوية {task.priority}
                    </span>
                    {getStatusBadge(task.status)}
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </div>

        {/* New Task Modal */}
        {showNewTask && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowNewTask(false)}>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-bg-secondary rounded-2xl p-6 w-full max-w-md border border-border"
              onClick={e => e.stopPropagation()}
            >
              <h3 className="font-syne font-bold text-xl mb-4">مهمة جديدة</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm mb-2">عنوان المهمة</label>
                  <input
                    type="text"
                    value={newTask.title}
                    onChange={e => setNewTask({...newTask, title: e.target.value})}
                    className="w-full px-4 py-2 bg-bg-primary border border-border rounded-xl focus:outline-none focus:border-accent-primary"
                    placeholder="مثال: إنشاء قاعدة بيانات"
                  />
                </div>
                
                <div>
                  <label className="block text-sm mb-2">الوصف</label>
                  <textarea
                    value={newTask.description}
                    onChange={e => setNewTask({...newTask, description: e.target.value})}
                    className="w-full px-4 py-2 bg-bg-primary border border-border rounded-xl focus:outline-none focus:border-accent-primary h-24"
                    placeholder="وصف تفصيلي للمهمة..."
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm mb-2">نوع المهمة</label>
                    <select
                      value={newTask.task_type}
                      onChange={e => setNewTask({...newTask, task_type: e.target.value})}
                      className="w-full px-4 py-2 bg-bg-primary border border-border rounded-xl focus:outline-none focus:border-accent-primary"
                    >
                      <option value="development">تطوير</option>
                      <option value="design">تصميم</option>
                      <option value="research">بحث</option>
                      <option value="deployment">نشر</option>
                      <option value="testing">اختبار</option>
                      <option value="security">أمان</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm mb-2">الأولوية (1-5)</label>
                    <input
                      type="number"
                      min="1"
                      max="5"
                      value={newTask.priority}
                      onChange={e => setNewTask({...newTask, priority: parseInt(e.target.value)})}
                      className="w-full px-4 py-2 bg-bg-primary border border-border rounded-xl focus:outline-none focus:border-accent-primary"
                    />
                  </div>
                </div>
              </div>
              
              <div className="flex gap-3 mt-6">
                <button
                  onClick={createTask}
                  disabled={creating}
                  className="flex-1 px-4 py-2 bg-accent-primary text-white rounded-xl hover:bg-accent-primary/80 transition-colors disabled:opacity-50"
                >
                  {creating ? 'جاري الإنشاء...' : 'إنشاء المهمة'}
                </button>
                <button
                  onClick={() => setShowNewTask(false)}
                  className="px-4 py-2 bg-bg-primary border border-border rounded-xl hover:bg-bg-tertiary transition-colors"
                >
                  إلغاء
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </main>
    </div>
  )
}