# Workshop: Large Project Best Practices with Claude Code

## สิ่งที่คุณจะได้เรียนรู้

```
Clone Project → Setup MCP → สร้าง Worktree → ทำ Issue #3
→ ถูก Interrupt → จอด #3 → ทำ Issue #6 → กลับมาต่อ #3
→ แก้ PR Review → Skills Deep Dive → Advanced Techniques
```

**เวลา:** ~100-115 นาที
**ระดับ:** Intermediate — เคยใช้ Claude Code มาก่อน (ไม่จำเป็นต้องผ่าน workshop อื่น)

---

## ✅ Section 0: Setup & Prerequisites (10 นาที)

### ตรวจสอบเครื่องมือ

```bash
python --version          # ต้องเป็น 3.11+
uv --version              # uv package manager
claude --version           # Claude Code CLI
node --version             # Node.js (สำหรับ MCP server)
```

ถ้ายังไม่มี uv:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Clone & Install

```bash
git clone https://github.com/spped2000/claude-workshop.git
cd claude-workshop/workshop-project
uv sync
uv run pytest
# ✅ ควรเห็น: X passed (ทุก test ผ่าน)
```

### ติดตั้ง GitHub MCP

```bash
# Windows PowerShell — set token ก่อน
$env:GITHUB_TOKEN="<token ที่ได้จากผู้สอน>"

# เพิ่ม GitHub MCP
claude mcp add github -e GITHUB_TOKEN=$env:GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github
```

```bash
# macOS/Linux
export GITHUB_TOKEN=<token>
claude mcp add github -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github
```

ตรวจสอบ:
```bash
claude mcp list
# ✅ ควรเห็น: github: connected
```

---

## 📦 Section 1: Claude Code Building Blocks — ภาพรวม (10 นาที)

> อ้างอิงจาก: https://claude.com/blog/skills-explained

Claude Code ไม่ได้มีแค่ "พิมพ์ prompt แล้วรอ" — มันมี **5 ส่วนประกอบ** ที่ทำงานร่วมกัน:

| Building Block | ทำหน้าที่ | ภาษาง่ายๆ |
|----------------|----------|-----------|
| **Prompts** | คำสั่งชั่วขณะ | "สิ่งที่ฉันต้องการ **ตอนนี้**" |
| **CLAUDE.md** | ความรู้พื้นฐาน | "สิ่งที่คุณต้อง **รู้**" |
| **Skills** | ความรู้เชิงกระบวนการ | "**วิธีทำ** สิ่งต่างๆ" |
| **MCP** | เชื่อมต่อเครื่องมือภายนอก | "**มือ** ที่จับสิ่งภายนอก" |
| **Subagents** | มอบหมายงาน | "**คนที่ทำงานแทน**" |

### Key Insight #1: Skills + MCP = Complementary

```
MCP  → เชื่อมต่อ Claude กับข้อมูลภายนอก (อ่าน GitHub issues, สร้าง PR)
Skills → สอน Claude ว่าจะทำอะไรกับข้อมูลนั้น (อ่าน → implement → test → PR)

= ทำงานด้วยกัน ไม่ใช่เลือกอันเดียว
```

### Key Insight #2: CLAUDE.md vs Skills — "รู้" vs "ทำ"

- **CLAUDE.md** = "Here's what you need to **know**" (project structure, conventions)
- **Skills** = "Here's **how** to do things" (step-by-step procedures)

### Key Insight #3: Progressive Disclosure

Skills ไม่โหลดทั้งหมดตั้งแต่แรก:
1. Claude อ่าน `description` ของทุก Skill (~100 tokens)
2. ถ้า relevant → โหลด full instructions (<5k tokens)
3. ถ้ามี bundled files → โหลดเฉพาะที่ต้องใช้

= **ประหยัด context window**

### ดู Handout

เปิดไฟล์ `BUILDING_BLOCKS.md` ที่แจก — ใช้ reference ตลอด workshop
ในแต่ละ section จะชี้ให้เห็นว่าใช้ building block ไหน

---

## 📝 Section 2: CLAUDE.md — Background Knowledge (10 นาที)

