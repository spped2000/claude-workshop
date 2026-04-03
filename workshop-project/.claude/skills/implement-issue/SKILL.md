---
name: implement-issue
description: Read a GitHub issue via MCP, implement the feature, write tests in a separate file, and open a PR. Use when given an issue number to work on.
argument-hint: [issue-number]
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash
---

# Implement Issue #$0

## Step 1 — Read the Issue via GitHub MCP

Use the GitHub MCP to read issue #$0 from repo spped2000/claude-workshop.
Display the acceptance criteria as a numbered checklist before proceeding.
If MCP is unresponsive, ask the user to run `claude mcp list` to verify the connection.

## Step 2 — Implement

Read CLAUDE.md first to understand the project structure and conventions.
Then implement all acceptance criteria:

- Use `async def` for all route handlers
- Edit the correct file as described in the project structure (main.py or routers/users.py)
- Do not modify logic unrelated to this issue
- If a new dependency is required, run `uv add <package>` and commit pyproject.toml

## Step 3 — Write Tests

Create a new file `tests/test_<feature_name>.py` — do not modify test_users.py.
Write tests covering every acceptance criteria in the issue.
Run `uv run pytest -v` — all tests including the original 9 must pass.
Fix any failures before moving to the next step.

## Step 4 — Create a PR via GitHub MCP

Use the GitHub MCP to create a pull request:
- **Branch**: create `feat/issue-$0-<short-description>` before committing
- **Title**: match the issue title exactly
- **Body**: describe what was implemented and include "Closes #$0" at the end

Display the PR URL when complete.
