---
allowed-tools: Read, Glob, Grep, Bash(git log:*), Bash(git blame:*), Bash(git show:*), Bash(git diff:*)
description: Investigate an issue or error with full context
argument-hint: [issue-description]
context: fork
agent: Explore
---

# /investigate - Deep Issue Investigation

## Pre-computed Context

Recent commits:
!`git log --oneline -20 2>/dev/null || echo "Not a git repo"`

Recent changes summary:
!`git diff HEAD~10 --stat 2>/dev/null | tail -20 || echo ""`

Open issues from tracker:
@docs/02_issues.md

Current task context:
@docs/01_progress.md

## Task

Investigate: **$ARGUMENTS**

### Investigation Process

#### Phase 1: Understand the Issue
- Parse the error message or issue description
- Identify key terms, file names, function names
- Note any stack traces or error codes

#### Phase 2: Gather Context
- Search for relevant files using Glob
- Search for relevant code using Grep
- Read key files identified
- Check git history for recent changes to relevant areas

#### Phase 3: Timeline Analysis
- When did this issue start? (git bisect mentally)
- What changed recently? (git log, git diff)
- Who touched relevant files? (git blame)

#### Phase 4: Root Cause Hypothesis
- Form 1-3 hypotheses about the root cause
- For each hypothesis:
  - Evidence supporting it
  - Evidence against it
  - How to verify

#### Phase 5: Verification
- Identify steps to confirm the root cause
- Note any additional information needed

### Output Format

```
## Investigation Report: [Issue Title]

### Issue Summary
[Brief description of the issue]

### Key Findings

#### Relevant Files
| File | Relevance |
|------|-----------|
| path/to/file.py:123 | Contains the error |
| path/to/other.py:45 | Calls the failing function |

#### Timeline
- [date]: [relevant change or event]
- [date]: [relevant change or event]

#### Code Analysis
[Key code snippets with line numbers]

### Root Cause Analysis

#### Hypothesis 1: [Description]
- **Evidence For**: [list]
- **Evidence Against**: [list]
- **Confidence**: High/Medium/Low

#### Hypothesis 2: [Description]
- **Evidence For**: [list]
- **Evidence Against**: [list]
- **Confidence**: High/Medium/Low

### Recommended Next Steps
1. [Action item]
2. [Action item]
3. [Action item]

### Questions for User
- [Any clarifying questions]
```

### Search Patterns to Use

For error messages:
```
Grep: "error text" or "ExceptionName"
```

For function names:
```
Grep: "def function_name" or "function function_name"
```

For class names:
```
Grep: "class ClassName"
```

For recent changes:
```bash
git log -p --since="1 week ago" -- path/to/file
git blame path/to/file
```
