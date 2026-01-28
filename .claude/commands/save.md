---
description: "Shutdown sequence: Updates progress, logs, and prepares for git commit."
---

# COMMAND: SAVE

**Trigger**: User types `/save` or "SAVE"

## Actions
1. **Sync Progress Tracker**:
   - Update `docs/01_progress.md`:
     - Mark completed tasks with `[x]`
     - Move active task to completed section
     - Update "Last Updated" timestamp
     - Update "Recent Updates" section

2. **Log Session Context**:
   - Append checkpoint entry to `docs/logs/session_context.md`:
     ```markdown
     ## Session: YYYY-MM-DD - [Session Name]
     **Time**: [timestamp]
     **Agent**: Claude
     **Mode**: [Execution | Planning | Refactoring]

     ### Objective
     [What was accomplished]

     ### Actions Taken
     [Bulleted list of changes]

     ### Files Created/Modified
     [List files with brief description]

     ### Context for Next Session
     [What the next agent should know]

     ---
     **CHECKPOINT**: [One-line summary]
     ```

3. **Git Status Check**:
   - Run `git status --short`
   - Show uncommitted changes
   - Ask: "Ready to commit? (I can help with commit message)"

4. **Propose Next Task**:
   - Read backlog from `docs/01_progress.md`
   - Suggest: "Next task: [task_name]"

## Integration with Protocol v3.0
This command implements the SAVE macro from `docs/00_MASTER_INDEX.md` Section III.

## Safety Rails
- Updates documentation BEFORE suggesting git commit
- Never auto-commits (always asks permission)
- Shows changes before commit

## See Also
- Progress tracker: `docs/01_progress.md`
- Session logs: `docs/logs/session_context.md`
- Git workflow: `docs/04_standards.md`
