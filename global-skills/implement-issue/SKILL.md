---
name: implement-issue
description: Read a GitHub issue via MCP, implement the feature following project conventions, write tests, and open a PR. Works with any GitHub repository.
argument-hint: [issue-number]
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash
---

# Implement Issue #$0

## Step 1 — Understand the Project

Read these files before doing anything else:
- `CLAUDE.md` (if present) — conventions, MCP servers, project structure
- `README.md` — tech stack, run commands, test instructions
- `pyproject.toml` or `package.json` — dependencies and scripts

Detect the current repo name:
- !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || git remote get-url origin 2>/dev/null || echo "unknown"`

## Step 2 — Read the Issue via GitHub MCP

Use the GitHub MCP to read issue #$0 from the repo detected in Step 1.
Summarize the acceptance criteria as a numbered checklist before proceeding.

If MCP is unavailable:
```
claude mcp list
claude mcp add github -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github
```

## Step 3 — Implement

Follow conventions from CLAUDE.md or README found in Step 1.
If no CLAUDE.md exists, infer conventions from the existing codebase:
- Read existing source files to understand patterns in use
- Match the code style of the file you are editing
- Do not modify logic unrelated to this issue
- Add new dependencies through the project's package manager

## Step 4 — Write Tests

Find the existing test pattern in the project and follow it.
Create a new test file separate from existing tests.
Run the full test suite — all tests including pre-existing ones must pass.

Detect test command:
- !`cat pyproject.toml 2>/dev/null | grep -A2 '\[tool.pytest' | head -5 || cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('npm test:', d.get('scripts',{}).get('test','not found'))" 2>/dev/null || echo "Check README for test command"`

## Step 5 — Commit and Create a PR

Create branch: `feat/issue-$0-<short-description>`
Commit only files related to this issue.

Create a PR via GitHub MCP:
- **Title**: match the issue title exactly
- **Body**:
  ```
  ## What was implemented
  <bullet points of changes made>

  ## Tests added
  <test file name and number of tests>

  Closes #$0
  ```

Display the PR URL when complete.