> Building Block ที่ใช้: **CLAUDE.md** (Background Knowledge)

### CLAUDE.md คืออะไร?

ไฟล์ที่ Claude อ่าน **อัตโนมัติ** ทุกครั้งที่เริ่ม session — เหมือนให้ "คู่มือพนักงานใหม่" ก่อนเริ่มงาน

### ดู CLAUDE.md ของ workshop project

```bash
cat workshop-project/CLAUDE.md
```

สังเกต:
- มีแค่ **38 บรรทัด** — สั้น กระชับ ได้ใจความ
- บอก: project structure, conventions, MCP config, run commands
- **ไม่** บอก: full API docs, ทุก function ในโปรเจค

### Demo: Claude รู้โดยไม่ต้องอ่านไฟล์

```bash
cd workshop-project
claude
```

พิมพ์ใน Claude:
```
What do you know about this project? What MCP servers are available?
```

สังเกต: Claude **ตอบได้ทันที** โดยไม่ต้องเปิดอ่านไฟล์ใดๆ เลย
= CLAUDE.md ทำให้ **ประหยัด tokens** ตั้งแต่เริ่ม session

ออกจาก Claude (`/exit`)

### Ancestor Loading vs Lazy Loading

```
📁 claude-workshop/
├── CLAUDE.md              ← Ancestor Loading: โหลดเสมอ (root)
├── workshop-project/
│   ├── CLAUDE.md          ← Ancestor Loading: โหลดเสมอ (parent dir)
│   └── app/
│       └── CLAUDE.md      ← Lazy Loading: โหลดเมื่อ Claude แตะไฟล์ใน app/
```

- **Ancestor Loading (UP):** CLAUDE.md ที่อยู่ **เหนือ** working directory → โหลด **ทุก session**
- **Lazy Loading (DOWN):** CLAUDE.md ที่อยู่ **ใน** subdirectory → โหลด **เมื่อทำงานในนั้น**

### Best Practices

| ควรทำ | ไม่ควรทำ |
|-------|---------|
| ≤200 บรรทัดต่อไฟล์ | เกิน 200 บรรทัด (Claude อาจไม่ follow ครบ) |
| Architecture, conventions, run commands | Full API documentation |
| MCP server config | ข้อมูลที่เปลี่ยนบ่อย |
| "What NOT to touch" section | รายชื่อทุก function |

---

## 🌳 Section 3: Git Worktrees — 1 Issue = 1 Worktree (10 นาที)

> Building Block ที่ใช้: **Infrastructure** (รองรับ pattern ของ building blocks อื่น)

### ปัญหาเดิม

```bash
# ทำ Issue #3 อยู่...
git stash
git checkout feat/issue-6
# แก้ Issue #6...
git checkout feat/issue-3
git stash pop
# 😱 merge conflict!
```

### Core Principle

```
1 Issue = 1 Git Worktree = 1 Claude Session
```

Worktree = directory แยกที่มี **branch ของตัวเอง** แต่ใช้ **git history เดียวกัน**

### สร้าง Worktree สำหรับ Issue #3

```bash
# ต้องอยู่ใน git root (workshop-project ไม่ใช่ git root — ต้องอยู่ที่ claude-workshop)
cd claude-workshop

# สร้าง worktree
git worktree add ../issue-3-validation -b feat/issue-3-validation
```

### Verify

```bash
# ดู worktrees ทั้งหมด
git worktree list
# claude-workshop           abc1234 [main]
# ../issue-3-validation     abc1234 [feat/issue-3-validation]

# ไปที่ worktree ใหม่
cd ../issue-3-validation

# ตรวจ branch
git branch
# * feat/issue-3-validation

# ตรวจว่ามี CLAUDE.md (shared จาก main repo)
cat workshop-project/CLAUDE.md
# ✅ เนื้อหาเหมือนกัน — ancestor loading
```

### `claude -w` — Shortcut

ที่เราเพิ่งทำ 3 ขั้นตอน:
```bash
git worktree add ../issue-3-validation -b feat/issue-3-validation   # 1. สร้าง worktree
cd ../issue-3-validation/workshop-project                           # 2. เข้า directory
claude                                                              # 3. เปิด Claude
```

