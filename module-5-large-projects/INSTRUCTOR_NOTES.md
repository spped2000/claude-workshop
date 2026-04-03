# Instructor Notes — Module 5: Large Project Best Practices

## Prep Checklist (ก่อน Workshop)

- [ ] ตรวจสอบว่า repo `spped2000/claude-workshop` มี Issue #3 และ #6 เปิดอยู่
- [ ] เตรียม GitHub Personal Access Token (scope: `repo`) สำหรับแจกผู้เรียน
- [ ] ทดสอบ `claude mcp list` → github connected ใน environment ที่ใช้สอน
- [ ] ทดสอบ `git worktree add` ใน repo ที่ clone มา
- [ ] พิมพ์ `BUILDING_BLOCKS.md` handout (หรือเตรียม digital copy)
- [ ] เตรียม review comments สำหรับ Section 6 (ดูด้านล่าง)
- [ ] ตรวจว่ามี skill `fix-review` และ `explore-issue` ใน skills directory

---

## Timing Guide

| Section | เวลา | เริ่ม | จบ | หมายเหตุ |
|---------|------|------|-----|---------|
| 0. Setup | 10 min | 0:00 | 0:10 | ช่วยคนที่ install ไม่ผ่าน |
| 1. Building Blocks | 10 min | 0:10 | 0:20 | Concept — ถามผู้เรียนให้มีส่วนร่วม |
| 2. CLAUDE.md | 10 min | 0:20 | 0:30 | Demo live + อธิบาย loading |
| 3. Worktrees | 10 min | 0:30 | 0:40 | Hands-on — ทุกคนสร้าง worktree |
| 4. Token Opt + Issue #3 | 15 min | 0:40 | 0:55 | Hands-on — ส่วนที่ยาวที่สุด |
| 5. Multiple Issues | 20 min | 0:55 | 1:15 | Hands-on — จอด #3, ทำ #6, กลับ #3 |
| **⚠️ ใส่ review comments** | - | ~1:10 | - | **ระหว่างที่ผู้เรียนทำ Phase C** |
| 6. PR Review | 15 min | 1:15 | 1:30 | Hands-on — ใช้ review comments ที่เตรียมไว้ |
| 7. Skills Deep Dive | 15 min | 1:30 | 1:45 | Concept + Demo — สำคัญมาก |
| 8. Advanced | 10 min | 1:45 | 1:55 | Instructor demo only |
| **Total** | **~115 min** | | | **ลดได้ถ้า cut Section 8** |

### ลดเวลา (ถ้าต้องการ ~100 min)

- Section 8 → 5 min (แค่ mention หัวข้อ + ชี้ resources)
- Section 1+2 → merge เป็น 15 min (CLAUDE.md เป็นส่วนหนึ่งของ Building Blocks)
- Section 7 → 10 min (ตัด 7C demo ออก แค่อธิบาย concept)

---

## Section-by-Section Notes

### Section 0: Setup

**Common Issues:**
- Windows: `uv` ต้อง restart terminal หลัง install
- MCP: token ต้อง set ก่อนรัน `claude mcp add` — ลำดับสำคัญ
- `git clone` ช้า → ให้ผู้เรียน clone ล่วงหน้าถ้าได้

**ถ้ามีคนช้า:** ให้เริ่ม Section 1 (concept) ก่อน แล้วค่อยให้คน setup ตามทีหลัง

### Section 1: Building Blocks

**คำถามที่ควรถาม:**
- "ใครเคยใช้ Claude Code มาก่อน? ปกติใช้ทำอะไร?" → mapping กับ Prompts
- "ใครเคยเห็น CLAUDE.md? รู้มั้ยว่ามันทำอะไร?" → mapping กับ Background Knowledge
- "ถ้าต้องทำงานเดิมซ้ำทุกวัน จะทำยังไง?" → mapping กับ Skills
- "ถ้า Claude ต้องอ่าน GitHub issue ที่อยู่ข้างนอก?" → mapping กับ MCP

**Key Point:** ย้ำว่า 5 building blocks ทำงาน **ร่วมกัน** — ไม่ใช่เลือกอันเดียว
จะมีตัวอย่างจริงใน Section 6-7

