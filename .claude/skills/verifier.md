# SKILL: Verification Workflow

**Purpose**: Ensure Claude verifies its work before marking tasks complete.

---

## Trigger Conditions

Activate this skill when:
- After significant code changes (>3 files modified)
- Before executing `/done` command
- After applying debug fixes
- When user says "verify", "check", "make sure", "test this"
- After completing a feature implementation
- Before creating a pull request

---

## Core Logic

### Verification Decision Tree

```
Start
  │
  ├─ Are there code changes? ─No─→ Skip verification
  │         │
  │        Yes
  │         │
  ├─ How many files changed?
  │         │
  │    ≤3 files → Quick verification (tests only)
  │    >3 files → Full verification
  │         │
  └─ Is this a bug fix? ─Yes─→ Verify fix + regression test
                │
               No
                │
         Standard verification
```

### Verification Checklist

#### Minimal (1-3 files)
- [ ] Run affected tests
- [ ] Quick lint check on changed files

#### Standard (4-10 files)
- [ ] Build succeeds
- [ ] All tests pass
- [ ] Lint check passes
- [ ] Type check passes (if applicable)

#### Full (>10 files or major changes)
- [ ] Clean build from scratch
- [ ] Full test suite
- [ ] All linting rules
- [ ] Type checking
- [ ] Security audit (dependencies)
- [ ] Documentation still accurate

#### Bug Fix Specific
- [ ] Original bug is fixed
- [ ] Related functionality still works
- [ ] No regression in adjacent code
- [ ] Test added to prevent recurrence

---

## Verification Methods by Project Type

### Python Project

```python
# Verification commands
build_check = "pip install -e . || python setup.py develop"
test_run = "pytest -v"
lint_check = "ruff check ."
type_check = "mypy . || pyright"
security_check = "pip-audit"
format_check = "ruff format --check ."
```

### Conda Environment Verification

```python
# Verify conda environment is active and correct
env_check = "conda info --envs"
env_packages = "conda list"
# Verify geospatial dependencies are importable
geo_check = "python -c 'import rasterio; import geopandas; import xarray'"
```

---

## Verification Workflow

### Step 1: Assess Scope

Count changed files:
```bash
git diff --name-only HEAD | wc -l
```

Identify change types:
```bash
git diff --stat HEAD
```

### Step 2: Select Verification Level

| Files Changed | Level | Actions |
|---------------|-------|---------|
| 1-3 | Minimal | Tests for changed files |
| 4-10 | Standard | Build + Tests + Lint |
| 11+ | Full | Everything + Security |

### Step 3: Execute Verification

Run appropriate checks based on level and project type.

### Step 4: Report Results

```
## Verification Results

### Changes Analyzed
- Files modified: X
- Lines added: Y
- Lines removed: Z

### Checks Performed

| Check | Status | Details |
|-------|--------|---------|
| Build | ✓ | No errors |
| Tests | ✓ | 45/45 passed |
| Lint | ✓ | 0 errors |
| Types | ✓ | No issues |

### Verdict
[VERIFIED | NEEDS FIXES | BLOCKED]
```

---

## Integration with Other Commands

### Before `/done`

When user triggers `/done`:
1. Run verification based on change scope
2. If verification fails → Report issues, don't mark done
3. If verification passes → Proceed with done workflow

### With `/commit-push-pr`

Before committing:
1. Run `/precommit` checks
2. If checks fail → Suggest `/quickfix`
3. If checks pass → Proceed with commit

### With `/delegate`

Before spawning agents:
1. Verify base branch is stable
2. After agent completion → Verify merged result

---

## Subagent Integration

For comprehensive verification, spawn the `verify-app` subagent:

```
Task: Run full verification on the current changes
Agent: verify-app
Model: sonnet
```

For background verification:

```
Task: Run complete test suite in background
Agent: background-verifier
Model: haiku
```

---

## Failure Handling

### Test Failures

1. Identify which tests failed
2. Determine if failure is:
   - New (caused by recent changes)
   - Pre-existing (unrelated to changes)
3. If new → Fix before proceeding
4. If pre-existing → Document and continue (with warning)

### Lint/Type Failures

1. Run auto-fix if available (`/quickfix`)
2. If auto-fix resolves → Re-run verification
3. If manual fix needed → Report specific issues

### Build Failures

1. This is a blocker
2. Do not proceed with any workflow
3. Report error details and suggest fixes

---

## Configuration

### Skip Verification

In rare cases, verification can be skipped:
- Documentation-only changes
- Configuration file updates (non-code)
- Explicit user override

### Custom Thresholds

Adjust file count thresholds in settings:
```json
{
  "verification": {
    "minimalThreshold": 3,
    "standardThreshold": 10,
    "alwaysRunSecurity": false
  }
}
```

---

## Examples

### Example 1: Small Bug Fix

```
Changed: 1 file (src/utils.py)

Verification Level: Minimal
Actions:
1. Run: pytest tests/test_utils.py
2. Run: ruff check src/utils.py

Result: VERIFIED (2/2 checks passed)
```

### Example 2: New Feature

```
Changed: 8 files (src/*, tests/*)

Verification Level: Standard
Actions:
1. Run: pip install -e .
2. Run: pytest
3. Run: ruff check .
4. Run: mypy .

Result: NEEDS FIXES (lint found 2 issues)
```

### Example 3: Major Refactor

```
Changed: 25 files across modules

Verification Level: Full
Actions:
1. Clean install
2. Full test suite
3. All linting
4. Type checking
5. Security audit
6. Spawn verify-app agent

Result: VERIFIED (all checks passed)
```