`claude -w` (หรือ `--worktree`) รวมทุกอย่างเป็น **คำสั่งเดียว**:
```bash
claude -w
```

#### เบื้องหลัง `claude -w` ทำอะไร

```
1. สร้าง git worktree ให้อัตโนมัติ (ตั้งชื่อ branch ให้)
2. cd เข้า worktree นั้น
3. เริ่ม Claude session ทันที
4. ถ้า Claude ไม่ได้แก้ไฟล์อะไร → worktree ถูกลบอัตโนมัติ (auto-cleanup)
5. ถ้า Claude แก้ไฟล์ → worktree ยังอยู่ บอก path + branch ให้
```

#### เมื่อไหร่ใช้อะไร

| สถานการณ์ | ใช้ | เหตุผล |
|-----------|-----|--------|
| Issue เร่งด่วน ทำเร็วๆ | `claude -w` | สะดวก ไม่ต้องคิดชื่อ branch |
| Issue สำคัญ ต้องตาม convention | Manual | ตั้งชื่อ branch เช่น `feat/issue-3-validation` |
| ลองทำอะไรดูก่อน (experiment) | `claude -w` | auto-cleanup ถ้าไม่ได้ใช้จริง |
| ทำงานร่วมกับทีม ต้อง push | Manual | ชื่อ branch ที่ชัดเจนสื่อสารง่ายกว่า |

> Desktop App (Mac/Windows) ก็มี checkbox **"worktree"** ที่ทำสิ่งเดียวกัน

เราสอน manual ก่อนเพื่อให้เข้าใจ concept — แล้วในชีวิตจริงจะใช้ `claude -w` ก็ได้

---

## ⚡ Section 4: Token Optimization — Implement Issue #3 (15 นาที)

> Building Blocks ที่ใช้: **Prompts** + **MCP** + **CLAUDE.md**

### Pattern ที่จะเรียนรู้

```
Research (อ่าน issue ผ่าน MCP)
    → /compact (บีบ context)
        → Implement (scoped prompt ชี้ไฟล์)
            → Test (รัน tests)
```

### เริ่มทำ

```bash
cd ../issue-3-validation/workshop-project
claude
```

### Step 1: ดู Context Baseline

พิมพ์ใน Claude:
```
/context
```

สังเกต: context แทบว่าง — มีแค่ CLAUDE.md overhead

### Step 2: Research Phase (ใช้ MCP)

```
Read issue #3 from spped2000/claude-workshop.
Summarize the acceptance criteria as a numbered checklist.
Do not implement yet.
```

Claude จะ:
1. เรียก GitHub MCP `get_issue` → อ่าน issue #3
2. แสดง acceptance criteria

### Step 3: ดู Context หลัง Research

```
/context
```

สังเกต: context **โตขึ้น** จาก MCP response + issue content

### Step 4: Compact!

```
/compact
```

Claude สรุป research ที่ผ่านมาเป็น **dense summary** แล้วแทนที่ full history

### Step 5: ดู Context หลัง Compact

```
/context
```

สังเกต: context **เล็กลงอย่างชัดเจน** — ลด 60-80%!

### Step 6: Implement ด้วย Scoped Prompt

```
Read app/models.py and implement the validation from issue #3.
Use EmailStr, Field(ge=0, le=150) for age, Field(min_length=1) for name.
Then write tests in tests/test_validation.py following the pattern in conftest.py.
```

**สังเกตว่า prompt นี้:**
- ✅ ชี้ไฟล์ที่ต้องอ่าน (`app/models.py`)
- ✅ บอก pattern ที่ต้อง follow (`conftest.py`)
- ✅ ระบุไฟล์ output (`tests/test_validation.py`)
- ❌ **ไม่ได้** บอก "look at the codebase and figure it out"

### Step 7: รัน Tests

```
Run uv run pytest -v and show me the results.
```

หรือรันเองใน terminal แยก:
```bash
uv run pytest -v
# ✅ ต้องผ่านทุก test (เดิม + ใหม่)
```

