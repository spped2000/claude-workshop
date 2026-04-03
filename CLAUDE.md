# Claude Workshop — MCP, Skills & Large Project Best Practices

## Overview

This repository contains hands-on workshops for learning Claude Code workflows.

## Modules

### Module 4: MCP & External Integrations (60 min)
GitHub Issue → Implement → Test → PR — all from a single Claude Code prompt.
See `PARTICIPANT_GUIDE.md` for the step-by-step lab guide.

### Module 5: Large Project Best Practices (100-115 min)
Worktrees, token optimization, multi-issue workflows, PR reviews, Skills deep dive.
See `module-5-large-projects/WORKSHOP.md` for the standalone workshop.
Reference: https://claude.com/blog/skills-explained

## Repository Structure

```
workshop-project/              ← Base FastAPI project (shared by both modules)
github-issues/                 ← Issue templates (reference copies of #1–#7)
instructor-demo/               ← Module 4 live demo script
module-5-large-projects/       ← Module 5 workshop materials
  ├── WORKSHOP.md              ← Main workshop (standalone)
  ├── BUILDING_BLOCKS.md       ← 5 Building Blocks handout
  ├── INSTRUCTOR_NOTES.md      ← Instructor timing & notes
  └── skills/explore-issue/    ← context:fork exploration skill
```

## Open GitHub Issues

This repo has 7 open issues — one per group:

| Group | Issue | Feature |
|-------|-------|---------|
| 1 | #1 | Add health check endpoint |
| 2 | #2 | Add request logging middleware |
| 3 | #3 | Add input validation for POST /users |
| 4 | #4 | Add soft delete for users |
| 5 | #5 | Add search endpoint GET /users/search |
| 6 | #6 | Add CORS configuration |
| 7 | #7 | Add response compression |

## MCP Setup

See `workshop-project/CLAUDE.md` for the canonical MCP server configuration.
