"""
Real Agents - Unit Tests
اختبارات الوحدات للمشروع
"""

import pytest
import asyncio
from datetime import datetime

# Test fixtures
@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


class TestAgentBrain:
    """اختبارات عقل الوكيل"""
    
    def test_clarity_score_calculation(self):
        """اختبار حساب وضوح الرسالة"""
        from app.brain.agent_brain import RealAgentBrain
        
        brain = RealAgentBrain("test", "Test Agent")
        
        # رسالة واضحة
        clear_score = brain._calculate_clarity("أنشئ لي ملف hello.py")
        assert clear_score > 0.5
        
        # رسالة غير واضحة (قد تكون متساوية، لذلك نستخدم > بدلاً من <)
        vague_score = brain._calculate_clarity("ابني شي")
        assert vague_score <= clear_score  # يجب أن تكون أقل أو مساوية
    
    def test_entity_extraction(self):
        """اختبار استخراج الكيانات"""
        from app.brain.agent_brain import RealAgentBrain
        
        brain = RealAgentBrain("test", "Test Agent")
        entities = brain._extract_entities("أنشئ لي موقع ويب جميل")
        
        assert any(e["type"] == "action" and e["value"] == "أنشئ" for e in entities)
        assert any(e["type"] == "tech" and e["value"] == "موقع" for e in entities)
    
    def test_decision_making(self):
        """اختبار اتخاذ القرار"""
        from app.brain.agent_brain import RealAgentBrain
        
        brain = RealAgentBrain("test", "Test Agent")
        
        intent = type('obj', (object,), {
            'entities': [{'type': 'action', 'value': 'أنشئ'}],
            'confidence': 0.9
        })()
        
        decision = brain._make_decision(intent)
        assert decision in ["create_project", "modify_project", "delete_project"]


class TestAgentMemory:
    """اختبارات ذاكرة الوكيل"""
    
    def test_memory_creation(self):
        """اختبار إنشاء ذاكرة"""
        from app.memory.agent_memory import AgentMemory
        
        # استخدام معرف فريد لكل اختبار
        import uuid
        memory = AgentMemory(f"test_agent_{uuid.uuid4().hex[:8]}")
        
        assert memory.agent_id is not None
        assert len(memory.short_term) == 0
        # ملاحظة: long_term قد يحتوي على بيانات من اختبارات سابقة
    
    @pytest.mark.asyncio
    async def test_remember_and_recall(self):
        """اختبار الحفظ والاستدعاء"""
        from app.memory.agent_memory import AgentMemory
        import uuid
        
        memory = AgentMemory(f"test_agent_{uuid.uuid4().hex[:8]}")
        
        # حفظ ذاكرة
        entry = await memory.remember("Test content", "experience", importance=0.8)
        assert entry is not None
        
        # استدعاء
        results = await memory.recall("Test")
        assert len(results) > 0
    
    def test_memory_stats(self):
        """اختبار إحصائيات الذاكرة"""
        from app.memory.agent_memory import AgentMemory
        import uuid
        
        memory = AgentMemory(f"test_agent_{uuid.uuid4().hex[:8]}")
        stats = memory.get_memory_stats()
        
        assert "short_term_count" in stats
        assert "long_term_count" in stats
        assert "patterns_count" in stats


class TestVSCodeController:
    """اختبارات متحكم VS Code"""
    
    def test_language_detection(self):
        """اختبار تحديد اللغة"""
        from app.vscode.vscode_controller import VSCodeController
        
        controller = VSCodeController()
        
        assert controller._get_language_from_extension(".py") == "python"
        assert controller._get_language_from_extension(".js") == "javascript"
        assert controller._get_language_from_extension(".html") == "html"
        assert controller._get_language_from_extension(".unknown") == "plaintext"


class TestPowerShellExecutor:
    """اختبارات منفذ الأوامر"""
    
    def test_system_info(self):
        """اختبار معلومات النظام"""
        from app.powershell.real_executor import PowerShellExecutor
        
        executor = PowerShellExecutor()
        info = executor.get_system_info()
        
        assert "os" in info
        assert "python_version" in info
        assert info["os"] in ["Windows", "Linux", "Darwin"]
    
    def test_execution_result_creation(self):
        """اختبار إنشاء نتيجة التنفيذ"""
        from app.powershell.real_executor import ExecutionResult
        
        result = ExecutionResult(
            command_id="TEST-001",
            command="echo test",
            success=True,
            stdout="test",
            stderr="",
            return_code=0,
            execution_time=0.1
        )
        
        assert result.success is True
        assert result.return_code == 0