### ⚠️ ยังไม่สร้าง PR! — จะถูก "interrupt" ใน section ถัดไป

### สรุป Token Optimization Techniques

| เทคนิค | ใช้เมื่อไหร่ | ตัวอย่างที่เพิ่งทำ |
|--------|-------------|------------------|
| `/context` | ตรวจ context usage | ดู before/after compact |
| `/compact` | หลัง research ก่อน implement | Step 4 |
| Scoped prompts | ทุก prompt | "Read X then do Y" ใน Step 6 |
| CLAUDE.md | ทุก session | Claude รู้ project โดยไม่ต้อง explore |

---

## 🔀 Section 5: Multiple Issues — The Interruption (20 นาที)

> Building Blocks ที่ใช้: **Prompts** + **MCP**

### สถานการณ์

คุณกำลังทำ Issue #3 อยู่ (validation) — ยังไม่ได้สร้าง PR
แต่ทีมแจ้งมาว่า Issue #6 (CORS) เร่งด่วน ต้องทำก่อน!

### Phase A: จอด Issue #3 (2 นาที)

```bash
# ออกจาก Claude
/exit

# กลับไป main repo
cd ../../claude-workshop
```

แค่นี้เลย! ไม่ต้อง stash, ไม่ต้อง commit — worktree ยังอยู่ตรงเดิม
ไฟล์ที่แก้ไปทั้งหมดยังอยู่ใน `../issue-3-validation/`

### Phase B: ทำ Issue #6 — CORS เร่งด่วน (10 นาที)

```bash
# สร้าง worktree ใหม่
git worktree add ../issue-6-cors -b feat/issue-6-cors

# ดู worktrees ทั้งหมด
git worktree list
# claude-workshop           [main]
# ../issue-3-validation     [feat/issue-3-validation]  ← จอดไว้
# ../issue-6-cors           [feat/issue-6-cors]         ← ใหม่!

# เข้า worktree ใหม่
cd ../issue-6-cors/workshop-project
claude
```

CORS เป็น issue ง่าย (~5 lines of code) — ใช้ **single-shot prompt**:

```
Read issue #6 from spped2000/claude-workshop.
Implement CORS configuration in app/main.py.
Write tests in tests/test_cors.py.
Run uv run pytest -v.
Then create a pull request with "Closes #6" in the body.
```

สังเกต:
- **Session ใหม่** ใน **worktree ใหม่** = clean context
- CLAUDE.md ยังโหลดอยู่ (ancestor loading)
- Claude ไม่รู้อะไรเลยเกี่ยวกับ Issue #3 = **ไม่มี context pollution**

### Phase C: กลับมาต่อ Issue #3 (8 นาที)

```bash
# ออกจาก Claude (/exit)
cd ../../issue-3-validation/workshop-project
claude
```

**มี 2 ตัวเลือก:**

**ตัวเลือก 1: `/resume`**
```
/resume
```
เลือก session เดิมจากรายการ → Claude จำ context ของ Issue #3 ที่ทำไว้

**ใช้เมื่อ:** context ยังไม่เยอะ, ต้องการต่อจากที่ค้างไว้

**ตัวเลือก 2: Session ใหม่**
แค่เริ่ม session ใหม่ — CLAUDE.md + code ที่แก้ไปแล้ว = Claude เข้าใจได้เร็ว

**ใช้เมื่อ:** context เก่าเยอะ, ต้องการ session ที่ clean กว่า

### สร้าง PR สำหรับ Issue #3

```
All tests pass. Create a pull request for issue #3.
Include a description that explains what was implemented.
Include "Closes #3" in the body.
```

### ดู Worktrees ทั้งหมด

```bash
cd ../../claude-workshop
git worktree list
```

### Cleanup (หลัง merge)

```bash
# หลัง PR ถูก merge แล้ว:
git worktree remove ../issue-3-validation
git worktree remove ../issue-6-cors
```

### Key Takeaways

