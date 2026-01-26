#!/bin/bash
# PreToolUse hook: Block operations on sensitive files and dangerous commands
# Exit code 2 blocks the operation
#
# Usage: Add to .claude/settings.json hooks.PreToolUse
# {
#   "matcher": "Write|Edit|Bash",
#   "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-check.sh"}]
# }

set -e

# Read input JSON from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# === FILE OPERATION CHECKS ===
if [ -n "$FILE_PATH" ]; then
    # Normalize path (remove trailing slashes, resolve . and ..)
    NORMALIZED_PATH=$(realpath -m "$FILE_PATH" 2>/dev/null || echo "$FILE_PATH")

    # Blocked file patterns (case-insensitive matching)
    BLOCKED_FILE_PATTERNS=(
        "\.env$"
        "\.env\."
        "\.env\.local"
        "\.env\.production"
        "\.env\.development"
        "credentials"
        "secrets"
        "\.pem$"
        "\.key$"
        "\.crt$"
        "\.p12$"
        "\.pfx$"
        "id_rsa"
        "id_ed25519"
        "id_ecdsa"
        "\.aws/credentials"
        "\.ssh/config"
        "\.netrc"
        "\.pypirc"
        "\.docker/config"
        "password"
        "api[_-]?key"
        "auth[_-]?token"
        "access[_-]?token"
        "private[_-]?key"
    )

    for pattern in "${BLOCKED_FILE_PATTERNS[@]}"; do
        if echo "$FILE_PATH" | grep -Eqi "$pattern"; then
            echo "🛑 BLOCKED: Cannot modify sensitive file matching pattern '$pattern'" >&2
            echo "   File: $FILE_PATH" >&2
            echo "   Reason: This file may contain secrets or credentials" >&2
            exit 2
        fi
    done

    # Block modifications to system directories
    BLOCKED_DIRECTORIES=(
        "^/etc/"
        "^/usr/"
        "^/var/"
        "^/bin/"
        "^/sbin/"
        "^/root/"
        "^/home/[^/]+/\."  # Hidden files in other users' homes
        "__pycache__/"
        "\.git/"
        "\.venv/"
        "venv/"
    )

    for pattern in "${BLOCKED_DIRECTORIES[@]}"; do
        if echo "$NORMALIZED_PATH" | grep -Eq "$pattern"; then
            echo "🛑 BLOCKED: Cannot modify files in protected directory" >&2
            echo "   Path: $FILE_PATH" >&2
            echo "   Pattern: $pattern" >&2
            exit 2
        fi
    done
fi

# === BASH COMMAND CHECKS ===
if [ -n "$COMMAND" ]; then
    # Dangerous command patterns
    DANGEROUS_PATTERNS=(
        "rm[[:space:]]+-rf[[:space:]]+/"
        "rm[[:space:]]+-rf[[:space:]]+~"
        "rm[[:space:]]+-rf[[:space:]]+\\\$HOME"
        "rm[[:space:]]+-rf[[:space:]]+\*"
        "rm[[:space:]]+-rf[[:space:]]+\.\."
        ">[[:space:]]*/dev/sd"
        ">[[:space:]]*/dev/nvme"
        "mkfs\."
        "dd[[:space:]]+if="
        "chmod[[:space:]]+-R[[:space:]]+777"
        "chmod[[:space:]]+777[[:space:]]+-R"
        "curl.*\|.*sh"
        "curl.*\|.*bash"
        "wget.*\|.*sh"
        "wget.*\|.*bash"
        ":(){:|:&};:"  # Fork bomb
        ">(){ >|>&};>"
        "git[[:space:]]+push[[:space:]]+.*--force"
        "git[[:space:]]+push[[:space:]]+-f"
        "git[[:space:]]+reset[[:space:]]+--hard[[:space:]]+origin"
        "git[[:space:]]+clean[[:space:]]+-fd"
        "DROP[[:space:]]+DATABASE"
        "DROP[[:space:]]+TABLE"
        "TRUNCATE[[:space:]]+TABLE"
        "DELETE[[:space:]]+FROM.*WHERE[[:space:]]+1"
    )

    for pattern in "${DANGEROUS_PATTERNS[@]}"; do
        if echo "$COMMAND" | grep -Eqi "$pattern"; then
            echo "🛑 BLOCKED: Potentially dangerous command detected" >&2
            echo "   Command: $COMMAND" >&2
            echo "   Pattern: $pattern" >&2
            echo "   Reason: This command could cause irreversible damage" >&2
            exit 2
        fi
    done

    # Warn about sudo (but don't block)
    if echo "$COMMAND" | grep -q "sudo"; then
        echo "⚠️  WARNING: Command uses sudo - requires elevated privileges" >&2
        echo "   Command: $COMMAND" >&2
    fi

    # Warn about package installations
    INSTALL_PATTERNS=(
        "pip install"
        "pip3 install"
        "conda install"
        "mamba install"
        "apt install"
        "apt-get install"
        "brew install"
    )

    for pattern in "${INSTALL_PATTERNS[@]}"; do
        if echo "$COMMAND" | grep -qi "$pattern"; then
            echo "ℹ️  INFO: Package installation detected" >&2
            echo "   Command: $COMMAND" >&2
            echo "   Note: Ensure you trust the packages being installed" >&2
            break
        fi
    done
fi

# All checks passed
exit 0
