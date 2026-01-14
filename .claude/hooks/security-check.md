# HOOK: security-check.sh

**Type**: PreToolUse
**Trigger**: Write, Edit, Bash operations
**Purpose**: Block dangerous operations on sensitive files

## Description

Security gate that prevents modifications to sensitive files and blocks dangerous shell commands. Returns exit code 2 to block operations.

## File Protection

### Blocked File Patterns

| Pattern | Description |
|---------|-------------|
| `.env`, `.env.*` | Environment files with secrets |
| `credentials`, `secrets` | Credential storage files |
| `*.pem`, `*.key`, `*.crt` | SSL/TLS certificates and keys |
| `*.p12`, `*.pfx` | PKCS#12 certificate archives |
| `id_rsa`, `id_ed25519`, `id_ecdsa` | SSH private keys |
| `.aws/credentials` | AWS credentials file |
| `.ssh/config` | SSH configuration |
| `.netrc`, `.npmrc`, `.pypirc` | Package manager auth files |
| `.docker/config` | Docker credentials |
| `password`, `api_key`, `auth_token` | Generic sensitive patterns |

### Protected Directories

| Path | Reason |
|------|--------|
| `/etc/`, `/usr/`, `/var/`, `/bin/`, `/sbin/` | System directories |
| `/root/` | Root user directory |
| `node_modules/`, `__pycache__/` | Dependency caches |
| `.venv/`, `venv/` | Virtual environments |
| `target/debug/`, `target/release/` | Rust build artifacts |
| `.git/` | Git internal directory |

## Command Protection

### Blocked Commands (Exit 2)

| Pattern | Description |
|---------|-------------|
| `rm -rf /`, `rm -rf ~`, `rm -rf *` | Destructive deletions |
| `mkfs.*`, `dd if=` | Disk operations |
| `curl \| sh`, `wget \| bash` | Remote code execution |
| `git push --force`, `git push -f` | Force push to remote |
| `git reset --hard origin` | Hard reset to remote |
| `DROP DATABASE`, `DROP TABLE` | Database destruction |
| Fork bombs | Process exhaustion attacks |

### Warnings Only (Exit 0)

| Pattern | Note |
|---------|------|
| `sudo` commands | Elevated privileges warning |
| `pip install`, `npm install`, etc. | Package installation info |

## Configuration

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-check.sh"
          }
        ]
      }
    ]
  }
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Operation allowed |
| 2 | Operation blocked |

## Requirements

- jq (for JSON parsing)
- grep with extended regex support

## See Also

- `validate-changes.sh` - Pre-commit validation
- `.claude/skills/arch_enforcer.md` - Architecture enforcement
- `docs/04_standards.md` - Security standards
