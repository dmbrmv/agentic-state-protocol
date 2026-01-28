# SKILL: Context Management

**Purpose**: Ensure documentation stays synchronized with code changes and project state.

---

## Trigger Conditions

Use this skill automatically when:
1. User says "Done", "Update", "Complete", or "SAVE"
2. A task is completed
3. Switching between topics/tasks
4. Significant code changes are made (>3 files modified)
5. Architecture decisions are made

---

## Core Logic

### 1. Source of Truth Principle
**Rule**: The `docs/` folder is the authoritative project state.

**Actions**:
- Before modifying code: Read relevant `docs/03_architecture.md`
- After modifying code: Update relevant architecture docs
- After completing task: Update `docs/01_progress.md`
- After session work: Update `docs/logs/session_context.md`

### 2. Consistency Checks

**When code changes**:
```python
if modified_files > 0:
    check_and_update([
        "docs/03_architecture.md",  # If system design changed
        "docs/01_progress.md",       # Task status
    ])
```

**When task status changes**:
```python
if task_status_changed:
    update("docs/01_progress.md")
    log_to("docs/logs/session_context.md")
```

### 3. Documentation Update Rules

**ALWAYS update** after:
- Creating new files -> Update architecture docs
- Modifying >3 files -> Update progress tracker
- Making design decisions -> Log in session_context.md
- Completing a task -> Mark in 01_progress.md
- Discovering blockers -> Add to 01_progress.md Section V

**NEVER**:
- Leave `docs/01_progress.md` outdated (violates DOCS = CODE rule)
- Make architecture changes without documenting them
- Complete a session without updating `docs/logs/session_context.md`

---

## Integration with Protocol v3.0

This skill enforces **Immutable Rule #3: DOCS = CODE**

From `docs/00_MASTER_INDEX.md`:
> "Code changes are incomplete without documentation updates"

---

## Automation Rules

### Auto-Read Context (No Permission Needed)
- When starting a task -> Read `docs/01_progress.md`
- When creating files -> Read `docs/03_architecture.md`
- When refactoring -> Read `docs/04_standards.md`

### Auto-Update Documentation (Always Do This)
- After task completion -> Update `docs/01_progress.md`
- After session work -> Update `docs/logs/session_context.md`
- After design changes -> Update `docs/03_architecture.md`

### Ask Permission Before
- Changing active task (show current task, ask to switch)
- Modifying files outside documented scope
- Making breaking changes

---

## Example Workflow

**Scenario**: User completes a feature implementation

```text
1. Detect: User says "DONE" or task is finished
2. Auto-Read: docs/01_progress.md (check active task)
3. Update: Move task to "Completed Tasks" section
4. Log: Append completion note to docs/logs/session_context.md
5. Check: Did this unblock other tasks? Update blockers list
6. Propose: "Next task: [name] from backlog?"
7. Verify: Show updated progress percentage
```

---

## Quality Checklist

Before considering a task "done":
- [ ] `docs/01_progress.md` reflects current state
- [ ] Relevant architecture docs updated
- [ ] Session context logged
- [ ] No orphaned code (all files documented)
- [ ] Decision log updated if design decisions made

---

## See Also
- Protocol rules: `docs/00_MASTER_INDEX.md`
- Progress tracker: `docs/01_progress.md`
- Session logs: `docs/logs/session_context.md`
- Architecture: `docs/03_architecture.md`