- **จอด** = แค่ออกจาก worktree (ไม่ต้อง stash)
- **กลับ** = cd เข้าไปใหม่ (ไม่มี conflict)
- **Context ไม่ปนกัน** = แต่ละ worktree มี session ของตัวเอง
- **CLAUDE.md shared** = ทุก worktree ได้ background knowledge เดียวกัน

---

## 🔍 Section 6: PR Review Cycle (15 นาที)

> Building Blocks ที่ใช้: **Skills** + **MCP** + **Prompts**

### สถานการณ์

PR ของ Issue #3 ได้รับ review comments จาก reviewer:
- "Please add a test for email with leading/trailing spaces"
- "The error message for invalid age should include the valid range (0-150)"

### ทำไมต้อง Session ใหม่ (ไม่ใช่ /resume)?

| | /resume | Session ใหม่ |
|---|---|---|
| Context | มี history ทั้งหมดจาก implementation | แค่ CLAUDE.md + code ปัจจุบัน |
| Token cost | สูง (carry forward ทุกอย่าง) | ต่ำ (เริ่มใหม่ clean) |
| เมื่อใช้ | Debug ต่อจากที่ค้าง | แก้ review comments (scope ต่าง) |

### เริ่ม Session ใหม่

```bash
cd ../issue-3-validation/workshop-project
claude
```

### Method 1: Manual (Prompts + MCP)

```
Read the review comments on PR #<N> from spped2000/claude-workshop.
Fix only what the reviewers requested. Do not change other files.
Run uv run pytest -v after fixing.
Then push to the existing branch.
```

เปลี่ยน `<N>` เป็นเลข PR ที่ได้จาก Section 5

Claude จะ:
1. ใช้ **MCP** อ่าน review comments
2. ใช้ **Prompt** (คำสั่ง) เป็นตัว guide
3. แก้เฉพาะที่ reviewer ขอ
4. Push ไป branch เดิม (ไม่สร้าง PR ใหม่)

### Method 2: `/fix-review` Skill (Skills + MCP)

ถ้ามี skill `fix-review` ติดตั้งอยู่:

```
/fix-review <N>
```

Claude จะทำเหมือน Method 1 แต่ **อัตโนมัติ** ตาม step ที่ Skill กำหนด:
1. อ่าน review comments ผ่าน MCP
2. แก้ตามที่ reviewer ขอ
3. รัน tests
4. Commit + push

### สังเกตความแตกต่าง

| | Method 1 (Manual) | Method 2 (Skill) |
|---|---|---|
| Building blocks | Prompts + MCP | Skills + MCP + Prompts |
| ต้องพิมพ์ | prompt ยาว ระบุทุกขั้นตอน | `/fix-review <N>` |
| ทำซ้ำได้ | ต้อง copy-paste prompt | พิมพ์ command เดิม |
| Consistent | ขึ้นกับ prompt ที่พิมพ์ | ทำเหมือนกันทุกครั้ง |

**นี่คือ complementary relationship จริงๆ:**
- **Skill** สอน Claude *วิธีทำ* (procedural knowledge)
- **MCP** ให้ Claude *เครื่องมือ* (tool connectivity)
- ผลลัพธ์: workflow ที่ reliable และ repeatable

---

## 🧩 Section 7: Skills Deep Dive (15 นาที)

> Building Blocks ที่ใช้: **Skills** + **MCP** + **Subagents**
> อ้างอิง: https://claude.com/blog/skills-explained

### 7A: How Skills Work (5 นาที)

#### SKILL.md Anatomy

```yaml
---
name: implement-issue                    # ชื่อ (เรียกด้วย /implement-issue)
description: Read GitHub issue...         # สำหรับ Progressive Disclosure
argument-hint: [issue-number]             # placeholder: /implement-issue <N>
disable-model-invocation: true            # true = user-only, false = auto
context: fork                             # fork = แยก context
agent: Explore                            # ใช้ subagent type ไหน
allowed-tools: Read Write Edit Bash       # จำกัด tools
---

# Instructions (markdown body)
## Step 1 — ...
## Step 2 — ...
# ใช้ $0 = argument แรก (เช่น issue number)
```

#### Progressive Disclosure — ทำไม Skills ถึง efficient

