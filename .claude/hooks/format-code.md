# HOOK: format-code.sh

**Type**: PostToolUse
**Trigger**: Edit, Write operations
**Purpose**: Auto-format code after file modifications

## Description

Automatically formats code files after Write or Edit tool operations. Detects file type by extension and applies the appropriate formatter if available.

## Supported Languages

| Extension | Primary Formatter | Fallback |
|-----------|-------------------|----------|
| `.py` | ruff format + check --fix | black |
| `.js`, `.jsx`, `.ts`, `.tsx` | prettier | npx prettier |
| `.json`, `.md`, `.mdx` | prettier | npx prettier |
| `.yaml`, `.yml` | prettier | npx prettier |
| `.css`, `.scss`, `.html` | prettier | npx prettier |
| `.rs` | rustfmt | - |
| `.go` | gofmt + goimports | - |
| `.sh`, `.bash` | shfmt | - |
| `.toml` | taplo | - |

## Configuration

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

## Behavior

1. Reads file path from stdin JSON (`tool_input.file_path`)
2. Exits silently if file doesn't exist
3. Detects language from file extension
4. Applies formatter if available on system
5. Errors are suppressed (always exits 0)

## Requirements

- jq (for JSON parsing)
- Formatters must be installed separately (ruff, prettier, rustfmt, etc.)

## See Also

- `markdown-formatter.py` - Markdown-specific formatting
- `validate-changes.sh` - Pre-commit validation
- `/quickfix` command - Manual lint fix
