# HOOK: validate-changes.sh

**Type**: PreToolUse
**Trigger**: Bash operations containing `git commit`
**Purpose**: Validate code quality before commits

## Description

Pre-commit hook that runs linters and type checkers before allowing git commits. Blocks commits if critical errors are found, allows warnings to proceed.

## Validation Checks

### Python Projects

Detected by: `pyproject.toml`, `requirements.txt`, or `setup.py`

| Tool | Check | Severity |
|------|-------|----------|
| ruff | Linting | Error (blocks) |
| mypy | Type checking | Warning (allows) |

## Configuration

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-changes.sh"
          }
        ]
      }
    ]
  }
}
```

## Behavior

1. Only triggers on commands containing `git commit`
2. Detects project type from manifest files
3. Runs appropriate linters/type checkers
4. Counts errors and warnings separately
5. Blocks commit if any errors found (exit 2)
6. Allows commit with warnings (exit 0)

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Commit allowed (possibly with warnings) |
| 2 | Commit blocked (errors found) |

## Requirements

- jq (for JSON parsing)
- Python tools must be installed (ruff, mypy)

## See Also

- `security-check.sh` - Security validation
- `/precommit` command - Manual validation
- `/quickfix` command - Auto-fix linting issues
- `.claude/skills/test_enforcer.md` - Test enforcement