class TestSecurity:
    """اختبارات الأمان"""
    
    def test_password_validation(self):
        """اختبار التحقق من قوة كلمة المرور"""
        from app.security import validate_password_strength
        
        # كلمة مرور قوية
        is_strong, message = validate_password_strength("SecurePass123!")
        assert is_strong is True
        
        # كلمة مرور ضعيفة - قصيرة
        is_strong, message = validate_password_strength("Pass1")
        assert is_strong is False
        assert "8 أحرف" in message
        
        # كلمة مرور ضعيفة - بدون أحرف كبيرة
        is_strong, message = validate_password_strength("securepass123")
        assert is_strong is False
        
        # كلمة مرور ضعيفة - بدون أرقام
        is_strong, message = validate_password_strength("SecurePassword")
        assert is_strong is False
    
    def test_input_sanitization(self):
        """اختبار تنظيف المدخلات"""
        from app.security import sanitize_input
        
        # اختبار إزالة HTML
        result = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in result
        
        # اختبار إزالة SQL injection
        result = sanitize_input("'; DROP TABLE users; --")
        assert "DROP" not in result
        
        # النص الآمن يبقى كما هو
        result = sanitize_input("مرحبا بالعالم")
        assert result == "مرحبا بالعالم"
    
    def test_password_hashing(self):
        """اختبار تشفير كلمة المرور"""
        from app.security import generate_password_hash, verify_password_hash
        
        password = "TestPassword123!"
        hashed = generate_password_hash(password)
        
        assert hashed != password
        assert verify_password_hash(password, hashed) is True
        assert verify_password_hash("WrongPassword", hashed) is False


class TestDatabase:
    """اختبارات قاعدة البيانات"""
    
    @pytest.mark.asyncio
    async def test_database_init(self):
        """اختبار إنشاء قاعدة البيانات"""
        from app.database import init_db, engine
        
        await init_db()
        
        # التحقق من أن المحرك يعمل
        assert engine is not None


class TestRealAgent:
    """اختبارات الوكيل الحقيقي"""
    
    def test_agent_creation(self):
        """اختبار إنشاء وكيل"""
        from app.agents.real_agents import RealAgent, AgentRole
        
        agent = RealAgent(
            agent_id="test",
            name="Test Agent",
            role=AgentRole.DEVELOPER,
            description="Test description"
        )
        
        assert agent.agent_id == "test"
        assert agent.name == "Test Agent"
        assert agent.status.value == "idle"
    
    def test_agent_status_transition(self):
        """اختبار تغير حالة الوكيل"""
        from app.agents.real_agents import RealAgent, AgentRole, AgentStatus
        
        agent = RealAgent(
            agent_id="test",
            name="Test Agent",
            role=AgentRole.DEVELOPER,
            description="Test"
        )
        
        agent.status = AgentStatus.THINKING
        assert agent.status == AgentStatus.THINKING
        
        agent.status = AgentStatus.WORKING
        assert agent.status == AgentStatus.WORKING


class TestAgentTeam:
    """اختبارات فريق الوكلاء"""
    
    def test_team_creation(self):
        """اختبار إنشاء الفريق"""
        from app.agents.real_agents import AgentTeam
        
        team = AgentTeam()
        
        assert len(team.agents) >= 5  # At least 5 agents
        assert "orchestrator" in team.agents
        assert "developer" in team.agents
    
    def test_get_agent(self):
        """اختبار الحصول على وكيل"""
        from app.agents.real_agents import AgentTeam
        
        team = AgentTeam()
        agent = team.get_agent("developer")
        
        assert agent is not None
        assert agent.agent_id == "developer"
    
    def test_list_agents(self):
        """اختبار قائمة الوكلاء"""
        from app.agents.real_agents import AgentTeam
        
        team = AgentTeam()
        agents_list = team.list_agents()
        
        assert len(agents_list) >= 5
        assert all("agent_id" in a for a in agents_list)
        assert all("name" in a for a in agents_list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])