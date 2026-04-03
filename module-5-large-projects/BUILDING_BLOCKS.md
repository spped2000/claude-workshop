# Claude Code Building Blocks — Reference Handout

> อ้างอิงจาก: https://claude.com/blog/skills-explained
> เพิ่มเติมจาก: https://github.com/shanraisshan/claude-code-best-practice

---

## 5 Building Blocks ของ Claude Code

Claude Code ไม่ได้มีแค่ "พิมพ์ prompt แล้วรอ" — มันมี **5 ส่วนประกอบ** ที่ทำงานร่วมกัน:

| Building Block | ทำหน้าที่อะไร | ภาษาง่ายๆ | ตัวอย่าง |
|----------------|--------------|-----------|---------|
| **Prompts** | คำสั่งชั่วขณะ | "สิ่งที่ฉันต้องการ **ตอนนี้**" | `Read issue #3 and implement it` |
| **CLAUDE.md** | ความรู้พื้นฐาน | "สิ่งที่คุณต้อง **รู้**" | Project structure, conventions, MCP config |
| **Skills** | ความรู้เชิงกระบวนการ | "**วิธีทำ** สิ่งต่างๆ" | `/implement-issue 3`, `/fix-review 5` |
| **MCP** | เชื่อมต่อเครื่องมือภายนอก | "**มือ** ที่จับสิ่งภายนอก" | GitHub MCP อ่าน issue, สร้าง PR |
| **Subagents** | มอบหมายงาน | "**คนที่ทำงานแทน**" | Explore agent, Plan agent |

---

## Comparison แบบละเอียด

| คุณสมบัติ | Prompts | CLAUDE.md | Skills | MCP | Subagents |
|----------|---------|-----------|--------|-----|-----------|
| **ให้อะไร** | คำสั่ง | ความรู้พื้นฐาน | วิธีทำงาน | เครื่องมือ | คนทำงาน |
| **คงอยู่** | แค่ conversation นี้ | ทุก session | ทุก session | ตลอดเวลา | เมื่อเรียกใช้ |
| **บรรจุ** | Natural language | Documents | Instructions + code | Tool definitions | Agent logic |
| **โหลดเมื่อ** | ทุก turn | เริ่ม session | เมื่อ relevant | Always available | เมื่อ invoke |
| **มี code** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **เหมาะสำหรับ** | คำขอครั้งเดียว | Context กลาง | Expertise เฉพาะทาง | Data access | งานเฉพาะทาง |

---

## Key Relationships — เข้าใจว่าอะไรทำงานกับอะไร

### 1. Skills + MCP = Complementary (ไม่ใช่ Competing)

```
MCP เชื่อมต่อ Claude กับข้อมูลภายนอก
Skills สอน Claude ว่าจะทำอะไรกับข้อมูลนั้น
```

**ตัวอย่าง:**

```
/implement-issue 3

เบื้องหลัง:
┌─────────────────────────────────────────────────┐
│  Skill บอก:  "อ่าน issue → implement → test → PR" │ ← procedural knowledge
│  MCP ให้:    get_issue, create_pull_request       │ ← tool connectivity
│  Prompt ให้:  $0 = 3 (issue number)               │ ← moment instruction
│  CLAUDE.md:  project structure, conventions        │ ← background knowledge
└─────────────────────────────────────────────────┘
= ทั้ง 4 building blocks ทำงานร่วมกันใน 1 command
```

### 2. CLAUDE.md vs Skills — "รู้" vs "ทำ"

| | CLAUDE.md | Skills |
|---|---|---|
| หน้าที่ | "นี่คือสิ่งที่คุณต้อง **รู้**" | "นี่คือ **วิธีทำ** สิ่งต่างๆ" |
| เมื่อโหลด | **ทุก session** (ancestor loading) | **เมื่อ relevant** (Progressive Disclosure) |
| ตัวอย่าง | "Use async def, Pydantic v2, tests in tests/" | "Step 1: Read issue, Step 2: Implement..." |
| ขนาด | ≤200 lines (loaded ทั้งหมด) | ~100 tokens metadata + <5k เมื่อ activate |

### 3. Skills vs Subagents — "วิธีทำ" vs "คนทำ"

| | Skills | Subagents |
|---|---|---|
| เปรียบเหมือน | **คู่มือฝึกอบรม** | **พนักงานเฉพาะทาง** |
| portable | ✅ ใช้ได้ทุก conversation | ❌ ต้อง define ในแต่ละ project |
| context | ใช้ context เดียวกัน (หรือ fork) | มี context แยกของตัวเอง |
| เมื่อใช้ | สอน Claude วิธีทำ **ขั้นตอน** | ให้ Claude **มอบหมาย** งานทั้งก้อน |

---

## Progressive Disclosure — ทำไม Skills ถึง Efficient

Skills ไม่ได้โหลดทั้งหมดเข้า context window ตั้งแต่แรก:

```
Step 1: Claude อ่าน description ของทุก Skill
        (~100 tokens ต่อ skill)
        ↓
        "อันนี้ relevant มั้ย?"
        ↓
Step 2: ถ้า relevant → โหลด full SKILL.md instructions
        (<5,000 tokens)
        ↓
Step 3: ถ้ามี bundled scripts/files → โหลดเฉพาะที่ต้องใช้
        (on-demand)
```

**ผลลัพธ์:** ถ้ามี 20 Skills ติดตั้ง แต่ใช้แค่ 1 อัน:
- ❌ โหลดทั้ง 20 = 100,000 tokens
- ✅ Progressive Disclosure = 2,000 + 5,000 = **7,000 tokens**

---

## SKILL.md Anatomy — Reference

```yaml
---
# Required
name: implement-issue              # ชื่อ (เรียกด้วย /implement-issue)
description: Read GitHub issue...  # สำหรับ Progressive Disclosure

# Optional — Control
argument-hint: [issue-number]      # placeholder สำหรับ argument
disable-model-invocation: true     # true = user-only, false = auto-invoke
user-invocable: true               # แสดงใน / menu

# Optional — Execution
context: fork                      # fork = แยก context, inline = ใช้ context เดิม
agent: Explore                     # ใช้ subagent type ไหน
allowed-tools: Read Write Edit     # จำกัด tools ที่ใช้ได้
effort: high                       # low, medium, high
model: sonnet                      # override model

# Optional — Discovery
paths: ["src/"]                    # auto-discover เมื่อทำงานในไฟล์เหล่านี้
---

# Markdown instructions body
# ใช้ $0 สำหรับ argument แรก, $1 สำหรับอันที่สอง
```

### Global vs Project Skills

| | Global Skills | Project Skills |
|---|---|---|
| ตำแหน่ง | `~/.claude/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| ใช้ได้ | ทุก project | เฉพาะ project นี้ |
| เหมาะสำหรับ | Workflow ทั่วไป (เช่น fix-review) | Workflow เฉพาะ project |

---

## Decision Framework — เมื่อไหร่ใช้อะไร

```
ต้องการอะไร?
│
├── ข้อมูลจากภายนอก (GitHub, API, DB)?
│   └── ใช้ MCP
│
├── workflow ที่ทำซ้ำหลายครั้ง?
│   └── ใช้ Skill
│       ├── มี side effects (push, create PR)?
│       │   └── disable-model-invocation: true
│       └── ไม่มี side effects?
│           └── disable-model-invocation: false (auto-invoke)
│
├── context ของ project (structure, conventions)?
│   └── ใช้ CLAUDE.md
│
├── งานที่ต้องทำตอนนี้เลย?
│   └── ใช้ Prompt
│
└── งานที่ต้อง delegate (explore, plan, parallel work)?
    └── ใช้ Subagent
        ├── ไม่อยากให้ปน context?
        │   └── context: fork หรือ isolation: "worktree"
        └── ต้องการ parallel?
            └── isolation: "worktree" หรือ /batch
```

---

## Links สำหรับศึกษาเพิ่ม

- **Skills Explained (Official Blog):** https://claude.com/blog/skills-explained
- **Claude Code Best Practices:** https://github.com/shanraisshan/claude-code-best-practice
- **Power-ups (Interactive Lessons):** พิมพ์ `/power-ups` ใน Claude Code
