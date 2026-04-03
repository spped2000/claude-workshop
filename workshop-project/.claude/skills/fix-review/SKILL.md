---
name: fix-review
description: Read PR review comments via GitHub MCP and fix all requested changes. Use when a PR has review feedback to address.
argument-hint: [pr-number]
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Glob Grep
---

# Fix Review Comments for PR #$0

## Step 1 — Read Review Comments

Use GitHub MCP to read all review comments on PR #$0.
List each comment with: file path, line number, and what the reviewer requested.

## Step 2 — Fix

Fix each comment exactly as requested.
Do not refactor or change code that was not mentioned in the review.
Do not add new features or tests beyond what reviewers explicitly asked for.
If a comment is unclear, make the minimal reasonable interpretation.

## Step 3 — Verify

Run the full test suite — all tests must pass.
List every file changed and which review comment it addresses.

## Step 4 — Push

Commit with message: `fix: address PR #$0 review comments`
Push to the existing branch — do not open a new PR.
Report the commit SHA when done.
