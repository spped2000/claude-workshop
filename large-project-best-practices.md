# Large Project Best Practices — Sessions, PRs & Token Optimization

## Core Principle

```
1 Issue = 1 Git Worktree = 1 Claude Session
```

ทำงานแบบนี้ทำให้:
- Context ไม่ปนกันระหว่าง issues
- ทำงานหลาย issue พร้อมกันได้ใน terminal คนละ tab
- ไม่ต้อง stash หรือ switch branch

---

## 1. Git Worktrees — ทำงานหลาย Issue พร้อมกัน

### ปัญหาที่แก้

```
# วิธีเดิม — ต้อง stash ทุกครั้งที่ switch
git stash
git checkout feat/issue-2
# แก้โค้ด...
git checkout feat/issue-1
git stash pop
```

### วิธีที่ดีกว่า — Worktrees

```bash
# สร้าง worktree แยกสำหรับแต่ละ issue
git worktree add ../issue-42 -b feat/issue-42
git worktree add ../issue-43 -b feat/issue-43
git worktree add ../issue-44 -b feat/issue-44

# เปิด Claude Code แยกกันในแต่ละ directory
cd ../issue-42 && claude   # terminal tab 1
cd ../issue-43 && claude   # terminal tab 2
cd ../issue-44 && claude   # terminal tab 3
```

แต่ละ session มี:
- Branch ของตัวเอง ไม่กระทบกัน
- Context ที่ clean ไม่มี history จาก issue อื่น
- CLAUDE.md เดียวกัน (shared จาก main repo)

```bash
# ดู worktrees ทั้งหมด
git worktree list

# ลบเมื่อ merge แล้ว
git worktree remove ../issue-42
```

---

## 2. Session Strategy — เมื่อไหรควรขึ้น Session ใหม่

### ขึ้น Session ใหม่เมื่อ

| สถานการณ์ | เหตุผล |
|-----------|--------|
| เริ่ม issue ใหม่ | Context จาก issue เก่าไม่เกี่ยวและกิน token |
| หลัง merge PR | งานเสร็จแล้ว context ไม่มีประโยชน์ต่อ |
| Context เริ่ม hallucinate | Claude เริ่มอ้างถึงสิ่งที่ไม่มีใน codebase |
| Session ยาวเกิน ~2 ชั่วโมง | Context window เริ่มเต็ม ประสิทธิภาพลด |

### ต่อ Session เดิมเมื่อ

| สถานการณ์ | เหตุผล |
|-----------|--------|
| แก้ review comments ของ PR เดิม | Claude ยังจำ context ของ implementation |
| Debug ปัญหาที่เพิ่งเจอ | ไม่ต้องอธิบาย background ใหม่ |
| Iterate บน feature เดิม | Context ที่สะสมมีประโยชน์ |

---

## 3. Token Optimization Techniques

### 3.1 CLAUDE.md — ลด Cold Start Cost

CLAUDE.md ที่ดีทำให้ Claude ไม่ต้อง explore codebase เอง
ทุก session ใหม่ Claude อ่านไฟล์นี้ก่อน = รู้ทุกอย่างทันที

```markdown
# CLAUDE.md — สิ่งที่ต้องมีเสมอ

## Architecture (ย่อที่สุด)
- Entry point: src/main.py
- API layer: src/routers/
- Business logic: src/services/
- Tests: tests/ — run with `uv run pytest`

## Key Conventions
- Async throughout (async def)
- Errors: raise HTTPException, never return error dicts
- New feature = new router file + new test file

## What NOT to touch
- src/legacy/ — deprecated, do not modify
- migrations/ — use `make migrate` not raw SQL
```

**ผลที่ได้:** Claude ไม่ต้องอ่าน 50 ไฟล์เพื่อเข้าใจ project
= ประหยัด input tokens ตั้งแต่ต้น session

### 3.2 `/compact` — บีบ Context กลางคัน

ใช้เมื่อ research phase เสร็จแล้วจะเข้า implementation:

```
# ใน Claude Code
/compact
```

Claude สรุป conversation ที่ผ่านมาเป็น dense summary
แล้วแทนที่ full history ด้วย summary นั้น
= ลด context ที่ carry forward ได้ 60-80%

**จังหวะที่ดีที่สุดคือ:**
```
อ่าน issue + explore codebase → /compact → implement + test → /compact → PR
```

### 3.3 Scoped Reading — อ่านเฉพาะที่จำเป็น

