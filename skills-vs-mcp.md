# Skills vs MCP — เจาะลึกความแตกต่างและ Use Cases

## ภาพรวม

```
Skills  = "สอน Claude ว่าทำอะไร ยังไง"  (prompt/instructions)
MCP     = "ให้ Claude มีมือใหม่"         (tools/connections)
```

ทั้งสองทำงานร่วมกันได้ — Skills บอก Claude ว่าจะใช้ MCP tool ไหน, MCP จัดหา tool นั้นให้

---

## 1. Skills คืออะไร

### หลักการทำงาน

Skills คือ prompt template ที่เก็บใน `SKILL.md` ไฟล์ เมื่อ invoke แล้ว Claude ได้รับ context จาก skill ก่อน แล้วค่อยทำงาน

```
~/.claude/skills/<skill-name>/SKILL.md    ← personal (ทุก project)
.claude/skills/<skill-name>/SKILL.md      ← project-specific
```

### Frontmatter Fields ที่สำคัญ

```yaml
---
name: pr-review
description: Review a pull request for code quality and conventions
argument-hint: [pr-number]
context: fork                    # รันใน isolated subagent
agent: Explore                   # subagent type
allowed-tools: Bash(gh *) Read   # tools ที่ใช้ได้โดยไม่ต้องขอ permission
model: claude-sonnet-4-6         # override model
effort: high                     # low / medium / high / max
disable-model-invocation: true   # Claude invoke เองไม่ได้ ต้องพิมพ์ /pr-review
user-invocable: false            # ไม่ขึ้น / menu แต่ Claude invoke ได้เอง
paths: "src/**/*.ts"             # load เฉพาะเมื่อทำงานกับไฟล์ที่ match
---
```

### 3 Loading Modes

| Mode | วิธี config | พฤติกรรม |
|------|------------|----------|
| **Inline** (default) | ไม่ต้องตั้งอะไร | description อยู่ใน context ตลอด, full content load เมื่อ invoke |
| **Manual only** | `disable-model-invocation: true` | Claude invoke เองไม่ได้, ต้องพิมพ์ `/skill-name` |
| **Hidden** | `user-invocable: false` | ไม่ขึ้น `/` menu, แต่ Claude invoke ได้ตามความเหมาะสม |

### Dynamic Context Injection `` !`command` ``

syntax `` !`command` `` รัน shell command **ก่อน** ส่ง prompt ให้ Claude — Claude เห็นผลลัพธ์จริง ไม่ใช่ command

```yaml
---
name: pr-summary
allowed-tools: Bash(gh *)
context: fork
---

## Pull Request Context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Task
สรุป PR นี้เป็นภาษาไทย บอกว่าแก้อะไร ทำไม และมีความเสี่ยงอะไรบ้าง
```

เมื่อ invoke: (1) คำสั่ง `` !`gh pr diff` `` รันก่อน → (2) ผลลัพธ์แทนที่ placeholder → (3) Claude ได้รับ prompt พร้อม diff จริงๆ

### Variables ที่ใช้ได้

```yaml
$ARGUMENTS          # ทุก argument ที่ส่งมา เช่น /deploy production
$0, $1, $2          # argument แยกตำแหน่ง เช่น $0 = "production"
${CLAUDE_SESSION_ID} # session ID ปัจจุบัน
${CLAUDE_SKILL_DIR} # path ของ skill directory
```

### ตัวอย่าง Skill ที่ดี

```yaml
---
name: deploy
description: Deploy the application to a target environment. Runs tests, builds, and deploys.
argument-hint: [environment]
disable-model-invocation: true
allowed-tools: Bash
---

## Deploy to $0

### Pre-deploy checklist
- Environment: $0
- Branch: !`git branch --show-current`
- Last commit: !`git log -1 --oneline`
- Tests: !`uv run pytest -q 2>&1 | tail -5`

### Steps
1. Confirm branch is clean (`git status`)
2. Run full test suite — abort if any fail
3. Build: `uv build`
4. Deploy to $0: `./scripts/deploy.sh $0`
5. Verify health check passes after deploy
6. Report result with timestamp
```

