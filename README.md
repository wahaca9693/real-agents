# 🤖 Real Agents - نظام الوكلاء الذكيين الحقيقيين

<div align="center">

**نظام وكلاء يفهمون، يتواصلون، ينفذون - 100% حقيقي**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 الوصف

**Real Agents** هو نظام وكلاء ذكاء اصطناعي حقيقيين يعملون كفريق متكامل:

- 🧠 **يفهمون** ما يريده المستخدم
- ❓ **يسألون** إذا ما فهموا
- 💻 **ينفذون أوامر حقيقية** على النظام
- 👥 **يتواصلون مع بعض** ويشاركون المعلومات
- 🧠 **يتعلمون** من التجارب
- 💾 **يتذكرون** كل شيء

---

## 🏗️ بنية المشروع

```
real-agents/
├── app/
│   ├── brain/                    # 🧠 عقل الوكيل
│   │   └── agent_brain.py       # فهم المستخدم، التفكير، التعلم
│   ├── agents/                   # 👥 فريق الوكلاء
│   │   ├── real_agents.py        # الوكلاء الحقيقيون
│   │   ├── routes.py             # مسارات API الوكلاء
│   │   └── team.py               # إدارة الفريق
│   ├── memory/                   # 💾 نظام الذاكرة
│   │   └── agent_memory.py       # ذاكرة قصيرة وطويلة المدى
│   ├── vscode/                   # 💻 تكامل VSCode
│   │   └── vscode_controller.py  # تحكم حقيقي بالـ VSCode
│   ├── powershell/               # ⚡ منفذ الأوامر
│   │   └── real_executor.py      # تنفيذ أوامر حقيقية
│   └── auth/                     # 🔐 نظام المصادقة
│       ├── auth_system.py        # نظام المصادقة
│       ├── email_service.py      # خدمة البريد
│       └── routes.py             # مسارات المصادقة
├── frontend/                     # 🎨 واجهة المستخدم (React + Vite)
│   ├── src/
│   │   ├── components/           # المكونات
│   │   │   ├── AgentMessage.jsx
│   │   │   ├── InputBox.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── Toast.jsx
│   │   └── pages/                # الصفحات
│   │       ├── Dashboard.jsx
│   │       ├── ChatPage.jsx
│   │       ├── Login.jsx
│   │       ├── Register.jsx
│   │       └── Settings.jsx
│   └── package.json
├── tests/                        # 🧪 الاختبارات
│   └── test_agents.py
├── workspace/                    # 📁 مساحة العمل
├── main.py                       # 🚀 نقطة البداية
├── requirements.txt              # 📦 تبعيات Python
└── .env.example                  # ⚙️ متغيرات البيئة

---

## 🤖 الوكلاء

| الوكيل | الدور | المسؤوليات |
|-------|-------|-----------|
| **Orchestrator** | المدير | التنسيق والتوزيع |
| **Developer** | المطور | كتابة الكود |
| **Designer** | المصمم | تصميم الواجهات |
| **Researcher** | الباحث | جمع المعلومات |
| **Tester** | الفاحص | اختبار الكود |
| **Deployer** | الناشر | النشر والتنفيذ |

---

## 💻 القدرات الحقيقية

### 1. VSCode Controller
```python
# ✅ إنشاء مشاريع حقيقية
await vscode.create_project("my-app", "python")

# ✅ إنشاء ملفات
await vscode.create_python_file("app.py", "# كود Python")
await vscode.create_js_file("app.js", "// كود JavaScript")
await vscode.create_html_file("index.html", "<html>...</html>")

# ✅ تعديل الملفات
await vscode.edit_file("app.py", modifications)

# ✅ فتح مشاريع في VSCode
await vscode.open_vscode("/path/to/project")
```

### 2. PowerShell Executor
```python
# ✅ تنفيذ أي أمر
await powershell.execute("pip install flask")

# ✅ أوامر Git
await powershell.git_clone("https://github.com/user/repo.git")
await powershell.git_command("commit -m 'message'")

# ✅ Docker
await powershell.docker_command("ps -a")
await powershell.run_docker_container("nginx")

# ✅ npm/npm
await powershell.run_npm_command("install", project_path)
```

### 3. Agent Brain
```python
# ✅ فهم المستخدم
await agent.think("ابني لي موقع ويب")

# ✅ السؤال إذا ما فهم
await agent.ask_user([
    "ما نوع التصميم المطلوب؟",
    "هل تريد REST API؟",
    "ما قاعدة البيانات المفضلة؟"
])

