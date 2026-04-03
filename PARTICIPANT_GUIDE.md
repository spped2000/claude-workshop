# Step-by-Step Guide: Module 4 — MCP & GitHub Workflow

## สิ่งที่คุณจะทำใน Lab นี้

```
GitHub Issue  →  Claude อ่าน  →  Implement  →  Tests Pass  →  PR ✅
```

---

## ✅ Step 0: ตรวจสอบ Prerequisites

ก่อนเริ่ม ตรวจสอบให้ครบ:

```bash
# 1. Python 3.11+
python --version

# 2. uv
uv --version

# 3. Claude Code
claude --version

# 4. Node.js (สำหรับ MCP server)
node --version
```

ถ้ายังไม่มี uv:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 🔧 Step 1: ติดตั้ง Project

```bash
# Clone repo
git clone https://github.com/spped2000/claude-workshop.git
cd claude-workshop/workshop-project

# ติดตั้ง dependencies ด้วย uv (เร็วกว่า pip มาก)
uv sync

# ทดสอบว่า project ทำงานได้
uv run pytest
# ✅ ควรเห็น: 9 passed
```

---

## 🔌 Step 2: ติดตั้ง GitHub MCP

```bash
# เพิ่ม GitHub MCP ใน Claude Code
claude mcp add github -e GITHUB_TOKEN=$env:GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github

# Set GitHub token (ใช้ token ที่ได้รับจากผู้สอน)
export GITHUB_TOKEN=<token ที่แจกให้>

# Windows PowerShell
$env:GITHUB_TOKEN="<token ที่แจกให้>"
```

**ตรวจสอบว่า MCP ติดตั้งสำเร็จ:**
```bash
claude mcp list
# ✅ ควรเห็น: github
```

---

## 🚀 Step 3: เปิด Claude Code ใน Project

```bash
claude
```

> Claude จะอ่าน `CLAUDE.md` อัตโนมัติ — รู้ว่ามี GitHub MCP และ project structure เป็นยังไง

---

## 📋 Step 4: ให้ Claude อ่าน Issue ของกลุ่มคุณ

| กลุ่ม | Issue # | หัวข้อ |
|-------|---------|--------|
| 1 | #1 | Add health check endpoint |
| 2 | #2 | Add request logging middleware |
| 3 | #3 | Add input validation for POST /users |
| 4 | #4 | Add soft delete for users |
| 5 | #5 | Add search endpoint GET /users/search |
| 6 | #6 | Add CORS configuration |
| 7 | #7 | Add response compression |

**พิมพ์ prompt นี้ใน Claude Code** (เปลี่ยน `<N>` เป็นหมายเลข issue ของกลุ่มคุณ):

```
Read issue #<N> from spped2000/claude-workshop and summarize
the acceptance criteria as a checklist.
```

**ผลที่ควรเห็น:**
- Claude เรียก GitHub MCP โดยตรง
- แสดง acceptance criteria เป็น checklist

---

## 💻 Step 5: Implement Feature

```
Implement all the acceptance criteria from issue #<N>.
Follow the conventions in CLAUDE.md.
Write the code and add tests.
```

**สิ่งที่ Claude จะทำ:**
1. อ่าน acceptance criteria จาก step ก่อน
2. แก้ไขไฟล์ที่เหมาะสมใน `app/`
3. สร้างหรืออัปเดต test file ใน `tests/`

---

## 🧪 Step 6: รัน Tests

```
Run the tests and show me the results.
```

หรือรันเองใน terminal:
```bash
uv run pytest -v
```

**ผลที่ต้องการ:**
```
✅ tests/test_users.py - 9 passed        (existing tests ต้องยังผ่าน)
✅ tests/test_<feature>.py - X passed    (tests ใหม่จาก Claude)
```

ถ้า test ล้มเหลว บอก Claude:
```
The test <ชื่อ test> is failing with this error: <error message>. Please fix it.
```

---

## 🔀 Step 7: สร้าง Pull Request

```
All tests pass. Please open a pull request for issue #<N>.
Include a description that explains what was implemented
and reference the issue number.
```

**Claude จะ:**
1. สร้าง branch ใหม่
2. Commit การเปลี่ยนแปลง
3. เรียก GitHub MCP เพื่อสร้าง PR
4. แสดง PR URL

---

## ✅ Checklist ตรวจสอบผลลัพธ์

หลังทำเสร็จ ตรวจสอบ:

- [ ] Claude อ่าน issue ด้วย MCP ได้ (ไม่ได้ copy-paste)
- [ ] Feature implement ถูกต้องตาม acceptance criteria
- [ ] `uv run pytest` ผ่านทุก test (รวม tests เดิม)
- [ ] PR ถูกสร้างบน GitHub
- [ ] PR description มี "Closes #<N>"
- [ ] PR description อธิบายว่า implement อะไรไปบ้าง

---

## 🐛 แก้ปัญหาเบื้องต้น

| ปัญหา | วิธีแก้ |
|-------|---------|
| `uv: command not found` | ติดตั้ง uv ตาม Step 0 |
| `github` ไม่ปรากฏใน `claude mcp list` | รัน `claude mcp add github -e GITHUB_TOKEN=$env:GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github` อีกครั้ง |
| MCP คืน 401 Unauthorized | ตรวจสอบว่า `GITHUB_TOKEN` set ถูกต้อง |
| MCP คืน 404 on issue | ใช้ `spped2000/claude-workshop` เป็น repo name |
| Tests ล้มเหลวเพราะ state ค้าง | `conftest.py` ควร reset อัตโนมัติ — ถามผู้สอน |
| Claude แก้ไฟล์ผิด | พิมพ์ `Re-read CLAUDE.md and confirm the correct file to edit.` |
| `pytest` ไม่เจอ tests | ตรวจสอบว่าอยู่ใน `workshop-project/` แล้วใช้ `uv run pytest` |

---

## 🏆 Track B: ทดลองเพิ่มเติม (ถ้าเสร็จเร็ว)

ติดตั้ง Filesystem MCP และทดลองใช้:

```bash
claude mcp add filesystem -- npx -y @anthropic-ai/mcp-server-filesystem /tmp/workshop
```

ลองถาม Claude:
```
List all Python files in this project and summarize what each one does.
```
