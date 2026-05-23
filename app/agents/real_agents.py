"""
🤖 Real Agents - وكلاء حقيقيون يتواصلون ويتعاونون
كل وكيل له عقل وذاكرة ويقدر يسأل ويتعلم
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import json
from enum import Enum

from app.brain.agent_brain import RealAgentBrain, UserIntent, AgentThought
from app.memory.agent_memory import AgentMemory, SharedMemory, shared_memory
from app.vscode.vscode_controller import vscode_controller, VSCodeController
from app.powershell.real_executor import powershell_executor, PowerShellExecutor


class AgentRole(Enum):
    """أدوار الوكلاء"""
    ORCHESTRATOR = "orchestrator"
    COORDINATOR = "coordinator"
    DEVELOPER = "developer"
    DESIGNER = "designer"
    RESEARCHER = "researcher"
    TESTER = "tester"
    DEPLOYER = "deployer"
    COMMUNICATOR = "communicator"


class AgentStatus(Enum):
    """حالة الوكيل"""
    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"


@dataclass
class AgentMessage:
    """رسالة بين الوكلاء"""
    from_agent: str
    to_agent: str
    content: str
    type: str  # question, answer, request, share, alert
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TaskResult:
    """نتيجة المهمة"""
    task_id: str
    success: bool
    output: Any
    files_created: List[str] = field(default_factory=list)
    commands_executed: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    agent_id: str


class RealAgent:
    """
    وكيل حقيقي - له عقل وذاكرة ويتواصل
    """
    
    def __init__(self, agent_id: str, name: str, role: AgentRole, description: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.description = description
        
        # عقل الوكيل
        self.brain = RealAgentBrain(agent_id, name)
        
        # ذاكرة الوكيل
        self.memory = AgentMemory(agent_id)
        
        # الأدوات
        self.vscode = vscode_controller
        self.powershell = powershell_executor
        
        # الحالة
        self.status = AgentStatus.IDLE
        self.current_task: Optional[str] = None
        self.last_thought: Optional[AgentThought] = None
        
        # الوكلاء الآخرون
        self.colleagues: Dict[str, 'RealAgent'] = {}
        
        # طابور الرسائل
        self.inbox: List[AgentMessage] = []
        
        # سجل النشاط
        self.activity_log: List[Dict] = []
    
    def register_colleague(self, agent: 'RealAgent'):
        """تسجيل وكيل زميل"""
        self.colleagues[agent.agent_id] = agent
    
    async def receive_message(self, message: AgentMessage):
        """استقبال رسالة"""
        self.inbox.append(message)
        await self._process_message(message)
    
    async def send_message(self, to_agent: str, content: str, 
                          msg_type: str = "message", context: Dict = None) -> bool:
        """إرسال رسالة لوكيل آخر"""
        
        if to_agent in self.colleagues:
            message = AgentMessage(
                from_agent=self.agent_id,
                to_agent=to_agent,
                content=content,
                type=msg_type,
                context=context or {}
            )
            await self.colleagues[to_agent].receive_message(message)
            return True
        
        return False
    
    async def broadcast_to_colleagues(self, content: str, msg_type: str = "broadcast"):
        """إرسال للجميع"""
        for agent_id in self.colleagues:
            await self.send_message(agent_id, content, msg_type)
    
    async def think(self, user_message: str) -> AgentThought:
        """التفكير في رسالة المستخدم"""
        
        self.status = AgentStatus.THINKING
        
        # استخدام العقل للتفكير
        thought = await self.brain.think(user_message)
        self.last_thought = thought
        
        self.status = AgentStatus.IDLE
        
        return thought
    
    async def ask_user(self, questions: List[str]) -> str:
        """طرح أسئلة على المستخدم"""
        return await self.brain.ask_for_clarification(questions)
    
    async def confirm(self, summary: str) -> str:
        """تأكيد الفهم"""
        return await self.brain.confirm_understanding(summary)
    
    async def learn(self, user_feedback: str):
        """التعلم من ردود الفعل"""
        await self.brain.learn_from_feedback(user_feedback)
    
    async def remember(self, content: str, memory_type: str = "experience"):
        """حفظ في الذاكرة"""
        return await self.memory.remember(content, memory_type)
    
    async def recall(self, query: str) -> List:
        """استدعاء من الذاكرة"""
        return await self.memory.recall(query)
    
    async def create_file(self, file_path: str, content: str) -> Dict:
        """إنشاء ملف"""
        result = await self.vscode.create_file(
            self.current_task or "default",
            file_path,
            content
        )
        
        await self.remember(f"Created file: {file_path}", "action")
        
        return result
    
    async def execute_command(self, command: str) -> Dict:
        """تنفيذ أمر"""
        result = await self.powershell.execute(command)
        
        await self.remember(f"Executed: {command[:50]}...", "command")
        
        return {
            "success": result.success,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.return_code
        }
    
    async def work_on_task(self, task_description: str) -> TaskResult:
        """العمل على مهمة"""
        
        self.status = AgentStatus.WORKING
        self.current_task = task_description
        
        result = TaskResult(
            task_id=f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            success=False,
            output=None,
            files_created=[],
            commands_executed=[],
            errors=[]
        )
        
        try:
            # التفكير أولاً
            thought = await self.think(task_description)
            
            # إذا يحتاج توضيح
            if thought.decision == "ask_clarification":
                return result
            
            # تنفيذ المهمة حسب القرار
            if thought.decision == "create_project":
                output = await self._create_project_workflow(task_description)
                result.output = output
                result.success = True
            else:
                output = await self.execute_command(task_description)
                result.output = output
                result.success = output.get("success", False)
            
            self.status = AgentStatus.IDLE
            
        except Exception as e:
            result.errors.append(str(e))
            self.status = AgentStatus.ERROR
        
        return result
    
    async def _create_project_workflow(self, description: str) -> Dict:
        """سير عمل إنشاء مشروع"""
        
        # فهم المتطلبات
        await self.brain.understand_user(description)
        
        # إنشاء المشروع
        project_name = description.split()[1] if len(description.split()) > 1 else "new-project"
        project_type = "python"
        
        for word in ["موقع", "website", "web"]:
            project_type = "javascript"
        
        for word in ["تطبيق", "app", "أندرويد", "android"]:
            project_type = "android"
        
        project_result = await self.vscode.create_project(project_name, project_type)
        
        return project_result
    
    async def _process_message(self, message: AgentMessage):
        """معالجة رسالة"""
        
        if message.type == "question":
            # سؤال من وكيل آخر
            response = await self.think(message.content)
            await self.send_message(
                message.from_agent,
                f"بعد التفكير: {response.decision}",
                "answer"
            )
        
        elif message.type == "request":
            # طلب من وكيل آخر
            result = await self.work_on_task(message.content)
            await self.send_message(
                message.from_agent,
                f"النتيجة: {result.output}",
                "response",
                {"task_id": result.task_id, "success": result.success}
            )
        
        elif message.type == "share":
            # مشاركة معرفة
            await self.memory.remember(message.content, "shared_knowledge")
    
    def get_status(self) -> Dict:
        """الحصول على الحالة"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "current_task": self.current_task,
            "memory_stats": self.memory.get_memory_stats(),
            "inbox_count": len(self.inbox)
        }
    
    def get_activity_log(self, limit: int = 20) -> List[Dict]:
        """الحصول على سجل النشاط"""
        return self.activity_log[-limit:]


