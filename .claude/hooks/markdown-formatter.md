# HOOK: markdown-formatter.py

**Type**: PostToolUse
**Trigger**: Edit, Write operations on `.md`, `.mdx`, `.markdown` files
**Purpose**: Fix markdown formatting issues automatically

## Description

Python script that post-processes markdown files to ensure consistent formatting:
- Adds language tags to unlabeled code blocks (auto-detection)
- Fixes excessive blank lines (max 2 consecutive)
- Removes trailing whitespace
- Ensures single newline at end of file

## Language Detection

Auto-detects programming language for unlabeled code blocks:

| Language | Detection Patterns |
|----------|-------------------|
| Python | `def`, `class`, `import`, `from`, `if __name__` |
| JavaScript | `function`, `const`, `let`, `var`, `=>` |
| TypeScript | JS patterns + type annotations (`: string`, `<T>`) |
| JSON | Starts with `{` or `[`, valid JSON parse |
| YAML | `---`, key-value patterns |
| Bash/Shell | Shebang, `if/then/fi`, `$VAR`, `&&`, `\|\|` |
| SQL | `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE` |
| Rust | `fn`, `let`, `mut`, `impl`, `struct`, `enum` |
| Go | `func`, `package`, `type`, `interface`, `chan` |
| HTML | Standard HTML tags |
| CSS | Selector patterns with `{}` |
| XML | `<?xml`, namespaced tags |
| Dockerfile | `FROM`, `RUN`, `CMD`, `COPY`, `ENV` |
| TOML | `[section]` headers with `key = value` |
| Makefile | Target patterns with tab indentation |

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
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/markdown-formatter.py"
          }
        ]
      }
    ]
  }
}
```

## Behavior

1. Reads file path from stdin JSON (`tool_input.file_path`)
2. Only processes `.md`, `.mdx`, `.markdown` files
3. Exits silently for other file types
4. Reads file, applies formatting, writes back if changed
5. Logs formatted files to stderr

## Requirements

- Python 3.10+
- No external dependencies (uses only stdlib)

## See Also

- `format-code.sh` - General code formatting
- `docs/04_standards.md` - Documentation standards
