#!/usr/bin/env python3
"""
PostToolUse hook: Fix markdown formatting issues.

- Adds language tags to unlabeled code blocks
- Fixes excessive blank lines
- Ensures consistent formatting

Usage: Add to .claude/settings.json hooks.PostToolUse
{
    "matcher": "Edit|Write",
    "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/markdown-formatter.py"}]
}
"""

import json
import sys
import re
import os
from pathlib import Path


def detect_language(code: str) -> str:
    """Detect programming language from code content."""
    s = code.strip()

    if not s:
        return "text"

    # JSON detection (try parsing)
    if re.search(r'^\s*[{\[]', s):
        try:
            json.loads(s)
            return 'json'
        except (json.JSONDecodeError, ValueError):
            pass

    # YAML detection
    if re.search(r'^---\s*$', s, re.MULTILINE) or re.search(r'^\w+:\s*[|\->]?\s*$', s, re.MULTILINE):
        return 'yaml'

    # Python
    if re.search(r'^\s*(def|class|import|from|async def|@\w+)\s+', s, re.MULTILINE):
        return 'python'
    if re.search(r'^\s*(if __name__|print\(|self\.|elif|except|raise|with\s+)', s, re.MULTILINE):
        return 'python'

    # Bash/Shell
    if re.search(r'^#!.*\b(bash|sh|zsh)\b', s, re.MULTILINE):
        return 'bash'
    if re.search(r'^\s*(if|then|fi|for|do|done|case|esac|while|until)\b', s, re.MULTILINE):
        return 'bash'
    if re.search(r'\$\{?\w+\}?|\$\(|&&|\|\||<<|>>', s):
        return 'bash'

    # SQL
    if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|FROM|WHERE|JOIN)\s+', s, re.IGNORECASE):
        return 'sql'

    # HTML
    if re.search(r'<(!DOCTYPE|html|head|body|div|span|p|a|img|script|style)\b', s, re.IGNORECASE):
        return 'html'

    # CSS
    if re.search(r'^\s*[.#]?\w+\s*\{[^}]*\}', s, re.MULTILINE):
        return 'css'

    # XML
    if re.search(r'<\?xml|<[a-z]+:[a-z]+', s, re.IGNORECASE):
        return 'xml'

    # Dockerfile
    if re.search(r'^(FROM|RUN|CMD|COPY|ADD|ENV|EXPOSE|WORKDIR)\s+', s, re.MULTILINE):
        return 'dockerfile'

    # TOML
    if re.search(r'^\s*\[\w+\]', s, re.MULTILINE) and re.search(r'^\s*\w+\s*=', s, re.MULTILINE):
        return 'toml'

    # Makefile
    if re.search(r'^[a-zA-Z_]+\s*:', s, re.MULTILINE) and re.search(r'^\t', s, re.MULTILINE):
        return 'makefile'

    # Default
    return 'text'


def format_markdown(content: str) -> str:
    """Format markdown content."""

    # Fix unlabeled code fences
    def add_language_tag(match):
        indent = match.group(1)
        info = match.group(2)
        body = match.group(3)
        closing = match.group(4)

        # If no language specified, detect it
        if not info.strip():
            lang = detect_language(body)
            return f"{indent}```{lang}\n{body}{closing}\n"
        return match.group(0)

    # Pattern for code blocks: captures indent, info string, body, closing
    # Matches:
    #   ```           <- opening fence with optional indent
    #   content       <- body
    #   ```           <- closing fence with matching indent
    pattern = r'(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$'
    content = re.sub(pattern, add_language_tag, content)

    # Fix excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # Fix trailing whitespace on lines
    content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

    # Ensure single newline at end of file
    content = content.rstrip() + '\n'

    return content


def main():
    """Main entry point."""
    try:
        # Read input JSON from stdin
        input_data = json.load(sys.stdin)
        file_path = input_data.get('tool_input', {}).get('file_path', '')

        # Only process markdown files
        if not file_path or not file_path.endswith(('.md', '.mdx', '.markdown')):
            sys.exit(0)

        # Check if file exists
        if not os.path.exists(file_path):
            sys.exit(0)

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Format content
        formatted = format_markdown(content)

        # Write back if changed
        if formatted != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"Formatted: {file_path}", file=sys.stderr)

    except json.JSONDecodeError:
        # Invalid JSON input, skip silently
        pass
    except Exception as e:
        # Log error but don't fail
        print(f"Markdown formatter error: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == '__main__':
    main()