class AgentTeam:
    """
    فريق الوكلاء الحقيقيين
    """
    
    def __init__(self):
        self.agents: Dict[str, RealAgent] = {}
        self.shared_memory = shared_memory
        
        self._create_team()
    
    def _create_team(self):
        """إنشاء فريق الوكلاء"""
        
        # Orchestrator - المدير
        orchestrator = RealAgent(
            agent_id="orchestrator",
            name="المدير الأعلى",
            role=AgentRole.ORCHESTRATOR,
            description="ينسق العمل بين الوكلاء ويفهم متطلبات المستخدم"
        )
        self.agents["orchestrator"] = orchestrator
        
        # Developer - المطور
        developer = RealAgent(
            agent_id="developer",
            name="المطور",
            role=AgentRole.DEVELOPER,
            description="يكتب الكود وينشئ المشاريع والملفات"
        )
        self.agents["developer"] = developer
        
        # Designer - المصمم
        designer = RealAgent(
            agent_id="designer",
            name="المصمم",
            role=AgentRole.DESIGNER,
            description="يصمم الواجهات والتجربة"
        )
        self.agents["designer"] = designer
        
        # Researcher - الباحث
        researcher = RealAgent(
            agent_id="researcher",
            name="الباحث",
            role=AgentRole.RESEARCHER,
            description="يبحث ويجمع المعلومات"
        )
        self.agents["researcher"] = researcher
        
        # Tester - الفاحص
        tester = RealAgent(
            agent_id="tester",
            name="الفاحص",
            role=AgentRole.TESTER,
            description="يفحص الكود ويكتشف الأخطاء"
        )
        self.agents["tester"] = tester
        
        # Deployer - الناشر
        deployer = RealAgent(
            agent_id="deployer",
            name="الناشر",
            role=AgentRole.DEPLOYER,
            description="ينشر التطبيقات ويشغل الأوامر"
        )
        self.agents["deployer"] = deployer
        
        # تسجيل الزملاء
        for agent in self.agents.values():
            for other_agent in self.agents.values():
                if other_agent.agent_id != agent.agent_id:
                    agent.register_colleague(other_agent)
    
    def get_agent(self, agent_id: str) -> Optional[RealAgent]:
        """الحصول على وكيل"""
        return self.agents.get(agent_id)
    
    async def assign_task(self, agent_id: str, task: str) -> TaskResult:
        """تعيين مهمة لوكيل"""
        agent = self.get_agent(agent_id)
        if agent:
            return await agent.work_on_task(task)
        return None
    
    async def coordinate_task(self, task: str) -> Dict:
        """تنسيق مهمة عبر الوكلاء"""
        
        # فهم المهمة
        orchestrator = self.get_agent("orchestrator")
        thought = await orchestrator.think(task)
        
        # إذا يحتاج توضيح
        if thought.decision == "ask_clarification":
            questions = orchestrator.brain.context.last_understanding.suggested_questions
            return {
                "type": "clarification_needed",
                "questions": questions,
                "agent": "orchestrator"
            }
        
        # تنفيذ المهمة
        developer = self.get_agent("developer")
        result = await developer.work_on_task(task)
        
        return {
            "type": "task_completed",
            "result": result,
            "agent": "developer",
            "thought": thought.decision
        }
    
    def list_agents(self) -> List[Dict]:
        """قائمة الوكلاء"""
        return [agent.get_status() for agent in self.agents.values()]
    
    async def agent_communicate(self, from_id: str, to_id: str, 
                                message: str, msg_type: str = "message") -> bool:
        """تواصل بين الوكلاء"""
        from_agent = self.get_agent(from_id)
        if from_agent:
            return await from_agent.send_message(to_id, message, msg_type)
        return False


# === Global Instance ===
real_agent_team = AgentTeam()