# ✅ التأكيد
summary = await agent.confirm("سأنشئ موقع ويب بـ React")
```

### 4. Memory System
```python
# ✅ حفظ في الذاكرة
await agent.remember("أنشأت ملف app.py", "experience")

# ✅ الاستدعاء من الذاكرة
memories = await agent.recall("ملفات")

# ✅ مشاركة معرفة
await shared_memory.share_knowledge(agent_id, knowledge)

# ✅ تعلم أنماط
await agent.learn_pattern("how_to_build_websites", success=True)
```

### 5. Communication
```python
# ✅ إرسال رسالة
await agent.send_message("developer", "أنشئ API")

# ✅ استقبال رسالة
await agent.receive_message(message)

# ✅ بث للجميع
await agent.broadcast_to_colleagues("العمل منتهي")
```

---

## 🚀 التشغيل

### 1. التثبيت

**الخطوة 1: استنساخ المشروع**
```bash
git clone https://github.com/wahaca9693/real-agents.git
cd real-agents
```

**الخطوة 2: إنشاء بيئة افتراضية**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو: venv\Scripts\activate  # Windows
```

**الخطوة 3: تثبيت التبعيات**
```bash
pip install -r requirements.txt
```

**الخطوة 4: إعداد متغيرات البيئة**
```bash
cp .env.example .env
# ثم عدل .env وأضف المفاتيح الخاصة بك
```

### 2. تشغيل الخادم

```bash
# تشغيل التطبيق
python main.py

# أو مع uvicorn
uvicorn main:app --reload --port 8000
```

### 3. تشغيل الواجهة الأمامية (الفرنت)
```bash
cd frontend
npm install
npm run dev
```

### 4. فتح API Docs
```
http://localhost:8000/docs
http://localhost:8000/redoc
```

---

## 📡 API Endpoints

### الوكلاء
| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/agents` | قائمة الوكلاء |
| GET | `/api/agents/{id}` | معلومات وكيل |
| POST | `/api/agents/{id}/task` | تعيين مهمة |
| POST | `/api/agents/{id}/think` | تفكير الوكيل |

### VSCode
| Method | Endpoint | الوصف |
|--------|----------|-------|
| POST | `/api/vscode/project` | إنشاء مشروع |
| POST | `/api/vscode/file` | إنشاء ملف |
| POST | `/api/vscode/python` | ملف Python |
| POST | `/api/vscode/js` | ملف JavaScript |
| POST | `/api/vscode/html` | ملف HTML |
| POST | `/api/vscode/react` | مكون React |

### الأوامر
| Method | Endpoint | الوصف |
|--------|----------|-------|
| POST | `/api/shell` | تنفيذ أمر |
| POST | `/api/shell/git` | أمر Git |
| POST | `/api/shell/npm` | أمر npm |
| POST | `/api/shell/docker` | أمر Docker |

### المحادثة
| Method | Endpoint | الوصف |
|--------|----------|-------|
| POST | `/api/chat` | محادثة تفاعلية |
| POST | `/api/coordinate` | تنسيق مهمة |

---

## 💡 أمثلة

### 1. بناء مشروع
```bash
curl -X POST http://localhost:8000/api/vscode/project \
  -H "Content-Type: application/json" \
  -d '{"name": "my-website", "type": "javascript"}'
```

### 2. تنفيذ أمر
```bash
curl -X POST http://localhost:8000/api/shell \
  -H "Content-Type: application/json" \
  -d '{"command": "pip install fastapi"}'
```

### 3. محادثة
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "ابني لي موقع ويب بسيط"}'
```

---

## 📊 الإحصائيات

| المقياس | القيمة |
|---------|--------|
| الملفات | 19 |
| سطور الكود | 2500+ |
| الوكلاء | 6 |
| الأدوات | 30+ |
| APIs | 25+ |

---

## 🔧 التقنيات المستخدمة

- **Python 3.8+** - اللغة الأساسية
- **FastAPI** - إطار الويب
- **asyncio** - التنفيذ غير المتزامن
- **subprocess** - تنفيذ الأوامر
- **pathlib** - إدارة الملفات
- **json** - التعامل مع البيانات

---

## 📝 الترخيص

MIT License - свободное использование

---

## 👨‍💻 المطور

**OpenHands Agent**

---

<div align="center">

**⭐ إذا أعجبك المشروع، أعطه نجمة!**

</div>