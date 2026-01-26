---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(gh pr:*), Bash(git branch:*), Bash(git log:*), Bash(git diff:*)
description: Quick commit, push, and create PR workflow with selective staging
argument-hint: [commit-message] [--all | --staged | file1 file2 ...]
---

# /commit-push-pr - Quick Git Workflow

## Pre-computed Context

Current branch:
!`git branch --show-current`

Git status:
!`git status --short`

Staged changes:
!`git diff --cached --stat`

Unstaged changes:
!`git diff --stat`

Untracked files:
!`git ls-files --others --exclude-standard | head -20`

Recent commits (for message style):
!`git log --oneline -5`

Remote tracking:
!`git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null || echo "No upstream configured"`

---

## CRITICAL: Selective Staging

**NEVER use `git add -A` or `git add .` by default.**

This command supports three staging modes:

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Selective** (default) | No flag | Show changes, ask user which files to include |
| **Staged only** | `--staged` | Only commit already-staged changes |
| **All changes** | `--all` | Stage everything (explicit opt-in only) |

### Why This Matters

When working with multiple Claude instances or on multiple topics:
- `git add -A` blends unrelated changes into one commit
- Results in messy, unfocused commit history
- Makes code review and bisecting harder
- Can accidentally commit work-in-progress from other tasks

---

## Task

Parse arguments: **$ARGUMENTS**

### Step 1: Determine Staging Mode

**If `--all` flag present:**
- User explicitly wants all changes
- Proceed with `git add -A`
- Skip to Step 2

**If `--staged` flag present:**
- Only commit what's already staged
- Do NOT add any new files
- Skip to Step 2

**If specific files listed:**
- Stage only those files: `git add <file1> <file2> ...`
- Skip to Step 2

**If no flag and nothing staged (DEFAULT):**
- Present the changes to the user
- Ask which files to include using `AskUserQuestion`:

```
Which changes should be included in this commit?

Changes detected:
- Modified: src/api/users.py
- Modified: src/models/user.py
- New file: tests/test_users.py
- Modified: docs/README.md (unrelated?)

Options:
1. All changes shown above
2. Only src/ changes (exclude docs/)
3. Let me specify files
4. Cancel - I'll stage manually
```

**If nothing staged and user selects files:**
- Stage only the selected files
- Proceed to Step 2

---

### Step 2: Verify Staged Changes

Show what will be committed:
```bash
git diff --cached --stat
```

If nothing staged after Step 1:
- Report "No changes to commit"
- Exit without error

---

### Step 3: Create Commit

**Commit message source (in priority order):**
1. Message provided in arguments (after removing flags)
2. Auto-generate based on staged changes

**Auto-generate rules:**
- Use conventional commits format (feat:, fix:, docs:, refactor:, test:, chore:)
- Match recent commit message style from the repo
- Keep first line under 72 characters
- Focus on the "why" not just the "what"

**Commit command:**
```bash
git commit -m "$(cat <<'EOF'
<type>: <description>

<optional body if changes are significant>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

### Step 4: Push to Remote

Check if push is needed:
```bash
git status -sb  # Shows ahead/behind status
```

Push with upstream tracking:
```bash
git push -u origin $(git branch --show-current)
```

---

### Step 5: Create PR (if applicable)

**Create PR only if:**
- Current branch is NOT main/master/develop
- No existing PR for this branch

**Check for existing PR:**
```bash
gh pr view --json number 2>/dev/null || echo "No existing PR"
```

**If no existing PR, create one:**
```bash
gh pr create --title "<commit title>" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points based on commits>

## Changes
<files changed summary>

---
🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

**If PR already exists:**
- Report the existing PR URL
- Do not create duplicate

---

## Output Summary

Report the following:
```
✓ Commit: <sha> - <message>
✓ Files:  <count> files changed
✓ Branch: <branch> → origin/<branch>
✓ PR:     <url> (or "PR already exists: <url>" or "Not on feature branch")
```

---

## Examples

### Commit only staged changes
```
/commit-push-pr --staged "fix: resolve user validation bug"
```

### Commit specific files
```
/commit-push-pr src/api/users.py src/models/user.py "feat: add user export endpoint"
```

### Commit all changes (explicit)
```
/commit-push-pr --all "chore: weekly cleanup"
```

### Interactive selection (default)
```
/commit-push-pr "feat: improve search performance"
```
→ Agent shows changes, asks which files to include

---

## Safety Rails

1. **NEVER auto-stage with `-A` unless `--all` flag is explicit**
2. **NEVER force push** - if push fails, report error and stop
3. **NEVER commit sensitive files** - check for .env, credentials, secrets
4. **ALWAYS show what will be committed** before committing
5. **ALWAYS use HEREDOC** for commit messages to preserve formatting

### Files to Never Commit (warn and exclude)
- `.env`, `.env.*`
- `*credentials*`, `*secret*`
- `*.pem`, `*.key`
- `node_modules/`, `__pycache__/`, `.venv/`
- Large binary files (>10MB)
