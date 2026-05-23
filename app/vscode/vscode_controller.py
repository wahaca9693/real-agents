"""
💻 VSCode Real Controller - تحكم حقيقي بـ VS Code
يفتح مشاريع ويكتب كود ويعدل ويقرأ - كل شيء حقيقي
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import os
import subprocess
import json
import asyncio
from pathlib import Path


class VSCodeCommand:
    """أمر VS Code"""
    OPEN_PROJECT = "code"
    OPEN_FILE = "code"
    CREATE_FILE = "new-file"
    EDIT_FILE = "edit"
    SAVE_FILE = "save"
    CLOSE_FILE = "close"
    FIND_IN_FILES = "find"
    REPLACE_IN_FILES = "replace"
    TERMINAL = "terminal"


@dataclass
class FileModification:
    """تعديل على ملف"""
    file_path: str
    action: str  # create, edit, delete, rename
    content: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None


@dataclass
class ProjectStructure:
    """هيكل المشروع"""
    name: str
    root: str
    language: str
    framework: Optional[str] = None
    files: List[str] = field(default_factory=list)
    folders: List[str] = field(default_factory=list)


class VSCodeController:
    """
    متحكم VS Code الحقيقي - يتحكم بالـ VS Code من خلال الأوامر
    """
    
    def __init__(self, workspace_root: str = "./workspace"):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        self.open_projects: Dict[str, str] = {}  # project_name -> path
        self.current_file: Optional[str] = None
        self.modifications_log: List[Dict] = []
    
    async def open_vscode(self, path: str = None) -> Dict:
        """فتح VS Code"""
        try:
            target = path or str(self.workspace_root)
            
            # استخدام الأمر الحقيقي لفتح VS Code
            if os.name == 'nt':  # Windows
                subprocess.Popen(["code", target], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
            else:  # Linux/Mac
                subprocess.Popen(["code", target], 
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                start_new_session=True)
            
            return {
                "success": True,
                "action": "opened_vscode",
                "path": target,
                "message": f"تم فتح VS Code في: {target}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "لم يتم فتح VS Code - تأكد من تثبيته"
            }
    
    async def create_project(self, project_name: str, project_type: str = "python") -> Dict:
        """إنشاء مشروع جديد وفتحه في VS Code"""
        
        project_path = self.workspace_root / "projects" / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # إنشاء هيكل المشروع حسب النوع
        if project_type == "python":
            await self._create_python_project(project_path, project_name)
        elif project_type == "javascript":
            await self._create_js_project(project_path, project_name)
        elif project_type == "android":
            await self._create_android_project(project_path, project_name)
        else:
            await self._create_generic_project(project_path, project_name)
        
        # فتح المشروع في VS Code
        await self.open_vscode(str(project_path))
        
        self.open_projects[project_name] = str(project_path)
        
        return {
            "success": True,
            "project_name": project_name,
            "project_path": str(project_path),
            "type": project_type,
            "structure": list(project_path.rglob("*"))
        }
    
    async def _create_python_project(self, path: Path, name: str):
        """إنشاء مشروع Python"""
        # إنشاء الملفات الأساسية
        (path / "main.py").write_text('''"""{} - Main Module"""\n\n\ndef main():\n    print("Hello from {}!")\n\n\nif __name__ == "__main__":\n    main()\n'''.format(name, name))
        
        (path / "requirements.txt").write_text("# Requirements\n")
        (path / "README.md").write_text(f"# {name}\n\n")
        (path / ".gitignore").write_text("__pycache__/\n*.pyc\n.env\nvenv/\n")
        
        # إنشاء مجلدات
        (path / "src").mkdir(exist_ok=True)
        (path / "tests").mkdir(exist_ok=True)
        (path / "docs").mkdir(exist_ok=True)
        
        # إنشاء ملفات الاختبار
        (path / "tests" / "test_main.py").write_text('''"""Tests for main module"""\nimport pytest\n\n\ndef test_example():\n    assert True\n''')
    
    async def _create_js_project(self, path: Path, name: str):
        """إنشاء مشروع JavaScript"""
        (path / "package.json").write_text(json.dumps({
            "name": name,
            "version": "1.0.0",
            "scripts": {"start": "node index.js"},
            "dependencies": {}
        }, indent=2))
        
        (path / "index.js").write_text('''// {} - Main Entry Point\n\nconsole.log("Hello from {}!");\n'''.format(name, name))
        
        (path / "README.md").write_text(f"# {name}\n\n")
        (path / "src").mkdir(exist_ok=True)
    
    async def _create_android_project(self, path: Path, name: str):
        """إنشاء مشروع أندرويد"""
        # هيكل مشروع أندرويد أساسي
        (path / "app").mkdir(exist_ok=True)
        (path / "app" / "src").mkdir(exist_ok=True)
        (path / "app" / "src" / "main").mkdir(exist_ok=True)
        (path / "app" / "src" / "main" / "kotlin").mkdir(exist_ok=True)
        (path / "app" / "src" / "main" / "res").mkdir(exist_ok=True)
        
        (path / "build.gradle.kts").write_text('''// Top-level build file\nplugins {\n    id("com.android.application") version "8.1.0" apply false\n}\n''')
        
        (path / "settings.gradle.kts").write_text('''pluginManagement {\n    repositories {\n        google()\n        mavenCentral()\n    }\n}\n\ndependencyResolutionManagement {\n    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)\n    repositories {\n        google()\n        mavenCentral()\n    }\n}\n\nrootProject.name = "{}"\ninclude(":app")\n'''.format(name))
        
        (path / "app" / "build.gradle.kts").write_text('''plugins {\n    id("com.android.application")\n}\n\nandroid {\n    namespace = "com.example.{}"\n    compileSdk = 34\n\n    defaultConfig {\n        applicationId = "com.example.{}"\n        minSdk = 24\n        targetSdk = 34\n    }\n\n    buildFeatures {\n        viewBinding = true\n    }\n}\n\ndependencies {\n    implementation("androidx.core:core-ktx:1.12.0")\n    implementation("androidx.appcompat:appcompat:1.6.1")\n}\n'''.format(name, name))
        
        # Main Activity
        main_activity_path = path / "app" / "src" / "main" / "kotlin" / "com" / "example" / f"{name.replace(' ', '')}Activity.kt"
        main_activity_path.parent.mkdir(parents=True, exist_ok=True)
        main_activity_path.write_text('''package com.example.{}

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class {}Activity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        // Your code here
    }}
}}
'''.format(name.replace(' ', '').lower(), name.replace(' ', '')))
    
    async def _create_generic_project(self, path: Path, name: str):
        """إنشاء مشروع عام"""
        (path / "README.md").write_text(f"# {name}\n\n")
        (path / "src").mkdir(exist_ok=True)
    
    async def create_file(self, project_name: str, file_path: str, content: str) -> Dict:
        """إنشاء ملف جديد"""
        
        # البحث عن المشروع - إما في المشاريع المفتوحة أو في workspace
        project_path = self.open_projects.get(project_name)
        if not project_path:
            # البحث في workspace/projects
            potential_path = self.workspace_root / "projects" / project_name
            if potential_path.exists():
                project_path = str(potential_path)
            else:
                # إنشاء المشروع إذا لم يكن موجوداً
                potential_path.mkdir(parents=True, exist_ok=True)
                project_path = str(potential_path)
        
        full_path = Path(project_path) / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # تحديد اللغة من امتداد الملف
        language = self._get_language_from_extension(full_path.suffix)
        
        full_path.write_text(content, encoding='utf-8')
        
        # محاولة فتح الملف في VS Code (اختياري)
        vscode_opened = False
        if os.name == 'nt':
            try:
                subprocess.Popen(["code", str(full_path)], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
                vscode_opened = True
            except FileNotFoundError:
                pass
        else:
            try:
                subprocess.Popen(["code", str(full_path)],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                start_new_session=True)
                vscode_opened = True
            except FileNotFoundError:
                pass
        
        self.modifications_log.append({
            "action": "create_file",
            "path": str(full_path),
            "language": language,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "file_path": str(full_path),
            "language": language,
            "opened_in_vscode": vscode_opened
        }
    
    async def edit_file(self, file_path: str, modifications: List[FileModification]) -> Dict:
        """تعديل ملف موجود"""
        
        path = Path(file_path)
        if not path.exists():
            return {"success": False, "error": "الملف غير موجود"}
        
        # قراءة الملف
        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # تطبيق التعديلات
        for mod in modifications:
            if mod.action == "replace_lines":
                # استبدال أسطر معينة
                if mod.line_start and mod.line_end:
                    new_lines = lines[:mod.line_start-1]
                    new_lines.append(mod.content or "")
                    new_lines.extend(lines[mod.line_end:])
                    lines = new_lines
            
            elif mod.action == "append":
                lines.append(mod.content or "")
            
            elif mod.action == "prepend":
                lines.insert(0, mod.content or "")
        
        # كتابة الملف
        path.write_text('\n'.join(lines), encoding='utf-8')
        
        self.modifications_log.append({
            "action": "edit_file",
            "path": str(path),
            "modifications_count": len(modifications),
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "file_path": str(path),
            "modifications_applied": len(modifications)
        }
    
    async def delete_file(self, file_path: str) -> Dict:
        """حذف ملف"""
        path = Path(file_path)
        
        if path.exists():
            path.unlink()
            
            self.modifications_log.append({
                "action": "delete_file",
                "path": str(path),
                "timestamp": datetime.now().isoformat()
            })
            
            return {"success": True, "deleted": str(path)}
        
        return {"success": False, "error": "الملف غير موجود"}
    
    async def read_file(self, file_path: str) -> Dict:
        """قراءة محتوى ملف"""
        path = Path(file_path)
        
        if not path.exists():
            return {"success": False, "error": "الملف غير موجود"}
        
        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        return {
            "success": True,
            "file_path": str(path),
            "content": content,
            "lines": len(lines),
            "size": len(content)
        }
    
    async def execute_in_terminal(self, command: str, project_name: str = None) -> Dict:
        """تنفيذ أمر في Terminal"""
        
        if project_name and project_name in self.open_projects:
            working_dir = self.open_projects[project_name]
        else:
            working_dir = str(self.workspace_root)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "command": command,
                "working_directory": working_dir,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out",
                "command": command
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    async def create_python_file(self, project_name: str, file_name: str, 
                                code_content: str, folder: str = "") -> Dict:
        """إنشاء ملف Python"""
        if folder:
            file_path = f"{folder}/{file_name}"
        else:
            file_path = file_name
        
        return await self.create_file(project_name, file_path, code_content)
    
    async def create_js_file(self, project_name: str, file_name: str,
                            code_content: str, folder: str = "") -> Dict:
        """إنشاء ملف JavaScript"""
        if not file_name.endswith('.js'):
            file_name += '.js'
        
        if folder:
            file_path = f"{folder}/{file_name}"
        else:
            file_path = file_name
        
        return await self.create_file(project_name, file_path, code_content)
    
    async def create_html_file(self, project_name: str, file_name: str,
                               html_content: str, folder: str = "") -> Dict:
        """إنشاء ملف HTML"""
        if not file_name.endswith('.html'):
            file_name += '.html'
        
        if folder:
            file_path = f"{folder}/{file_name}"
        else:
            file_path = file_name
        
        return await self.create_file(project_name, file_path, html_content)
    
    async def create_css_file(self, project_name: str, file_name: str,
                              css_content: str, folder: str = "") -> Dict:
        """إنشاء ملف CSS"""
        if not file_name.endswith('.css'):
            file_name += '.css'
        
        if folder:
            file_path = f"{folder}/{file_name}"
        else:
            file_path = file_name
        
        return await self.create_file(project_name, file_path, css_content)
    
    async def create_react_component(self, project_name: str, component_name: str) -> Dict:
        """إنشاء مكون React"""
        component_code = '''import React from 'react';

const {} = () => {{
    return (
        <div className="{}">
            {/* Component content */}
        </div>
    );
}};

export default {};
'''.format(component_name, component_name.lower(), component_name)
        
        folder = "src/components"
        return await self.create_file(
            project_name, 
            f"{folder}/{component_name}.jsx", 
            component_code
        )
    
    async def create_flask_route(self, project_name: str, route_path: str,
                                 code_content: str) -> Dict:
        """إنشاء route في Flask"""
        return await self.create_file(project_name, route_path, code_content)
    
    async def create_fastapi_endpoint(self, project_name: str, endpoint_file: str,
                                      code_content: str) -> Dict:
        """إنشاء endpoint في FastAPI"""
        return await self.create_file(project_name, endpoint_file, code_content)
    
    def _get_language_from_extension(self, extension: str) -> str:
        """تحديد اللغة من امتداد الملف"""
        languages = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascriptreact',
            '.ts': 'typescript',
            '.tsx': 'typescriptreact',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.md': 'markdown',
            '.sql': 'sql',
            '.kt': 'kotlin',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust'
        }
        return languages.get(extension, 'plaintext')
    
    def get_modifications_log(self) -> List[Dict]:
        """الحصول على سجل التعديلات"""
        return self.modifications_log
    
    def list_open_projects(self) -> List[Dict]:
        """قائمة المشاريع المفتوحة"""
        return [
            {"name": name, "path": path}
            for name, path in self.open_projects.items()
        ]


# === Global Instance ===
vscode_controller = VSCodeController()