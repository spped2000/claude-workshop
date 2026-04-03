# Instructor Demo Script — Section 4.2: GitHub MCP Live Demo

**Total time: 15 minutes**  
**Goal:** ผู้เรียนเห็น end-to-end workflow: อ่าน issue → implement → test → PR ใน Claude Code

---

## Before You Start (checklist)

- [ ] `cd` เข้า `workshop-project/`
- [ ] Claude Code เปิดอยู่และอยู่ใน directory นั้น
- [ ] GitHub MCP ติดตั้งแล้ว (`claude mcp list` เห็น `github`)
- [ ] `GITHUB_TOKEN` set ใน environment
- [ ] มี GitHub repo `spped2000/claude-workshop` พร้อม issue #1 อยู่แล้ว
- [ ] รัน `uv sync` แล้ว และ `uv run pytest` ผ่าน 9 tests

---

## [0:00 – 2:00] Setup: แสดง CLAUDE.md

**พูด:**
> "ก่อน implement อะไร เรามาดูก่อนว่า Claude รู้อะไรเกี่ยวกับ project นี้บ้าง"

**พิมพ์ใน Claude Code:**
```
Show me the contents of CLAUDE.md
```

**ชี้ให้เห็น:**
- Section "Available MCP Servers" — Claude รู้ว่ามี `github` MCP
- Section "Project Structure" — Claude รู้ว่าไฟล์อยู่ที่ไหน
- Section "Coding Conventions" — Claude รู้ว่าต้อง `async def` และ Pydantic v2

**พูด:**
> "ไฟล์นี้คือ context ที่ Claude อ่านอัตโนมัติเวลาเปิด project
> เราไม่ต้องอธิบาย project ทุกครั้ง — เขียนครั้งเดียว ใช้ได้ตลอด"

---

## [2:00 – 5:00] Step 1: อ่าน Issue ด้วย MCP

**พูด:**
> "ทีนี้เราจะให้ Claude อ่าน GitHub issue โดยตรง ไม่ต้อง copy-paste เลย"

**พิมพ์ใน Claude Code:**
```
Use the GitHub MCP to read issue #1 from spped2000/claude-workshop
and summarize the acceptance criteria as a numbered checklist.
```

**รอให้ Claude:**
1. เรียก `get_issue` tool (จะเห็น tool call ใน output)
2. แสดง JSON response จาก GitHub
3. สรุป acceptance criteria

**ชี้ให้เห็น:**
- Tool call ที่ปรากฏ: `github.get_issue(owner="spped2000", repo="claude-workshop", issue_number=1)`
- Claude อ่าน issue body โดยตรง — ไม่ใช่แค่ชื่อ issue
- Acceptance criteria ถูก format เป็น checklist

**พูด:**
> "นี่คือ MCP ทำงาน — Claude เรียก GitHub API ได้โดยตรง
> เหมือน developer ที่เปิด GitHub tab — แต่ Claude ทำให้แทน"

---

## [5:00 – 10:00] Step 2: Implement จาก Single Prompt

**พูด:**
> "ทีนี้ implement ทุก acceptance criteria จาก prompt เดียว"

**พิมพ์ใน Claude Code:**
```
Implement all the acceptance criteria from issue #1.
Follow the conventions in CLAUDE.md.
Write the code and add tests.
```

**รอให้ Claude:**
1. อ่าน acceptance criteria ที่เพิ่ง summarize ไว้
2. แก้ไข `app/main.py` เพื่อเพิ่ม `GET /health`
3. สร้างหรือแก้ไข test file

**ชี้ให้เห็น:**
- Claude รู้ว่าต้องแก้ `main.py` เพราะ CLAUDE.md บอกว่า health check ไม่ได้อยู่ใน router
- Test ใช้ pattern เดียวกับ `tests/conftest.py` ที่มีอยู่แล้ว (`async def test_...`)
- Claude ไม่ต้องถามว่า "test ไว้ที่ไหน?" เพราะ project structure ชัดเจน

**Pause และพูด:**
> "สังเกตว่า Claude เลือกแก้ไฟล์ถูกต้องได้เพราะ CLAUDE.md บอก project structure ไว้
> ถ้าไม่มี CLAUDE.md Claude อาจจะสร้างไฟล์ใหม่หรือแก้ผิดที่"

---

## [10:00 – 13:00] Step 3: Run Tests และสร้าง PR

**พิมพ์ใน Claude Code:**
```
Run the tests, then open a pull request for issue #1.
The PR description should reference the issue number and list what was added.
```

**รอให้ Claude:**
1. Run `uv run pytest` — เห็น output ว่าผ่านทุก test
2. เรียก `create_pull_request` ผ่าน GitHub MCP
3. แสดง PR URL

**ชี้ให้เห็น:**
- Test output ทุก test pass รวมถึง test ใหม่
- PR body มี "Closes #1" — GitHub จะ auto-close issue เมื่อ merge
- PR description อธิบายว่า implement อะไรไปบ้าง

**เปิด GitHub และแสดง PR จริง:**
> "นี่คือ PR ที่ Claude สร้างให้ — พร้อม review ได้เลย"

---

## [13:00 – 15:00] Discussion + Transition

**ถามผู้เรียน:**

1. "ถ้าไม่มี CLAUDE.md ใน project นี้ จะต่างกันยังไง?"
   - *คำตอบที่ต้องการ:* Claude ต้อง explore codebase เอง, อาจแก้ผิดไฟล์, ไม่รู้ว่ามี MCP อะไรบ้าง

2. "ถ้า issue #1 ไม่มี acceptance criteria ชัดเจน จะเกิดอะไร?"
   - *คำตอบที่ต้องการ:* Claude จะ implement ตามความเข้าใจตัวเอง ซึ่งอาจไม่ตรง spec

3. "Workflow นี้ต่างจากการ copy-paste code จาก ChatGPT ยังไง?"
   - *คำตอบที่ต้องการ:* ไม่ต้อง switch context, MCP ดึงข้อมูลจาก source of truth โดยตรง, สร้าง PR ได้เลย

**Transition:**
> "ทีนี้ถึงเวลา lab — แต่ละกลุ่มจะทำ issue ของตัวเอง
> ก่อนเริ่ม ตั้งค่า GitHub MCP ตาม step ใน PARTICIPANT_GUIDE.md ก่อนนะ"

---

## Appendix: สิ่งที่อาจผิดพลาด

### MCP ไม่ตอบสนอง
```bash
claude mcp list
# ต้องเห็น: github
```
ถ้าไม่เห็น:
```bash
claude mcp add github -- npx -y @anthropic-ai/mcp-server-github
export GITHUB_TOKEN=<token>
```

### `get_issue` คืน 404
- ตรวจสอบว่า repo name ใช้ `spped2000/claude-workshop`
- ตรวจสอบว่า `GITHUB_TOKEN` มีสิทธิ์อ่าน repo นั้น

### Tests ล้มเหลวตอน run ครั้งแรก
- ตรวจสอบ `tests/conftest.py` — `autouse=True` fixture จะ reset DB อัตโนมัติ
- ใช้ `uv run pytest -v` เพื่อดู error ละเอียด

### Claude แก้ไฟล์ผิด
ให้บอก:
```
Please re-read CLAUDE.md and confirm which file should contain the health check endpoint.
```

### `uv run pytest` ไม่เจอ test files
```bash
# ต้องรันจาก workshop-project/ เสมอ
cd workshop-project
uv run pytest -v
```
