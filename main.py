"""
🌟 Real Agents - Main Application
نظام الوكلاء الحقيقيين
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from contextlib import asynccontextmanager
import uvicorn
import os
import logging
from datetime import datetime
import json

from app.agents.real_agents import real_agent_team, RealAgent, AgentMessage
from app.vscode.vscode_controller import vscode_controller
from app.powershell.real_executor import powershell_executor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("RealAgents")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة الحياة"""
    logger.info("=" * 70)
    logger.info("🌟 REAL AGENTS - نظام الوكلاء الحقيقيين")
    logger.info("=" * 70)
    
    # عرض فريق الوكلاء
    logger.info("")
    logger.info("🤖 فريق الوكلاء:")
    for agent in real_agent_team.list_agents():
        logger.info(f"  • {agent['name']} ({agent['role']}) - {agent['status']}")
    
    logger.info("")
    logger.info("💻 الأدوات المتاحة:")
    logger.info("  • VSCode Controller - إنشاء مشاريع وملفات حقيقية")
    logger.info("  • PowerShell Executor - تنفيذ أوامر حقيقية")
    logger.info("  • Memory System - ذاكرة وكلاء")
    logger.info("")
    
    logger.info("✅ النظام جاهز!")
    logger.info("=" * 70)
    
    yield
    
    logger.info("🌟 Real Agents shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Real Agents",
    description="🌟 نظام وكلاء حقيقيين - يفهمون، يتواصلون، ينفذون",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = datetime.now()
    logger.info(f"📥 {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        duration = (datetime.now() - start).total_seconds()
        logger.info(f"📤 {request.method} {request.url.path} - {response.status_code} ({duration:.3f}s)")
        return response
    except Exception as e:
        logger.error(f"❌ {request.method} {request.url.path} - Error: {e}")
        raise


# Root
@app.get("/")
async def root():
    return {
        "name": "Real Agents",
        "tagline": "🤖 وكلاء حقيقيون يفهمون وينفذون",
        "version": "1.0.0",
        "status": "operational",
        "agents": real_agent_team.list_agents(),
        "capabilities": {
            "understands_user": True,
            "asks_clarifications": True,
            "creates_real_files": True,
            "executes_real_commands": True,
            "communicates_between_agents": True,
            "remembers_and_learns": True,
            "integrates_with_vscode": True
        }
    }


# === Agent Endpoints ===
@app.get("/api/agents")
async def list_agents():
    """قائمة الوكلاء"""
    return {
        "agents": real_agent_team.list_agents(),
        "total": len(real_agent_team.list_agents())
    }


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """معلومات وكيل"""
    agent = real_agent_team.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="الوكيل غير موجود")
    return agent.get_status()


@app.post("/api/agents/{agent_id}/think")
async def agent_think(agent_id: str, request: dict):
    """تفكير الوكيل"""
    agent = real_agent_team.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="الوكيل غير موجود")
    
    message = request.get("message", "")
    thought = await agent.think(message)
    
    return {
        "agent_id": agent_id,
        "thought": {
            "thinking": thought.thinking,
            "reasoning": thought.reasoning,
            "decision": thought.decision,
            "confidence": thought.confidence
        }
    }


@app.post("/api/agents/{agent_id}/task")
async def agent_task(agent_id: str, request: dict):
    """تعيين مهمة لوكيل"""
    agent = real_agent_team.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="الوكيل غير موجود")
    
    task = request.get("task", "")
    result = await agent.work_on_task(task)
    
    return {
        "agent_id": agent_id,
        "task_id": result.task_id,
        "success": result.success,
        "output": result.output,
        "files_created": result.files_created,
        "errors": result.errors
    }


@app.post("/api/agents/{from_id}/send/{to_id}")
async def send_between_agents(from_id: str, to_id: str, request: dict):
    """إرسال رسالة بين وكلاء"""
    message = request.get("message", "")
    msg_type = request.get("type", "message")
    
    success = await real_agent_team.agent_communicate(from_id, to_id, message, msg_type)
    
    return {
        "success": success,
        "from": from_id,
        "to": to_id,
        "message": message
    }


@app.get("/api/agents/{agent_id}/inbox")
async def get_agent_inbox(agent_id: str):
    """صندوق وارد الوكيل"""
    agent = real_agent_team.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="الوكيل غير موجود")
    
    inbox = agent.inbox
    agent.inbox = []  # مسح بعد القراءة
    
    return {"inbox": inbox, "count": len(inbox)}


