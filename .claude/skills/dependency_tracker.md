# SKILL: Dependency Tracking

**Purpose**: Track external dependencies, validate compatibility, perform security audits, and monitor for outdated packages.

---

## Trigger Conditions

Use this skill when:
1. User runs `/status` command (show dependency status)
2. Before adding new dependencies
3. After modifying dependency files (requirements.txt, package.json, etc.)
4. Periodically during long sessions
5. User asks about dependency issues
6. Before `/save` checkpoint (quick security check)

---

## Core Logic

### 1. Dependency Detection

**Supported Manifests**:

| Language | Primary Files | Lock Files |
|----------|--------------|------------|
| Python | requirements.txt, pyproject.toml, setup.py, Pipfile | Pipfile.lock, poetry.lock |
| JavaScript | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml |
| Rust | Cargo.toml | Cargo.lock |
| Go | go.mod | go.sum |

**Detection Flow**:
```text
1. Scan project root for manifest files
2. Identify primary language/framework
3. Parse direct dependencies
4. Map to lock file for exact versions
5. Build dependency tree (direct + transitive)
6. Cache for session
```

### 2. Dependency Change Tracking

**Monitor for Changes**:
```text
On session start:
1. Snapshot current dependencies
2. Hash manifest files

During session:
1. Detect manifest modifications
2. Compare to snapshot
3. Identify added/removed/updated

On change detected:
1. Validate new dependencies
2. Security scan
3. Compatibility check
4. Report findings
```

**Change Report Format**:
```text
DEPENDENCY CHANGES DETECTED
════════════════════════════════════════

File Modified: package.json

## Added
+ lodash@4.17.21
+ axios@1.6.0

## Removed
- request@2.88.2 (deprecated)

## Updated
~ express: 4.18.0 → 4.19.0 (minor)

## Validation
- lodash@4.17.21: ✓ Clean
- axios@1.6.0: ✓ Clean
- express@4.19.0: ✓ Clean

All changes validated.
════════════════════════════════════════
```

### 3. Security Audit

**Audit Commands by Language**:
```text
Python:
  pip-audit
  safety check -r requirements.txt

JavaScript:
  npm audit --json
  yarn audit --json

Rust:
  cargo audit

Go:
  govulncheck ./...
```

**Audit Report Format**:
```text
SECURITY AUDIT REPORT
════════════════════════════════════════

Scan Time: [timestamp]
Packages Scanned: [N] direct, [M] transitive

## Vulnerabilities Found

### CRITICAL (Must Fix)

CVE-2024-XXXXX: SQL Injection in [package]
- Package: sqlparse@0.4.2
- Severity: CRITICAL (CVSS 9.8)
- Fixed In: 0.4.4
- Details: Improper input validation allows SQL injection
- Action: Upgrade to sqlparse>=0.4.4

### HIGH (Should Fix)

CVE-2024-YYYYY: XSS in [package]
...

### MEDIUM (Review)
...

### LOW (Informational)
...

## Summary
| Severity | Count | Auto-Fixable |
|----------|-------|--------------|
| Critical | 1 | Yes |
| High | 2 | Yes |
| Medium | 0 | - |
| Low | 3 | No |

## Recommendations
1. Run: pip install --upgrade sqlparse
2. Run: npm audit fix
3. Review low-severity issues

Auto-fix available for 3 vulnerabilities. Apply?
════════════════════════════════════════
```

### 4. Compatibility Validation

**Before Adding Dependency**:
```text
DEPENDENCY CHECK: [package-name]
════════════════════════════════════════

Package: [package]@[requested-version]
Latest: [latest-version]

## Compatibility Analysis

Runtime Compatibility:
- Python version: 3.11 → [COMPATIBLE | INCOMPATIBLE]
- Node version: 20.x → [COMPATIBLE | INCOMPATIBLE]

Dependency Conflicts:
- [existing-pkg] requires [dep]<2.0
- [new-pkg] requires [dep]>=2.5
- CONFLICT: Version ranges incompatible

Peer Dependencies:
- Requires: react>=18.0 → [SATISFIED | MISSING]

## License Analysis

License: MIT
Project License: MIT
Compatibility: [COMPATIBLE | REVIEW NEEDED | INCOMPATIBLE]

## Security Check

Known Vulnerabilities: [None | N issues]
Last Published: [date]
Maintainer Activity: [Active | Inactive | Abandoned]
Downloads/Week: [N]

## Recommendation

[SAFE TO ADD | CAUTION | DO NOT ADD]

Reason: [explanation]
════════════════════════════════════════
```

### 5. Outdated Package Tracking

