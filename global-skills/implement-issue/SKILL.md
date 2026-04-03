---
name: implement-issue
description: Read a GitHub issue via MCP, implement the feature following project conventions, write tests, and open a PR. Works with any GitHub repository.
argument-hint: [issue-number]
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash
---

# Implement Issue #$0

## Step 1 — ตรวจสอบ Project Context

อ่านไฟล์เหล่านี้ก่อนทำอะไรทั้งนั้น:
- `CLAUDE.md` (ถ้ามี) — conventions, MCP servers, project structure
- `README.md` — quick start, tech stack, run commands
- `pyproject.toml` หรือ `package.json` — dependencies, test/run scripts

Detect repo name อัตโนมัติ:
- !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || git remote get-url origin 2>/dev/null || echo "unknown"`

## Step 2 — อ่าน Issue ผ่าน GitHub MCP

ใช้ GitHub MCP อ่าน issue #$0 จาก repo ที่ detect ได้ใน Step 1
สรุป acceptance criteria เป็น numbered checklist ก่อนทำต่อ

ถ้า MCP ไม่ตอบสนอง:
```
claude mcp list   # ตรวจสอบว่ามี github MCP ไหม
claude mcp add github -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github
```

## Step 3 — Implement

Follow conventions จาก CLAUDE.md หรือ README ที่อ่านใน Step 1
ถ้าไม่มี CLAUDE.md ให้ infer จาก codebase:
- ดูไฟล์ที่มีอยู่แล้วใน project เพื่อเข้าใจ pattern ที่ใช้
- ห้ามแก้ logic ที่ไม่เกี่ยวกับ issue นี้
- ถ้าต้องการ dependency ใหม่ ให้เพิ่มผ่าน package manager ของ project นั้น

## Step 4 — Write Tests

หา test pattern จาก existing tests ใน project แล้ว follow pattern เดิม
สร้าง test file ใหม่แยกจาก tests เดิม
รัน test suite ของ project — ต้องผ่านทั้งหมดรวมถึง tests เดิม

Detect test command อัตโนมัติ:
- !`cat pyproject.toml 2>/dev/null | grep -A2 '\[tool.pytest' || cat package.json 2>/dev/null | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('scripts',{}).get('test',''))" 2>/dev/null || echo "check README for test command"`

## Step 5 — Commit และสร้าง PR

สร้าง branch: `feat/issue-$0-<short-description>`
Commit เฉพาะไฟล์ที่เกี่ยวกับ issue นี้

สร้าง PR ผ่าน GitHub MCP:
- **Title**: ตรงกับ issue title
- **Body**:
  ```
  ## What was implemented
  <bullet points ของสิ่งที่ทำ>

  ## Tests added
  <ชื่อ test file และจำนวน tests>

  Closes #$0
  ```

แสดง PR URL เมื่อเสร็จสมบูรณ์
