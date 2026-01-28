---
description: "Spawn parallel Claude Task agents for subtasks with supervised autonomy."
---

# COMMAND: DELEGATE

**Trigger**: User types `/delegate <task>` or `/delegate`

## Purpose
Break complex tasks into parallelizable subtasks and spawn Claude Task agents to work on them concurrently. Maintains supervised autonomy through explicit boundaries, checkpoints, and human-approved merging.

## Actions

1. **Read Delegation Context**:
   - `docs/01_progress.md` (active task for context)
   - `docs/03_architecture.md` (understand boundaries)
   - `docs/logs/delegation_registry.md` (check for active sessions)

2. **Check for Existing Session**:
   ```
   DELEGATION CHECK
   ════════════════════════════════════════

   Active Delegation Session: [Yes/No]

   If Yes:
   - Session ID: [id]
   - Started: [timestamp]
   - Agents: [N running, M complete]
   - Use /sync to manage existing session
   ```

3. **Task Decomposition**:
   If `<task>` not provided, analyze active task from `docs/01_progress.md`.

   ```
   DELEGATION ANALYSIS
   ════════════════════════════════════════

   Main Task: [task name or description]

   ## Parallelization Analysis

   Can this task be parallelized? [Yes/No/Partially]

   Reasoning:
   - [Why parallelizable or not]
   - [Dependencies between subtasks]
   - [Shared resources or conflicts]

   ## Proposed Subtasks

   ### Subtask 1: [name]
   - Description: [what this subtask accomplishes]
   - Scope: [files/modules this agent can modify]
   - Estimated Complexity: [Low | Medium | High]
   - Dependencies: [None | depends on subtask N]

   ### Subtask 2: [name]
   - Description: [what this subtask accomplishes]
   - Scope: [files/modules this agent can modify]
   - Estimated Complexity: [Low | Medium | High]
   - Dependencies: [None | depends on subtask N]

   ### Subtask 3: [name]
   ...

   ## Execution Plan

   Parallel Group 1: [Subtask 1, Subtask 2] (can run simultaneously)
   Sequential After: [Subtask 3] (depends on Group 1)

   ## Resource Allocation

   Agents Required: [N]
   Estimated Duration: [relative estimate]
   Potential Conflicts: [list or None]

   ════════════════════════════════════════

   Approve this delegation plan?
   > [yes] Proceed with spawning agents
   > [modify] Adjust subtasks
   > [cancel] Abort delegation
   ```

4. **Create Delegation Registry** (on approval):
   - Create/update `docs/logs/delegation_registry.md`:
   ```markdown
   # Delegation Registry

   ## Active Session

   **Session ID**: DEL-[timestamp]
   **Created**: [timestamp]
   **Parent Task**: [task from docs/01_progress.md]
   **Status**: ACTIVE

   ### Spawned Agents

   | Agent ID | Subtask | Status | Scope | Spawned | Last Update |
   |----------|---------|--------|-------|---------|-------------|
   | AGT-001 | [name] | RUNNING | src/module/* | [time] | [time] |
   | AGT-002 | [name] | RUNNING | src/other/* | [time] | [time] |

   ### Completed Agents

   (None yet)

   ### Session Notes

   - [Any important context for this delegation]
   ```

