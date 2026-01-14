---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(gh pr:*), Bash(git branch:*), Bash(git log:*), Bash(git diff:*)
description: Quick commit, push, and create PR workflow
argument-hint: [commit-message]
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

Recent commits (for message style):
!`git log --oneline -5`

Remote tracking:
!`git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null || echo "No upstream configured"`

## Task

Based on the above context, execute the quick git workflow:

### Step 1: Analyze Changes
- Review the staged and unstaged changes
- If no changes staged, add all changes with `git add -A`
- If specific files should be excluded, note them

### Step 2: Create Commit
Use the provided message: **$ARGUMENTS**

If no message provided, generate one based on:
- The changes shown above
- Recent commit message style
- Conventional commits format (feat:, fix:, docs:, refactor:, etc.)

Create commit:
```bash
git commit -m "<message>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 3: Push to Remote
- Push to the current branch's upstream
- If no upstream, push with `-u origin <branch>`

```bash
git push -u origin $(git branch --show-current)
```

### Step 4: Create PR (if on feature branch)
If current branch is NOT main/master/develop:
- Create a pull request using `gh pr create`
- Use the commit message as PR title
- Generate a brief PR description

```bash
gh pr create --title "<title>" --body "<description>"
```

### Output
Report:
- Commit SHA
- Files changed
- Branch pushed to
- PR URL (if created)
