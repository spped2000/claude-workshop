---
name: explore-issue
description: Research a GitHub issue and summarize findings without polluting main context. Use when you want to understand an issue before implementing.
argument-hint: [issue-number]
context: fork
agent: Explore
allowed-tools: Read Glob Grep
---

# Explore Issue #$0

## Step 1 — Detect Repository

- !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || git remote get-url origin 2>/dev/null || echo "unknown"`

## Step 2 — Read the Issue

Use the GitHub MCP to read issue #$0 from the repository detected above.
If MCP is unavailable, fall back to: `gh issue view $0 --json title,body,labels`

## Step 3 — Analyze Codebase Impact

Find all files that need to change to implement issue #$0:
- Search for relevant functions, models, routes, and tests
- Check CLAUDE.md for project structure and conventions
- Identify dependencies that may need to be added

## Step 4 — Return Summary

Return a concise report:

```
Issue #$0: <title>

Files to modify:
  - <file path> → <what needs to change and why>
  - ...

New files to create:
  - <file path> → <purpose>

Dependencies to add:
  - <package> (if any)

Key considerations:
  - <gotchas, ordering issues, breaking changes>
```

Do NOT make any edits. This is a read-only exploration.
