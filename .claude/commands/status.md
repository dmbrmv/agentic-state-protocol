---
description: "Project health dashboard: git state, tests, docs, dependencies."
---

# COMMAND: STATUS

**Trigger**: User types `/status` or "STATUS"

## Purpose
Quick read-only dashboard showing project health at a glance. Aggregates information from git, tests, documentation sync status, and dependency health without modifying any state.

## Actions

1. **Read Project State**:
   - `docs/01_progress.md` (active task, progress)
   - `docs/02_issues.md` (open issues count by severity)
   - `docs/logs/session_context.md` (last checkpoint)

2. **Gather System Status**:
   - Git: branch, uncommitted changes, ahead/behind remote
   - Tests: last run results (if cached)
   - Dependencies: outdated packages, vulnerabilities
   - Documentation: sync status with code

3. **Generate Dashboard**:
   ```
   PROJECT HEALTH DASHBOARD
   ══════════════════════════════════════════════════════════════

   ## Task Status
   ┌─────────────────────────────────────────────────────────────┐
   │ Current Goal: [from docs/01_progress.md]                    │
   │ Active Task:  [from docs/01_progress.md]                    │
   │ Progress:     [████████░░░░░░░░░░░░] 40%                    │
   │ Mode:         [Execution | Planning | Refactoring]          │
   └─────────────────────────────────────────────────────────────┘

   ## Git Status
   ┌─────────────────────────────────────────────────────────────┐
   │ Branch:       [current-branch]                              │
   │ Remote:       [ahead by N | behind by M | up to date]       │
   │ Uncommitted:  [N files modified, M files staged]            │
   │ Last Commit:  [hash] [message] ([time ago])                 │
   └─────────────────────────────────────────────────────────────┘

   ## Test Status
   ┌─────────────────────────────────────────────────────────────┐
   │ Last Run:     [timestamp] [PASS | FAIL]                     │
   │ Results:      [X passed, Y failed, Z skipped]               │
   │ Coverage:     [XX% | Not tracked]                           │
   │ Failed Tests: [list or "None"]                              │
   └─────────────────────────────────────────────────────────────┘

   ## Documentation Status
   ┌─────────────────────────────────────────────────────────────┐
   │ docs/01_progress.md:    [synced | outdated | unknown]       │
   │ docs/03_architecture.md:[synced | outdated | unknown]       │
   │ docs/04_standards.md:   [synced | no changes needed]        │
   │ Last Checkpoint:        [timestamp from session_context]    │
   └─────────────────────────────────────────────────────────────┘

   ## Dependency Status
   ┌─────────────────────────────────────────────────────────────┐
   │ Outdated:     [N packages need updates]                     │
   │ Security:     [CLEAN | N vulnerabilities found]             │
   │ Lock File:    [synced | out of sync]                        │
   └─────────────────────────────────────────────────────────────┘

   ## Open Issues
   ┌─────────────────────────────────────────────────────────────┐
   │ Critical: [N]  High: [M]  Medium: [P]  Low: [Q]             │
   │ Total: [sum] issues                                         │
   │ Oldest Unresolved: [ISSUE-XXX] ([age])                      │
   └─────────────────────────────────────────────────────────────┘

   ══════════════════════════════════════════════════════════════

   ## Quick Actions
   • Uncommitted changes? → /save to checkpoint
   • Tests failing? → /test --failed to investigate
   • Docs outdated? → Update docs or /save
   • Dependencies outdated? → Review and update
   • Issues pending? → /debug --issue <id>

   ══════════════════════════════════════════════════════════════
   ```

4. **Suggest Actions** (contextual):
   - If uncommitted changes > 0:
     `"Consider: /save to checkpoint your work"`
   - If tests failing:
     `"Consider: /test --failed to investigate failures"`
   - If docs outdated:
     `"Consider: Update docs or run /save to sync"`
   - If critical issues:
     `"Consider: /debug --issue ISSUE-XXX for critical issue"`
   - If dependencies have vulnerabilities:
     `"Consider: Review and update vulnerable dependencies"`

## Status Checks Performed

| Check | Method | Indicators |
|-------|--------|------------|
| Git status | `git status --short` | Modified, staged files |
| Branch info | `git branch -vv` | Ahead/behind tracking |
| Test results | Cached from last `/test` | Pass/fail counts |
| Doc sync | Compare timestamps | Modified after last update |
| Dependencies | `pip-audit`, `npm audit` | Vulnerability count |
| Issues | Parse `docs/02_issues.md` | Count by severity |

## Documentation Sync Detection

Docs considered **outdated** when:
- Source files modified more recently than docs
- Active task changed but progress not updated
- Architecture changes not reflected in docs
- New files created without doc updates

Docs considered **synced** when:
- `docs/logs/session_context.md` has recent checkpoint
- Progress tracker reflects current work
- No structural code changes since last doc update

## Status Options

| Option | Description |
|--------|-------------|
| `/status` | Full dashboard (default) |
| `/status --git` | Git status only |
| `/status --tests` | Test status only |
| `/status --deps` | Dependency status only |
| `/status --issues` | Issue summary only |
| `/status --json` | Machine-readable output |

## Integration with Protocol v3.0

This command is **read-only** and safe to run at any time:
- Does NOT modify any files
- Does NOT update docs
- Does NOT commit changes
- Provides awareness without side effects

Useful as first command in a session (alternative to `/boot` for quick check).

## Health Indicators

| Indicator | Green | Yellow | Red |
|-----------|-------|--------|-----|
| Tests | All pass | Some skip | Any fail |
| Git | Clean/synced | Uncommitted | Conflicts |
| Docs | Synced | Minor drift | Outdated |
| Deps | Clean | Outdated | Vulnerable |
| Issues | 0 critical | Some high | Critical open |

## See Also

- Progress tracker: `docs/01_progress.md`
- Issues: `docs/02_issues.md`
- Boot command: `/boot`
- Save command: `/save`
- Test command: `/test`
