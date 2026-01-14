# SKILL: Parallel Agent Coordination

**Purpose**: Manage multi-instance task delegation with supervised checkpoints and safe merging.

---

## Trigger Conditions

Use this skill when:
1. User invokes `/delegate` command
2. User invokes `/sync` command
3. Checking status of delegated agents
4. Agent reaches a checkpoint
5. Resolving conflicts between agent outputs
6. Managing agent lifecycle events

---

## Core Logic

### 1. Agent Lifecycle Management

**Agent States**:
```text
PENDING    → Task defined, agent not yet spawned
SPAWNING   → Agent creation in progress
RUNNING    → Agent actively working
CHECKPOINT → Agent reached milestone, awaiting review
COMPLETE   → Agent finished successfully
FAILED     → Agent encountered unrecoverable error
MERGED     → Agent's work integrated into main
ABORTED    → Agent cancelled before completion
```

**State Transitions**:
```text
PENDING ──────► SPAWNING ──────► RUNNING
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
               CHECKPOINT      COMPLETE         FAILED
                    │               │               │
                    ▼               ▼               │
                RUNNING         MERGED ◄───────────┘
                                                (if recoverable)
```

**Transition Rules**:
```text
PENDING → SPAWNING: When /delegate approved
SPAWNING → RUNNING: When Task tool returns agent ID
RUNNING → CHECKPOINT: When agent outputs checkpoint format
RUNNING → COMPLETE: When agent outputs completion format
RUNNING → FAILED: On error, timeout, or boundary violation
CHECKPOINT → RUNNING: When checkpoint reviewed and continued
COMPLETE → MERGED: When human approves via /sync
COMPLETE → ABORTED: When human rejects via /sync
FAILED → MERGED: If partial work salvageable and approved
```

### 2. Delegation Registry Structure

**File**: `docs/logs/delegation_registry.md`

```markdown
# Delegation Registry

## Active Session

**Session ID**: DEL-[timestamp]
**Created**: [ISO timestamp]
**Parent Task**: [from docs/01_progress.md]
**Parent Agent**: Main session
**Status**: ACTIVE | MERGING | COMPLETE | ABORTED

### Configuration
- Max Parallel Agents: 3
- Agent Timeout: 3600s
- Human Approval Required: Yes

### Agents

#### AGT-001
- **Subtask**: [description]
- **Status**: RUNNING
- **Scope**:
  - Allowed: src/module/*, tests/test_module/*
  - Forbidden: docs/01_progress.md, .claude/**
- **Spawned**: [timestamp]
- **Last Activity**: [timestamp]
- **Checkpoints**: 0
- **Output**: [pending | file path]

#### AGT-002
...

### Completed Agents
[Archived agent records after merge]

### Session Events Log
| Timestamp | Event | Agent | Details |
|-----------|-------|-------|---------|
| [time] | SPAWNED | AGT-001 | Started subtask X |
| [time] | CHECKPOINT | AGT-001 | Reached milestone |
| [time] | COMPLETE | AGT-001 | Subtask finished |
| [time] | MERGED | AGT-001 | Changes integrated |

## Archived Sessions
[Previous delegation sessions for reference]
```

### 3. Checkpoint Protocol

**Checkpoint Triggers**:
- Agent explicitly outputs checkpoint format
- Periodic time-based (every 30 min)
- Before any risky operation
- When reaching scope boundary
- On encountering blocker

**Checkpoint Format** (agents must output):
```text
═══════════════════════════════════════
AGENT CHECKPOINT: [AGT-XXX]
═══════════════════════════════════════

Status: [COMPLETE | BLOCKED | IN_PROGRESS]
Progress: [0-100]%

## Changes Made
| File | Action | Description |
|------|--------|-------------|
| [path] | [created/modified] | [brief] |

## Tests Run
- Executed: [Y/N]
- Result: [PASS/FAIL/SKIPPED]
- Failed: [list if any]

## Blockers
[None | Description of blocking issue]

## Questions for Parent
[None | Questions requiring human/parent input]

## Request
[CONTINUE | MERGE | HELP | ABORT]

═══════════════════════════════════════
```

### 4. Boundary Enforcement

**Scope Validation** (before agent actions):
```text
For each file operation:
1. Check if path in agent's allowed scope
2. Check if path NOT in forbidden list
3. If violation:
   a. Block the operation
   b. Log violation attempt
   c. Notify in next checkpoint
```

**Global Forbidden Paths** (all agents):
```text
- docs/01_progress.md       # Progress tracker (parent only)
- docs/00_MASTER_INDEX.md   # Protocol (immutable)
- .claude/**                # Configuration
- .git/**                   # Git internals
- Remote operations         # No git push
```

