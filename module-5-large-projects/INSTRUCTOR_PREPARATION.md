# Instructor Preparation Guide — Module 5: Large Project Best Practices

> ไฟล์นี้สำหรับ **ผู้สอนอ่านเตรียมตัว** ก่อนสอน Workshop
> เขียนแบบ step-by-step ละเอียด — อธิบายว่าแต่ละ step ทำอะไร ทำไมถึงทำ และต้องพูดอะไรกับผู้เรียน

---

## สารบัญ

- [ภาพรวม Workshop](#ภาพรวม-workshop)
- [ไฟล์ทั้งหมดใน Workshop](#ไฟล์ทั้งหมดใน-workshop)
- [เตรียมตัวก่อนสอน](#เตรียมตัวก่อนสอน)
- [Section 0: Setup](#section-0-setup--prerequisites-10-นาที)
- [Section 1: Building Blocks](#section-1-claude-code-building-blocks-10-นาที)
- [Section 2: CLAUDE.md](#section-2-claudemd--background-knowledge-10-นาที)
- [Section 3: Git Worktrees](#section-3-git-worktrees-10-นาที)
- [Section 4: Token Optimization + Issue #3](#section-4-token-optimization--implement-issue-3-15-นาที)
- [Section 5: Multiple Issues](#section-5-multiple-issues--the-interruption-20-นาที)
- [Section 6: PR Review Cycle](#section-6-pr-review-cycle-15-นาที)
- [Section 7: Skills Deep Dive](#section-7-skills-deep-dive-15-นาที)
- [Section 8: Advanced Techniques](#section-8-advanced-techniques-10-นาที)
- [แก้ปัญหาเบื้องต้น](#แก้ปัญหาเบื้องต้น)

---

## ภาพรวม Workshop

### เป้าหมาย

ผู้เรียนจะได้เรียนรู้วิธีทำงานกับโปรเจคใหญ่ด้วย Claude Code อย่างมีประสิทธิภาพ:
- เข้าใจ 5 Building Blocks ของ Claude Code
- ใช้ Git Worktrees ทำหลาย issue พร้อมกัน
- ใช้เทคนิค Token Optimization ประหยัด context
- แก้ PR review comments อย่างมีระบบ
- ใช้ Skills + MCP ทำงานร่วมกัน

### เรื่องราว (Narrative)

Workshop เล่าเรื่องของ developer ที่ทำงานจริง 1 วัน:

```
เช้า: ได้รับ Issue #3 (input validation) → เริ่ม research → implement
กลางวัน: ถูก interrupt ด้วย Issue #6 (CORS) เร่งด่วน → จอด #3 → ทำ #6 → PR
บ่าย: กลับมาต่อ #3 → PR → ได้ review comments → แก้ → push
เย็น: เรียนรู้ Skills automation + advanced techniques
```

### ทำไมเลือก Issue #3 และ #6?

- **Issue #3 (input validation)** — ซับซ้อนปานกลาง ต้องแก้ models.py + เพิ่ม dependency + เขียน tests หลายตัว
  เหมาะสำหรับสอน research → compact → implement flow
- **Issue #6 (CORS)** — ง่ายมาก (~5 lines) ทำเสร็จใน 5 นาที
  เหมาะเป็น "urgent interrupt" ที่สาธิตว่า worktree ช่วยให้ switch เร็ว

### เวลา

| Section | เวลา | ประเภท |
|---------|------|--------|
| 0. Setup | 10 min | Hands-on |
| 1. Building Blocks | 10 min | Concept |
| 2. CLAUDE.md | 10 min | Concept + Demo |
| 3. Worktrees | 10 min | Hands-on |
| 4. Token Opt + Issue #3 | 15 min | Hands-on |
| 5. Multiple Issues | 20 min | Hands-on |
| 6. PR Review | 15 min | Hands-on |
| 7. Skills Deep Dive | 15 min | Concept + Demo |
| 8. Advanced | 10 min | Instructor Demo |
| **รวม** | **~115 min** | |

---

## ไฟล์ทั้งหมดใน Workshop

### โครงสร้าง Repository

```
spped2000/claude-workshop (GitHub)
│
├── CLAUDE.md                          ← [1] Root CLAUDE.md
├── PARTICIPANT_GUIDE.md               ← [2] คู่มือ Module 4 (ไม่ใช้ใน Module 5)
├── large-project-best-practices.md    ← [3] Reference document
├── skills-vs-mcp.md                   ← [4] Skills vs MCP comparison
│
├── workshop-project/                  ← [5] FastAPI project ที่ผู้เรียนทำงาน
│   ├── CLAUDE.md                      ← [6] Project CLAUDE.md
│   ├── README.md                      ← [7] Quick start guide
│   ├── pyproject.toml                 ← [8] Dependencies + pytest config
│   ├── app/
│   │   ├── __init__.py
│   │   ├── CLAUDE.md                  ← [9] Subdirectory CLAUDE.md (lazy loading demo)
│   │   ├── main.py                    ← [10] FastAPI app
│   │   ├── models.py                  ← [11] Pydantic models (ผู้เรียนแก้ไฟล์นี้ใน Issue #3)
│   │   ├── database.py                ← [12] In-memory storage
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── users.py               ← [13] User CRUD routes
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                ← [14] Test fixtures (autouse reset)
│   │   ├── test_users.py              ← [15] 9 existing user tests
│   │   └── test_health.py             ← [16] 3 health check tests
│   └── .claude/
│       └── skills/
│           ├── implement-issue/SKILL.md  ← [17] Skill: implement issue
│           ├── fix-review/SKILL.md       ← [18] Skill: fix PR review
│           └── explore-issue/SKILL.md    ← [19] Skill: explore issue (context:fork)
│
├── module-5-large-projects/           ← [20] โฟลเดอร์ Workshop นี้
│   ├── WORKSHOP.md                    ← [21] เอกสาร workshop หลัก
│   ├── BUILDING_BLOCKS.md             ← [22] Handout: 5 building blocks
│   ├── INSTRUCTOR_NOTES.md            ← [23] Quick reference สำหรับผู้สอน
│   ├── INSTRUCTOR_PREPARATION.md      ← [24] ไฟล์นี้ — เตรียมตัวละเอียด
│   └── skills/
│       └── explore-issue/SKILL.md     ← [25] Copy ต้นฉบับของ explore-issue
│
├── github-issues/                     ← [26] สำเนา issue templates
│   ├── issue-101-health-check.md
│   ├── issue-102-request-logging.md
│   ├── issue-103-input-validation.md  ← ใช้ใน workshop (= GitHub Issue #3)
│   ├── issue-104-soft-delete.md
│   ├── issue-105-search-endpoint.md
│   ├── issue-106-cors-configuration.md ← ใช้ใน workshop (= GitHub Issue #6)
│   └── issue-107-response-compression.md
│
├── global-skills/                     ← [27] Skills ต้นฉบับ (reference)
│   ├── implement-issue/SKILL.md
│   └── fix-review/SKILL.md
│
└── instructor-demo/                   ← [28] Demo script Module 4
    └── demo-script.md
```

### อธิบายไฟล์สำคัญทีละตัว

---

#### [1] `CLAUDE.md` (Root)

```
ตำแหน่ง: claude-workshop/CLAUDE.md
บทบาท: Ancestor CLAUDE.md — โหลดทุก session ที่เปิดใน repo นี้
```

**เนื้อหาหลัก:**
- ภาพรวมว่า repo นี้มี 2 modules (Module 4 + Module 5)
- โครงสร้าง directory
- ตาราง 7 GitHub issues
- ชี้ไปที่ `workshop-project/CLAUDE.md` สำหรับ MCP config

**ทำไมสำคัญ:**
เมื่อผู้เรียนเปิด Claude Code ที่ใดก็ตามใน repo นี้ Claude จะอ่านไฟล์นี้ก่อนเสมอ
เป็นตัวอย่าง "ancestor loading" — โหลดขึ้นไปเรื่อยๆ จาก directory ปัจจุบันถึง root

---

#### [6] `workshop-project/CLAUDE.md` (Project)

```
ตำแหน่ง: claude-workshop/workshop-project/CLAUDE.md
บทบาท: Project-specific CLAUDE.md — บอก Claude ทุกอย่างเกี่ยวกับ FastAPI project
```

**เนื้อหาหลัก (38 บรรทัด):**
- Project overview: FastAPI + in-memory storage + Python 3.11
- MCP servers ที่ใช้ได้: github (get_issue, create_branch, create_pull_request)
- Task ที่ต้องทำ: Read issue → implement → test → PR
- Coding conventions: async def, Pydantic v2, no SQLAlchemy
- Project structure map: ไฟล์ไหนทำอะไร
- Run commands: `uv run pytest`, `uv run uvicorn`
- Test pattern: ตัวอย่าง code สำหรับเขียน test

**ทำไมสำคัญ:**
ไฟล์นี้คือ "คู่มือพนักงานใหม่" — Claude อ่านแล้วรู้ทุกอย่างเกี่ยวกับ project โดยไม่ต้อง explore ไฟล์เอง
เป็นตัวอย่างที่ดีของ CLAUDE.md: สั้น (38 บรรทัด), ชัดเจน, ครบถ้วน

**อธิบายให้ผู้เรียนฟัง:**
> "ไฟล์นี้ 38 บรรทัด แต่ทำให้ Claude ประหยัด tokens ไปเป็นหมื่น
> เพราะ Claude ไม่ต้องเปิดอ่าน 10 ไฟล์เพื่อเข้าใจ project"

---

#### [9] `workshop-project/app/CLAUDE.md` (Subdirectory)

```
ตำแหน่ง: claude-workshop/workshop-project/app/CLAUDE.md
บทบาท: Subdirectory CLAUDE.md — demo lazy loading
```

**เนื้อหา (5 บรรทัด):**
```markdown
# App Layer — Component Context
- main.py: FastAPI entry point, middleware registration, health check
- routers/users.py: All user CRUD routes — new feature routes go here
- models.py: Pydantic v2 request/response models, use Field() for validation
- database.py: In-memory dict store — never import SQLAlchemy
```

**ทำไมสำคัญ:**
ไฟล์นี้สาธิต "lazy loading" — Claude จะ **ไม่** อ่านไฟล์นี้ตอนเริ่ม session
จะอ่านก็ต่อเมื่อ Claude ทำงานกับไฟล์ใน `app/` directory เท่านั้น

**อธิบายให้ผู้เรียนฟัง:**
> "Root CLAUDE.md โหลดเสมอ (ancestor loading)
> แต่ CLAUDE.md ที่อยู่ลึกลงไปใน subdirectory จะโหลดเมื่อ Claude เข้าไปทำงานในนั้น
> แบบนี้ project ใหญ่ที่มี 50 components ไม่ต้องโหลด CLAUDE.md ทุกอันตั้งแต่แรก"

---

#### [10] `workshop-project/app/main.py`

```python
from fastapi import FastAPI
from app.routers import users

app = FastAPI(title="Workshop API", version="1.0.0")
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": app.version}
```

**บทบาท:** Entry point ของ FastAPI app — **ตั้งใจให้ขาด** middleware (logging, CORS, GZip)
ผู้เรียนที่ทำ Issue #6 (CORS) จะแก้ไฟล์นี้

---

#### [11] `workshop-project/app/models.py`

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
```

**บทบาท:** Pydantic models — **ตั้งใจไม่มี validation** (ไม่มี EmailStr, ไม่มี Field)
ผู้เรียนที่ทำ Issue #3 (validation) จะแก้ไฟล์นี้เป็นหลัก

**อธิบายให้ผู้เรียนฟัง (ก่อน Section 4):**
> "ดู models.py ตอนนี้ — name เป็นแค่ str, email เป็นแค่ str, age เป็นแค่ int
> ไม่มี validation เลย ส่ง email: 'xxx' หรือ age: -999 ก็รับ
> Issue #3 ให้เราเพิ่ม validation เข้าไป"

---

#### [12] `workshop-project/app/database.py`

```python
from typing import Any

users_db: dict[int, dict[str, Any]] = {}
_next_id: int = 1

def get_next_id() -> int: ...
def get_user(user_id: int) -> dict | None: ...
def create_user(data: dict) -> dict: ...
def update_user(user_id: int, data: dict) -> dict | None: ...
def delete_user(user_id: int) -> bool: ...
```

**บทบาท:** In-memory dict storage — **ตั้งใจไม่มี** soft_delete, restore, search

---

#### [14] `workshop-project/tests/conftest.py`

```python
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app import database

@pytest.fixture(autouse=True)
def reset_db():
    database.users_db.clear()
    database._next_id = 1
    yield

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
```

**บทบาท:** Test fixtures ที่สำคัญมาก:
- `reset_db` (autouse=True) → **reset database ทุก test** อัตโนมัติ ไม่ต้องเรียกเอง
- `client` → AsyncClient สำหรับ test async endpoints

**อธิบายให้ผู้เรียนฟัง:**
> "`autouse=True` หมายความว่า fixture นี้รันก่อนทุก test โดยอัตโนมัติ
> ไม่ต้องเขียน `def test_something(reset_db)` — มันรันเองเสมอ
> นี่ทำให้ทุก test เริ่มจาก database ว่างเสมอ ไม่มี state ค้าง"

---

#### [8] `workshop-project/pyproject.toml`

```toml
[project]
name = "workshop-api"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi==0.115.0",
    "uvicorn[standard]==0.30.6",
    "pydantic==2.8.0",
]

[dependency-groups]
dev = [
    "httpx==0.27.0",
    "pytest==8.3.0",
    "pytest-asyncio==0.23.8",
    "anyio==4.4.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

**จุดสำคัญ:**
- `asyncio_mode = "auto"` → ผู้เรียน **ไม่ต้อง** เขียน `@pytest.mark.asyncio` บนทุก test
- Dependencies แยกเป็น `dependencies` (production) กับ `dev` (testing)
- `pydantic[email]` **ยังไม่มี** — ผู้เรียน Issue #3 จะต้องเพิ่มเอง (`uv add pydantic[email]`)

---

#### [17] `workshop-project/.claude/skills/implement-issue/SKILL.md`

```yaml
---
name: implement-issue
description: Read a GitHub issue via MCP, implement the feature, write tests, open a PR.
argument-hint: [issue-number]
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash
---
```

**บทบาท:** Skill ที่ทำ workflow ทั้งหมดใน 1 command: `/implement-issue 3`
- Step 1: อ่าน issue ผ่าน GitHub MCP
- Step 2: Implement ตาม acceptance criteria
- Step 3: เขียน tests + รัน
- Step 4: สร้าง PR ผ่าน GitHub MCP

**`disable-model-invocation: true`** → Claude จะ **ไม่เรียก** skill นี้เอง ผู้เรียนต้องพิมพ์ `/implement-issue` เอง
เพราะ skill นี้มี side effects (create PR, push code)

---

#### [18] `workshop-project/.claude/skills/fix-review/SKILL.md`

```yaml
---
name: fix-review
description: Read PR review comments via GitHub MCP and fix all requested changes.
argument-hint: [pr-number]
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Glob Grep
---
```

**บทบาท:** Skill สำหรับแก้ PR review comments: `/fix-review 5`
- Step 1: อ่าน review comments ผ่าน MCP
- Step 2: แก้เฉพาะที่ reviewer ขอ
- Step 3: รัน tests
- Step 4: Commit + push (ไม่สร้าง PR ใหม่)

**ใช้ใน Section 6** — เปรียบเทียบกับ manual approach

---

#### [19] `workshop-project/.claude/skills/explore-issue/SKILL.md`

```yaml
---
name: explore-issue
description: Research a GitHub issue and summarize findings without polluting main context.
argument-hint: [issue-number]
context: fork
agent: Explore
allowed-tools: Read Glob Grep
---
```

**บทบาท:** Skill สำหรับ research ที่ไม่ปน context: `/explore-issue 4`
- `context: fork` → ทำงานใน context แยก
- `agent: Explore` → ใช้ Explore subagent (read-only, เร็ว)
- Return summary กลับ → main context ไม่บวม

**ใช้ใน Section 7C** — สาธิต `context: fork`

---

#### [22] `module-5-large-projects/BUILDING_BLOCKS.md`

**บทบาท:** Handout ที่แจกให้ผู้เรียน — ใช้ reference ตลอด workshop
- ตาราง 5 Building Blocks
- Comparison แบบละเอียด
- Skills + MCP complementary relationship
- Progressive Disclosure
- SKILL.md anatomy (frontmatter fields)
- Decision framework: เมื่อไหร่ใช้อะไร

**อธิบายให้ผู้เรียนฟัง (ตอนแจก):**
> "เก็บไฟล์นี้ไว้ เปิดดูได้ตลอด workshop
> เวลาผมพูดถึง building block ไหน เปิดดูตาราง reference ได้เลย"

---

## เตรียมตัวก่อนสอน

### Checklist

- [ ] **GitHub Token** — เตรียม Personal Access Token (scope: `repo`) สำหรับแจกผู้เรียน
      หรือให้ผู้เรียนสร้างเอง (ต้องมี GitHub account)
- [ ] **ทดสอบ clone ใหม่** — `git clone → uv sync → uv run pytest` ต้อง 12 passed
- [ ] **ทดสอบ MCP** — `claude mcp list` ต้องเห็น `github: connected`
- [ ] **ทดสอบ worktree** — `git worktree add ../test -b test` ต้องทำงานได้
- [ ] **Issues มีอยู่** — `gh issue list --repo spped2000/claude-workshop` ต้องเห็น #3 และ #6 เปิดอยู่
- [ ] **พิมพ์/share BUILDING_BLOCKS.md** — handout สำหรับผู้เรียน
- [ ] **เตรียม review comments** — จะใส่ใน PR ของผู้เรียนระหว่าง Section 5→6 transition
- [ ] **ลบ branches เก่า** — ถ้าเคยทดสอบมาก่อน ลบ `feat/issue-3-*` และ `feat/issue-6-*` ออก

### Review Comments ที่เตรียมไว้

ใส่ใน PR ของ Issue #3 (validation) ของผู้เรียน ระหว่าง transition Section 5→6:

**Comment 1** — ไฟล์ `tests/test_validation.py`, บรรทัดท้ายๆ:
```
Please add a test case for email with leading/trailing spaces,
e.g. " alice@example.com ". Should the API accept or reject this?
```

**Comment 2** — ไฟล์ `app/models.py`, บรรทัดที่มี age field:
```
The validation error message for invalid age should include the valid range.
Users should see something like "Age must be between 0 and 150".
```

**Comment 3** — ไฟล์ `tests/test_validation.py`, หลัง test สุดท้าย:
```
Please add boundary tests: age=0 and age=150 should be valid,
age=-1 and age=151 should be rejected.
```

---

## Section 0: Setup & Prerequisites (10 นาที)

### สิ่งที่ต้องอธิบาย

> "ก่อนเริ่ม เราต้องมีเครื่องมือ 4 อย่าง: Python 3.11+, uv (package manager เร็วกว่า pip 10 เท่า), Claude Code CLI, และ Node.js (สำหรับรัน MCP server)"

### Step-by-step

**Step 0.1: ตรวจเครื่องมือ**

ให้ผู้เรียนรันทีละคำสั่ง:

```bash
python --version          # ต้อง 3.11+
uv --version              # ถ้าไม่มี → ติดตั้ง (ดูด้านล่าง)
claude --version           # Claude Code CLI
node --version             # Node.js สำหรับ MCP
```

ถ้ายังไม่มี uv:
```bash
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> **อธิบาย:** "uv เป็น package manager สำหรับ Python ที่เร็วกว่า pip มาก เขียนด้วย Rust
> ใช้แทน `pip install` ด้วย `uv sync` และแทน `pip install package` ด้วย `uv add package`"

**Step 0.2: Clone และ Install**

```bash
git clone https://github.com/spped2000/claude-workshop.git
cd claude-workshop/workshop-project
uv sync
```

> **อธิบาย:** "`uv sync` อ่าน `pyproject.toml` แล้วติดตั้ง dependencies ทั้งหมดให้
> สร้าง `.venv` ใน directory นี้โดยอัตโนมัติ"

**Step 0.3: ทดสอบว่า project ทำงาน**

```bash
uv run pytest -v
```

> **อธิบาย:** "ต้องเห็น 12 passed — 9 tests สำหรับ user CRUD + 3 tests สำหรับ health check
> ถ้า fail อะไร แจ้งผมเลย"

**ผลที่ต้องเห็น:**
```
tests/test_health.py::test_health_returns_200 PASSED
tests/test_health.py::test_health_response_body PASSED
tests/test_health.py::test_health_works_with_empty_db PASSED
tests/test_users.py::test_list_users_empty PASSED
... (9 tests)
============================= 12 passed ==============================
```

**Step 0.4: ติดตั้ง GitHub MCP**

```bash
# Windows PowerShell — set token ก่อน
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# เพิ่ม MCP server
claude mcp add github -e GITHUB_TOKEN=$env:GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github
```

```bash
# macOS/Linux
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
claude mcp add github -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github
```

> **อธิบาย:** "คำสั่งนี้บอก Claude Code ว่ามี MCP server ชื่อ `github`
> MCP คือ Model Context Protocol — ทำให้ Claude ใช้เครื่องมือภายนอกได้
> ในที่นี้ Claude จะอ่าน GitHub issues, สร้าง branches, เปิด PR ได้โดยตรง
> `-e GITHUB_TOKEN=...` ส่ง token ให้ MCP server ใช้ authenticate กับ GitHub"

**Step 0.5: ตรวจว่า MCP ทำงาน**

```bash
claude mcp list
```

**ผลที่ต้องเห็น:**
```
github: connected
```

> **ถ้า "Failed to connect":** token อาจไม่ถูกต้อง หรือ set token หลังจาก mcp add
> วิธีแก้: set token ก่อน แล้วรัน `claude mcp add` อีกครั้ง

---

## Section 1: Claude Code Building Blocks (10 นาที)

### สิ่งที่ต้องอธิบาย

> "ก่อนลงมือทำ ผมอยากให้เห็นภาพรวมก่อน
> Claude Code ไม่ได้มีแค่พิมพ์ prompt แล้วรอ — มันมี 5 ส่วนประกอบที่ทำงานร่วมกัน"

### Step-by-step

**Step 1.1: แจก Handout**

แจก `BUILDING_BLOCKS.md` (พิมพ์ หรือ share digital) แล้วเปิดให้ดูตาราง:

| Building Block | ทำหน้าที่ | ภาษาง่ายๆ |
|----------------|----------|-----------|
| **Prompts** | คำสั่งชั่วขณะ | "สิ่งที่ฉันต้องการ **ตอนนี้**" |
| **CLAUDE.md** | ความรู้พื้นฐาน | "สิ่งที่คุณต้อง **รู้**" |
| **Skills** | ความรู้เชิงกระบวนการ | "**วิธีทำ** สิ่งต่างๆ" |
| **MCP** | เชื่อมต่อเครื่องมือภายนอก | "**มือ** ที่จับสิ่งภายนอก" |
| **Subagents** | มอบหมายงาน | "**คนที่ทำงานแทน**" |

> **อธิบาย:**
> "ลองคิดแบบนี้:
> - **Prompts** = คำสั่งที่คุณพิมพ์ตอนนี้ เช่น 'อ่าน issue #3 ให้หน่อย' — มันหายไปหลัง conversation จบ
> - **CLAUDE.md** = ความรู้พื้นฐานเกี่ยวกับ project — Claude อ่านทุกครั้งที่เริ่ม session โดยไม่ต้องบอก
> - **Skills** = procedure ที่สอน Claude ว่า 'ถ้าต้อง implement issue ให้ทำ step 1, 2, 3, 4'
> - **MCP** = เครื่องมือที่ Claude ใช้เชื่อมกับโลกภายนอก — อ่าน GitHub issues, สร้าง PR
> - **Subagents** = คน (Claude ตัวเล็ก) ที่ Claude ส่งไปทำงานแทน — เช่น research codebase"

**Step 1.2: Key Insight — Skills + MCP = Complementary**

> **อธิบาย:**
> "สิ่งที่สำคัญที่สุดที่อยากให้จำ: Skills กับ MCP ทำงาน **ด้วยกัน** ไม่ใช่เลือกอย่างเดียว
>
> MCP = ให้มือ Claude จับสิ่งภายนอก (อ่าน issue, สร้าง PR)
> Skills = สอน Claude ว่าจะใช้มือนั้นทำอะไร (อ่าน → implement → test → PR)
>
> ถ้ามี MCP แต่ไม่มี Skill → Claude มีเครื่องมือแต่ไม่รู้ workflow
> ถ้ามี Skill แต่ไม่มี MCP → Claude รู้ workflow แต่ไม่มีเครื่องมือ
>
> ต้องมีทั้งคู่ — จะเห็นตัวอย่างจริงใน Section 6-7"

**Step 1.3: Key Insight — Progressive Disclosure**

> **อธิบาย:**
> "Skills ฉลาดตรงที่ไม่โหลดทั้งหมดตั้งแต่แรก
> ถ้ามี 20 Skills ติดตั้ง Claude ไม่ได้อ่านทุกอันเต็มๆ
> มันอ่านแค่ 'คำอธิบาย' สั้นๆ ของแต่ละ Skill (~100 tokens)
> แล้วค่อยโหลดเต็มเฉพาะตัวที่ relevant
> แบบนี้ประหยัด context window มาก — จะอธิบายเพิ่มใน Section 7"

**Step 1.4: ถามผู้เรียน (interactive)**

> "คำถาม: ใน setup ที่เราเพิ่งทำ (Section 0) เราใช้ building block อะไรไปบ้างแล้ว?"
>
> คำตอบ: **MCP** (ติดตั้ง GitHub MCP server)
> ที่เหลือจะได้ใช้ในแต่ละ section ต่อไป

---

## Section 2: CLAUDE.md — Background Knowledge (10 นาที)

### สิ่งที่ต้องอธิบาย

> "ตอนนี้เรามาดู building block แรกที่ Claude ใช้ทุก session — CLAUDE.md
> มันเหมือนให้คู่มือพนักงานใหม่ก่อนวันแรกของการทำงาน"

### Step-by-step

**Step 2.1: อ่าน CLAUDE.md ด้วยกัน**

```bash
cat workshop-project/CLAUDE.md
```

> **อธิบายขณะอ่าน:**
> "ดูนะ ไฟล์นี้แค่ 38 บรรทัด แต่บอก Claude ทุกอย่าง:
> - บรรทัด 1-4: overview — FastAPI, in-memory, Python 3.11
> - บรรทัด 6-8: MCP servers ที่ใช้ได้ — github
> - บรรทัด 10-14: task — อ่าน issue → implement → test → PR
> - บรรทัด 16-22: coding conventions — async def, Pydantic v2
> - บรรทัด 24-33: project structure map — ไฟล์ไหนทำอะไร
> - บรรทัด 35-38: run commands — `uv run pytest`, `uv run uvicorn`
>
> Claude อ่านไฟล์นี้ก่อนทุก session — รู้ทุกอย่างใน ~500 tokens
> ถ้าไม่มีไฟล์นี้ Claude ต้อง explore ไฟล์เอง — เสีย 5,000-10,000 tokens"

**Step 2.2: Demo — Claude รู้จาก CLAUDE.md**

```bash
cd workshop-project
claude
```

พิมพ์ใน Claude:
```
What do you know about this project? What MCP servers are available?
```

> **ชี้ให้ผู้เรียนเห็น:**
> "ดู — Claude ตอบได้ทันทีว่า:
> - 'FastAPI REST API with in-memory storage'
> - 'GitHub MCP is available'
> - 'Tests are in tests/ directory'
>
> แต่ดูที่ tool calls — Claude **ไม่ได้ใช้ Read tool** อ่านไฟล์ใดๆ เลย
> ทั้งหมดมาจาก CLAUDE.md ที่โหลดตอนเริ่ม session"

ออกจาก Claude:
```
/exit
```

**Step 2.3: อธิบาย Loading Model**

วาดรูป (whiteboard หรือ share screen):

```
📁 claude-workshop/
├── CLAUDE.md              ← Ancestor Loading: โหลดเสมอ ↑
├── workshop-project/
│   ├── CLAUDE.md          ← Ancestor Loading: โหลดเสมอ ↑
│   └── app/
│       └── CLAUDE.md      ← Lazy Loading: โหลดเมื่อแตะ app/ ↓
```

> **อธิบาย:**
> "CLAUDE.md มี 2 แบบ:
>
> **Ancestor Loading (ขึ้น ↑):** Claude หา CLAUDE.md จาก directory ปัจจุบัน ขึ้นไปเรื่อยๆ จนถึง root
> ทุกอันที่เจอ → โหลด **ทุก session** ทันที
>
> **Lazy Loading (ลง ↓):** CLAUDE.md ที่อยู่ใน subdirectory ลึกกว่า working directory
> → โหลด **เมื่อ Claude เข้าไปทำงานกับไฟล์ใน directory นั้น** เท่านั้น
>
> ทำไมสำคัญ? ถ้า project มี 50 modules แต่คุณทำงานแค่ 2 modules
> Claude ไม่ต้องอ่าน CLAUDE.md ของทั้ง 50 → ประหยัด tokens"

**Step 2.4: Best Practices**

> "CLAUDE.md ที่ดี:
> - **สั้น** — ≤200 บรรทัด (Claude อาจไม่ follow ถ้ายาวเกิน)
> - **Architecture** — ไฟล์อะไรอยู่ตรงไหน ทำอะไร
> - **Conventions** — ใช้ async def, ตั้งชื่อแบบไหน
> - **Run commands** — test ยังไง, start server ยังไง
> - **What NOT to touch** — ไฟล์ที่ห้ามแก้
>
> CLAUDE.md ที่ไม่ดี:
> - Full API documentation (ยาวเกิน)
> - ข้อมูลที่เปลี่ยนบ่อย (outdated เร็ว)
> - Copy-paste ทั้ง README"

---

## Section 3: Git Worktrees (10 นาที)

### สิ่งที่ต้องอธิบาย

> "ถ้าทำ 3 issues พร้อมกัน ปกติต้อง stash → switch branch → แก้ → switch back → pop
> มีวิธีที่ดีกว่ามาก — Git Worktrees"

### Step-by-step

**Step 3.1: อธิบายปัญหาเดิม**

> "สมมติทำ Issue #3 อยู่ ยังไม่เสร็จ แล้ว Issue #6 เร่งด่วนเข้ามา:
>
> ```bash
> git stash                         # เก็บงาน Issue #3 ไว้ก่อน
> git checkout -b feat/issue-6      # สร้าง branch Issue #6
> # ... แก้ Issue #6 ...
> git commit && git push
> git checkout feat/issue-3         # กลับไป Issue #3
> git stash pop                     # เอางานเดิมกลับมา
> # 😱 merge conflict!
> ```
>
> ปัญหา: stash อาจ conflict, context ปนกัน, ลืม stash pop"

**Step 3.2: อธิบาย Worktree**

> "Worktree = directory แยกที่มี branch ของตัวเอง แต่ใช้ git history เดียวกัน
>
> ```
> 📁 (parent directory)
> ├── claude-workshop/          ← main branch (git root)
> ├── issue-3-validation/       ← feat/issue-3-validation (worktree)
> └── issue-6-cors/             ← feat/issue-6-cors (worktree)
> ```
>
> แต่ละ directory มี branch ของตัวเอง เปิด terminal แยก ไม่กระทบกัน
> ไม่ต้อง stash, ไม่ต้อง switch — แค่ `cd` ไปอีก directory"

**Step 3.3: ผู้เรียนสร้าง Worktree**

> "ต้องรันจาก **git root** คือ `claude-workshop` ไม่ใช่ `workshop-project`"

```bash
cd claude-workshop

# สร้าง worktree
git worktree add ../issue-3-validation -b feat/issue-3-validation
```

> **อธิบายคำสั่ง:**
> "`git worktree add` = สร้าง directory ใหม่
> `../issue-3-validation` = path ของ directory ใหม่ (ข้างๆ claude-workshop)
> `-b feat/issue-3-validation` = สร้าง branch ใหม่ชื่อนี้"

**Step 3.4: Verify**

```bash
git worktree list
```

**ผลที่ต้องเห็น:**
```
/path/to/claude-workshop           abc1234 [main]
/path/to/issue-3-validation        abc1234 [feat/issue-3-validation]
```

```bash
cd ../issue-3-validation
ls workshop-project/
cat workshop-project/CLAUDE.md | head -5
ls workshop-project/.claude/skills/
```

> **ชี้ให้เห็น:**
> "ดู — worktree มีไฟล์เหมือน repo เดิมเลย
> CLAUDE.md ยังอยู่ (ancestor loading จาก main repo)
> Skills 3 ตัวก็อยู่ (implement-issue, fix-review, explore-issue)
> แต่อยู่บน branch แยก — แก้อะไรไม่กระทบ main"

**Step 3.5: อธิบาย `claude -w` (shortcut)**

> **อธิบาย:**
> "ที่เราเพิ่งทำ 2 คำสั่ง:
> ```bash
> git worktree add ../issue-3-validation -b feat/issue-3-validation
> cd ../issue-3-validation/workshop-project
> claude
> ```
>
> Claude Code มี flag `-w` (หรือ `--worktree`) ที่รวม **ทุกอย่าง** ให้ในคำสั่งเดียว:
> ```bash
> claude -w
> ```
>
> เบื้องหลัง `claude -w` ทำอะไร:
> 1. สร้าง git worktree ให้อัตโนมัติ (ตั้ง branch name ให้)
> 2. cd เข้าไปใน worktree นั้น
> 3. เริ่ม Claude session ทันที
> 4. **ถ้า Claude ไม่ได้แก้ไฟล์อะไรเลย** → worktree ถูกลบอัตโนมัติ (auto-cleanup)
> 5. **ถ้า Claude แก้ไฟล์** → worktree ยังอยู่ บอก path และ branch ให้
>
> ข้อดีของ `-w`:
> - **ไม่ต้องคิดชื่อ branch** — Claude ตั้งให้
> - **ไม่ต้อง cd** — เข้า worktree ให้เลย
> - **auto-cleanup** — ถ้าไม่ได้ใช้จริง ลบให้ไม่ต้องจัดการเอง
>
> ข้อเสียของ `-w` (ทำไมเราสอน manual ก่อน):
> - **ไม่เห็นว่าเกิดอะไร** — ผู้เรียนไม่เข้าใจว่า worktree คืออะไร
> - **ชื่อ branch อาจไม่ตรง convention** — manual ตั้งเองได้ เช่น `feat/issue-3-validation`
> - **ต้องเข้าใจ concept ก่อน** ถึงจะใช้ shortcut ได้อย่างมั่นใจ
>
> ในชีวิตจริง:
> - **ทำ issue เร่งด่วนเร็วๆ** → ใช้ `claude -w` (สะดวก)
> - **ทำ issue สำคัญ ต้องตั้งชื่อ branch ตาม convention** → ใช้ manual
>
> Desktop App (Mac/Windows) ก็มี checkbox 'worktree' ที่ทำสิ่งเดียวกัน"
>
> **Demo (ถ้ามีเวลา):**
> ```bash
> cd claude-workshop
> claude -w
> ```
> ให้ผู้เรียนเห็นว่า Claude สร้าง worktree + เริ่ม session ทันที
> แล้ว `/exit` → ถ้าไม่ได้แก้อะไร worktree จะถูกลบอัตโนมัติ

**Step 3.6: Core Principle**

> "จำไว้: **1 Issue = 1 Worktree = 1 Claude Session**
> - Context ไม่ปนกันระหว่าง issues
> - ทำงานหลาย issue พร้อมกันได้ (terminal คนละ tab)
> - ไม่ต้อง stash หรือ switch branch"

---

## Section 4: Token Optimization + Implement Issue #3 (15 นาที)

### สิ่งที่ต้องอธิบาย

> "ตอนนี้เรามาทำ Issue #3 กัน — แต่ระหว่างทำ จะสอนเทคนิค Token Optimization ไปด้วย
> เทคนิคหลัก: **Research → /compact → Implement → Test**"

### Step-by-step

**Step 4.1: เข้า Worktree + เปิด Claude**

```bash
cd ../issue-3-validation/workshop-project
claude
```

**Step 4.2: ดู Context Baseline**

พิมพ์ใน Claude:
```
/context
```

> **อธิบาย:**
> "`/context` แสดง context usage เป็น visual grid
> ตอนนี้แทบว่าง — มีแค่ CLAUDE.md overhead
> จำตรงนี้ไว้ จะกลับมาดูอีกทีหลัง research"

**Step 4.3: Research Phase**

```
Read issue #3 from spped2000/claude-workshop.
Summarize the acceptance criteria as a numbered checklist.
Do not implement yet.
```

> **อธิบายขณะ Claude ทำงาน:**
> "ดูที่ Claude ทำ:
> 1. เรียก GitHub MCP → tool call `get_issue` → ดึง issue #3 จาก GitHub
> 2. สรุป acceptance criteria เป็น checklist
>
> สังเกตว่าเราบอก 'Do not implement yet' — ทำไม?
> เพราะเราต้องการ **แยก** research ออกจาก implementation
> research ใช้ tokens เยอะ (MCP response ยาว)
> เราจะ compact ก่อน แล้วค่อย implement"

**Step 4.4: ดู Context หลัง Research**

```
/context
```

> **ชี้ให้เห็น:**
> "เปรียบเทียบกับ Step 4.2 — context **โตขึ้น** ชัดเจน
> เพราะ MCP response (issue body) + Claude's summary เข้ามาใน context
> ถ้า implement ต่อเลย context จะยิ่งโต"

**Step 4.5: /compact**

```
/compact
```

> **อธิบาย:**
> "`/compact` ทำอะไร: Claude สรุป conversation ทั้งหมดที่ผ่านมาเป็น 'dense summary'
> แล้วแทนที่ full history ด้วย summary สั้นๆ นั้น
> เหมือนเขียน 'meeting notes' แทนที่จะเก็บ transcript ทั้ง meeting
> ลด context ได้ 60-80%
>
> จังหวะที่ดีที่สุด: **หลัง research ก่อน implement**
> เพราะ research details ไม่จำเป็นตอน implement — แค่ summary ก็พอ"

**Step 4.6: ดู Context หลัง Compact**

```
/context
```

> **ชี้ให้เห็น:**
> "เห็นมั้ย — context **เล็กลง** อย่างชัดเจน!
> แต่ Claude ยังจำได้ว่าต้องทำอะไร (จาก summary)
> นี่คือเทคนิคที่ใช้ได้ตลอด: research → /compact → implement"

**Step 4.7: Implement ด้วย Scoped Prompt**

```
Read app/models.py and implement the validation from issue #3.
Use EmailStr, Field(ge=0, le=150) for age, Field(min_length=1) for name.
Then write tests in tests/test_validation.py following the pattern in conftest.py.
```

> **อธิบาย prompt:**
> "สังเกตว่า prompt นี้:
> - ✅ **ชี้ไฟล์** ที่ต้องอ่าน: `app/models.py`
> - ✅ **บอก pattern** ที่ต้อง follow: `conftest.py`
> - ✅ **ระบุ output**: `tests/test_validation.py`
> - ✅ **บอกรายละเอียด**: EmailStr, Field(ge=0, le=150)
>
> เทียบกับ prompt แย่: 'Look at the codebase and implement issue #3'
> prompt แย่ → Claude อ่านหลายไฟล์ → เสีย tokens → อาจแก้ไฟล์ผิด
> prompt ดี → Claude ไปตรงจุด → ประหยัด tokens → แม่นยำกว่า"

**Step 4.8: รัน Tests**

```
Run uv run pytest -v and show me the results.
```

**ผลที่ต้องเห็น:**
```
tests/test_health.py ... PASSED (3 tests)
tests/test_users.py ... PASSED (9 tests)
tests/test_validation.py ... PASSED (6+ tests)
============================= X passed ==============================
```

> **⚠️ สำคัญ: ยังไม่สร้าง PR!**
> "ทำได้ดีมาก! แต่... เราจะยังไม่สร้าง PR
> เพราะใน Section ถัดไป จะมี issue เร่งด่วนเข้ามา
> เราจะสาธิตว่า worktree ช่วยให้ switch ได้โดยไม่เสียงานที่ทำไว้"

---

## Section 5: Multiple Issues — The Interruption (20 นาที)

### สิ่งที่ต้องอธิบาย

> "สถานการณ์: คุณทำ Issue #3 อยู่ ยังไม่เสร็จ
> แต่ทีมแจ้งมาว่า Issue #6 (CORS) เร่งด่วน — frontend team รอ deploy อยู่
> ต้องทำ Issue #6 ก่อน แล้วค่อยกลับมาทำ #3 ต่อ
>
> ถ้าใช้ git แบบเดิม (stash + switch) จะยุ่งมาก
> แต่เรามี worktree — ดูว่าง่ายแค่ไหน"

### Phase A: จอด Issue #3 (2 นาที)

**Step 5A.1: ออกจาก Claude**

```
/exit
```

**Step 5A.2: กลับไป main repo**

```bash
cd ../../claude-workshop
```

> **อธิบาย:**
> "แค่นี้เลย! ไม่ต้อง stash, ไม่ต้อง commit
> ไฟล์ที่แก้ไปทั้งหมดยังอยู่ใน `issue-3-validation/`
> worktree นั้นจะรออยู่จนกว่าเราจะกลับไป"

### Phase B: ทำ Issue #6 — CORS (10 นาที)

**Step 5B.1: สร้าง Worktree ใหม่**

```bash
git worktree add ../issue-6-cors -b feat/issue-6-cors
```

**Step 5B.2: ดู Worktrees ทั้งหมด**

```bash
git worktree list
```

> **ชี้ให้เห็น:**
> "เห็น 3 worktrees:
> - `claude-workshop` → main (git root)
> - `issue-3-validation` → feat/issue-3-validation (จอดไว้ ยังมีงานค้าง)
> - `issue-6-cors` → feat/issue-6-cors (ใหม่ สำหรับ CORS)
>
> แต่ละอันอิสระจากกัน ไม่กระทบกัน"

**Step 5B.3: เข้า Worktree + Install + Claude**

```bash
cd ../issue-6-cors/workshop-project
uv sync
claude
```

> **อธิบาย:** "`uv sync` ต้องรันใน worktree ใหม่ด้วย เพราะ `.venv` แยกกัน"

**Step 5B.4: Single-shot Prompt**

```
Read issue #6 from spped2000/claude-workshop.
Implement CORS configuration in app/main.py.
Write tests in tests/test_cors.py.
Run uv run pytest -v.
Then create a pull request with "Closes #6" in the body.
```

> **อธิบาย:**
> "CORS เป็น issue ง่าย — แค่ ~5 lines ใน main.py
> เราใช้ single-shot prompt ทำทุกอย่างในครั้งเดียว
>
> สังเกต: session ใหม่ + worktree ใหม่ = **clean context**
> Claude ไม่รู้อะไรเลยเกี่ยวกับ Issue #3 ที่เราทำค้างไว้
> = **ไม่มี context pollution** ระหว่าง issues"

รอจนเสร็จ — Claude จะ:
1. อ่าน issue #6 ผ่าน MCP
2. เพิ่ม CORSMiddleware ใน main.py
3. สร้าง tests/test_cors.py
4. รัน pytest
5. สร้าง PR ผ่าน MCP

> **เมื่อเห็น PR URL:**
> "ดี! Issue #6 เสร็จ — PR ถูกสร้างแล้วบน GitHub
> ทำได้ภายใน 5-10 นาที เพราะ CORS ง่าย + worktree = clean start"

**Step 5B.5: ออกจาก Claude**

```
/exit
```

### Phase C: กลับมาต่อ Issue #3 (8 นาที)

**Step 5C.1: กลับไป Worktree ของ Issue #3**

```bash
cd ../../issue-3-validation/workshop-project
```

> **อธิบาย:**
> "แค่ `cd` กลับไป — ไฟล์ที่แก้ไปอยู่ครบ tests ที่เขียนไว้ก็อยู่
> ไม่มี stash pop, ไม่มี merge conflict
> เหมือนเดินออกจากห้องแล้วเดินกลับเข้ามา"

**Step 5C.2: เปิด Claude — 2 ตัวเลือก**

> **อธิบาย 2 ตัวเลือก:**
>
> "มี 2 วิธี:
>
> **ตัวเลือก 1: `/resume`**
> ```bash
> claude
> ```
> แล้วพิมพ์ `/resume` → เลือก session เดิม → Claude จำ context ของ Issue #3
> **ข้อดี:** Claude จำทุกอย่างที่ทำไว้
> **ข้อเสีย:** context เก่ามีขนาดใหญ่ (ถ้าทำเยอะ)
>
> **ตัวเลือก 2: Session ใหม่**
> ```bash
> claude
> ```
> แค่เริ่ม session ใหม่ — CLAUDE.md โหลดอัตโนมัติ + code ที่แก้ไปยังอยู่ในไฟล์
> Claude อ่าน code ปัจจุบันก็เข้าใจได้เร็ว
> **ข้อดี:** context clean กว่า ประหยัด tokens
> **ข้อเสีย:** ต้องอธิบาย context เล็กน้อย
>
> **แนะนำ:** ถ้า session เดิมสั้น (ทำไม่เยอะ) → `/resume`
> ถ้า session เดิมยาว (research + implement + debug เยอะ) → session ใหม่"

ให้ผู้เรียนเลือกอันไหนก็ได้ แล้วสร้าง PR:

```
All tests pass. Create a pull request for issue #3.
Include a description that explains what was implemented.
Include "Closes #3" in the body.
```

> **⚠️ สำหรับผู้สอน:** ตอนที่ผู้เรียนกำลังทำ Phase C → **ไปใส่ review comments ใน PR ของผู้เรียน** (ดูหัวข้อ "Review Comments ที่เตรียมไว้" ใน section เตรียมตัว)

**Step 5C.3: สรุป**

> "สรุปสิ่งที่ทำ:
> 1. จอด Issue #3 = แค่ออกจาก worktree
> 2. ทำ Issue #6 ใน worktree ใหม่ = clean context
> 3. กลับมาต่อ Issue #3 = cd กลับไป
>
> ไม่มี stash, ไม่มี conflict, ไม่มี context pollution
> ทำได้เพราะ: **1 Issue = 1 Worktree = 1 Claude Session**"

---

## Section 6: PR Review Cycle (15 นาที)

### สิ่งที่ต้องอธิบาย

> "PR ถูกสร้างแล้ว แต่งานยังไม่จบ — ต้องรอ review
> สมมติ reviewer ใส่ comments มา 2-3 ข้อ (ผมเตรียมไว้ให้แล้ว)
> เรามาดูวิธีแก้ review comments อย่างมีประสิทธิภาพ"

### Step-by-step

**Step 6.1: ทำไมต้อง Session ใหม่ (ไม่ใช่ /resume)?**

> **อธิบาย:**
> "คำถาม: ทำไมไม่ `/resume` session เดิม?
>
> เหตุผล: session เดิมมี context จาก implementation ทั้งหมด
> - Research phase (MCP response, issue body)
> - Implementation details (file reads, edits, debug)
> - Test runs
>
> ทั้งหมดนี้ **ไม่จำเป็น** สำหรับแก้ review comments
> เราแค่ต้องรู้ว่า reviewer ขออะไร แล้วแก้ตรงจุด
>
> Session ใหม่ = clean context = **ประหยัด tokens**
> CLAUDE.md + code ปัจจุบัน = Claude เข้าใจ project ได้เลย"

**Step 6.2: เปิด Session ใหม่**

```bash
cd ../issue-3-validation/workshop-project
claude
```

**Step 6.3: Method 1 — Manual (Prompts + MCP)**

```
Read the review comments on PR #<N> from spped2000/claude-workshop.
Fix only what the reviewers requested. Do not change other files.
Run uv run pytest -v after fixing.
Then push to the existing branch.
```

> **อธิบาย:**
> "Method 1 ใช้ 2 building blocks:
> - **MCP** → อ่าน review comments จาก GitHub
> - **Prompts** → บอก Claude ว่าต้องแก้อะไร
>
> สังเกต: เราบอก 'Do not change other files' — scope ชัดเจน
> Claude จะแก้เฉพาะที่ reviewer ขอ ไม่ refactor อย่างอื่น"

**Step 6.4: Method 2 — `/fix-review` Skill (Skills + MCP)**

> "ถ้าเราต้องแก้ review comments บ่อย สร้าง Skill ให้ทำอัตโนมัติ"

ออกจาก Claude แล้วเปิดใหม่ (หรือทำใน session เดิมก็ได้):

```
/fix-review <N>
```

> **อธิบาย:**
> "Method 2 ใช้ 3 building blocks:
> - **Skills** → สอน Claude ว่า 'อ่าน comments → แก้ → test → push'
> - **MCP** → เครื่องมือจริงที่อ่าน comments + push code
> - **Prompts** → `<N>` = PR number
>
> ผลลัพธ์เหมือนกับ Method 1 แต่:
> - **ต้องพิมพ์น้อยกว่า** (1 command vs หลายบรรทัด)
> - **consistent** — ทำเหมือนกันทุกครั้ง
> - **repeatable** — ใช้กับ PR ไหนก็ได้
>
> **นี่คือ complementary relationship จริงๆ:**
> Skill สอน *วิธีทำ* (procedural knowledge)
> MCP ให้ *เครื่องมือ* (tool connectivity)
> ทำงานด้วยกันใน 1 command"

**Step 6.5: ดู Skill ที่ใช้**

```bash
cat .claude/skills/fix-review/SKILL.md
```

> **อธิบาย:**
> "ดู SKILL.md:
> - `name: fix-review` → เรียกด้วย `/fix-review`
> - `disable-model-invocation: true` → Claude ไม่เรียกเอง (มี side effects: push code)
> - `allowed-tools: Read Write Edit Bash Glob Grep` → tools ที่ใช้ได้
>
> ข้างในมี 4 steps:
> 1. Read review comments ผ่าน GitHub MCP
> 2. Fix เฉพาะที่ reviewer ขอ
> 3. Run tests
> 4. Commit + push
>
> มันเหมือน 'recipe' ที่ Claude ทำตาม"

---

## Section 7: Skills Deep Dive (15 นาที)

### สิ่งที่ต้องอธิบาย

> "เราเห็น Skill ทำงานจริงแล้วใน Section 6
> ตอนนี้มาเข้าใจ Skills ให้ลึกขึ้น — ทำงานยังไง ทำไมถึง efficient
> อ้างอิงจาก: https://claude.com/blog/skills-explained"

### 7A: How Skills Work (5 นาที)

**Step 7A.1: SKILL.md Anatomy**

แสดง skill ตัวอย่าง:

```bash
cat .claude/skills/implement-issue/SKILL.md
```

> **อธิบายทีละส่วน:**
> "SKILL.md มี 2 ส่วน:
>
> **ส่วน 1: Frontmatter (YAML)**
> ```yaml
> ---
> name: implement-issue         # ชื่อ → เรียกด้วย /implement-issue
> description: Read GitHub...    # คำอธิบายสั้นๆ → ใช้สำหรับ Progressive Disclosure
> argument-hint: [issue-number]  # placeholder → /implement-issue <N>
> disable-model-invocation: true # user-only (Claude ไม่เรียกเอง)
> allowed-tools: Read Write...   # จำกัด tools ที่ใช้ได้
> ---
> ```
>
> **ส่วน 2: Instructions (Markdown)**
> ```markdown
> # Implement Issue #$0    ← $0 = argument ที่ผู้เรียนใส่
> ## Step 1 — Read Issue
> ## Step 2 — Implement
> ## Step 3 — Write Tests
> ## Step 4 — Create PR
> ```
>
> Claude อ่าน instructions แล้วทำตาม step-by-step"

**Step 7A.2: Progressive Disclosure**

> **อธิบาย:**
> "ทำไม Skills ถึง efficient?
>
> สมมติมี 20 Skills ติดตั้ง Claude ไม่ได้โหลดทั้ง 20 ตัว
>
> ```
> Step 1: Claude อ่าน description ทั้ง 20 ตัว
>         20 × ~100 tokens = 2,000 tokens เท่านั้น
>         แล้วถาม: 'อันไหน relevant กับ task ปัจจุบัน?'
>
> Step 2: relevant 1 ตัว → โหลด full instructions
>         ~5,000 tokens
>
> Step 3: ถ้ามี bundled scripts/files → โหลดเฉพาะที่ต้องใช้
>
> Total: 7,000 tokens
> vs โหลดทั้ง 20 ตัว: ~100,000 tokens ❌
> ```
>
> ประหยัดไป 93%! นี่คือ 'Progressive Disclosure' — โหลดเฉพาะที่ต้องใช้"

**Step 7A.3: Auto vs Manual Invocation**

> **อธิบาย:**
> "มี 2 แบบ:
>
> **Auto-invoke** (`disable-model-invocation: false`):
> Claude เรียก Skill เองเมื่อมัน 'เห็นว่า relevant'
> เหมาะสำหรับ: coding conventions, formatting rules
> ตัวอย่าง: Skill ที่บอก 'Always use camelCase in this project'
>
> **Manual-only** (`disable-model-invocation: true`):
> ผู้ใช้ต้องพิมพ์ `/skill-name` เอง
> เหมาะสำหรับ: actions ที่มี side effects (create PR, push code, delete files)
> ตัวอย่าง: `/implement-issue`, `/fix-review`
>
> Rule of thumb: **ถ้ามัน push/create/delete อะไรก็ตาม → manual-only**"

### 7B: Skills + MCP = Complementary (5 นาที)

**Step 7B.1: 4 Building Blocks ใน 1 Command**

> **อธิบาย:**
> "มาดูว่า `/implement-issue 3` ใช้ building blocks อะไรบ้าง:
>
> ```
> ผู้เรียนพิมพ์ → /implement-issue 3
>
> Skill  → บอก Claude: 'อ่าน issue → implement → test → PR'
>           = procedural knowledge (วิธีทำ)
>
> MCP    → ให้ Claude: get_issue, create_pull_request
>           = tool connectivity (เครื่องมือ)
>
> Prompt → ให้ Claude: $0 = 3 (issue number)
>           = moment-to-moment instruction (คำสั่งตอนนี้)
>
> CLAUDE.md → ให้ Claude: project structure, conventions
>             = background knowledge (ความรู้พื้นฐาน)
>
> = ทั้ง 4 building blocks ทำงานร่วมกัน!
> ```
>
> ถ้าขาดอันไหน:
> - ไม่มี Skill → Claude ไม่รู้ว่าต้องทำ step อะไรบ้าง
> - ไม่มี MCP → Claude อ่าน issue จาก GitHub ไม่ได้
> - ไม่มี Prompt → Claude ไม่รู้ว่าจะทำ issue หมายเลขอะไร
> - ไม่มี CLAUDE.md → Claude ไม่รู้ว่าแก้ไฟล์ไหน"

### 7C: `context: fork` Demo (5 นาที)

**Step 7C.1: อธิบายปัญหา**

> "เวลา Claude research (อ่านไฟล์หลายตัว, MCP response ยาว)
> ข้อมูลทั้งหมดเข้ามาใน main context → context บวม
> ต้อง /compact บ่อย
>
> มีวิธีดีกว่า: `context: fork`
> ส่ง subagent ไปทำ research ใน context แยก
> แล้ว return แค่ summary สั้นๆ กลับมา
> main context ไม่บวมเลย"

**Step 7C.2: ดู Skill**

```bash
cat .claude/skills/explore-issue/SKILL.md
```

> **ชี้:**
> "ดู 2 fields สำคัญ:
> - `context: fork` → ทำงานใน context แยก (ไม่ปน main)
> - `agent: Explore` → ใช้ Explore subagent (read-only, เร็ว)
>
> Explore agent มีแค่ tools: Read, Glob, Grep — อ่านอย่างเดียว ไม่แก้อะไร"

**Step 7C.3: ลองใช้**

เปิด Claude ใน workshop-project:

```
/explore-issue 4
```

> **อธิบายขณะทำงาน:**
> "ดู Claude ส่ง subagent ออกไปทำ:
> 1. Subagent อ่าน issue #4 ผ่าน MCP (ใน context ของมัน)
> 2. Subagent อ่านไฟล์ที่เกี่ยวข้อง (database.py, models.py, users.py)
> 3. Subagent ส่ง summary กลับมา
>
> ดู `/context` ตอนนี้ — context ไม่ได้โตมากเลย
> ถ้าทำแบบเดียวกันโดยไม่มี `context: fork` context จะบวมมาก"

```
/context
```

> **ชี้:**
> "เห็นมั้ย — เราได้ข้อมูลครบว่า Issue #4 ต้องแก้อะไร
> แต่ context แทบไม่โต เพราะ research ทำใน context แยก
>
> นี่คือ 3 building blocks ทำงานร่วมกัน:
> - Skill → สอนวิธี research (procedural knowledge)
> - Subagent → ทำ research แทน (task delegation)
> - MCP → อ่าน issue จาก GitHub (tool connectivity)
>
> + `context: fork` = **token optimization**"

---

## Section 8: Advanced Techniques (10 นาที)

### สิ่งที่ต้องอธิบาย

> "Section สุดท้าย — ผมจะโชว์เทคนิค advanced ที่ไม่ได้ลงมือทำ
> แต่อยากให้รู้ว่ามี เพื่อไปใช้ต่อหลัง workshop"

### 8A: Subagents (4 นาที)

> **อธิบาย:**
> "Claude Code มี subagent types 5 ตัวที่พร้อมใช้:
>
> | Type | ทำอะไร |
> |------|--------|
> | **Explore** | ค้นหา codebase (read-only, เร็ว) |
> | **Plan** | วางแผน implementation ก่อน code |
> | **general-purpose** | ทำงานทั่วไป (full tools) |
> | **statusline-setup** | ตั้งค่า UI |
> | **claude-code-guide** | ตอบคำถามเกี่ยวกับ Claude Code |
>
> ที่น่าสนใจคือ `isolation: 'worktree'`:
> เหมือน git worktree ที่เราทำ แต่ subagent สร้างให้อัตโนมัติ
> ทำงานบน copy แยกของ repo ไม่กระทบ codebase หลัก
>
> และ `/batch` สำหรับ changesets ใหญ่:
> สมมติต้อง rename function ใน 100 ไฟล์
> `/batch 'Rename getUserName to fetchUserName'`
> Claude สร้าง worktree agents หลายตัว ทำ parallel!"

### 8B: Hooks & Scheduled Tasks (3 นาที)

> **อธิบาย:**
> "**Hooks** = script ที่รันอัตโนมัติเมื่อมี event:
> - `SessionStart` → ทำอะไรเมื่อเริ่ม session (เช่น load context เพิ่ม)
> - `PreToolUse` → ทำอะไรก่อน Claude ใช้ tool (เช่น validate)
> - `PostToolUse` → ทำอะไรหลังใช้ tool (เช่น auto-format code)
>
> ตัวอย่างจริง: Hook ที่เล่นเสียงเมื่อ Claude ทำเสร็จ
>
> **Scheduled Tasks:**
> `/loop 5m /babysit` → ทุก 5 นาที Claude ตรวจ PR review แล้ว auto-fix
> `/loop 30m 'Check for new issues'` → ตรวจ issues ใหม่ทุก 30 นาที
> รันได้นานสุด 3 วัน แล้วหยุดอัตโนมัติ"

### 8C: Memory & Continued Learning (3 นาที)

> **อธิบาย:**
> "**Memory System:**
> Claude Code จำข้อมูลข้าม sessions ได้ 3 ระดับ:
> - **User** (ที่ `~/.claude/`) → ใช้กับทุก project
> - **Project** (ที่ `.claude/`) → ใช้กับ project นี้ ทุกคนเห็น
> - **Local** (ที่ `.claude/` gitignored) → เฉพาะคุณ
>
> ใช้ `/memory` ดูและจัดการ
>
> **เรียนรู้ต่อหลัง workshop:**
> พิมพ์ `/power-ups` ใน Claude Code → มี 10 บทเรียน interactive
> ครอบคลุม: @files, modes, undo, background tasks, CLAUDE.md, MCPs, skills, agents
>
> **Resources:**
> - https://claude.com/blog/skills-explained
> - https://github.com/shanraisshan/claude-code-best-practice"

---

## แก้ปัญหาเบื้องต้น

### ปัญหาที่พบบ่อยระหว่างสอน

| ปัญหา | สาเหตุ | วิธีแก้ |
|-------|--------|---------|
| `uv: command not found` | ยังไม่ install หรือ ต้อง restart terminal | ติดตั้ง + restart terminal |
| MCP "Failed to connect" | Token set หลัง mcp add | Set token ก่อน แล้ว `claude mcp add` ใหม่ |
| MCP 401 Unauthorized | Token ไม่ถูกต้อง/หมดอายุ | ตรวจ token, สร้างใหม่ถ้าจำเป็น |
| MCP 404 on issue | ใช้ repo name ผิด | ต้องเป็น `spped2000/claude-workshop` |
| `git worktree add` error | ไม่ได้อยู่ที่ git root | `cd` ไปที่ `claude-workshop` (ไม่ใช่ `workshop-project`) |
| Branch already exists | เคยสร้างไว้แล้ว | `git branch -D feat/issue-N` แล้วลองใหม่ |
| `uv sync` ไม่ทำงานใน worktree | `.venv` ไม่ได้ share | รัน `uv sync` ในแต่ละ worktree |
| Tests fail เพราะ state ค้าง | `conftest.py` มี autouse reset | ตรวจว่า import ถูก, restart Claude |
| Claude แก้ไฟล์ผิด | ไม่มี CLAUDE.md หรือ prompt ไม่ชี้ไฟล์ | `Re-read CLAUDE.md and confirm the correct file.` |
| `/compact` ไม่ลดมาก | Conversation สั้น | ปกติ — จะเห็นผลชัดเมื่อ conversation ยาว |
| `/resume` ไม่เห็น session | Session หมดอายุ | เริ่ม session ใหม่ได้ |
| `/fix-review` ไม่เจอ | Skill ไม่อยู่ใน `.claude/skills/` | `ls .claude/skills/` ตรวจ |
| `/explore-issue` ไม่ทำงาน | MCP ไม่ connected + Skill missing | ตรวจ `claude mcp list` + `ls .claude/skills/` |
| PR create fails | ไม่ได้ push branch | `git push -u origin <branch>` ก่อน |
| worktree remove error | มี modified files | ใช้ `--force` flag |

### ถ้าผู้เรียนทำไม่ทัน

- Section 5 Phase C (กลับมาต่อ) → ข้ามได้ ให้สร้าง PR จาก Phase B แทน
- Section 6 (PR Review) → สาธิตหน้าจอผู้สอนแทน
- Section 7C (context:fork demo) → อธิบาย concept แค่อย่างเดียว ไม่ต้อง demo
- Section 8 → ตัดทั้ง section ชี้ resources ท้ายสุด

### ถ้าผู้เรียนเสร็จเร็ว

- ลองทำ Issue อื่น (เช่น #4 หรือ #5) ใน worktree ใหม่
- ลองสร้าง Skill ของตัวเอง ใน `.claude/skills/my-skill/SKILL.md`
- ลอง `/implement-issue <N>` แบบ single command
- ลอง `/power-ups` สำหรับบทเรียนเพิ่มเติม