@app.get("/api/agents/{agent_id}/memory")
async def get_agent_memory(agent_id: str):
    """ذاكرة الوكيل"""
    agent = real_agent_team.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="الوكيل غير موجود")
    
    return agent.memory.get_memory_stats()


# === Coordinate Endpoint - المحرك الرئيسي ===
@app.post("/api/coordinate")
async def coordinate_task(request: dict):
    """تنسيق مهمة - المحرك الرئيسي"""
    task = request.get("task", "")
    
    if not task:
        raise HTTPException(status_code=400, detail="المهمة مطلوبة")
    
    result = await real_agent_team.coordinate_task(task)
    
    return result


@app.post("/api/execute")
async def execute_command(request: dict):
    """تنفيذ أمر"""
    command = request.get("command", "")
    description = request.get("description", "")
    
    if not command:
        raise HTTPException(status_code=400, detail="الأمر مطلوب")
    
    result = await powershell_executor.execute(command, description)
    
    return {
        "success": result.success,
        "command": command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return_code": result.return_code,
        "execution_time": result.execution_time
    }


# === VSCode Endpoints ===
@app.post("/api/vscode/project")
async def create_project(request: dict):
    """إنشاء مشروع وفتحه في VS Code"""
    project_name = request.get("name", "new-project")
    project_type = request.get("type", "python")
    
    result = await vscode_controller.create_project(project_name, project_type)
    
    return result


@app.post("/api/vscode/file")
async def create_file(request: dict):
    """إنشاء ملف"""
    project_name = request.get("project_name", "default")
    file_path = request.get("path", "new_file.txt")
    content = request.get("content", "")
    
    result = await vscode_controller.create_file(project_name, file_path, content)
    
    return result


@app.get("/api/vscode/file")
async def read_file(request: dict):
    """قراءة ملف"""
    file_path = request.get("path", "")
    
    if not file_path:
        raise HTTPException(status_code=400, detail="المسار مطلوب")
    
    result = await vscode_controller.read_file(file_path)
    
    return result


@app.post("/api/vscode/python")
async def create_python_file(request: dict):
    """إنشاء ملف Python"""
    project_name = request.get("project_name", "default")
    file_name = request.get("name", "main.py")
    code = request.get("code", "# Python code here")
    folder = request.get("folder", "")
    
    result = await vscode_controller.create_python_file(project_name, file_name, code, folder)
    
    return result


@app.post("/api/vscode/js")
async def create_js_file(request: dict):
    """إنشاء ملف JavaScript"""
    project_name = request.get("project_name", "default")
    file_name = request.get("name", "index.js")
    code = request.get("code", "// JavaScript code here")
    folder = request.get("folder", "")
    
    result = await vscode_controller.create_js_file(project_name, file_name, code, folder)
    
    return result


@app.post("/api/vscode/html")
async def create_html_file(request: dict):
    """إنشاء ملف HTML"""
    project_name = request.get("project_name", "default")
    file_name = request.get("name", "index.html")
    html = request.get("html", "<!DOCTYPE html><html><head></head><body></body></html>")
    folder = request.get("folder", "")
    
    result = await vscode_controller.create_html_file(project_name, file_name, html, folder)
    
    return result


@app.post("/api/vscode/react")
async def create_react_component(request: dict):
    """إنشاء مكون React"""
    project_name = request.get("project_name", "default")
    component_name = request.get("name", "Component")
    
    result = await vscode_controller.create_react_component(project_name, component_name)
    
    return result


@app.post("/api/vscode/open")
async def open_vscode(request: dict):
    """فتح VS Code"""
    path = request.get("path", None)
    result = await vscode_controller.open_vscode(path)
    return result


# === PowerShell Endpoints ===
@app.post("/api/shell")
async def run_shell_command(request: dict):
    """تشغيل أمر Shell"""
    command = request.get("command", "")
    timeout = request.get("timeout", 60)
    
    if not command:
        raise HTTPException(status_code=400, detail="الأمر مطلوب")
    
    result = await powershell_executor.execute(command, timeout=timeout)
    
    return {
        "success": result.success,
        "command": command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return_code": result.return_code
    }


@app.post("/api/shell/bash")
async def run_bash_command(request: dict):
    """تشغيل أمر Bash"""
    command = request.get("command", "")
    result = await powershell_executor.execute_bash(command)
    return {
        "success": result.success,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return_code": result.return_code
    }