---

## 2. MCP คืออะไร

### หลักการทำงาน

MCP (Model Context Protocol) คือ protocol มาตรฐานสำหรับต่อ Claude เข้ากับ external systems Claude เรียก MCP tools ได้เหมือน function call ปกติ

```
Claude Code  →  MCP Protocol  →  External System
"อ่าน issue"    แปลงคำสั่ง        GitHub API
```

### 4 ประเภท Capability

| ประเภท | คืออะไร | ตัวอย่าง |
|--------|---------|---------|
| **Tools** | Function ที่เรียกได้ | `get_issue`, `create_pr`, `query_db` |
| **Resources** | ข้อมูลที่ reference ด้วย @ | `@github:issue://123`, `@docs:file://api` |
| **Prompts** | Template จาก MCP server | `/mcp-deploy-prompt` |
| **Push/Channel** | Server ส่ง event เข้า session | CI result, monitoring alert |

### Transport Types

```bash
# HTTP (แนะนำสำหรับ remote services)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Stdio (สำหรับ local process เช่น npx packages)
claude mcp add github -e GITHUB_TOKEN=$env:GITHUB_TOKEN \
  -- npx -y @modelcontextprotocol/server-github

# SSE (deprecated — ใช้ HTTP แทน)
claude mcp add --transport sse old-service https://api.example.com/sse
```

### Scope และ Precedence

```
Local   > Project (.mcp.json) > User > Managed
```

| Scope | เก็บที่ | ใช้เมื่อ |
|-------|--------|--------|
| **Local** (default) | `~/.claude.json` ผูกกับ project path | personal dev, sensitive credentials |
| **Project** | `.mcp.json` ใน repo | ทีมใช้ร่วมกัน, check in git |
| **User** | `~/.claude.json` ทุก project | เครื่องมือส่วนตัวที่ใช้ทุก project |
| **Managed** | system-wide | IT admin lock down |

### Tool Search — ประหยัด Context

MCP จะ defer tool definitions ไม่โหลดทั้งหมดตั้งแต่แรก:
- Session เริ่มต้น: โหลดแค่ **ชื่อ tool**
- เมื่อ Claude ต้องการ tool นั้น: โหลด full definition
- ผลลัพธ์: เพิ่ม MCP server เยอะแค่ไหนก็ไม่กิน context

```bash
ENABLE_TOOL_SEARCH=true   # default — defer definitions
ENABLE_TOOL_SEARCH=auto   # โหลดถ้าใช้ <10% context, ไม่งั้น defer
ENABLE_TOOL_SEARCH=false  # โหลดทุกอย่างตั้งแต่แรก
```

---

## 3. เปรียบเทียบเชิงลึก

| มิติ | Skills | MCP |
|------|--------|-----|
| **คืออะไร** | Prompt/instructions ใน markdown | Connection ไป external API/tools |
| **Claude ได้อะไร** | Knowledge + workflow steps | Callable functions + live data |
| **ต้องการ network ไหม** | ❌ (อ่านจาก file) | ✅ (ต่อ external system) |
| **ข้อมูล real-time ได้ไหม** | ผ่าน `` !`command` `` เท่านั้น | ✅ ดึงข้อมูลล่าสุดทุกครั้ง |
| **เปลี่ยน state ภายนอกได้ไหม** | ผ่าน Bash เท่านั้น | ✅ สร้าง PR, write DB จริง |
| **Configuration** | YAML frontmatter + markdown | `.mcp.json` หรือ `claude mcp add` |
| **ใช้ร่วมในทีมได้ไหม** | ✅ project skills | ✅ project scope `.mcp.json` |
| **Isolated execution** | ✅ `context: fork` | ❌ (ใช้ session เดิม) |
| **Override model/effort** | ✅ per-skill | ❌ |

---