```
# ❌ แบบนี้ทำให้ Claude อ่านไฟล์เยอะ
"Look at the codebase and implement X"

# ✅ แบบนี้ดีกว่า — ชี้เป้าให้ชัด
"Read src/routers/users.py and app/models.py,
then add a search endpoint following the same pattern"
```

ถ้า CLAUDE.md บอก structure ชัด Claude จะชี้เป้าให้ตัวเองได้

### 3.4 Skills ด้วย `context: fork` — Isolated Context

สำหรับ task ที่ต้อง explore เยอะแต่ไม่อยากให้ผลลัพธ์ปนใน main context:

```yaml
---
name: explore-issue
description: Research an issue and summarize findings without polluting main context
context: fork
agent: Explore
allowed-tools: Read Glob Grep
---

Read issue #$0 and find all files that need to change.
Return a concise list: filename → what needs to change and why.
Do not make any edits.
```

Subagent ทำงานใน context แยก → return summary กลับมา
= main session ไม่บวมจาก exploration

### 3.5 Reference ไม่ Re-explain

```
# ❌ เสีย tokens อธิบายซ้ำ
"As I mentioned before, we're using FastAPI with in-memory storage
and the user model has name, email, age fields. Now fix the bug where..."

# ✅ อ้างอิงแทน
"Fix the 422 error in POST /users — the test in tests/test_users.py
line 34 shows the exact failure"
```

---

## 4. PR Review Cycle — แก้ Review Comments อย่างมีประสิทธิภาพ

### Pattern ที่แนะนำ

```bash
# 1. เปิด session ใหม่ใน worktree เดิม (ไม่ต้องสร้างใหม่)
cd ../issue-42
claude

# 2. เริ่ม session ด้วย context ที่กระชับ — อย่าอธิบายยาว
```

```
# Prompt เปิด session สำหรับแก้ review
PR #87 has review comments. Read the comments and fix them:
- src/routers/users.py line 45: reviewer says to use 404 not 400
- tests/test_users.py: add edge case for empty name

Do not change anything else.
```

**สิ่งที่ระบุ:**
- PR number
- ไฟล์ที่ต้องแก้ + บรรทัด (ถ้าทำได้)
- Scope ที่ชัดเจน — "Do not change anything else"

### ดึง Review Comments ผ่าน GitHub MCP อัตโนมัติ

```
Read the review comments on PR #87 from spped2000/claude-workshop
and fix all requested changes. Do not modify files that were not mentioned.
```

Claude จะ:
1. ดึง review comments ผ่าน MCP
2. แก้ตามที่ reviewer ขอ
3. ไม่แตะไฟล์อื่น

---

## 5. Skill สำหรับ PR Review Fix

```yaml
# .claude/skills/fix-review/SKILL.md
---
name: fix-review
description: Read PR review comments via MCP and fix all requested changes
argument-hint: [pr-number]
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Glob Grep
---

# Fix Review Comments for PR #$0

## Step 1 — Read Review Comments
Use GitHub MCP to read all review comments on PR #$0.
List each comment with: file, line number, and what the reviewer asked for.

## Step 2 — Fix
Fix each comment exactly as requested.
Do not refactor or change code that was not mentioned in the review.
Do not add new features or tests beyond what reviewers asked for.

## Step 3 — Verify
Run `uv run pytest -v` — all tests must pass.
List every file you changed and why.

## Step 4 — Push
Commit with message: `fix: address PR #$0 review comments`
Push to the existing branch — do not create a new PR.
```

ใช้งาน:
```
/fix-review 87
```

---

## 6. สรุป Best Practices

```
Setup:
  ✅ CLAUDE.md ครบ — architecture, conventions, run commands
  ✅ 1 issue = 1 worktree = 1 session
  ✅ Skills สำหรับ workflow ที่ทำซ้ำ

ระหว่าง session:
  ✅ /compact หลัง research phase ก่อน implement
  ✅ ชี้ไฟล์และบรรทัดแทนการอธิบายยาว
  ✅ "Do not change X" บอก scope ชัดเจน

PR review:
  ✅ เปิด session ใหม่ใน worktree เดิม
  ✅ ดึง review comments ผ่าน MCP
  ✅ /fix-review skill จัดการให้อัตโนมัติ

หลีกเลี่ยง:
  ❌ ทำหลาย issue ใน session เดียว
  ❌ "Look at the whole codebase and..."
  ❌ อธิบาย context ซ้ำที่มีใน CLAUDE.md อยู่แล้ว
  ❌ Session ที่ยาวเกินโดยไม่ /compact
```