**Check Commands**:
```text
Python:
  pip list --outdated --format=json

JavaScript:
  npm outdated --json

Rust:
  cargo outdated --format json

Go:
  go list -m -u all
```

**Outdated Report**:
```text
OUTDATED PACKAGES REPORT
════════════════════════════════════════

## Major Updates (Breaking Changes Likely)
| Package | Current | Latest | Age |
|---------|---------|--------|-----|
| django | 3.2.0 | 5.0.0 | 2 years |
| react | 17.0.2 | 18.2.0 | 1 year |

## Minor Updates (New Features)
| Package | Current | Latest |
|---------|---------|--------|
| requests | 2.28.0 | 2.31.0 |
| lodash | 4.17.20 | 4.17.21 |

## Patch Updates (Bug Fixes)
| Package | Current | Latest |
|---------|---------|--------|
| pytest | 7.4.0 | 7.4.3 |

## Summary
- Major: 2 (review carefully)
- Minor: 5 (generally safe)
- Patch: 8 (recommended)

## Recommendations
1. Apply patch updates: Low risk, bug fixes
2. Review minor updates: Check changelogs
3. Plan major updates: May require code changes

Update patch versions now?
════════════════════════════════════════
```

### 6. License Compliance

**Allowed Licenses** (configurable):
```text
Default allowed:
- MIT
- Apache-2.0
- BSD-2-Clause
- BSD-3-Clause
- ISC
- Unlicense

Review required:
- GPL-2.0
- GPL-3.0
- LGPL-*
- MPL-*

Typically forbidden:
- AGPL-*
- Proprietary
- Unknown
```

**License Report**:
```text
LICENSE COMPLIANCE
════════════════════════════════════════

## License Distribution
| License | Count | Packages |
|---------|-------|----------|
| MIT | 45 | lodash, express, ... |
| Apache-2.0 | 12 | ... |
| BSD-3 | 8 | ... |

## Review Required
| Package | License | Reason |
|---------|---------|--------|
| some-pkg | GPL-3.0 | Copyleft license |

## Unknown Licenses
- custom-pkg (no license file)

## Compliance Status
[COMPLIANT | REVIEW NEEDED | NON-COMPLIANT]
════════════════════════════════════════
```

---

## Integration with Protocol v3.0

**State Updates**:
- Log dependency changes to `docs/logs/session_context.md`
- Add security vulnerabilities to `docs/02_issues.md`
- Reference in `/status` dashboard

**Decision Authority**:
- `docs/04_standards.md` may specify:
  - Required dependencies
  - Forbidden dependencies
  - Allowed licenses
- Always check standards before adding dependencies

**Mandatory Loop Integration**:
- STATE CHECK: Read current dependency state
- ALIGN: Verify dependency changes relate to task
- EXECUTE: Validate and report
- COMMIT: Log findings

---

## Automation Rules

### Auto-Check (No Permission)
```text
✓ Detect dependency file changes
✓ Parse and diff dependencies
✓ Cache security scan results
✓ Report findings in output
```

### Ask Permission Before
```text
? Installing new packages
? Updating existing packages
? Applying security fixes
? Removing dependencies
```

### Alert Immediately
```text
! Critical security vulnerability found
! License compliance violation
! Major breaking update available
! Abandoned/deprecated package detected
```

### Block Operations
```text
✗ Adding package with critical vulnerability
✗ Adding package with incompatible license
✗ Downgrading to vulnerable version
```

---

## Quality Gates

**Before Adding Dependency**:
- [ ] Package exists and is actively maintained
- [ ] No known critical vulnerabilities
- [ ] Compatible with existing dependencies
- [ ] License compatible with project
- [ ] Documented in appropriate manifest

**Before /save Checkpoint**:
- [ ] No new critical vulnerabilities introduced
- [ ] Lock files in sync with manifests
- [ ] All dependency changes documented

**Before /done Task Completion**:
- [ ] Any new dependencies justified
- [ ] Security audit passed
- [ ] License compliance verified

---

## Configuration

**Default Settings** (in `.claude/settings.local.json`):
```json
{
  "dependencies": {
    "autoAudit": true,
    "auditOnStart": true,
    "blockCriticalVulnerabilities": true,
    "allowedLicenses": ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"],
    "warnOnOutdated": true,
    "outdatedThreshold": {
      "major": "warn",
      "minor": "info",
      "patch": "auto"
    }
  }
}
```

---

## See Also

- Status command: `/status`
- Standards: `docs/04_standards.md`
- Issues: `docs/02_issues.md`
- Session logs: `docs/logs/session_context.md`
