import { useState, useRef, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Sidebar from '../components/Sidebar'
import AgentMessage, { UserMessage, TypingIndicator } from '../components/AgentMessage'
import InputBox from '../components/InputBox'
import { X, MoreHorizontal, Plus } from 'lucide-react'
import { useToast } from '../components/Toast'

const mockMessages = [
  {
    id: 1,
    type: 'agent',
    agentId: 'orchestrator',
    stage: 'completed',
    progress: 100,
    message: 'تم استلام طلبك! سأقوم بتنسيق العمل بين الوكلاء.',
    tools: ['Brain System'],
    currentPhase: 'فهم المتطلبات',
    timestamp: '10:30 ص'
  },
  {
    id: 2,
    type: 'agent',
    agentId: 'developer',
    stage: 'completed',
    progress: 100,
    message: 'جيد! سأبدأ بإنشاء المشروع الآن.',
    tools: ['VSCode Controller', 'File System'],
    currentPhase: 'إنشاء هيكل المشروع',
    timestamp: '10:31 ص'
  },
  {
    id: 3,
    type: 'agent',
    agentId: 'designer',
    stage: 'working',
    progress: 65,
    message: 'جارٍ تصميم الواجهة الأمامية للمشروع...',
    tools: ['UI Designer', 'Theme System'],
    currentPhase: 'تصميم الواجهة',
    timestamp: '10:32 ص'
  },
]

export default function ChatPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { success, error: showError } = useToast()
  const messagesEndRef = useRef(null)
  
  const [messages, setMessages] = useState(mockMessages)
  const [isProcessing, setIsProcessing] = useState(false)
  const [projectName, setProjectName] = useState('مشروع جديد')
  const [projectStatus, setProjectStatus] = useState('active')

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (message) => {
    // إضافة رسالة المستخدم
    const userMsg = {
      id: Date.now(),
      type: 'user',
      message,
      timestamp: new Date().toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' })
    }
    setMessages(prev => [...prev, userMsg])

    setIsProcessing(true)
    setProjectStatus('working')

    // محاكاة استجابة الوكيل
    await new Promise(resolve => setTimeout(resolve, 2000))

    const agentResponse = {
      id: Date.now() + 1,
      type: 'agent',
      agentId: 'orchestrator',
      stage: 'working',
      progress: 0,
      message: `تم استلام طلبك: "${message}"`,
      tools: ['Brain System'],
      currentPhase: 'جارٍ المعالجة...',
      timestamp: new Date().toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' })
    }
    setMessages(prev => [...prev, agentResponse])

    // تحديث التقدم
    for (let i = 20; i <= 80; i += 20) {
      await new Promise(resolve => setTimeout(resolve, 1000))
      setMessages(prev => prev.map(msg => 
        msg.id === agentResponse.id 
          ? { ...msg, progress: i, currentPhase: `المرحلة ${i/20} من 4` }
          : msg
      ))
    }

    setMessages(prev => prev.map(msg => 
      msg.id === agentResponse.id 
        ? { ...msg, progress: 100, stage: 'completed', currentPhase: 'تم الاكتمال!' }
        : msg
    ))

    setProjectStatus('active')
    setIsProcessing(false)
    success('تم تنفيذ المهمة بنجاح!')
  }

  return (
    <div className="flex min-h-screen bg-bg-primary">
      <Sidebar />
      
      <main className="flex-1 mr-[280px] flex flex-col h-screen">
        {/* Header */}
        <header className="flex items-center justify-between px-6 py-4 border-b border-border bg-bg-secondary">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/app')}
              className="p-2 rounded-lg hover:bg-bg-hover transition-colors"
            >
              <Plus size={20} className="text-text-secondary rotate-45" />
            </button>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-syne font-semibold text-lg">{projectName}</h1>
                <span className={`w-2.5 h-2.5 rounded-full ${
                  projectStatus === 'active' ? 'bg-success animate-pulse' :
                  projectStatus === 'working' ? 'bg-warning animate-pulse' :
                  'bg-text-muted'
                }`} />
              </div>
              <p className="text-xs text-text-muted">المحادثة #{id}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button className="p-2 rounded-lg hover:bg-bg-hover transition-colors">
              <MoreHorizontal size={20} className="text-text-secondary" />
            </button>
            <button
              onClick={() => navigate('/app')}
              className="p-2 rounded-lg hover:bg-bg-hover transition-colors"
            >
              <X size={20} className="text-text-secondary" />
            </button>
          </div>
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {/* Welcome Message */}
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-12"
            >
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center mx-auto mb-6">
                <span className="text-4xl">🧠</span>
              </div>
              <h2 className="font-syne font-bold text-2xl mb-2">مرحباً بك!</h2>
              <p className="text-text-secondary max-w-md mx-auto">
                أنا المدير الأعلى، أخبرني بما تريد وسأقوم بتنسيق العمل بين الوكلاء
              </p>
            </motion.div>
          )}

          {/* Messages */}
          <AnimatePresence>
            {messages.map((msg, index) => {
              if (msg.type === 'user') {
                return (
                  <div key={msg.id} className="flex justify-start">
                    <UserMessage message={msg.message} timestamp={msg.timestamp} />
                  </div>
                )
              }
              
              return (
                <AgentMessage
                  key={msg.id}
                  agentId={msg.agentId}
                  stage={msg.stage}
                  progress={msg.progress}
                  message={msg.message}
                  tools={msg.tools}
                  currentPhase={msg.currentPhase}
                  timestamp={msg.timestamp}
                />
              )
            })}
          </AnimatePresence>

          {/* Typing Indicator */}
          {isProcessing && (
            <TypingIndicator />
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Box */}
        <InputBox
          onSend={handleSend}
          isProcessing={isProcessing}
          placeholder="اكتب طلبك للوكلاء (مثال: ابني مشروع Python للموقع)..."
        />
      </main>
    </div>
  )
}