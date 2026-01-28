#!/bin/bash
# Debug Statement Detection Hook
# Runs PostToolUse to warn about console.log/print statements left in code
#
# This hook checks edited/written files for common debug statements
# and provides a warning if found.

set -e

# Get the file that was just modified from environment
FILE_PATH="${CLAUDE_TOOL_ARG_file_path:-}"

# Exit if no file path
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Exit if file doesn't exist (might have been deleted)
if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Get file extension
EXT="${FILE_PATH##*.}"

# Define patterns based on file type
case "$EXT" in
    js|jsx|ts|tsx|mjs|cjs)
        PATTERNS=(
            "console\.log\("
            "console\.debug\("
            "console\.info\("
            "console\.warn\("
            "console\.error\("
            "debugger"
        )
        ;;
    py)
        PATTERNS=(
            "print\("
            "breakpoint\(\)"
            "pdb\.set_trace\(\)"
            "import pdb"
            "import ipdb"
        )
        ;;
    rb)
        PATTERNS=(
            "puts "
            "p "
            "pp "
            "binding\.pry"
            "byebug"
        )
        ;;
    go)
        PATTERNS=(
            "fmt\.Print"
            "log\.Print"
            "fmt\.Sprintf.*debug"
        )
        ;;
    rs)
        PATTERNS=(
            "println!\("
            "dbg!\("
            "eprintln!\("
        )
        ;;
    *)
        # Unknown file type, skip check
        exit 0
        ;;
esac

# Check for debug statements
FOUND_DEBUG=0
FOUND_LINES=""

for pattern in "${PATTERNS[@]}"; do
    # Use grep with extended regex to find matches, capture line numbers
    MATCHES=$(grep -En "$pattern" "$FILE_PATH" 2>/dev/null || true)
    if [ -n "$MATCHES" ]; then
        FOUND_DEBUG=1
        FOUND_LINES="${FOUND_LINES}${MATCHES}\n"
    fi
done

# If debug statements found, output warning (but don't block)
if [ "$FOUND_DEBUG" -eq 1 ]; then
    echo "WARNING: Debug statements detected in $FILE_PATH:"
    echo -e "$FOUND_LINES" | head -10
    echo ""
    echo "Consider removing debug statements before committing."
    echo "Run '/quickfix' to auto-clean or manually remove."
fi

# Always exit 0 (warning only, don't block)
exit 0