5. **Spawn Task Agents**:
   For each approved subtask, spawn using Claude Code Task tool with strict instructions:

   ```
   ══════════════════════════════════════════════════════════════
   DELEGATED AGENT INSTRUCTIONS
   ══════════════════════════════════════════════════════════════

   You are Agent [AGT-XXX], a delegated agent working on a specific subtask.

   ## Your Subtask
   [Subtask description]

   ## Boundaries (STRICTLY ENFORCED)

   ### ALLOWED - You MAY:
   - Read any file in the project
   - Modify files in: [explicit scope list]
   - Create new files in: [explicit scope list]
   - Run tests for your changes
   - Use Read, Edit, Write, Grep, Glob, Bash tools

   ### FORBIDDEN - You MUST NOT:
   - Modify files outside your scope
   - Modify docs/01_progress.md (reserved for parent)
   - Modify docs/00_MASTER_INDEX.md (protocol)
   - Modify .claude/** (configuration)
   - Modify .git/** (git internals)
   - Run git push (no remote operations)
   - Spawn additional agents (no sub-delegation)
   - Make commits (parent will commit)

   ## Checkpoint Requirements

   Before completing, you MUST provide:

   1. **Summary of Changes**
      - List all files created/modified
      - Brief description of each change

   2. **Test Results**
      - Run tests for your modified files
      - Report PASS/FAIL

   3. **Blockers or Issues**
      - Any problems encountered
      - Any decisions that need parent review

   4. **Completion Status**
      - COMPLETE: All work done
      - BLOCKED: Need help/clarification
      - PARTIAL: Some work done, more needed

   ## Output Format

   When done, output exactly:

   ```
   ═══════════════════════════════════════
   AGENT CHECKPOINT: [AGT-XXX]
   ═══════════════════════════════════════

   Status: [COMPLETE | BLOCKED | PARTIAL]
   Subtask: [subtask name]

   ## Changes Made
   | File | Action | Description |
   |------|--------|-------------|
   | [path] | [created/modified/deleted] | [brief desc] |

   ## Test Results
   - Tests Run: [Y/N]
   - Result: [PASS/FAIL/SKIPPED]
   - Details: [any relevant info]

   ## Issues Encountered
   [List or "None"]

   ## Notes for Parent
   [Any context needed for merge review]

   ═══════════════════════════════════════
   ```

   ══════════════════════════════════════════════════════════════
   ```

6. **Report Spawned Agents**:
   ```
   DELEGATION STARTED
   ════════════════════════════════════════

   Session ID: DEL-[timestamp]

   Agents Spawned:
   1. AGT-001: [subtask 1] → Working on [scope]
   2. AGT-002: [subtask 2] → Working on [scope]

   Monitor Progress:
   • /sync --status  → Check agent status
   • /sync           → Review and merge when ready

   Note: Agents are working in parallel. Use /sync to manage results.

   ════════════════════════════════════════
   ```

## Delegation Limits

| Limit | Value | Rationale |
|-------|-------|-----------|
| Max parallel agents | 3 | Prevent resource exhaustion |
| Max scope per agent | 20 files | Keep changes reviewable |
| Agent timeout | 1 hour | Prevent runaway sessions |
| Sub-delegation | Forbidden | Maintain control hierarchy |

## Scope Definition Guidelines

Good scope definitions:
- `src/api/*` - Single module
- `src/utils/parser.py, src/utils/validator.py` - Specific files
- `tests/test_api/*` - Related tests

Bad scope definitions:
- `src/**` - Too broad
- `*` - Everything (forbidden)
- Overlapping scopes between agents

## Integration with Protocol v3.0

This command:
1. **STATE CHECK**: Reads `docs/01_progress.md` for task context
2. **ALIGN**: Verifies delegation relates to active work
3. **EXECUTE**: Spawns agents with strict boundaries
4. **COMMIT**: Updates `docs/logs/delegation_registry.md`

Respects:
- `parallel_coordinator.md` skill for lifecycle management
- `arch_enforcer.md` for scope boundaries
- Human approval required at merge via `/sync`

## Safety Rails

- **ALWAYS** require human approval for delegation plan
- **ALWAYS** define explicit scope boundaries
- **NEVER** allow agents to modify core docs
- **NEVER** allow agents to push to remote
- **NEVER** allow agents to spawn sub-agents
- **LIMIT** to 3 parallel agents maximum
- **TRACK** all delegations in registry

## Error Handling

If agent fails or times out:
```
AGENT FAILURE
════════════════════════════════════════

Agent: AGT-XXX
Subtask: [name]
Status: FAILED/TIMEOUT

Error: [error details]

Options:
1. Retry this subtask
2. Absorb into main context and continue manually
3. Cancel delegation session

Select option:
```

## See Also

- Sync command: `/sync`
- Skill: `parallel_coordinator.md`
- Delegation registry: `docs/logs/delegation_registry.md`
- Architecture: `docs/03_architecture.md`
