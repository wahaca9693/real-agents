"""
🧠 Real Agent Brain - عقل الوكيل الحقيقي
يفهم المستخدم ويسأل إذا ما فهم ويسوي التعديلات
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import re
import asyncio


class UnderstandingLevel(Enum):
    """مستوى الفهم"""
    FULL = "full"
    PARTIAL = "partial"
    UNCLEAR = "unclear"


@dataclass
class UserIntent:
    """نية المستخدم"""
    intent_id: str
    raw_text: str
    understood: bool
    confidence: float
    entities: List[Dict] = field(default_factory=list)
    missing_info: List[str] = field(default_factory=list)
    clarifications_needed: List[str] = field(default_factory=list)
    suggested_questions: List[str] = field(default_factory=list)


@dataclass
class ConversationContext:
    """سياق المحادثة"""
    context_id: str
    history: List[Dict] = field(default_factory=list)
    current_project: Optional[str] = None
    user_preferences: Dict = field(default_factory=dict)
    last_understanding: Optional[UserIntent] = None


@dataclass
class AgentThought:
    """تفكير الوكيل"""
    thought_id: str
    thinking: str
    reasoning: str
    decision: str
    confidence: float
    alternatives: List[str] = field(default_factory=list)


class RealAgentBrain:
    """
    عقل الوكيل الحقيقي - يفهم ويتواصل ويتعلم
    """
    
    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context = ConversationContext(
            context_id=f"CTX-{agent_id}",
            history=[]
        )
        self.understand_level = UnderstandingLevel.FULL
        self.questions_asked = []
        self.learned_patterns: List[Dict] = []
    
    async def understand_user(self, message: str, context: Dict = None) -> UserIntent:
        """فهم ما يقوله المستخدم"""
        
        # تحليل النص
        entities = self._extract_entities(message)
        missing_info = self._find_missing_info(message)
        
        # تحديد ما إذا كان واضح
        clarity_score = self._calculate_clarity(message)
        
        # أنشئ ملف - نعتبره واضح دائماً
        if ("أنشئ" in message or "ابني" in message) and ("ملف" in message or ".py" in message or ".js" in message):
            clarity_score = 1.0
            missing_info = []
        
        intent = UserIntent(
            intent_id=f"INT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            raw_text=message,
            understood=clarity_score > 0.5,
            confidence=clarity_score,
            entities=entities,
            missing_info=missing_info
        )
        
        # توليد أسئلة للتوضيح فقط إذا كان هناك أسئلة فعلية
        if missing_info and clarity_score < 0.8:
            intent.clarifications_needed = missing_info
            intent.suggested_questions = missing_info
        
        self.context.last_understanding = intent
        
        return intent
    
    def _extract_entities(self, text: str) -> List[Dict]:
        """استخراج الكيانات من النص"""
        entities = []
        
        # استخراج الأفعال
        verbs = ["ابني", "أسوي", "أنشئ", "عدّل", "احذف", "أرسل", "أنزل", "أبحث", "أحلل"]
        for verb in verbs:
            if verb in text:
                entities.append({"type": "action", "value": verb})
        
        # استخراج الكلمات التقنية
        tech_words = ["موقع", "تطبيق", "قاعدة بيانات", "API", "داشبورد", "واجهة", "كود"]
        for word in tech_words:
            if word in text:
                entities.append({"type": "tech", "value": word})
        
        # استخراج الأسماء
        patterns = [
            r'لي\s+(\w+)',
            r'أنشئ\s+(\w+)',
            r'ابني\s+(\w+)',
            r'سوي\s+(\w+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                entities.append({"type": "object", "value": match.group(1)})
        
        return entities
    
    def _find_missing_info(self, text: str) -> List[str]:
        """البحث عن معلومات ناقصة"""
        missing = []
        
        # أنشئ/ابني ملف محدد - لا نسأل
        if ("أنشئ" in text or "ابني" in text) and ("ملف" in text or ".py" in text or ".js" in text or ".html" in text):
            return []  # واضح جداً
        
        # أمر واضح لإنشاء ملف
        if ("أنشئ" in text or "ابني" in text) and "hello" in text.lower():
            return []  # واضح - يريد ملف hello
        
        vague_words = ["شيء", "حاجة", "بيانات", "معلومات"]
        if any(w in text for w in vague_words):
            missing.append("ما المقصود بـ 'البيانات' بالتحديد؟")
        
        if "ابني" in text or "أسوي" in text:
            # لا نسأل إذا كان هناك تفاصيل كافية
            if not any(ext in text for ext in [".py", ".js", ".html", ".txt", "ملف", "مشروع"]):
                missing.append("ما نوع المشروع؟ (موقع، تطبيق، سكربت)")
        
        if "سهل" in text or "صعب" in text:
            missing.append("ما المستوى المطلوب؟")
        
        return missing
    
    def _calculate_clarity(self, text: str) -> float:
        """حساب وضوح الرسالة"""
        score = 0.5
        
        # إضافة نقاط للأسئلة الواضحة
        clear_patterns = [
            r'ابني\s+(?:لي\s+)?\w+',  # ابني لي موقع
            r'أنشئ\s+\w+',            # أنشئ قاعدة بيانات
            r'عدّل\s+على\s+\w+',      # عدّل على الملف
            r'أضف\s+\w+',             # أضف ميزة
        ]
        
        for pattern in clear_patterns:
            if re.search(pattern, text):
                score += 0.2
        
        # خصم نقاط للكلمات المبهمة
        vague_words = ["شيء", "حاجة", "بس", "إيه", "هيك", "يكون"]
        for word in vague_words:
            if word in text:
                score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _generate_clarification_questions(self, text: str) -> List[str]:
        """توليد أسئلة للتوضيح"""
        questions = []
        
        if "ابني" in text or "أسوي" in text:
            questions.append("ما نوع المشروع الذي تريد؟ (موقع ويب، تطبيق جوال، برنامج)")
        
        if "بيانات" in text:
            questions.append("ما نوع البيانات التي تتعامل معها؟")
        
        if len(text) < 20:
            questions.append("ممكن توضح أكثر؟")
        
        return questions
    
    def _generate_suggested_questions(self, text: str) -> List[str]:
        """توليد أسئلة مقترحة بناءً على السياق"""
        questions = []
        
        # أنشئ ملف - نسأل عن المحتوى
        if ("أنشئ" in text or "ابني" in text) and ("ملف" in text or ".py" in text or ".js" in text):
            if len(text) < 30:  # وصف قصير جداً
                questions.append("ما المحتوى الذي تريده في الملف؟")
                return questions
        
        # سؤال عام
        if "?" not in text:
            questions.append("ممكن توضح أكثر؟")
        
        return questions if questions else []
    
    async def think(self, message: str, knowledge_base: Dict = None) -> AgentThought:
        """التفكير قبل اتخاذ إجراء"""
        
        # تحليل الرسالة
        intent = await self.understand_user(message)
        
        # التفكير المنطقي
        reasoning_steps = []
        
        if intent.understood:
            reasoning_steps.append("الفهم: الرسالة واضحة")
            decision = self._make_decision(intent)
        else:
            reasoning_steps.append("الحاجة للتوضيح: الرسالة غير واضحة بما يكفي")
            decision = "ask_clarification"
        
        return AgentThought(
            thought_id=f"THINK-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            thinking=f"الوكيل {self.agent_name} يفكر في: {message[:50]}...",
            reasoning="\n".join(reasoning_steps),
            decision=decision,
            confidence=intent.confidence,
            alternatives=["ask_user", "research", "delegate"]
        )
    
    def _make_decision(self, intent: UserIntent) -> str:
        """اتخاذ قرار"""
        entities = {e['type']: e['value'] for e in intent.entities}
        
        if 'action' in entities:
            action = entities['action']
            if action in ["ابني", "أسوي", "أنشئ"]:
                return "create_project"
            elif action in ["عدّل", "أحسن"]:
                return "modify_project"
            elif action in ["احذف"]:
                return "delete_project"
            elif action in ["أرسل"]:
                return "send_message"
            elif action in ["أنزل", "حمّل"]:
                return "download"
            elif action in ["أبحث"]:
                return "search"
        
        return "general_task"
    
    async def ask_for_clarification(self, questions: List[str]) -> str:
        """طرح أسئلة على المستخدم"""
        self.questions_asked.extend(questions)
        
        if len(questions) == 1:
            return f"🤔 ما زلت أحتاج توضيح بسيط:\n\n❓ {questions[0]}"
        
        return f"""🤔 حتى أقدر أساعدك بشكل أفضل، عندي 몇 أسئلة:

