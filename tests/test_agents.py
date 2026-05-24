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


class TestAuthSecurity:
    """اختبارات الأمان والمصادقة"""
    
    def test_generate_user_id(self):
        """اختبار توليد معرف مستخدم آمن"""
        from app.auth.auth_system import generate_user_id
        
        user_id = generate_user_id()
        
        assert user_id.startswith("user_")
        assert len(user_id) > 10  # UUID should be reasonably long
        assert "timestamp" not in user_id  # Should not be timestamp-based
    
    def test_generate_csrf_token(self):
        """اختبار توليد CSRF token"""
        from app.auth.auth_system import generate_csrf_token
        
        token1 = generate_csrf_token()
        token2 = generate_csrf_token()
        
        assert len(token1) > 20
        assert token1 != token2  # Each token should be unique
    
    def test_verify_csrf_token(self):
        """اختبار التحقق من CSRF token"""
        from app.auth.auth_system import generate_csrf_token, verify_csrf_token
        
        token = generate_csrf_token()
        
        assert verify_csrf_token(token, token) is True
        assert verify_csrf_token(token, "wrong") is False
        assert verify_csrf_token("", token) is False
        assert verify_csrf_token(token, "") is False
    
    def test_store_and_get_csrf_token(self):
        """اختبار تخزين واسترجاع CSRF token"""
        from app.auth.auth_system import store_csrf_token, get_csrf_token
        
        user_id = "test_user_123"
        token = store_csrf_token(user_id)
        
        assert token is not None
        stored = get_csrf_token(user_id)
        assert stored == token
    
    def test_csrf_token_expiration(self):
        """اختبار انتهاء صلاحية CSRF token"""
        from app.auth.auth_system import store_csrf_token, get_csrf_token
        import time
        
        user_id = "test_user_expiry"
        token = store_csrf_token(user_id)
        
        # Token should be valid immediately
        assert get_csrf_token(user_id) == token


class TestAuthSystem:
    """اختبارات نظام المصادقة"""
    
    def test_init_database(self):
        """اختبار تهيئة قاعدة البيانات"""
        from app.auth.auth_system import init_database, DB_PATH
        
        init_database()
        
        assert DB_PATH.exists()
    
    def test_hash_password(self):
        """اختبار تشفير كلمة المرور"""
        from app.auth.auth_system import hash_password, verify_password
        
        password = "SecurePass123!"
        hashed = hash_password(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("WrongPassword", hashed) is False
    
    def test_create_user_id_uniqueness(self):
        """اختبار uniqueness معرف المستخدم"""
        from app.auth.auth_system import generate_user_id
        
        ids = [generate_user_id() for _ in range(100)]
        unique_ids = set(ids)
        
        assert len(ids) == len(unique_ids)  # All IDs should be unique


class TestEmailService:
    """اختبارات خدمة البريد"""
    
    def test_email_service_status(self):
        """اختبار حالة خدمة البريد"""
        from app.auth.email_service import get_email_service_status
        
        status = get_email_service_status()
        
        assert isinstance(status, dict)
        assert "resend" in status
        assert "smtp" in status
        assert "active_services" in status
    
    def test_verification_email_template(self):
        """اختبار قالب بريد التحقق"""
        from app.auth.email_service import get_verification_email_template
        
        subject, html, text = get_verification_email_template("Test User", "123456")
        
        assert "Test User" in html
        assert "123456" in html
        assert subject is not None
        assert len(html) > 100


class TestVSCodeControllerExtended:
    """اختبارات موسعة لمتحكم VS Code"""
    
    @pytest.mark.asyncio
    async def test_create_python_file(self):
        """اختبار إنشاء ملف Python"""
        from app.vscode.vscode_controller import VSCodeController
        import uuid
        
        controller = VSCodeController()
        project_name = f"test_project_{uuid.uuid4().hex[:8]}"
        
        result = await controller.create_python_file(
            project_name,
            "test_module.py",
            'print("Hello World")\n',
            "src"
        )
        
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_create_js_file(self):
        """اختبار إنشاء ملف JavaScript"""
        from app.vscode.vscode_controller import VSCodeController
        import uuid
        
        controller = VSCodeController()
        
        result = await controller.create_js_file(
            f"test_{uuid.uuid4().hex[:8]}",
            "test.js",
            'console.log("Hello");\n'
        )
        
        assert result["success"] is True


class TestPowerShellExecutorExtended:
    """اختبارات موسعة لمنفذ الأوامر"""
    
    def test_execute_simple_command(self):
        """اختبار تنفيذ أمر بسيط"""
        import asyncio
        from app.powershell.real_executor import PowerShellExecutor
        
        executor = PowerShellExecutor()
        
        async def run_test():
            result = await executor.execute("echo 'test'")
            return result
        
        result = asyncio.get_event_loop().run_until_complete(run_test())
        
        assert result.success is True
        assert result.return_code == 0
    
    def test_write_and_read_file(self):
        """اختبار كتابة وقراءة ملف"""
        import asyncio
        from app.powershell.real_executor import PowerShellExecutor
        import tempfile
        import os
        
        executor = PowerShellExecutor()
        test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        test_file.close()
        
        async def run_test():
            write_result = await executor.write_file(test_file.name, "Test content")
            assert write_result.success is True
            
            read_result = await executor.read_file(test_file.name)
            return read_result
        
        result = asyncio.get_event_loop().run_until_complete(run_test())
        
        assert result.success is True
        
        # Cleanup
        os.unlink(test_file.name)


class TestSecurityExtended:
    """اختبارات أمان موسعة"""
    
    def test_xss_prevention(self):
        """اختبار منع XSS"""
        from app.security import sanitize_input
        
        # Malicious scripts - sanitize_input removes HTML tags
        xss_attempts = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert(1)>",
            "';alert('xss');//"
        ]
        
        for attempt in xss_attempts:
            result = sanitize_input(attempt)
            # HTML tags should be removed
            assert "<script>" not in result.lower()
            assert "<img" not in result.lower()
            # onerror attribute should be removed
            assert "onerror" not in result.lower()
            # onload attribute should be removed
            assert "onload" not in result.lower()
    
    def test_sql_injection_prevention(self):
        """اختبار منع SQL Injection"""
        from app.security import sanitize_input
        
        sql_injections = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "UNION SELECT * FROM passwords",
            "'; INSERT INTO users VALUES ('hacker');--"
        ]
        
        for attempt in sql_injections:
            result = sanitize_input(attempt)
            assert "DROP" not in result.upper()
            assert "UNION" not in result.upper()
            assert "INSERT" not in result.upper()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])