```
มี 20 Skills ติดตั้ง:

Step 1: Claude อ่าน description ทั้ง 20 ตัว
        = 20 × ~100 tokens = 2,000 tokens
        "อันไหน relevant?"

Step 2: relevant 1 ตัว → โหลด full instructions
        = ~5,000 tokens

Total: 7,000 tokens
vs โหลดทั้ง 20: 100,000 tokens ❌
```

#### Auto vs Manual Invocation

| | Auto-invoke | Manual-only |
|---|---|---|
| Setting | `disable-model-invocation: false` | `disable-model-invocation: true` |
| ใครเรียก | Claude เรียกเอง (เมื่อ relevant) | User พิมพ์ `/skill-name` |
| เหมาะสำหรับ | Coding conventions, formatting | Create PR, push code (มี side effects) |
| ตัวอย่าง | "Always use camelCase" | `/implement-issue`, `/fix-review` |

### 7B: Skills + MCP = Complementary (5 นาที)

#### ตัวอย่างจริง: `/implement-issue 3`

```
ผู้เรียนพิมพ์ → /implement-issue 3

เบื้องหลัง:
┌─────────────────────────────────────────────────┐
│  Skill  → "อ่าน issue → implement → test → PR"  │ ← procedural knowledge
│  MCP    → get_issue, create_pull_request         │ ← tool connectivity
│  Prompt → $0 = 3 (issue number)                  │ ← moment instruction
│  CLAUDE.md → project structure, conventions      │ ← background knowledge
│                                                   │
│  = ทั้ง 4 building blocks ทำงานร่วมกันใน 1 cmd   │
└─────────────────────────────────────────────────┘
```

#### When to use what?

| ต้องการ | ใช้ | เหตุผล |
|--------|-----|--------|
| อ่าน/เขียนข้อมูล GitHub | **MCP** | ต้องการ tool connectivity |
| Workflow ที่ทำซ้ำ | **Skill** | procedural knowledge |
| Exploration ไม่ปน context | **Skill** + `context: fork` | isolated execution |
| Coding conventions | **Skill** (auto-invoke) | always relevant |
| Project structure | **CLAUDE.md** | background knowledge |

### 7C: `context: fork` Demo (5 นาที)

#### ปัญหา

เมื่อ Claude research issue → ข้อมูลทั้งหมดเข้า main context
ถ้า research เยอะ → context บวม → ต้อง `/compact` บ่อย

#### Solution: `context: fork`

ดู skill `/explore-issue` ที่เตรียมไว้:

```yaml
---
name: explore-issue
description: Research a GitHub issue and summarize findings
context: fork        # ← KEY: แยก context
agent: Explore       # ← ใช้ Explore subagent
allowed-tools: Read Glob Grep
---
Read issue #$0 and find all files that need to change.
Return a concise list. Do not make edits.
```

#### ลองใช้

เปิด Claude ใน workshop-project:
```
/explore-issue 4
```

สังเกต:
1. **Subagent** แยกออกไปทำ research (context ของมันเอง)
2. **Return summary** กลับมาให้ main session
3. **Main context ไม่บวม** — ได้แค่ summary สั้นๆ

```
/context
```
ดู: context ยังเล็กอยู่ ทั้งที่ได้ข้อมูลครบ!

#### Building Blocks ที่ใช้ร่วมกัน

```
/explore-issue 4
     │
     ├── Skill → สอนวิธี research (procedural knowledge)
     ├── Subagent → ทำ research แทน (task delegation)
     ├── MCP → อ่าน issue จาก GitHub (tool connectivity)
     └── context: fork → แยก context (token optimization)
```

---

## 🚀 Section 8: Advanced Techniques (10 นาที)

> สาธิตโดยผู้สอน — ไม่ต้องทำตาม

### 8A: Subagents (4 นาที)

Claude Code มี **5 official subagent types:**

| Type | ทำอะไร | เมื่อใช้ |
|------|--------|---------|
| **Explore** | ค้นหา codebase แบบ read-only | หา function, เข้าใจ pattern |
| **Plan** | ออกแบบ implementation plan | วางแผนก่อน code |
| **general-purpose** | ทำงานทั่วไปแบบอิสระ | task ที่ซับซ้อน multi-step |
| **statusline-setup** | ตั้งค่า status line | UI customization |
| **claude-code-guide** | ตอบคำถามเกี่ยวกับ Claude Code | help & docs |