{chr(10).join([f'{i+1}. {q}' for i, q in enumerate(questions)])}

الرجاء الإجابة على أي سؤال تريد."""
    
    async def confirm_understanding(self, summary: str) -> str:
        """تأكيد الفهم"""
        return f"""✅ فهمت طلبك:
        
"{summary}"

هل هذا صحيح؟ إذا نعم، سأبدأ التنفيذ. إذا لا، أخبرني بالتصحيح."""
    
    async def learn_from_feedback(self, user_response: str):
        """التعلم من ردود الفعل"""
        
        if any(word in user_response.lower() for word in ["نعم", "صح", "تمام", "اكمل"]):
            self.learned_patterns.append({
                "type": "confirmed",
                "timestamp": datetime.now().isoformat()
            })
        elif any(word in user_response.lower() for word in ["لا", "خطأ", "غلط"]):
            self.learned_patterns.append({
                "type": "rejected",
                "timestamp": datetime.now().isoformat()
            })
        
        # تحديث سياق المحادثة
        self.context.history.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": self.context.last_understanding.raw_text if self.context.last_understanding else "",
            "user_feedback": user_response
        })
    
    async def suggest_alternatives(self, intent: UserIntent) -> List[str]:
        """اقتراح بدائل"""
        alternatives = []
        
        if "ابني" in intent.raw_text or "أسوي" in intent.raw_text:
            alternatives = [
                "أقدر أبني لك موقع ويب باستخدام React",
                "أقدر أبني لك تطبيق API باستخدام FastAPI",
                "أقدر أسوي سكربت Python للأتمتة"
            ]
        
        return alternatives