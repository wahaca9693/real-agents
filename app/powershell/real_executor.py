"""
⚡ PowerShell Real Executor - منفذ أوامر حقيقي
ينفذ أوامر حقيقية على النظام - ليس مجرد محاكاة
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import subprocess
import os
import shutil
import platform
from pathlib import Path


@dataclass
class Command:
    """أمر"""
    command_id: str
    command: str
    description: str
    category: str
    parameters: Dict[str, Any] = None


@dataclass
class ExecutionResult:
    """نتيجة التنفيذ"""
    command_id: str
    command: str
    success: bool
    stdout: str
    stderr: str
    return_code: int
    execution_time: float


class PowerShellExecutor:
    """
    منفذ PowerShell الحقيقي - ينفذ أي أمر على النظام
    """
    
    def __init__(self, workspace_dir: str = "./workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.execution_history: List[ExecutionResult] = []
        self.environment = self._get_system_info()
    
    def _get_system_info(self) -> Dict:
        """الحصول على معلومات النظام"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
            "cwd": os.getcwd()
        }
    
    async def execute(self, command: str, description: str = "", 
                     timeout: int = 60, shell: str = "powershell") -> ExecutionResult:
        """تنفيذ أمر"""
        
        start_time = datetime.now()
        
        try:
            # تحديد الـ shell
            if self.environment["os"] == "Windows":
                shell_cmd = ["powershell", "/c", command]
            else:
                # Linux/Mac
                shell_cmd = command.split()
            
            # تنفيذ الأمر
            if self.environment["os"] == "Windows":
                result = subprocess.run(
                    ["powershell", "-Command", command],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=str(self.workspace_dir)
                )
            else:
                # For Linux, use bash or sh
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=str(self.workspace_dir)
                )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            exec_result = ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=command,
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                execution_time=execution_time
            )
            
            self.execution_history.append(exec_result)
            
            return exec_result
            
        except subprocess.TimeoutExpired:
            exec_result = ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=command,
                success=False,
                stdout="",
                stderr="Command timed out",
                return_code=-1,
                execution_time=timeout
            )
            self.execution_history.append(exec_result)
            return exec_result
            
        except Exception as e:
            exec_result = ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=command,
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=0
            )
            self.execution_history.append(exec_result)
            return exec_result
    
    async def execute_bash(self, command: str, description: str = "", 
                           timeout: int = 60) -> ExecutionResult:
        """تنفيذ أمر Bash"""
        return await self.execute(command, description, timeout, shell="bash")
    
    async def execute_python(self, code: str) -> ExecutionResult:
        """تنفيذ كود Python"""
        return await self.execute(
            f"python -c \"{code.replace('\"', '\\\"')}\"",
            "Python inline execution",
            timeout=30
        )
    
    async def install_package(self, package: str, package_manager: str = "pip") -> ExecutionResult:
        """تثبيت حزمة"""
        
        if package_manager == "pip":
            return await self.execute(f"pip install {package}", f"Installing {package}")
        elif package_manager == "npm":
            return await self.execute(f"npm install {package}", f"Installing {package}")
        elif package_manager == "apt":
            return await self.execute(f"sudo apt install {package}", f"Installing {package}")
        
        return ExecutionResult(
            command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            command=f"install {package}",
            success=False,
            stdout="",
            stderr="Unknown package manager",
            return_code=-1,
            execution_time=0
        )
    
    async def git_clone(self, repo_url: str, target_dir: str = None) -> ExecutionResult:
        """استنساخ مستودع Git"""
        
        if not target_dir:
            target_dir = self.workspace_dir / "repos"
        else:
            target_dir = Path(target_dir)
        
        return await self.execute(
            f"git clone {repo_url} {target_dir}",
            f"Cloning {repo_url}"
        )
    
    async def git_command(self, command: str, repo_path: str = None) -> ExecutionResult:
        """تنفيذ أمر Git"""
        
        if repo_path:
            full_cmd = f"cd {repo_path} && git {command}"
        else:
            full_cmd = f"git {command}"
        
        return await self.execute(full_cmd, f"Git: {command}")
    
    async def create_directory(self, dir_path: str) -> ExecutionResult:
        """إنشاء مجلد"""
        path = Path(dir_path)
        path.mkdir(parents=True, exist_ok=True)
        
        return ExecutionResult(
            command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            command=f"mkdir {dir_path}",
            success=True,
            stdout=f"Directory created: {dir_path}",
            stderr="",
            return_code=0,
            execution_time=0
        )
    
    async def delete_path(self, path: str, force: bool = False) -> ExecutionResult:
        """حذف ملف أو مجلد"""
        
        path_obj = Path(path)
        
        try:
            if path_obj.is_file():
                path_obj.unlink()
            elif path_obj.is_dir():
                if force:
                    shutil.rmtree(path_obj)
                else:
                    path_obj.rmdir()
            
            return ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=f"delete {path}",
                success=True,
                stdout=f"Deleted: {path}",
                stderr="",
                return_code=0,
                execution_time=0
            )
        except Exception as e:
            return ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=f"delete {path}",
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=0
            )
    
    async def copy_path(self, source: str, destination: str) -> ExecutionResult:
        """نسخ ملف أو مجلد"""
        
        try:
            shutil.copy2(source, destination)
            
            return ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=f"copy {source} to {destination}",
                success=True,
                stdout=f"Copied: {source} -> {destination}",
                stderr="",
                return_code=0,
                execution_time=0
            )
        except Exception as e:
            return ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=f"copy {source}",
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=0
            )
    
    async def move_path(self, source: str, destination: str) -> ExecutionResult:
        """نقل ملف أو مجلد"""
        
        try:
            shutil.move(source, destination)
            
            return ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=f"move {source} to {destination}",
                success=True,
                stdout=f"Moved: {source} -> {destination}",
                stderr="",
                return_code=0,
                execution_time=0
            )
        except Exception as e:
            return ExecutionResult(
                command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                command=f"move {source}",
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=0
            )
    
    async def list_directory(self, dir_path: str = ".") -> ExecutionResult:
        """عرض محتويات مجلد"""
        return await self.execute(
            f"ls -la {dir_path}" if self.environment["os"] != "Windows" else f"Get-ChildItem -Path {dir_path}",
            f"List directory: {dir_path}"
        )
    
    async def read_file(self, file_path: str) -> ExecutionResult:
        """قراءة ملف"""
        return await self.execute(
            f"cat {file_path}" if self.environment["os"] != "Windows" else f"Get-Content {file_path}",
            f"Read file: {file_path}"
        )
    
    async def write_file(self, file_path: str, content: str) -> ExecutionResult:
        """كتابة ملف"""
        
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        
        return ExecutionResult(
            command_id=f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            command=f"write {file_path}",
            success=True,
            stdout=f"Written: {file_path} ({len(content)} bytes)",
            stderr="",
            return_code=0,
            execution_time=0
        )
    
    async def search_files(self, pattern: str, directory: str = ".") -> ExecutionResult:
        """البحث عن ملفات"""
        
        return await self.execute(
            f"find {directory} -name '{pattern}'" if self.environment["os"] != "Windows" else f"Get-ChildItem -Path {directory} -Recurse -Filter '{pattern}'",
            f"Search: {pattern}"
        )
    
    async def process_list(self) -> ExecutionResult:
        """عرض العمليات الجارية"""
        
        if self.environment["os"] == "Windows":
            return await self.execute("Get-Process | Select-Object -First 20 Name, CPU, WorkingSet", "Process list")
        else:
            return await self.execute("ps aux | head -20", "Process list")
    
    async def kill_process(self, pid: int) -> ExecutionResult:
        """إيقاف عملية"""
        return await self.execute(f"kill {pid}" if self.environment["os"] != "Windows" else f"Stop-Process -Id {pid} -Force", f"Kill process {pid}")
    
    async def network_info(self) -> ExecutionResult:
        """معلومات الشبكة"""
        
        if self.environment["os"] == "Windows":
            return await self.execute("ipconfig /all", "Network info")
        else:
            return await self.execute("ifconfig", "Network info")
    
    async def check_port(self, host: str, port: int) -> ExecutionResult:
        """فحص منفذ"""
        return await self.execute(
            f"Test-NetConnection -ComputerName {host} -Port {port}" if self.environment["os"] == "Windows" else f"nc -zv {host} {port}",
            f"Check port {port}"
        )
    
    async def download_file(self, url: str, destination: str = None) -> ExecutionResult:
        """تحميل ملف"""
        
        if not destination:
            destination = self.workspace_dir / "downloads"
        
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        
        return await self.execute(
            f"curl -o {destination} {url}" if self.environment["os"] != "Windows" else f"Invoke-WebRequest -Uri {url} -OutFile {destination}",
            f"Download: {url}"
        )
    
    async def docker_command(self, command: str) -> ExecutionResult:
        """تنفيذ أمر Docker"""
        return await self.execute(f"docker {command}", f"Docker: {command}")
    
    async def run_docker_container(self, image: str, name: str = None, 
                                   ports: Dict = None, env: Dict = None) -> ExecutionResult:
        """تشغيل حاوية Docker"""
        
        cmd_parts = ["docker", "run", "-d"]
        
        if name:
            cmd_parts.extend(["--name", name])
        
        if ports:
            for host_port, container_port in ports.items():
                cmd_parts.extend(["-p", f"{host_port}:{container_port}"])
        
        if env:
            for key, value in env.items():
                cmd_parts.extend(["-e", f"{key}={value}"])
        
        cmd_parts.append(image)
        
        return await self.execute(" ".join(cmd_parts), f"Run container: {image}")
    
    async def run_npm_command(self, command: str, project_path: str = None) -> ExecutionResult:
        """تنفيذ أمر npm"""
        
        if project_path:
            full_cmd = f"cd {project_path} && npm {command}"
        else:
            full_cmd = f"npm {command}"
        
        return await self.execute(full_cmd, f"npm: {command}")
    
    async def run_gradle_command(self, command: str, project_path: str) -> ExecutionResult:
        """تنفيذ أمر Gradle"""
        return await self.execute(f"cd {project_path} && ./gradlew {command}", f"Gradle: {command}")
    
    async def system_update(self) -> ExecutionResult:
        """تحديث النظام"""
        
        if self.environment["os"] == "Windows":
            return await self.execute("winget upgrade --all", "System update")
        else:
            return await self.execute("sudo apt update && sudo apt upgrade -y", "System update")
    
    def get_execution_history(self, limit: int = 50) -> List[Dict]:
        """الحصول على سجل التنفيذ"""
        return [
            {
                "command_id": r.command_id,
                "command": r.command,
                "success": r.success,
                "return_code": r.return_code,
                "execution_time": r.execution_time,
                "timestamp": datetime.now().isoformat()
            }
            for r in self.execution_history[-limit:]
        ]
    
    def get_system_info(self) -> Dict:
        """الحصول على معلومات النظام"""
        return self.environment


# === Global Instance ===
powershell_executor = PowerShellExecutor()