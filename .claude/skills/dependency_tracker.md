# SKILL: Dependency Tracking

**Purpose**: Track external dependencies, validate compatibility, perform security audits, and monitor for outdated packages.

---

## Trigger Conditions

Use this skill when:
1. User runs `/status` command (show dependency status)
2. Before adding new dependencies
3. After modifying dependency files (pyproject.toml, requirements.txt, environment.yml)
4. Periodically during long sessions
5. User asks about dependency issues
6. Before `/save` checkpoint (quick security check)

---

## Core Logic

### 1. Dependency Detection

**Supported Manifests**:

| Language | Primary Files | Lock Files |
|----------|--------------|------------|
| Python (pip) | requirements.txt, pyproject.toml, setup.py, Pipfile | Pipfile.lock, poetry.lock |
| Python (conda) | environment.yml, conda-env.yml | conda-lock.yml |

**Detection Flow**:
```text
1. Scan project root for manifest files
2. Check for conda environment.yml first (preferred for scientific Python)
3. Fall back to pyproject.toml / requirements.txt
4. Parse direct dependencies
5. Map to lock file for exact versions
6. Build dependency tree (direct + transitive)
7. Cache for session
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

File Modified: pyproject.toml

## Added
+ xarray==2024.1.0
+ netCDF4==1.6.5

## Removed
- deprecated-pkg==1.0.0

## Updated
~ numpy: 1.26.0 → 1.26.4 (patch)
~ pandas: 2.1.0 → 2.2.0 (minor)

## Validation
- xarray==2024.1.0: ✓ Clean
- netCDF4==1.6.5: ✓ Clean
- numpy==1.26.4: ✓ Clean

All changes validated.
════════════════════════════════════════
```

### 3. Security Audit

**Audit Commands**:
```text
Python (pip):
  pip-audit
  safety check -r requirements.txt

Python (conda):
  # No direct conda audit tool; check pip packages within conda env
  pip-audit --desc
  # Check for known CVEs in conda packages
  conda list --json | python -c "import sys,json; [print(f'{p[\"name\"]}=={p[\"version\"]}') for p in json.load(sys.stdin)]" | safety check --stdin
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
2. Review low-severity issues

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

Dependency Conflicts:
- [existing-pkg] requires [dep]<2.0
- [new-pkg] requires [dep]>=2.5
- CONFLICT: Version ranges incompatible

## Conda/Pip Ecosystem Checks

GDAL Version Conflicts:
- System GDAL: [version]
- rasterio requires: GDAL [version range]
- fiona requires: GDAL [version range]
- Status: [COMPATIBLE | CONFLICT]

NumPy ABI Compatibility:
- Installed numpy: [version]
- Package compiled against: numpy [version]
- Status: [COMPATIBLE | ABI MISMATCH]
  NOTE: numpy ABI breaks between major versions (1.x vs 2.x)
  Packages compiled against numpy 1.x may segfault with numpy 2.x

Conda vs Pip Mixing:
- Package available via conda-forge: [YES | NO]
- Recommendation: [Install via conda | pip is safe | WARNING: prefer conda]
  NOTE: Mixing conda and pip for packages with C extensions (numpy, scipy,
  gdal, rasterio, fiona, shapely, pyproj) frequently causes ABI conflicts.
  Always prefer conda-forge for these packages.

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
Python (pip):
  pip list --outdated --format=json

Python (conda):
  conda update --dry-run --all --json 2>/dev/null
  # Or compare installed vs latest
  conda search --outdated --json
```

**Outdated Report**:
```text
OUTDATED PACKAGES REPORT
════════════════════════════════════════

## Major Updates (Breaking Changes Likely)
| Package | Current | Latest | Age |
|---------|---------|--------|-----|
| numpy | 1.26.4 | 2.1.0 | 6 months |
| pandas | 2.1.0 | 2.2.0 | 3 months |

## Minor Updates (New Features)
| Package | Current | Latest |
|---------|---------|--------|
| xarray | 2024.1.0 | 2024.6.0 |
| rasterio | 1.3.9 | 1.3.10 |

## Patch Updates (Bug Fixes)
| Package | Current | Latest |
|---------|---------|--------|
| pytest | 7.4.0 | 7.4.3 |

## Summary
- Major: 2 (review carefully -- especially numpy 1.x→2.x ABI break)
- Minor: 5 (generally safe)
- Patch: 8 (recommended)

## Recommendations
1. Apply patch updates: Low risk, bug fixes
2. Review minor updates: Check changelogs
3. Plan major updates: May require code changes and recompilation of C extensions

## Conda-Specific Notes
- Before major numpy update: Check that all C-extension packages have
  conda-forge builds for the new numpy version
- Use `conda update --dry-run <pkg>` to preview dependency resolution
- Never `pip install --upgrade numpy` in a conda environment

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
| MIT | 25 | numpy, pandas, ... |
| BSD-3 | 15 | scipy, scikit-learn, ... |
| Apache-2.0 | 8 | ... |

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
? Switching package from pip to conda or vice versa
```

### Alert Immediately
```text
! Critical security vulnerability found
! License compliance violation
! Major breaking update available
! Abandoned/deprecated package detected
! NumPy ABI incompatibility detected
! Conda/pip conflict detected
```

### Block Operations
```text
✗ Adding package with critical vulnerability
✗ Adding package with incompatible license
✗ Downgrading to vulnerable version
✗ pip install of C-extension package in conda env without checking conda-forge first
```

---

## Quality Gates

**Before Adding Dependency**:
- [ ] Package exists and is actively maintained
- [ ] No known critical vulnerabilities
- [ ] Compatible with existing dependencies
- [ ] License compatible with project
- [ ] Documented in appropriate manifest
- [ ] Available via conda-forge (preferred for scientific packages with C extensions)

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
    },
    "preferConda": true,
    "condaChannels": ["conda-forge", "defaults"]
  }
}
```

---

## See Also

- Status command: `/status`
- Standards: `docs/04_standards.md`
- Issues: `docs/02_issues.md`
- Session logs: `docs/logs/session_context.md`
