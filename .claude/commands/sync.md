---
description: "Merge work from parallel agent sessions with review and validation."
---

# COMMAND: SYNC

**Trigger**: User types `/sync` or `/sync --status`

## Purpose
Review, validate, and merge work from delegated parallel agents back into the main context. Ensures human supervision at merge points, conflict detection, and verification through testing.

## Actions

1. **Read Delegation State**:
   - `docs/logs/delegation_registry.md` (active session, agent statuses)
   - Check Task tool for agent outputs

2. **Check for Active Session**:
   ```
   SYNC CHECK
   ════════════════════════════════════════

   Active Delegation Session: [Yes/No]

   If No:
   - No active delegation session found
   - Use /delegate to start a new session
   ```

3. **Generate Status Report**:
   ```
   SYNC STATUS REPORT
   ════════════════════════════════════════

   Session ID: DEL-[timestamp]
   Parent Task: [task name]
   Started: [timestamp]
   Duration: [elapsed time]

   ## Agent Status Overview

   | Agent | Subtask | Status | Files Changed | Tests |
   |-------|---------|--------|---------------|-------|
   | AGT-001 | [name] | COMPLETE | 3 | PASS |
   | AGT-002 | [name] | COMPLETE | 2 | PASS |
   | AGT-003 | [name] | RUNNING | - | - |

   ## Summary
   - Total Agents: 3
   - Complete: 2
   - Running: 1
   - Failed: 0

   ## Ready to Merge
   - AGT-001: [subtask 1]
   - AGT-002: [subtask 2]

   ## Still Running
   - AGT-003: [subtask 3] (estimated: [time remaining])

   ## Conflicts Detected
   [List of file conflicts between agents, or "None"]

   ════════════════════════════════════════

   Options:
   > /sync --merge AGT-001    → Review and merge specific agent
   > /sync --merge-all        → Review and merge all complete agents
   > /sync --wait             → Wait for running agents
   > /sync --abort            → Cancel delegation session
   ```

4. **Review Phase** (for each agent being merged):
   ```
   REVIEWING: AGT-001
   ════════════════════════════════════════

   Subtask: [subtask name]
   Status: COMPLETE

   ## Changes Made by Agent

   | File | Action | Lines |
   |------|--------|-------|
   | src/module/file1.py | modified | +42, -10 |
   | src/module/file2.py | modified | +15, -5 |
   | tests/test_module.py | created | +38 |

   ## Code Diff Preview

   ### src/module/file1.py
   ```diff
   @@ -10,5 +10,8 @@
    def existing_function():
   -    old_code
   +    new_improved_code
   +    with_additional_logic
   ```

   [Additional diffs...]

   ## Agent's Test Results
   - Tests Run: Yes
   - Result: PASS (5/5)
   - Coverage: 85%

   ## Automated Review (via /review logic)

   Architecture: [PASS | VIOLATIONS]
   Standards: [PASS | VIOLATIONS]
   Security: [CLEAN | ISSUES]

   Issues Found: [N or None]
   [List any issues if found]

   ## Conflict Check

   Files also modified by other agents: [None | list]
   Potential merge conflicts: [None | list]

   ════════════════════════════════════════

   Approve merge of AGT-001?
   > [yes] Merge these changes
   > [no] Reject and discard
   > [review] See full diff details
   > [fix] Request modifications before merge
   ```

5. **Merge Execution** (on approval):
   ```
   MERGING: AGT-001
   ════════════════════════════════════════

   Applying changes from AGT-001...

   ✓ src/module/file1.py - merged
   ✓ src/module/file2.py - merged
   ✓ tests/test_module.py - merged

   Running verification tests...

   ✓ Tests: PASS (all affected tests)

   Merge Status: SUCCESS

   ════════════════════════════════════════
   ```

6. **Conflict Resolution** (if conflicts detected):
   ```
   CONFLICT DETECTED
   ════════════════════════════════════════

   File: src/shared/utils.py

   Modified by:
   - AGT-001: Lines 20-35
   - AGT-002: Lines 25-40

   ## AGT-001's Version
   ```python
   def helper():
       return "version A"
   ```

   ## AGT-002's Version
   ```python
   def helper():
       return "version B"
   ```

   Resolution Options:
   > [1] Keep AGT-001's version
   > [2] Keep AGT-002's version
   > [3] Manual merge (I'll help combine them)
   > [4] Skip this file (resolve later)

   ════════════════════════════════════════
   ```

