---
name: implement-issue
description: Read a GitHub issue via MCP, implement the feature, write tests in a separate file, and open a PR. Use when given an issue number to work on.
argument-hint: [issue-number]
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash
---

# Implement Issue #$0

## Step 1 — อ่าน Issue ผ่าน GitHub MCP

ใช้ GitHub MCP อ่าน issue #$0 จาก repo spped2000/claude-workshop
แสดง acceptance criteria เป็น numbered checklist ก่อนทำต่อ
ถ้า MCP ไม่ตอบสนอง ให้แจ้งผู้ใช้ว่า `claude mcp list` เพื่อตรวจสอบ

## Step 2 — Implement

อ่าน CLAUDE.md ก่อนเพื่อเข้าใจ project structure และ conventions
จากนั้น implement ตาม acceptance criteria ทุกข้อ:

- ใช้ `async def` สำหรับทุก route handler
- แก้ไฟล์ที่ถูกต้องตาม project structure (main.py หรือ routers/users.py ตามที่ issue ระบุ)
- ห้ามแก้ logic ที่ไม่เกี่ยวกับ issue นี้
- ถ้าต้องการ dependency ใหม่ ให้รัน `uv add <package>` และ commit pyproject.toml ด้วย

## Step 3 — Write Tests

สร้างไฟล์ `tests/test_<feature_name>.py` แยกใหม่ (อย่าแก้ test_users.py)
เขียน test ครอบคลุมทุก acceptance criteria ใน issue
รัน `uv run pytest -v` — ต้องผ่านทุก test รวมถึง 9 tests เดิม
ถ้า test ล้มเหลวให้แก้จนผ่านก่อนไป step ถัดไป

## Step 4 — สร้าง PR ผ่าน GitHub MCP

ใช้ GitHub MCP สร้าง pull request:
- **Title**: ตรงกับ issue title
- **Body**: อธิบายว่า implement อะไรบ้าง และใส่ "Closes #$0" ท้าย body
- **Branch**: สร้าง branch ชื่อ `feat/issue-$0-<short-description>` ก่อน commit

แสดง PR URL เมื่อเสร็จสมบูรณ์