### Section 2: CLAUDE.md

**Demo Flow:**
1. `cat workshop-project/CLAUDE.md` → อ่านให้ผู้เรียนเห็น (สั้น ชัด)
2. `claude` → ถาม "What do you know about this project?"
3. ชี้ให้เห็น: Claude ไม่ได้ใช้ Read tool อ่านไฟล์ใดๆ — ตอบจาก CLAUDE.md
4. `/exit`

**Talking Points:**
- "ถ้าไม่มี CLAUDE.md → Claude ต้อง explore files เอง → เสีย 5,000-10,000 tokens"
- "CLAUDE.md 38 บรรทัด → Claude รู้ทุกอย่างใน ~500 tokens"

### Section 3: Worktrees

**Common Mistakes:**
- `git worktree add` ต้องรันจาก **git root** (claude-workshop) ไม่ใช่ workshop-project
- Path `../issue-3-validation` ต้องไม่มี directory นั้นอยู่ก่อน
- ถ้า branch มีอยู่แล้ว: `git branch -D feat/issue-3-validation` ก่อน

**ถ้าผู้เรียนสับสน:** วาดรูป directory structure บน whiteboard:
```
📁 (parent)
├── claude-workshop/     ← git root (main)
├── issue-3-validation/  ← worktree (feat/issue-3)
└── issue-6-cors/        ← worktree (feat/issue-6)
```

### Section 4: Token Optimization

**สิ่งที่ต้องเน้น:**
- `/context` ก่อนและหลัง `/compact` → ให้เห็น **difference ชัดๆ**
- ถ้า context ไม่ลดมาก (conversation สั้น) → อธิบายว่าจะเห็นผลชัดขึ้นเมื่อ conversation ยาว

**Scoped Prompt vs Generic Prompt:**
```
❌ "Look at the codebase and implement issue #3"
✅ "Read app/models.py and implement validation using EmailStr, Field(ge=0, le=150)"
```

ย้ำ: ชี้ไฟล์ + pattern = ลด token usage + ลดโอกาส Claude แก้ไฟล์ผิด

### Section 5: Multiple Issues — THE KEY SECTION