## 4. Use Cases — ใช้อะไรเมื่อไหร่

### ใช้ Skills เมื่อ...

#### A. สอน Convention ที่ต้องทำซ้ำ

```yaml
---
name: commit
description: Create a git commit following conventional commits format
disable-model-invocation: true
allowed-tools: Bash(git *)
---

สร้าง commit ตาม Conventional Commits:
- prefix: feat, fix, refactor, docs, test, chore
- body อธิบาย "why" ไม่ใช่ "what"
- ต้องรัน tests ก่อน commit เสมอ

!`git diff --staged`

ดู diff ข้างบนแล้วสร้าง commit message ที่เหมาะสม
```

#### B. Workflow ที่ซับซ้อนแต่ใช้ tools ที่มีอยู่แล้ว

```yaml
---
name: code-review
description: Review code changes for quality, security, and conventions
context: fork
agent: Explore
allowed-tools: Read Grep Glob Bash(git *)
---

Review โค้ดใน PR นี้:
- Diff: !`git diff main...HEAD`
- ตรวจ security vulnerabilities
- ตรวจ coding conventions ตาม .eslintrc
- ตรวจ test coverage
สรุปเป็น bullet points พร้อม severity: Critical / Warning / Suggestion
```

#### C. Reference Knowledge ที่ Claude ต้องรู้ตลอด

```yaml
---
name: api-conventions
description: REST API design conventions for this project
user-invocable: false  # Claude load เองเมื่อเหมาะสม
---

## API Design Rules
- ใช้ snake_case สำหรับ JSON fields
- Pagination ใช้ cursor-based เสมอ ห้าม offset
- Error format: { "error": { "code": "...", "message": "..." } }
- Version ใน URL path: /v1/...
```

#### D. Task ที่ต้องการ Isolation

```yaml
---
name: analyze-bundle
description: Analyze webpack bundle size and suggest optimizations
context: fork
agent: general-purpose
---
วิเคราะห์ bundle size รายงานไฟล์ที่ใหญ่ที่สุด 10 อันดับ
และแนะนำวิธี optimize โดยไม่ต้องทำการเปลี่ยนแปลงใดๆ
```

---

### ใช้ MCP เมื่อ...

#### A. ต้องการข้อมูล Real-time จาก External System

```
# Skills ทำได้ผ่าน !`gh issue view` แต่...
# MCP ดีกว่าเพราะ:
- ไม่ต้องติดตั้ง gh CLI ในเครื่อง
- ดึงข้อมูล structured (JSON) โดยตรง
- Claude เข้าถึง metadata ครบกว่า (labels, assignees, linked PRs)
```

```bash
claude mcp add github -e GITHUB_TOKEN=... \
  -- npx -y @modelcontextprotocol/server-github
```

#### B. ต้องการ Write Access ไปยัง External System

```
# Skills ทำได้ผ่าน Bash แต่ต้องมี tool นั้นติดตั้งในเครื่อง
# MCP ทำได้โดยตรงผ่าน API:
```

| Action | ด้วย Skills (Bash) | ด้วย MCP |
|--------|-------------------|---------|
| สร้าง PR | `gh pr create ...` (ต้องมี gh CLI) | `github.create_pull_request(...)` |
| Query DB | `psql -c "SELECT ..."` (ต้องมี psql) | `postgres.query(...)` |
| ส่ง Slack | `curl -X POST slack webhook` | `slack.send_message(...)` |

#### C. ทีมต้องการ Shared Tools โดยไม่ต้อง Setup แต่ละคน

```json
// .mcp.json — check in git ให้ทุกคนใช้ร่วมกัน
{
  "mcpServers": {
    "github": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

#### D. ต้องการ @ mention Resources

```
# ใน chat พิมพ์:
Can you fix the bug described in @github:issue://42?

