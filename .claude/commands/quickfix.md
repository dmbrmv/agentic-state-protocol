---
allowed-tools: Bash(ruff:*), Bash(npm run:*), Bash(npx:*), Bash(cargo:*), Bash(go:*), Bash(gofmt:*), Bash(prettier:*), Bash(black:*), Bash(git diff:*)
description: Run linters with auto-fix on modified files
---

# /quickfix - Auto-Fix Linting Issues

## Pre-computed Context

Modified files (not staged):
!`git diff --name-only HEAD 2>/dev/null || echo "Not a git repo"`

Staged files:
!`git diff --cached --name-only 2>/dev/null || echo ""`

All changed files:
!`git diff --name-only HEAD 2>/dev/null | head -20`

File types changed:
!`git diff --name-only HEAD 2>/dev/null | sed 's/.*\.//' | sort -u`

Project type detection:
!`ls -la pyproject.toml package.json Cargo.toml go.mod 2>/dev/null | head -5 || echo "Unknown project type"`

## Task

Run appropriate linter with **auto-fix** on all modified files.

### Python Project (pyproject.toml, requirements.txt, setup.py)

```bash
# Format with ruff
ruff format .

# Fix linting issues
ruff check --fix .

# Alternative: black + isort
black .
isort .
```

### JavaScript/TypeScript Project (package.json)

```bash
# ESLint with auto-fix
npx eslint --fix .

# Prettier formatting
npx prettier --write .

# If npm scripts exist
npm run lint:fix 2>/dev/null || npm run lint -- --fix 2>/dev/null || true
npm run format 2>/dev/null || true
```

### Rust Project (Cargo.toml)

```bash
# Format code
cargo fmt

# Fix clippy warnings (where possible)
cargo clippy --fix --allow-dirty --allow-staged
```

### Go Project (go.mod)

```bash
# Format code
gofmt -w .

# Fix imports
goimports -w .

# Run go mod tidy
go mod tidy
```

### Execution Strategy

1. Detect project type from context above
2. Run the appropriate formatters/linters
3. Only process **changed files** when possible for speed
4. Report what was fixed

### Output Format

```
## Quickfix Results

### Files Processed
- [list of files]

### Fixes Applied
- [formatter/linter]: [count] fixes
- [formatter/linter]: [count] fixes

### Remaining Issues
- [any issues that couldn't be auto-fixed]

### Next Steps
- [suggestions if manual fixes needed]
```
