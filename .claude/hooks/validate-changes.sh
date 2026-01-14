#!/bin/bash
# PreToolUse hook: Validate changes before commit operations
# Exit code 2 blocks the operation
#
# Usage: Add to .claude/settings.json hooks.PreToolUse
# {
#   "matcher": "Bash",
#   "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-changes.sh"}]
# }

set -e

# Read input JSON from stdin
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only validate git commit commands
if ! echo "$COMMAND" | grep -q "git commit"; then
    exit 0
fi

# Get project root
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR"

ERRORS=0
WARNINGS=0

echo "=== Pre-commit Validation ===" >&2

# Detect project type and run appropriate checks
# Python project
if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
    echo "Checking Python project..." >&2

    # Ruff check (if available)
    if command -v ruff &> /dev/null; then
        if ! ruff check . --quiet 2>/dev/null; then
            echo "❌ Ruff found linting errors" >&2
            ERRORS=$((ERRORS + 1))
        else
            echo "✓ Ruff check passed" >&2
        fi
    fi

    # MyPy check (if available and configured)
    if command -v mypy &> /dev/null && [ -f "pyproject.toml" ]; then
        if grep -q "\[tool.mypy\]" pyproject.toml 2>/dev/null; then
            if ! mypy . --quiet 2>/dev/null; then
                echo "⚠ MyPy found type errors" >&2
                WARNINGS=$((WARNINGS + 1))
            else
                echo "✓ MyPy check passed" >&2
            fi
        fi
    fi
fi

# JavaScript/TypeScript project
if [ -f "package.json" ]; then
    echo "Checking JavaScript/TypeScript project..." >&2

    # ESLint check
    if command -v npx &> /dev/null && [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] || [ -f "eslint.config.js" ]; then
        if ! npx eslint . --quiet 2>/dev/null; then
            echo "❌ ESLint found errors" >&2
            ERRORS=$((ERRORS + 1))
        else
            echo "✓ ESLint check passed" >&2
        fi
    fi

    # TypeScript check
    if [ -f "tsconfig.json" ]; then
        if command -v npx &> /dev/null; then
            if ! npx tsc --noEmit 2>/dev/null; then
                echo "❌ TypeScript found errors" >&2
                ERRORS=$((ERRORS + 1))
            else
                echo "✓ TypeScript check passed" >&2
            fi
        fi
    fi
fi

# Rust project
if [ -f "Cargo.toml" ]; then
    echo "Checking Rust project..." >&2

    # Clippy check
    if command -v cargo &> /dev/null; then
        if ! cargo clippy --quiet -- -D warnings 2>/dev/null; then
            echo "❌ Clippy found warnings/errors" >&2
            ERRORS=$((ERRORS + 1))
        else
            echo "✓ Clippy check passed" >&2
        fi
    fi
fi

# Go project
if [ -f "go.mod" ]; then
    echo "Checking Go project..." >&2

    # Go vet
    if command -v go &> /dev/null; then
        if ! go vet ./... 2>/dev/null; then
            echo "❌ Go vet found issues" >&2
            ERRORS=$((ERRORS + 1))
        else
            echo "✓ Go vet passed" >&2
        fi
    fi

    # Golangci-lint
    if command -v golangci-lint &> /dev/null; then
        if ! golangci-lint run --quiet 2>/dev/null; then
            echo "⚠ Golangci-lint found issues" >&2
            WARNINGS=$((WARNINGS + 1))
        else
            echo "✓ Golangci-lint passed" >&2
        fi
    fi
fi

echo "=== Validation Complete ===" >&2
echo "Errors: $ERRORS, Warnings: $WARNINGS" >&2

# Block commit if errors found
if [ $ERRORS -gt 0 ]; then
    echo "❌ Commit blocked: Fix $ERRORS error(s) first" >&2
    exit 2
fi

# Allow commit with warnings
if [ $WARNINGS -gt 0 ]; then
    echo "⚠ Proceeding with $WARNINGS warning(s)" >&2
fi

exit 0
