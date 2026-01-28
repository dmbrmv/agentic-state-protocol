---
description: Run verification in background and notify when complete
context: fork
agent: background-verifier
---

# /verify-background - Background Verification

## Pre-computed Context

Project type:
!`ls pyproject.toml package.json Cargo.toml go.mod 2>/dev/null | head -1 || echo "unknown"`

Current branch:
!`git branch --show-current 2>/dev/null || echo "not a git repo"`

Recent changes:
!`git diff --stat HEAD~5 2>/dev/null | tail -10 || echo ""`

## Task

Run comprehensive verification **in the background** using the `background-verifier` agent.

This allows you to continue working while verification runs.

### Verification Pipeline

The background verifier will execute:

1. **Environment Check** (~5s)
   - Verify tools installed
   - Check dependencies

2. **Build Verification** (~1-5m)
   - Clean build from scratch
   - Record warnings

3. **Test Execution** (~5-30m)
   - Full test suite
   - Coverage report

4. **Code Quality** (~1-3m)
   - Linting (all files)
   - Type checking
   - Complexity analysis

5. **Security Scan** (~1-2m)
   - Dependency audit
   - Secret detection

### Progress Checkpoints

The agent will output progress like:
```
[CHECKPOINT] Stage 2/5: Build Verification
- Status: IN_PROGRESS
- Duration: 1m 30s
```

### Final Report

When complete, you'll receive:
```
## Background Verification Complete

- Duration: 15m 30s
- Status: PASS/FAIL

| Stage | Status | Duration |
|-------|--------|----------|
| Environment | PASS | 5s |
| Build | PASS | 2m |
| Tests | PASS | 10m |
| Quality | WARN | 2m |
| Security | PASS | 1m |

Recommendation: MERGE READY / NEEDS ATTENTION
```

### How to Check Progress

While running, you can:
1. Continue working on other tasks
2. Check the agent's output file for progress
3. Wait for the completion notification

### When to Use

- Before merging large PRs
- After major refactoring
- Before releases
- When you want thorough verification but need to keep working