@app.post("/api/shell/git")
async def run_git_command(request: dict):
    """تشغيل أمر Git"""
    command = request.get("command", "status")
    repo_path = request.get("repo_path", None)
    result = await powershell_executor.git_command(command, repo_path)
    return {
        "success": result.success,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


@app.post("/api/shell/npm")
async def run_npm_command(request: dict):
    """تشغيل أمر npm"""
    command = request.get("command", "install")
    project_path = request.get("project_path", None)
    result = await powershell_executor.run_npm_command(command, project_path)
    return {
        "success": result.success,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


@app.post("/api/shell/docker")
async def run_docker_command(request: dict):
    """تشغيل أمر Docker"""
    command = request.get("command", "ps")
    result = await powershell_executor.docker_command(command)
    return {
        "success": result.success,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


# === File Operations ===
@app.post("/api/files/create")
async def create_file_endpoint(request: dict):
    """إنشاء ملف"""
    path = request.get("path", "file.txt")
    content = request.get("content", "")
    result = await powershell_executor.write_file(path, content)
    return {"success": result.success, "path": path}


@app.post("/api/files/read")
async def read_file_endpoint(request: dict):
    """قراءة ملف"""
    path = request.get("path", "")
    if not path:
        raise HTTPException(status_code=400, detail="المسار مطلوب")
    result = await powershell_executor.read_file(path)
    return {"content": result.stdout}


@app.post("/api/files/delete")
async def delete_file_endpoint(request: dict):
    """حذف ملف"""
    path = request.get("path", "")
    force = request.get("force", False)
    result = await powershell_executor.delete_path(path, force)
    return {"success": result.success}


@app.post("/api/files/copy")
async def copy_file_endpoint(request: dict):
    """نسخ ملف"""
    source = request.get("source", "")
    destination = request.get("destination", "")
    result = await powershell_executor.copy_path(source, destination)
    return {"success": result.success}


@app.post("/api/files/list")
async def list_directory_endpoint(request: dict):
    """عرض مجلد"""
    path = request.get("path", ".")
    result = await powershell_executor.list_directory(path)
    return {"files": result.stdout}


# === System Endpoints ===
@app.get("/api/system/info")
async def system_info():
    """معلومات النظام"""
    return powershell_executor.get_system_info()


@app.get("/api/system/history")
async def command_history():
    """سجل الأوامر"""
    return {"history": powershell_executor.get_execution_history()}


@app.get("/api/health")
async def health():
    """فحص الصحة"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": len(real_agent_team.list_agents()),
        "system": powershell_executor.get_system_info()
    }


# === Interactive Chat Endpoint ===
@app.post("/api/chat")
async def chat(request: dict):
    """
    محادثة تفاعلية - المحرك الرئيسي
    يفهم المستخدم ويسأل إذا ما فهم ويشارك المعلومات بين الوكلاء
    """
    message = request.get("message", "")
    
    if not message:
        raise HTTPException(status_code=400, detail="الرسالة مطلوبة")
    
    # استخدام Orchestrator لفهم الرسالة
    orchestrator = real_agent_team.get_agent("orchestrator")
    thought = await orchestrator.think(message)
    
    # إذا القرار هو السؤال
    if thought.decision == "ask_clarification":
        understanding = orchestrator.brain.context.last_understanding
        return {
            "type": "clarification",
            "questions": understanding.suggested_questions,
            "missing_info": understanding.missing_info,
            "agent": "orchestrator"
        }
    
    # تنفيذ المهمة
    result = await orchestrator.work_on_task(message)
    
    # إذا كان هناك ملفات تم إنشاؤها
    if result.files_created:
        await orchestrator.broadcast_to_colleagues(
            f"أنشأت الملفات: {result.files_created}",
            "share"
        )
    
    return {
        "type": "task_result",
        "success": result.success,
        "output": result.output,
        "thought": thought.decision,
        "files_created": result.files_created,
        "commands_executed": result.commands_executed,
        "errors": result.errors
    }


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            "timestamp": datetime.now().isoformat()
        }
    )


# Run
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         🌟 REAL AGENTS - نظام الوكلاء الحقيقيين 🌟           ║
    ║                                                              ║
    ║    🤖 يفهم - يسأل - يتعلم - ينشئ ملفات حقيقية               ║
    ║    💻 VSCode - PowerShell - ذاكرة وكلاء                      ║
    ║    👥 فريق وكلاء يتواصلون مع بعض                            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )