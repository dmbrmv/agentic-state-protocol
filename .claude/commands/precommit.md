---
allowed-tools: Bash(ruff:*), Bash(pytest:*), Bash(npm:*), Bash(npx:*), Bash(cargo:*), Bash(go:*), Bash(mypy:*), Bash(pyright:*), Bash(git diff:*), Bash(git status:*)
description: Run all pre-commit checks (lint, format, test, typecheck)
---

# /precommit - Comprehensive Pre-Commit Validation

## Pre-computed Context

Modified files:
!`git diff --name-only HEAD 2>/dev/null | head -30`

Staged files:
!`git diff --cached --name-only 2>/dev/null | head -30`

Current branch:
!`git branch --show-current`

Project files:
!`ls -la pyproject.toml package.json Cargo.toml go.mod tsconfig.json .eslintrc* 2>/dev/null | head -10 || echo "Unknown"`

## Task

Run comprehensive pre-commit validation. **Do NOT auto-fix**, just report status.

### Check Categories

Run all applicable checks for the detected project type:

#### 1. Format Check (no modifications)
- Python: `ruff format --check .`
- JavaScript: `npx prettier --check .`
- Rust: `cargo fmt --check`
- Go: `gofmt -l .`

#### 2. Lint Check
- Python: `ruff check .`
- JavaScript: `npx eslint .`
- Rust: `cargo clippy -- -D warnings`
- Go: `golangci-lint run`

#### 3. Type Check
- Python: `mypy .` or `pyright`
- TypeScript: `npx tsc --noEmit`
- Rust: (included in cargo build)
- Go: (included in go build)

#### 4. Test Check (affected tests only if possible)
- Python: `pytest -x --tb=short`
- JavaScript: `npm test`
- Rust: `cargo test`
- Go: `go test ./...`

### Execution Order

1. Format check (fastest)
2. Lint check
3. Type check
4. Test check (slowest)

Stop early if critical failures found.

### Output Format

```
## Pre-Commit Check Results

| Check | Status | Details |
|-------|--------|---------|
| Format | ✓/✗ | [details] |
| Lint | ✓/✗ | [details] |
| Types | ✓/✗ | [details] |
| Tests | ✓/✗ | [X/Y passed] |

### Summary
- Total Checks: 4
- Passed: X
- Failed: Y

### Verdict
[READY TO COMMIT | NEEDS FIXES | BLOCKED]

### Required Fixes
[If any checks failed, list specific fixes needed]
```

### Quick Reference

If all checks pass:
```
✓ Format | ✓ Lint | ✓ Types | ✓ Tests → READY TO COMMIT
```

If fixes needed:
```
✓ Format | ✗ Lint | ✓ Types | ✓ Tests → Run /quickfix then retry
```
