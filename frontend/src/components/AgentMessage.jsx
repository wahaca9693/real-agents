import { motion } from 'framer-motion'
import { Bot, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

const stageColors = {
  working: 'badge-warning',
  completed: 'badge-success',
  error: 'badge-danger',
  pending: 'badge-info',
}

const agentAvatars = {
  orchestrator: '🧠',
  developer: '👨‍💻',
  designer: '🎨',
  researcher: '🔬',
  tester: '🧪',
  deployer: '🚀',
}

const agentNames = {
  orchestrator: 'المدير الأعلى',
  developer: 'المطور',
  designer: 'المصمم',
  researcher: 'الباحث',
  tester: 'الفاحص',
  deployer: 'الناشر',
}

const stageLabels = {
  working: 'جارٍ العمل',
  completed: 'مكتمل',
  error: 'خطأ',
  pending: 'قيد الانتظار',
}

export default function AgentMessage({ 
  agentId = 'orchestrator',
  stage = 'working',
  progress = 0,
  message = '',
  tools = [],
  currentPhase = '',
  timestamp = new Date().toLocaleTimeString('ar-SA')
}) {
  const avatar = agentAvatars[agentId] || '🤖'
  const name = agentNames[agentId] || agentId
  const stageLabel = stageLabels[stage] || stage
  const stageClass = stageColors[stage] || 'badge-info'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="bg-bg-card border border-border rounded-2xl p-5"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-bg-hover flex items-center justify-center text-xl">
            {avatar}
          </div>
          <div>
            <h3 className="font-syne font-semibold">{name}</h3>
            <p className="text-xs text-text-muted">{timestamp}</p>
          </div>
        </div>
        
        {/* Stage Badge */}
        <div className={`badge ${stageClass}`}>
          {stage === 'working' && (
            <Loader2 size={12} className="animate-spin" />
          )}
          {stage === 'completed' && <CheckCircle size={12} />}
          {stage === 'error' && <AlertCircle size={12} />}
          <span>{stageLabel}</span>
        </div>
      </div>

      {/* Message */}
      <div className="text-text-primary leading-relaxed mb-4">
        {message}
      </div>

      {/* Progress Bar */}
      {(stage === 'working' || progress > 0) && (
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-text-secondary">التقدم</span>
            <span className="text-xs text-accent-primary font-mono">{progress}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-bar-fill" 
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {/* Current Phase */}
      {currentPhase && (
        <div className="flex items-center gap-2 text-sm text-text-secondary mb-3">
          <span>📁</span>
          <span>المرحلة:</span>
          <span className="text-text-primary">{currentPhase}</span>
        </div>
      )}

      {/* Tools Used */}
      {tools.length > 0 && (
        <div className="flex items-center gap-2 text-sm text-text-secondary">
          <span>⚙️</span>
          <span>الأدوات:</span>
          <div className="flex flex-wrap gap-2">
            {tools.map((tool, i) => (
              <span 
                key={i}
                className="px-2 py-0.5 rounded-md bg-bg-hover text-xs font-mono text-accent-primary"
              >
                {tool}
              </span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}

// User Message Component
export function UserMessage({ message, timestamp = new Date().toLocaleTimeString('ar-SA') }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex justify-start"
    >
      <div className="bg-accent-primary text-white rounded-2xl rounded-tr-sm px-5 py-4 max-w-[80%]">
        <p className="leading-relaxed">{message}</p>
        <p className="text-xs text-white/60 mt-2">{timestamp}</p>
      </div>
    </motion.div>
  )
}

// Typing Indicator
export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-bg-card border border-border rounded-2xl p-5"
    >
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded-xl bg-bg-hover flex items-center justify-center text-xl">
          🤖
        </div>
        <div>
          <h3 className="font-syne font-semibold">الوكلاء</h3>
          <p className="text-xs text-text-muted">جارٍ الكتابة...</p>
        </div>
      </div>
      <div className="flex gap-1.5">
        <div className="typing-dot" />
        <div className="typing-dot" />
        <div className="typing-dot" />
      </div>
    </motion.div>
  )
}