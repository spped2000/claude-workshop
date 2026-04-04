# Global Skills — ใช้ได้ทุก Project

Skills เหล่านี้ออกแบบมาให้ทำงานได้กับ **ทุก GitHub repository** โดยไม่ต้อง config เพิ่ม

##  วิธีติดตั้ง

```bash 
# macOS / Linux
mkdir -p ~/.claude/skills/implement-issue
cp global-skills/implement-issue/SKILL.md ~/.claude/skills/implement-issue/

# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\.claude\skills\implement-issue"
Copy-Item "global-skills\implement-issue\SKILL.md" "$HOME\.claude\skills\implement-issue\"
```

ตรวจสอบ:
```bash
claude  # เปิด Claude Code แล้วพิมพ์
/implement-issue 42
```

## ความแตกต่าง: Global vs Project Skill

| | Global (`~/.claude/skills/`) | Project (`.claude/skills/`) |
|---|---|---|
| ใช้ได้กับ | ทุก project ทุก repo | เฉพาะ project นั้น |
| Repo name | Auto-detect จาก `gh` / `git remote` | Hardcode ใน skill |
| Conventions | อ่านจาก CLAUDE.md / README ของแต่ละ project | ระบุเฉพาะเจาะจง |
| Test command | Auto-detect จาก pyproject.toml / package.json | ระบุตรงๆ เช่น `uv run pytest` |
| เหมาะกับ | workflow ที่ใช้ซ้ำข้าม project | workshop / team ที่ใช้ stack เดียวกัน |

## Skills ที่มี

### `/implement-issue <N>`

อ่าน GitHub issue → implement → test → PR ใน project ที่เปิดอยู่

**ต้องมี:**
- GitHub MCP (`claude mcp add github -e GITHUB_TOKEN=... -- npx -y @modelcontextprotocol/server-github`)
- `GITHUB_TOKEN` ที่มีสิทธิ์ `repo`

**ตัวอย่าง:**
```
/implement-issue 42
/implement-issue 101
```
