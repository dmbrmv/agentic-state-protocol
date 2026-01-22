# Debug Statement Check Hook

## Purpose

Detects debug statements (console.log, print, etc.) left in code after edits. Provides warnings to help keep code clean before commits.

## Trigger

- **Event**: PostToolUse
- **Matcher**: Edit, Write
- **Behavior**: Warning only (non-blocking)

## Detected Patterns

### JavaScript/TypeScript
- `console.log()`
- `console.debug()`
- `console.info()`
- `console.warn()`
- `console.error()`
- `debugger`

### Python
- `print()`
- `breakpoint()`
- `pdb.set_trace()`
- `import pdb`
- `import ipdb`

### Ruby
- `puts`
- `p`
- `pp`
- `binding.pry`
- `byebug`

### Go
- `fmt.Print*`
- `log.Print*`

### Rust
- `println!()`
- `dbg!()`
- `eprintln!()`

## Configuration

Hook is configured in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/debug-statement-check.sh"
          }
        ]
      }
    ]
  }
}
```

## Output Example

```
WARNING: Debug statements detected in src/utils.ts:
45: console.log('debugging value:', value)
67: console.log(result)

Consider removing debug statements before committing.
Run '/quickfix' to auto-clean or manually remove.
```

## Notes

- This hook provides warnings only, it does not block operations
- Use `/quickfix` or `/precommit` to clean up before committing
- Legitimate logging should use proper logging frameworks, not debug statements
- The hook respects file extensions and only checks relevant files