7. **Post-Merge Actions**:
   ```
   POST-MERGE VERIFICATION
   ════════════════════════════════════════

   Running full test suite...
   Result: [PASS | FAIL]

   If FAIL:
   - Failed tests: [list]
   - Likely cause: [analysis]
   - Options:
     > Rollback last merge
     > Investigate and fix
     > Continue anyway (not recommended)

   ════════════════════════════════════════
   ```

8. **Session Completion**:
   ```
   DELEGATION SESSION COMPLETE
   ════════════════════════════════════════

   Session ID: DEL-[timestamp]
   Duration: [total time]

   ## Merge Summary

   | Agent | Subtask | Status | Merged |
   |-------|---------|--------|--------|
   | AGT-001 | [name] | COMPLETE | ✓ |
   | AGT-002 | [name] | COMPLETE | ✓ |
   | AGT-003 | [name] | COMPLETE | ✓ |

   ## Results
   - Subtasks Completed: 3/3
   - Files Modified: 12
   - Tests: PASS
   - Conflicts Resolved: 1

   ## Updated Documentation
   - docs/01_progress.md: Updated with completed subtasks
   - docs/logs/session_context.md: Logged merge session
   - docs/logs/delegation_registry.md: Session archived

   ════════════════════════════════════════

   Parent task progress: [X%] → [Y%]

   Next: Continue with remaining work or /done if complete
   ```

9. **Update Documentation**:
   - Update `docs/01_progress.md`:
     - Mark completed subtasks
     - Update progress percentage
   - Log to `docs/logs/session_context.md`:
     ```
     ### Delegation Sync: [timestamp]
     - Session: DEL-[id]
     - Agents Merged: [N]
     - Files Changed: [M]
     - Conflicts: [P resolved]
     - Tests: PASS/FAIL
     ```
   - Archive session in `docs/logs/delegation_registry.md`

## Sync Options

| Option | Description |
|--------|-------------|
| `/sync` | Full sync workflow (status + merge prompts) |
| `/sync --status` | Status check only, no merge |
| `/sync --merge <agent>` | Merge specific agent |
| `/sync --merge-all` | Merge all complete agents |
| `/sync --wait` | Wait for running agents to complete |
| `/sync --abort` | Cancel entire delegation session |
| `/sync --rollback <agent>` | Undo a merged agent's changes |

## Merge Requirements

Before merging an agent:
- [ ] Agent status is COMPLETE
- [ ] Agent's tests passed
- [ ] No blocking conflicts with other agents
- [ ] Automated review passed (no critical issues)
- [ ] Human approved the merge

## Integration with Protocol v3.0

This command follows the mandatory loop:
1. **STATE CHECK**: Read delegation registry and agent outputs
2. **ALIGN**: Verify merges relate to parent task
3. **EXECUTE**: Apply approved merges with verification
4. **COMMIT**: Update progress tracker and session context

Integrates with:
- `parallel_coordinator.md` skill for lifecycle
- `/review` command logic for automated review
- `/test` command logic for verification

## Safety Rails

- **ALWAYS** require human approval for each merge
- **ALWAYS** run tests after merging
- **ALWAYS** check for conflicts before merging
- **NEVER** auto-merge without review
- **NEVER** merge agents with failed tests (unless explicitly approved)
- **PROVIDE** rollback capability for merged changes
- **ARCHIVE** all delegation sessions for audit

## Error Handling

### Agent Timeout
```
AGENT TIMEOUT: AGT-XXX

Agent did not complete within time limit.

Options:
> [1] Wait longer (extend timeout)
> [2] Retrieve partial work
> [3] Mark as failed and continue
> [4] Abort entire session
```

### Merge Failure
```
MERGE FAILED: AGT-XXX

Error: [error details]

Options:
> [1] Retry merge
> [2] Skip this agent
> [3] Rollback and investigate
> [4] Abort session
```

### Test Failure After Merge
```
POST-MERGE TESTS FAILED

Merged Agent: AGT-XXX
Failed Tests: [list]

Options:
> [1] Rollback this merge
> [2] Investigate and fix
> [3] Continue (mark issue for later)
```

## See Also

- Delegate command: `/delegate`
- Skill: `parallel_coordinator.md`
- Delegation registry: `docs/logs/delegation_registry.md`
- Review command: `/review`
- Test command: `/test`
