import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Brain, Zap, Shield, Code, ArrowLeft, Users, Clock, BarChart3 } from 'lucide-react'

const features = [
  {
    icon: Brain,
    title: 'وكلاء ذكيون',
    description: 'فريق من 6 وكلاء متخصصين يعملون معاً لتنفيذ مشاريعك'
  },
  {
    icon: Zap,
    title: 'سرعة فائقة',
    description: 'إنجاز المهام المعقدة في دقائق بدلاً من ساعات'
  },
  {
    icon: Shield,
    title: 'أمان عالي',
    description: 'حماية متقدمة لبياناتك ورمزك المصدري'
  },
  {
    icon: Code,
    title: 'كود نظيف',
    description: 'إنتاج كود منظم ومُوثق وجاهز للإنتاج'
  },
]

const stats = [
  { value: '6+', label: 'وكلاء متخصصين' },
  { value: '1,000+', label: 'مشروع منجز' },
  { value: '99%', label: 'نسبة النجاح' },
  { value: '24/7', label: 'خدمة مستمرة' },
]

const agents = [
  { emoji: '🧠', name: 'المدير الأعلى', role: 'ينسق العمل بين الوكلاء' },
  { emoji: '👨‍💻', name: 'المطور', role: 'يكتب الكود وينشئ المشاريع' },
  { emoji: '🎨', name: 'المصمم', role: 'يصمم الواجهات والتجربة' },
  { emoji: '🔬', name: 'الباحث', role: 'يبحث ويجمع المعلومات' },
  { emoji: '🧪', name: 'الفاحص', role: 'يفحص الكود ويكتشف الأخطاء' },
  { emoji: '🚀', name: 'الناشر', role: 'ينشر التطبيقات' },
]

export default function Landing() {
  return (
    <div className="min-h-screen bg-bg-primary bg-gradient-radial">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 glass border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center">
              <span className="text-xl">🧠</span>
            </div>
            <span className="font-syne font-bold text-xl gradient-text">Real Agents</span>
          </div>
          
          <div className="flex items-center gap-4">
            <Link 
              to="/login"
              className="px-5 py-2.5 rounded-xl text-text-secondary hover:text-text-primary transition-colors"
            >
              تسجيل الدخول
            </Link>
            <Link to="/register" className="btn-primary">
              ابدأ مجاناً
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-block px-4 py-1.5 rounded-full bg-accent-primary/10 text-accent-primary text-sm mb-6">
              منصة الوكلاء البرمجيين الأولى عربياً
            </span>
            
            <h1 className="font-syne font-bold text-5xl md:text-6xl mb-6 leading-tight">
              <span className="gradient-text">فريق تطوير كامل</span>
              <br />
              <span className="text-text-primary">بين يديك</span>
            </h1>
            
            <p className="text-xl text-text-secondary max-w-2xl mx-auto mb-10 leading-relaxed">
              6 وكلاء ذكيين متخصصين يعملون كفريق واحد لتنفيذ مشاريعك البرمجية
              بسرعة ودقة عالية، من التصميم حتى النشر
            </p>
            
            <div className="flex items-center justify-center gap-4">
              <Link to="/register" className="btn-primary px-8 py-4 text-lg">
                ابدأ مشروعك الآن
              </Link>
              <Link 
                to="/login"
                className="flex items-center gap-2 px-6 py-4 text-text-secondary hover:text-text-primary transition-colors"
              >
                <ArrowLeft size={20} />
                <span>لديك حساب؟</span>
              </Link>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16"
          >
            {stats.map((stat, i) => (
              <div key={i} className="card text-center">
                <div className="font-syne font-bold text-3xl gradient-text mb-1">{stat.value}</div>
                <div className="text-sm text-text-secondary">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Agents Section */}
      <section className="py-20 px-6 bg-bg-secondary">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="font-syne font-bold text-3xl mb-4">فريق الوكلاء</h2>
            <p className="text-text-secondary max-w-2xl mx-auto">
              كل وكيل له دور متخصص، يعملون معاً بتنسيق من المدير الأعلى
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {agents.map((agent, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }}
                className="card text-center hover:border-accent-primary/30 transition-colors"
              >
                <div className="text-4xl mb-3">{agent.emoji}</div>
                <h3 className="font-syne font-semibold mb-1">{agent.name}</h3>
                <p className="text-xs text-text-muted">{agent.role}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="font-syne font-bold text-3xl mb-4">لماذا Real Agents؟</h2>
            <p className="text-text-secondary max-w-2xl mx-auto">
              نقدم لك تجربة تطوير فريدة تجمع بين الذكاء الاصطناعي والخبرة البرمجية
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="card-hover"
              >
                <div className="w-12 h-12 rounded-xl bg-accent-primary/10 flex items-center justify-center mb-4">
                  <feature.icon size={24} className="text-accent-primary" />
                </div>
                <h3 className="font-syne font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-text-secondary leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="card text-center relative overflow-hidden"
            style={{
              background: 'linear-gradient(135deg, rgba(79, 142, 247, 0.1), rgba(124, 92, 252, 0.1))'
            }}
          >
            <div className="absolute inset-0 bg-gradient-to-br from-accent-primary/5 to-accent-secondary/5" />
            <div className="relative">
              <h2 className="font-syne font-bold text-3xl mb-4">جاهز تبدأ؟</h2>
              <p className="text-text-secondary mb-8 max-w-lg mx-auto">
                ابدأ مشروعك الأول الآن واحصل على تجربة مجانية، لا حاجة لبطاقة ائتمان
              </p>
              <Link to="/register" className="btn-primary px-10 py-4 text-lg inline-block">
                ابدأ مجاناً
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center">
              <span className="text-sm">🧠</span>
            </div>
            <span className="font-syne font-semibold gradient-text">Real Agents</span>
          </div>
          <p className="text-sm text-text-muted">
            © 2024 منصة الوكلاء البرمجيين. جميع الحقوق محفوظة
          </p>
        </div>
      </footer>
    </div>
  )
}