#### `isolation: "worktree"` — Parallel Independent Work

```yaml
# ใน agent frontmatter
isolation: "worktree"
# Agent ทำงานใน git worktree แยก
# ไม่กระทบ main codebase
```

#### `/batch` — Large Changesets

```bash
# ต้อง rename function ใน 100 ไฟล์?
/batch "Rename getUserName to fetchUserName in all files"
```

Claude จะ:
1. สร้าง **worktree agents หลายตัว** พร้อมกัน
2. แต่ละตัวทำงาน **parallel** บน files ของตัวเอง
3. รวมผลลัพธ์กลับ

### 8B: Hooks & Scheduled Tasks (3 นาที)

#### Hooks — Lifecycle Events

```
SessionStart     → ทำอะไรเมื่อเริ่ม session
PreToolUse       → ทำอะไรก่อน Claude ใช้ tool
PostToolUse      → ทำอะไรหลัง Claude ใช้ tool
Stop             → ทำอะไรเมื่อ Claude หยุด
```

ตัวอย่าง:
- Auto-format code หลัง Claude เขียน
- เล่นเสียง notification เมื่อ Claude ทำเสร็จ
- Pre-commit checks ก่อน commit

#### Scheduled Tasks

```bash
# ทำซ้ำทุก 5 นาที: auto-address PR review comments
/loop 5m /babysit

# ทำซ้ำทุก 30 นาที: check for new issues
/loop 30m "Check for new issues assigned to me"

# Cloud-based cron
/schedule
```

### 8C: Memory & Continued Learning (3 นาที)

#### Memory System

Claude Code มีระบบ memory ที่จำข้อมูลข้าม sessions:

| Scope | อยู่ที่ | เห็นโดย |
|-------|---------|--------|
| **User** | `~/.claude/` | ทุก project ของคุณ |
| **Project** | `.claude/` | ทุกคนใน project |
| **Local** | `.claude/` (gitignored) | คุณคนเดียว |

```bash
# ดู memory ทั้งหมด
/memory

# CLAUDE.md vs Memory
# CLAUDE.md = explicit, version-controlled, ทุกคนเห็น
# Memory = implicit, auto-generated, personal
```

#### เรียนรู้ต่อ

```bash
# Interactive lessons (10 บทเรียน)
/power-ups

# ครอบคลุม: @files, modes, undo, background tasks,
# CLAUDE.md, MCPs, skills, agents, remote control, model dialing
```

**Resources:**
- **Skills Explained:** https://claude.com/blog/skills-explained
- **Best Practices:** https://github.com/shanraisshan/claude-code-best-practice

---

## 📋 Checklist ตรวจสอบผลลัพธ์

หลังทำ workshop จบ ตรวจสอบว่าคุณ:

### Concepts
- [ ] เข้าใจ 5 Building Blocks และเมื่อไหร่ใช้อะไร
- [ ] เข้าใจ CLAUDE.md: ancestor loading vs lazy loading
- [ ] เข้าใจ Progressive Disclosure ของ Skills
- [ ] เข้าใจว่า Skills + MCP เป็น complementary ไม่ใช่ competing

### Hands-on
- [ ] สร้าง worktree สำหรับ Issue #3 สำเร็จ
- [ ] ใช้ `/context` + `/compact` ดู before/after
- [ ] Implement Issue #3 ด้วย scoped prompt
- [ ] จอด Issue #3 แล้วทำ Issue #6 ใน worktree แยก
- [ ] กลับมาต่อ Issue #3 (ด้วย `/resume` หรือ session ใหม่)
- [ ] สร้าง PR ทั้ง 2 issues
- [ ] แก้ review comments (manual หรือ `/fix-review`)
- [ ] ทดลอง `/explore-issue` ด้วย `context: fork`