**Scope Isolation**:
```text
- Agent scopes should not overlap
- If overlap unavoidable, mark as conflict-prone
- Conflicts resolved at merge time, not runtime
```

### 5. Conflict Detection

**Pre-Merge Conflict Check**:
```text
For each pair of agents:
1. Compare modified file lists
2. If overlap:
   a. Mark conflict
   b. Prepare diff comparison
   c. Require human resolution
```

**Conflict Types**:
```text
FILE_CONFLICT:    Same file modified by multiple agents
IMPORT_CONFLICT:  Incompatible import changes
API_CONFLICT:     Breaking interface changes
TEST_CONFLICT:    Test expectations differ
```

**Resolution Strategies**:
```text
1. CHOOSE_ONE:    Select one agent's version
2. MANUAL_MERGE:  Human combines changes
3. SEQUENTIAL:    Apply changes in order
4. ABORT:         Discard conflicting agent
```

### 6. Supervision Levels

**SUPERVISED (Default)**:
```text
- Human reviews each checkpoint
- Human approves each merge
- Human resolves conflicts
- Most control, most oversight
```

**SEMI-AUTONOMOUS** (Requires explicit enable):
```text
- Agents proceed through checkpoints automatically
- Auto-merge if tests pass and no conflicts
- Human approves final result only
- Less overhead, less control
```

**NEVER ALLOWED**:
```text
✗ Fully autonomous merge
✗ Pushing to remote without human
✗ Modifying core docs without review
✗ Sub-delegation (agents spawning agents)
```

---

## Integration with Protocol v3.0

**State Management**:
- Delegation registry lives in `docs/logs/`
- Persists across sessions
- Updates `docs/01_progress.md` only after human-approved merge
- All delegations logged to session context

**Authority Hierarchy**:
```text
1. Human (highest)
2. Parent Agent (main session)
3. Delegated Agents (scoped authority)
4. Sub-agents (forbidden)
```

**Decision Authority**:
- Delegated agents cannot override parent decisions
- Delegated agents cannot access parent's restricted files
- Merge decisions always require human approval

---

## Enforcement Actions

### Auto-Track (No Permission)
```text
✓ Monitor agent status
✓ Record checkpoints
✓ Detect boundary violations
✓ Update delegation registry
```

### Stop and Ask
```text
? Agent requesting out-of-scope access
? Agent timeout approaching
? Conflict detected between agents
? Agent reporting blocker
```

### Reject Automatically
```text
✗ Agent attempting to modify forbidden paths
✗ Agent attempting remote operations
✗ Agent attempting to spawn sub-agents
✗ Agent exceeding resource limits
```

---

## Resource Management

### Limits
| Resource | Limit | Rationale |
|----------|-------|-----------|
| Parallel Agents | 3 | Prevent context overload |
| Agent Timeout | 1 hour | Prevent runaway |
| Scope Size | 20 files | Keep changes reviewable |
| Checkpoint Interval | 30 min | Ensure progress visibility |

### Monitoring
```text
Track per agent:
- Elapsed time
- Files modified count
- Checkpoint count
- Error count
- Token usage (if available)
```

---

## Error Handling

### Agent Failure
```text
On agent error:
1. Capture error details
2. Mark agent as FAILED
3. Preserve any work done
4. Notify in /sync status
5. Offer recovery options:
   - Retry with same scope
   - Salvage partial work
   - Abandon and redistribute
```

### Timeout
```text
On agent timeout:
1. Attempt graceful checkpoint
2. If no response, mark FAILED
3. Preserve any output
4. Offer:
   - Extend timeout
   - Force complete
   - Abort
```

### Boundary Violation
```text
On scope violation attempt:
1. Block the operation
2. Log violation
3. Continue agent (don't fail)
4. Report in checkpoint
5. Review before merge
```

---

## Session Lifecycle

### Start Session (/delegate)
```text
1. Validate no active session
2. Create delegation registry entry
3. Analyze task for subtasks
4. Propose delegation plan
5. On approval, spawn agents
6. Monitor agent startup
```

### During Session
```text
1. Monitor agent status
2. Process checkpoints
3. Detect conflicts
4. Handle errors
5. Update registry
```

### End Session (/sync complete)
```text
1. Verify all agents complete/failed
2. Merge approved agents
3. Run integration tests
4. Update docs/01_progress.md
5. Archive session in registry
6. Log to session context
```

---

## See Also

- Delegate command: `/delegate`
- Sync command: `/sync`
- Delegation registry: `docs/logs/delegation_registry.md`
- Architecture enforcer: `arch_enforcer.md`
