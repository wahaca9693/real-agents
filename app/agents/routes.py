"""
Agent Team API Routes
مسارات API لفريق الوكلاء
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.agents.team import (
    agent_manager,
    AgentType,
    get_team_info,
    get_agents_list,
    create_task
)

router = APIRouter(prefix="/team", tags=["فريق العمل"])

# ============================================================================
# Pydantic Models - نماذج البيانات
# ============================================================================

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="عنوان المهمة")
    description: str = Field(..., min_length=10, description="وصف المهمة")
    task_type: str = Field(
        default="development",
        description="نوع المهمة: development, design, research, deployment, testing, security, documentation, full_stack, complex"
    )
    priority: int = Field(default=1, ge=1, le=5, description="الأولوية: 1-5")

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    type: str
    priority: int
    status: str
    assigned_agents: List[str]
    result: Optional[dict] = None

class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: str
    capabilities: List[str]
    icon: str
    status: str
    completed_tasks: int
    performance: float

# ============================================================================
# Team Endpoints - مسارات الفريق
# ============================================================================

@router.get("/team", summary="معلومات الفريق")
async def get_team():
    """
    الحصول على معلومات فريق العمل
    """
    return {
        "success": True,
        "team": get_team_info()
    }

@router.get("/list", summary="قائمة الوكلاء")
async def list_agents():
    """
    الحصول على قائمة جميع الوكلاء في الفريق
    """
    return {
        "success": True,
        "count": len(get_agents_list()),
        "agents": get_agents_list()
    }

@router.get("/stats", summary="إحصائيات الفريق")
async def get_team_stats():
    """
    الحصول على إحصائيات أداء الفريق
    """
    from app.agents.team import agent_manager
    
    if not agent_manager.active_team:
        return {"success": False, "error": "لا يوجد فريق نشط"}
    
    team = agent_manager.active_team
    
    # حساب الإحصائيات
    total_tasks = len(team.tasks)
    completed_tasks = len([t for t in team.tasks if t.status == "completed"])
    in_progress = len([t for t in team.tasks if t.status == "in_progress"])
    failed_tasks = len([t for t in team.tasks if t.status == "failed"])
    
    # متوسط أداء الوكلاء
    avg_performance = sum(a.performance_score for a in team.agents) / len(team.agents) if team.agents else 0
    
    return {
        "success": True,
        "stats": {
            "total_tasks": total_tasks,
            "completed": completed_tasks,
            "in_progress": in_progress,
            "failed": failed_tasks,
            "completion_rate": f"{(completed_tasks / total_tasks * 100):.1f}%" if total_tasks > 0 else "0%",
            "team_performance": f"{avg_performance:.1f}",
            "agents_count": len(team.agents),
            "available_agents": len(team.get_available_agents())
        }
    }

@router.get("/leaderboard", summary="لوحة المتصدرين")
async def get_leaderboard():
    """
    الحصول على ترتيب الوكلاء حسب الأداء
    """
    agents = get_agents_list()
    sorted_agents = sorted(agents, key=lambda x: x["performance"], reverse=True)
    
    return {
        "success": True,
        "leaderboard": [
            {
                "rank": i + 1,
                "name": a["name"],
                "role": a["role"],
                "performance": a["performance"],
                "completed_tasks": a["completed_tasks"],
                "icon": a["icon"]
            }
            for i, a in enumerate(sorted_agents)
        ]
    }

# ============================================================================
# Agent Endpoints - مسارات الوكلاء الفرديين
# ============================================================================

@router.get("/by-id/{agent_id}", summary="معلومات وكيل")
async def get_agent(agent_id: str):
    """
    الحصول على معلومات وكيل محدد
    """
    agents = get_agents_list()
    agent = next((a for a in agents if a["id"] == agent_id), None)
    
    if not agent:
        raise HTTPException(status_code=404, detail="الوكيل غير موجود")
    
    return {
        "success": True,
        "agent": agent
    }

@router.get("/role/{role}", summary="الوكلاء حسب الدور")
async def get_agents_by_role(role: str):
    """
    الحصول على الوكلاء من نوع محدد
    """
    try:
        agent_type = AgentType(role)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"نوع الوكيل '{role}' غير معروف")
    
    return {
        "success": True,
        "role": role,
        "agents": [a for a in get_agents_list() if a["role"] == role]
    }

@router.get("/available", summary="الوكلاء المتاحين")
async def get_available_agents():
    """
    الحصول على الوكلاء المتاحين حالياً
    """
    return {
        "success": True,
        "agents": [a for a in get_agents_list() if a["status"] == "idle"]
    }

# ============================================================================
# Task Endpoints - مسارات المهام
# ============================================================================

@router.post("/tasks/create", summary="إنشاء مهمة جديدة", response_model=TaskResponse)
async def create_new_task(request: TaskCreateRequest):
    """
    إنشاء مهمة جديدة وتوزيعها على الوكلاء المناسبين
    """
    result = create_task(
        title=request.title,
        description=request.description,
        task_type=request.task_type
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result["task"]

@router.get("/tasks/list", summary="قائمة المهام")
async def list_tasks():
    """
    الحصول على قائمة جميع المهام
    """
    from app.agents.team import agent_manager
    if agent_manager.active_team:
        return {
            "success": True,
            "count": len(agent_manager.active_team.tasks),
            "tasks": [t.to_dict() for t in agent_manager.active_team.tasks]
        }
    return {"success": True, "tasks": []}

@router.get("/tasks/by-id/{task_id}", summary="معلومات مهمة")
async def get_task(task_id: str):
    """
    الحصول على معلومات مهمة محددة
    """
    from app.agents.team import agent_manager
    if agent_manager.active_team:
        task = next((t for t in agent_manager.active_team.tasks if t.id == task_id), None)
        if task:
            return {"success": True, "task": task.to_dict()}
    
    raise HTTPException(status_code=404, detail="المهمة غير موجودة")

@router.get("/tasks/status/{status}", summary="المهام حسب الحالة")
async def get_tasks_by_status(status: str):
    """
    الحصول على المهام حسب حالتها
    """
    from app.agents.team import agent_manager
    if agent_manager.active_team:
        tasks = [t.to_dict() for t in agent_manager.active_team.tasks if t.status == status]
        return {
            "success": True,
            "status": status,
            "count": len(tasks),
            "tasks": tasks
        }
    return {"success": True, "tasks": []}