**Timing:**
- Phase A (จอด): 2 min — ง่ายมาก แค่ exit + cd
- Phase B (Issue #6): 10 min — CORS เป็น issue ง่าย
- Phase C (กลับ): 8 min — สอน /resume vs session ใหม่

**⚠️ สำคัญ: ใส่ Review Comments ระหว่าง Phase C**

ขณะที่ผู้เรียนกำลังกลับมาทำ Issue #3 + สร้าง PR → **ผู้สอนไปใส่ review comments** ใน PR ที่ผู้เรียนสร้าง

**ใส่ comment ยังไง:**
1. ไปที่ GitHub → PR ของผู้เรียน
2. กด "Files changed"
3. กด "+" ที่บรรทัดที่ต้องการ comment
4. พิมพ์ comment (ดูด้านล่าง)
5. กด "Start a review" → "Submit review" → "Request changes"

### Section 6: PR Review

**⚠️ ต้องมี review comments ก่อนเริ่ม section นี้**

ถ้าผู้เรียนยังไม่มี PR → ให้ใช้ PR ของผู้สอน (demo PR)

**Method 1 vs Method 2:**
- สอน Method 1 (manual) **ก่อน** เพื่อให้เข้าใจ flow
- แล้วโชว์ Method 2 (`/fix-review`) ว่าทำสิ่งเดียวกันใน 1 command
- ย้ำ: "นี่คือ complementary — Skill สอน *วิธีทำ*, MCP ให้ *เครื่องมือ*"

### Section 7: Skills Deep Dive

**สิ่งที่สำคัญที่สุดใน section นี้:**
1. Progressive Disclosure → ทำไม Skills ถึง efficient
2. ตัวอย่าง `/implement-issue 3` → 4 building blocks ทำงานร่วมกัน
3. `context: fork` demo → main context ไม่บวม

**ถ้าเวลาไม่พอ:** ตัด 7C (demo) ออก แค่อธิบาย concept ของ `context: fork`

### Section 8: Advanced

**Section นี้เป็น awareness ไม่ใช่ hands-on**
- ผู้สอนโชว์ concept + ชี้ resources
- ไม่ต้องให้ผู้เรียนทำตาม
- ย้ำ `/power-ups` สำหรับเรียนต่อหลัง workshop

---

## Pre-Written Review Comments

ใส่ใน PR ของ Issue #3 (input validation) ของผู้เรียน:

### Comment 1 (ง่าย — เพิ่ม test)
**File:** `tests/test_validation.py`
**บรรทัด:** ท้ายไฟล์
**Comment:**
```
Please add a test case for email with leading/trailing spaces, e.g. " alice@example.com ".
The API should either reject it or strip whitespace — pick one and test it.
```

### Comment 2 (ปานกลาง — ปรับ error message)
**File:** `app/models.py`
**บรรทัด:** ที่มี `age` field
**Comment:**
```
The validation error message for invalid age should include the valid range.
Instead of just "value is not a valid integer", users should see something like
"Age must be between 0 and 150".
```

### Comment 3 (ง่าย — เพิ่ม boundary test)
**File:** `tests/test_validation.py`
**บรรทัด:** หลัง test สุดท้าย
**Comment:**
```
Please add boundary tests for age=0 and age=150 — both should be valid.
Also test age=-1 and age=151 — both should be rejected.
```

---

## Common Pitfalls & Recovery

| ปัญหา | สาเหตุ | วิธีแก้ |
|-------|--------|---------|
| MCP "Failed to connect" | Token ไม่ได้ set ก่อน `mcp add` | Set `$env:GITHUB_TOKEN` ก่อน แล้ว `claude mcp add` อีกครั้ง |
| `git worktree add` error: branch exists | Branch ถูกสร้างไว้แล้ว | `git branch -D feat/issue-N` แล้วลองใหม่ |
| `git worktree add` error: path exists | Directory มีอยู่แล้ว | ลบ directory ก่อน หรือใช้ path อื่น |
| Claude hallucinate file | Context window เต็ม | `/compact` หรือเปิด session ใหม่ |
| Tests fail หลัง implement | State ค้างจาก test ก่อน | `conftest.py` มี `autouse=True` reset — ถ้ายังเป็นให้ดู import |
| PR create fails | ไม่ได้ push branch ก่อน | Claude ควร push ให้ แต่ถ้าไม่ ให้ `git push -u origin <branch>` |
| `/fix-review` ไม่เจอ | Skill ไม่ได้ install | ตรวจ `.claude/skills/fix-review/SKILL.md` |
| `/explore-issue` error | MCP ไม่ connected | `claude mcp list` ตรวจ github |
| ผู้เรียนทำ issue ผิดตัว | สับสน issue number | ไม่เป็นไร — เรียนรู้ได้เหมือนกัน |
| Context เต็มกลาง session | Session ยาวเกินไป | `/compact` หรือ `/exit` แล้วเริ่มใหม่ |

---

## Timing Adjustment Scenarios

### ถ้ามี 90 นาที (ลด 25 min)
- Section 1+2 → merge เป็น 15 min (CLAUDE.md เป็นส่วนหนึ่งของ Building Blocks)
- Section 7 → 10 min (ตัด 7C demo)
- Section 8 → 5 min (แค่ list resources)

### ถ้ามี 75 นาที (ลด 40 min)
- Section 1+2 → merge เป็น 10 min
- Section 5 → 15 min (ตัด Phase C resume demo)
- Section 7 → 5 min (แค่โชว์ comparison table)
- Section 8 → ตัดทั้งหมด (ชี้ resources ท้าย workshop)

### ถ้ามี 120+ นาที (เพิ่ม)
- Section 4 → ให้ผู้เรียนลอง Issue #5 (search) ที่ซับซ้อนกว่า
- Section 7 → hands-on สร้าง Skill ของตัวเอง
- Section 8 → hands-on `/loop` demo

---

## Post-Workshop

- Share `BUILDING_BLOCKS.md` ให้ผู้เรียน
- ชี้ไปที่ `/power-ups` สำหรับเรียนเพิ่ม
- ชี้ไปที่ https://github.com/shanraisshan/claude-code-best-practice
- ชี้ไปที่ https://claude.com/blog/skills-explained
