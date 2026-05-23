"""
🧠 Agent Memory System - نظام ذاكرة الوكلاء
يتذكر كل شيء ويتعلم من التجارب
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json
import os


@dataclass
class MemoryEntry:
    """ذاكرة واحدة"""
    memory_id: str
    type: str  # experience, preference, knowledge, skill
    content: str
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    importance: float = 0.5  # 0.0 to 1.0


@dataclass
class LearnedPattern:
    """نمط متعلم"""
    pattern_id: str
    description: str
    success_rate: float
    occurrences: int
    context: str
    learned_at: datetime


class AgentMemory:
    """
    ذاكرة الوكيل - يتذكر كل شيء ويتعلم
    """
    
    def __init__(self, agent_id: str, memory_dir: str = "./workspace/memory"):
        self.agent_id = agent_id
        self.memory_dir = Path(memory_dir) / agent_id
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.short_term: List[MemoryEntry] = []  # آخر 10 محادثات
        self.long_term: Dict[str, MemoryEntry] = {}  # الذاكرة طويلة المدى
        self.patterns: List[LearnedPattern] = []
        
        self._load_long_term_memory()
    
    async def remember(self, content: str, memory_type: str = "experience",
                      tags: List[str] = None, importance: float = 0.5) -> MemoryEntry:
        """حفظ في الذاكرة"""
        
        memory = MemoryEntry(
            memory_id=f"MEM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            type=memory_type,
            content=content,
            tags=tags or [],
            importance=importance
        )
        
        # إضافة للذاكرة قصيرة المدى
        self.short_term.append(memory)
        
        # الاحتفاظ بآخر 10 ذكريات فقط
        if len(self.short_term) > 10:
            self.short_term.pop(0)
        
        # إضافة للذاكرة طويلة المدى إذا كانت مهمة
        if importance > 0.6:
            self.long_term[memory.memory_id] = memory
            self._save_memory(memory)
        
        return memory
    
    async def recall(self, query: str) -> List[MemoryEntry]:
        """استدعاء من الذاكرة"""
        
        results = []
        query_lower = query.lower()
        
        # البحث في الذاكرة قصيرة المدى
        for memory in self.short_term:
            if query_lower in memory.content.lower():
                memory.access_count += 1
                memory.last_accessed = datetime.now()
                results.append(memory)
        
        # البحث في الذاكرة طويلة المدى
        for memory in self.long_term.values():
            if query_lower in memory.content.lower():
                memory.access_count += 1
                memory.last_accessed = datetime.now()
                results.append(memory)
        
        # ترتيب حسب الأهمية
        results.sort(key=lambda x: (x.importance, x.access_count), reverse=True)
        
        return results[:5]
    
    async def learn_pattern(self, description: str, success: bool, context: str):
        """تعلم نمط جديد"""
        
        # البحث عن نمط مشابه
        existing = None
        for pattern in self.patterns:
            if pattern.description == description:
                existing = pattern
                break
        
        if existing:
            # تحديث النمط الموجود
            existing.occurrences += 1
            if success:
                existing.success_rate = (existing.success_rate * (existing.occurrences - 1) + 1) / existing.occurrences
            else:
                existing.success_rate = (existing.success_rate * (existing.occurrences - 1)) / existing.occurrences
        else:
            # نمط جديد
            pattern = LearnedPattern(
                pattern_id=f"PAT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                description=description,
                success_rate=1.0 if success else 0.0,
                occurrences=1,
                context=context,
                learned_at=datetime.now()
            )
            self.patterns.append(pattern)
        
        # حفظ النمط
        self._save_pattern(description, success, context)
    
    async def get_recent_context(self) -> List[str]:
        """الحصول على سياق حديث للمحادثة"""
        context = []
        for memory in self.short_term[-5:]:
            context.append(f"{memory.type}: {memory.content[:100]}...")
        return context
    
    async def save_preference(self, key: str, value: Any):
        """حفظ تفضيل"""
        prefs_file = self.memory_dir / "preferences.json"
        
        prefs = {}
        if prefs_file.exists():
            prefs = json.loads(prefs_file.read_text())
        
        prefs[key] = value
        prefs_file.write_text(json.dumps(prefs, indent=2, ensure_ascii=False))
    
    async def get_preference(self, key: str, default: Any = None) -> Any:
        """الحصول على تفضيل"""
        prefs_file = self.memory_dir / "preferences.json"
        
        if prefs_file.exists():
            prefs = json.loads(prefs_file.read_text())
            return prefs.get(key, default)
        
        return default
    
    def _load_long_term_memory(self):
        """تحميل الذاكرة طويلة المدى"""
        memories_file = self.memory_dir / "memories.json"
        
        if memories_file.exists():
            data = json.loads(memories_file.read_text())
            for item in data:
                memory = MemoryEntry(
                    memory_id=item["memory_id"],
                    type=item["type"],
                    content=item["content"],
                    tags=item.get("tags", []),
                    importance=item.get("importance", 0.5)
                )
                self.long_term[memory.memory_id] = memory
    
    def _save_memory(self, memory: MemoryEntry):
        """حفظ ذاكرة"""
        memories_file = self.memory_dir / "memories.json"
        
        memories = []
        if memories_file.exists():
            memories = json.loads(memories_file.read_text())
        
        memories.append({
            "memory_id": memory.memory_id,
            "type": memory.type,
            "content": memory.content,
            "tags": memory.tags,
            "importance": memory.importance,
            "created_at": memory.created_at.isoformat()
        })
        
        memories_file.write_text(json.dumps(memories, indent=2, ensure_ascii=False))
    
    def _save_pattern(self, description: str, success: bool, context: str):
        """حفظ نمط"""
        patterns_file = self.memory_dir / "patterns.json"
        
        patterns = []
        if patterns_file.exists():
            patterns = json.loads(patterns_file.read_text())
        
        # البحث عن نمط مشابه
        found = False
        for p in patterns:
            if p["description"] == description:
                p["occurrences"] += 1
                p["success_rate"] = (p["success_rate"] * (p["occurrences"] - 1) + (1 if success else 0)) / p["occurrences"]
                found = True
                break
        
        if not found:
            patterns.append({
                "pattern_id": f"PAT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "description": description,
                "success_rate": 1.0 if success else 0.0,
                "occurrences": 1,
                "context": context,
                "learned_at": datetime.now().isoformat()
            })
        
        patterns_file.write_text(json.dumps(patterns, indent=2, ensure_ascii=False))
    
    def get_memory_stats(self) -> Dict:
        """إحصائيات الذاكرة"""
        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term),
            "patterns_count": len(self.patterns),
            "total_memories": len(self.short_term) + len(self.long_term),
            "high_importance_memories": len([m for m in self.long_term.values() if m.importance > 0.7])
        }


class SharedMemory:
    """
    ذاكرة مشتركة بين الوكلاء
    """
    
    def __init__(self, shared_dir: str = "./workspace/shared"):
        self.shared_dir = Path(shared_dir)
        self.shared_dir.mkdir(parents=True, exist_ok=True)
    
    async def share_knowledge(self, agent_id: str, knowledge: Dict):
        """مشاركة معرفة"""
        
        knowledge_file = self.shared_dir / f"{agent_id}_knowledge.json"
        
        knowledge_data = []
        if knowledge_file.exists():
            knowledge_data = json.loads(knowledge_file.read_text())
        
        knowledge_data.append({
            "timestamp": datetime.now().isoformat(),
            "knowledge": knowledge
        })
        
        knowledge_file.write_text(json.dumps(knowledge_data, indent=2, ensure_ascii=False))
    
    async def get_shared_knowledge(self, agent_id: str) -> List[Dict]:
        """الحصول على المعرفة المشتركة"""
        knowledge_file = self.shared_dir / f"{agent_id}_knowledge.json"
        
        if knowledge_file.exists():
            return json.loads(knowledge_file.read_text())
        
        return []
    
    async def broadcast_to_agents(self, sender_id: str, message: str, agents: List[str]):
        """إرسال رسالة لكل الوكلاء"""
        
        for agent_id in agents:
            if agent_id != sender_id:
                message_file = self.shared_dir / f"inbox_{agent_id}.json"
                
                inbox = []
                if message_file.exists():
                    inbox = json.loads(message_file.read_text())
                
                inbox.append({
                    "from": sender_id,
                    "message": message,
                    "timestamp": datetime.now().isoformat(),
                    "read": False
                })
                
                message_file.write_text(json.dumps(inbox, indent=2, ensure_ascii=False))
    
    async def check_inbox(self, agent_id: str) -> List[Dict]:
        """فحص صندوق الوارد"""
        message_file = self.shared_dir / f"inbox_{agent_id}.json"
        
        if message_file.exists():
            inbox = json.loads(message_file.read_text())
            
            # تحديث كقراءة
            for msg in inbox:
                msg["read"] = True
            
            message_file.write_text(json.dumps(inbox, indent=2, ensure_ascii=False))
            
            return inbox
        
        return []
    
    async def clear_inbox(self, agent_id: str):
        """مسح صندوق الوارد"""
        message_file = self.shared_dir / f"inbox_{agent_id}.json"
        if message_file.exists():
            message_file.unlink()


# === Global Instances ===
shared_memory = SharedMemory()