import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Send, Paperclip, Zap, Pause, Square } from 'lucide-react'

export default function InputBox({ 
  onSend, 
  disabled = false, 
  isProcessing = false,
  placeholder = 'اكتب طلبك للوكلاء...'
}) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      const newHeight = Math.min(textareaRef.current.scrollHeight, 150)
      textareaRef.current.style.height = `${newHeight}px`
    }
  }, [message])

  const handleSubmit = () => {
    if (!message.trim() || disabled || isProcessing) return
    
    onSend(message)
    setMessage('')
    
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="border-t border-border bg-bg-secondary p-4">
      <div className="flex items-end gap-3">
        {/* Input Area */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled || isProcessing}
            rows={1}
            className="w-full px-5 py-4 pr-14 rounded-2xl bg-bg-card border border-border text-text-primary placeholder-text-muted outline-none resize-none transition-all duration-200 focus:border-border-active focus:shadow-[0_0_0_3px_var(--accent-glow)]"
            style={{ minHeight: '56px', maxHeight: '150px' }}
          />
          
          {/* Action Buttons */}
          <div className="absolute left-3 bottom-3 flex items-center gap-1">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-2 rounded-lg text-text-muted hover:text-text-secondary hover:bg-bg-hover transition-colors"
              title="إرفاق ملف"
            >
              <Paperclip size={18} />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-2 rounded-lg text-accent-primary hover:bg-accent-primary/10 transition-colors"
              title="إرسال سريع"
            >
              <Zap size={18} />
            </motion.button>
          </div>
        </div>

        {/* Send/Stop Button */}
        <motion.button
          onClick={isProcessing ? () => {} : handleSubmit}
          disabled={!message.trim() || disabled}
          whileHover={!isProcessing && message.trim() ? { scale: 1.05 } : {}}
          whileTap={!isProcessing && message.trim() ? { scale: 0.95 } : {}}
          className={`w-14 h-14 rounded-full flex items-center justify-center transition-all duration-200 ${
            isProcessing 
              ? 'bg-warning cursor-pointer' 
              : message.trim() 
                ? 'cursor-pointer' 
                : 'opacity-50 cursor-not-allowed'
          }`}
          style={{
            background: isProcessing 
              ? undefined 
              : message.trim() 
                ? 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))' 
                : 'var(--bg-hover)'
          }}
        >
          {isProcessing ? (
            <Square size={20} className="text-white" />
          ) : (
            <Send size={20} className="text-white" />
          )}
        </motion.button>
      </div>

      {/* Quick Actions */}
      <div className="flex items-center gap-2 mt-3 overflow-x-auto pb-1">
        {['ابني مشروع', 'أنشئ ملف', 'شغل أمر', 'صمم واجهة'].map((action, i) => (
          <button
            key={i}
            onClick={() => setMessage(action)}
            className="px-3 py-1.5 rounded-full text-xs bg-bg-hover text-text-secondary hover:text-text-primary hover:bg-bg-card transition-colors whitespace-nowrap"
          >
            {action}
          </button>
        ))}
      </div>
    </div>
  )
}