# Claude ดึง issue 42 มาอ่านอัตโนมัติ พร้อม metadata ครบ
```

#### E. Real-time Monitoring / Push Events

```bash
# MCP server ส่ง event เข้า session ได้โดยตรง
claude mcp add --transport http --channels sentry https://mcp.sentry.io/mcp
# → Claude รับ alert ทันทีเมื่อ production error เกิดขึ้น
```

---

### ใช้ทั้งคู่ร่วมกัน

```yaml
---
name: implement-issue
description: Read a GitHub issue and implement the feature with tests and PR
argument-hint: [issue-number]
allowed-tools: Bash Read Write Edit Glob Grep github__get_issue github__create_pull_request
---

## Task: Implement Issue #$0

อ่าน issue ก่อน (ผ่าน GitHub MCP):
ใช้ github MCP tool เพื่อดึง issue #$0 จาก repo นี้

จากนั้น:
1. Implement ตาม acceptance criteria ทุกข้อ
2. Follow conventions ใน CLAUDE.md
3. เขียน tests ใน tests/test_<feature>.py
4. รัน `uv run pytest` ให้ผ่านทั้งหมด
5. สร้าง PR ผ่าน GitHub MCP พร้อม "Closes #$0" ใน description
```

---

## 5. ทำไม Workshop นี้ถึงใช้ MCP ไม่ใช่ Skills

Workshop Module 4 นี้ **ต้องการ MCP** เพราะ 3 เหตุผล:

### เหตุผล 1: ต้องอ่านข้อมูลจาก GitHub จริง

```
Skills approach:
  ผู้เรียนต้องเปิด GitHub browser แล้ว copy-paste issue ลงใน Claude
  → ไม่สาธิต workflow อัตโนมัติ

MCP approach:
  Claude เรียก github.get_issue(number=1) โดยตรง
  → ผู้เรียนเห็น tool call จริงๆ เข้าใจว่า MCP คืออะไร ✅
```

### เหตุผล 2: ต้องสร้าง PR จริงบน GitHub

```
Skills + Bash:
  ต้องติดตั้ง gh CLI ในเครื่องผู้เรียนทุกคน
  → เสียเวลา setup, ผู้เรียนอาจ OS ต่างกัน

MCP:
  ผ่าน GITHUB_TOKEN เดียว ทุก OS ทำงานได้เหมือนกัน ✅
```

### เหตุผล 3: Workshop สอนเรื่อง MCP โดยตรง

```
จุดประสงค์ของ Module 4 คือทำให้ผู้เรียนเข้าใจว่า:
  "MCP = Claude ต่อ external system ได้โดยตรง"

ถ้าใช้ Skills + Bash แทน MCP → ผู้เรียนไม่เห็น MCP ทำงานจริง
การใช้ GitHub MCP ทำให้ผู้เรียนเห็น tool call ชัดๆ ใน UI ✅
```

### สรุป Decision Matrix ของ Workshop นี้

| ความต้องการ | Skills | MCP | เลือก |
|------------|--------|-----|-------|
| อ่าน issue จาก GitHub live | ผ่าน `` !`gh issue view` `` (ต้องมี gh CLI) | ✅ โดยตรง | **MCP** |
| สร้าง PR บน GitHub | ผ่าน `` !`gh pr create` `` (ต้องมี gh CLI) | ✅ โดยตรง | **MCP** |
| บอก Claude ว่าต้องทำอะไร | ✅ CLAUDE.md | ❌ | **CLAUDE.md** (ไม่ใช่ Skills เพราะเป็น project-wide context) |
| สอน coding convention | ✅ CLAUDE.md | ❌ | **CLAUDE.md** |

---

## 6. Quick Reference

```
ถามตัวเองว่า...

"Claude ต้องรู้อะไร หรือทำตาม workflow อะไร?"
→ Skills หรือ CLAUDE.md

"Claude ต้องดึงข้อมูล หรือเปลี่ยน state ใน external system?"
→ MCP

"ต้องการทั้งสอง?"
→ Skills บอก Claude ว่าใช้ MCP tool ไหน + MCP ให้ tool นั้น
```
