#!/bin/bash
# PostToolUse hook: Auto-format code after Write/Edit operations
# Reads JSON from stdin with tool_input.file_path
#
# Usage: Add to .claude/settings.json hooks.PostToolUse
# {
#   "matcher": "Edit|Write",
#   "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh"}]
# }

set -e

# Read input JSON from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Exit if no file path or file doesn't exist
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Get file extension
EXT="${FILE_PATH##*.}"

# Format based on extension
case "$EXT" in
    # Python files
    py)
        if command -v ruff &> /dev/null; then
            ruff format "$FILE_PATH" 2>/dev/null || true
            ruff check --fix "$FILE_PATH" 2>/dev/null || true
        elif command -v black &> /dev/null; then
            black -q "$FILE_PATH" 2>/dev/null || true
        fi
        ;;

    # Shell scripts
    sh|bash)
        if command -v shfmt &> /dev/null; then
            shfmt -w "$FILE_PATH" 2>/dev/null || true
        fi
        ;;

    # TOML files
    toml)
        if command -v taplo &> /dev/null; then
            taplo format "$FILE_PATH" 2>/dev/null || true
        fi
        ;;

    # Config and documentation files (JSON, YAML, Markdown)
    json|yaml|yml|md)
        if command -v prettier &> /dev/null; then
            prettier --write "$FILE_PATH" 2>/dev/null || true
        elif command -v npx &> /dev/null; then
            npx prettier --write "$FILE_PATH" 2>/dev/null || true
        fi
        ;;
esac

exit 0