### Tests
- [ ] `uv run pytest` ผ่านทุก test ใน Issue #3 worktree
- [ ] `uv run pytest` ผ่านทุก test ใน Issue #6 worktree

---

## 🐛 แก้ปัญหาเบื้องต้น

| ปัญหา | วิธีแก้ |
|-------|---------|
| `uv: command not found` | ติดตั้ง uv ตาม Section 0 |
| `github` ไม่อยู่ใน `claude mcp list` | รันคำสั่ง `claude mcp add` อีกครั้ง — ตรวจ token |
| MCP 401 Unauthorized | ตรวจ `GITHUB_TOKEN` set ถูกต้อง |
| MCP 404 on issue | ใช้ `spped2000/claude-workshop` เป็น repo name |
| `git worktree add` error | ต้องอยู่ใน git root (claude-workshop ไม่ใช่ workshop-project) |
| Worktree branch exists | `git branch -D feat/issue-N` แล้วลองใหม่ |
| Tests fail เพราะ state ค้าง | `conftest.py` reset อัตโนมัติ — ตรวจว่า import ถูก |
| Claude แก้ไฟล์ผิด | พิมพ์ `Re-read CLAUDE.md and confirm the correct file.` |
| `/compact` ไม่ลด context เท่าไหร่ | ปกติถ้า conversation สั้น — ลองทำ research เพิ่มแล้ว compact |
| `/resume` ไม่เห็น session เดิม | session อาจหมดอายุ — เริ่มใหม่ก็ได้ |
| `/fix-review` ไม่เจอ | ตรวจว่ามี SKILL.md ใน `.claude/skills/fix-review/` |
| `/explore-issue` ไม่ทำงาน | ตรวจว่ามี skill + MCP connected |

---

## 📚 สรุป Best Practices

```
Setup:
  ✅ CLAUDE.md ครบ — architecture, conventions, run commands (≤200 lines)
  ✅ 1 Issue = 1 Worktree = 1 Session
  ✅ Skills สำหรับ workflow ที่ทำซ้ำ

ระหว่าง Session:
  ✅ /context ตรวจ context usage
  ✅ /compact หลัง research phase ก่อน implement
  ✅ Scoped prompts — ชี้ไฟล์ + pattern แทน "look at codebase"
  ✅ Reference ไม่ re-explain — "Fix line 45" ไม่ต้องอธิบายซ้ำ
  ✅ context: fork สำหรับ exploration ที่ไม่อยากให้ปน context

Multiple Issues:
  ✅ จอด = ออกจาก worktree (ไม่ต้อง stash)
  ✅ กลับ = cd เข้าไปใหม่ (/resume หรือ session ใหม่)
  ✅ ทำ parallel ได้ใน terminal คนละ tab

PR Review:
  ✅ Session ใหม่ใน worktree เดิม (ไม่ /resume)
  ✅ MCP อ่าน review comments
  ✅ /fix-review skill จัดการให้อัตโนมัติ

Building Blocks:
  ✅ Skills + MCP = complementary (ไม่ใช่ competing)
  ✅ CLAUDE.md = "รู้" / Skills = "ทำ"
  ✅ Progressive Disclosure = efficient context management
  ✅ Subagents + context: fork = isolated execution

หลีกเลี่ยง:
  ❌ ทำหลาย issue ใน session เดียว (context pollution)
  ❌ "Look at the whole codebase and..." (waste tokens)
  ❌ อธิบาย context ซ้ำที่มีใน CLAUDE.md อยู่แล้ว
  ❌ Session ยาวเกินโดยไม่ /compact
  ❌ /resume เพื่อแก้ review comments (context เก่าเปลือง)
```

---

## 🔗 Resources

| Resource | Link |
|----------|------|
| Skills Explained (Official Blog) | https://claude.com/blog/skills-explained |
| Claude Code Best Practices | https://github.com/shanraisshan/claude-code-best-practice |
| Building Blocks Handout | `BUILDING_BLOCKS.md` (ในโฟลเดอร์นี้) |
| Workshop Project | https://github.com/spped2000/claude-workshop |
| Power-ups (Interactive Lessons) | พิมพ์ `/power-ups` ใน Claude Code |
