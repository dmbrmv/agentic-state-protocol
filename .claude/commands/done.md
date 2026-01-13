---
description: "Task completion sequence: Mark task done and propose next action."
---

# COMMAND: DONE

**Trigger**: User types `/done` or "DONE"

## Actions
1. **Mark Task Complete**:
   - Read `docs/01_progress.md`
   - Move active task from "Active Task" to "Completed Tasks" section
   - Add completion timestamp and summary
   - Check off task: `- [x] Task name`

2. **Log to Session Context**:
   - Append brief completion note to `docs/logs/session_context.md`:
     ```markdown
     ### Task Completed: [task_name]
     - Completed: YYYY-MM-DD
     - Files modified: [list]
     - Outcome: [brief summary]
     ```

3. **Propose Next Task**:
   - Read backlog from `docs/01_progress.md` (Section III)
   - Analyze priority order
   - Check dependencies (if Task #2 blocks Task #1, suggest #1 first)
   - Propose: "Next task suggestion: [task_name] (Priority: High/Medium/Low)"

4. **Context Check**:
   - Verify if completed task unblocks other tasks
   - Update blockers list if applicable
   - Show updated progress percentage

## Integration with Protocol v3.0
This command implements the DONE macro from `docs/00_MASTER_INDEX.md` Section III.

## Output Format
```
TASK COMPLETE: [task_name]

Updated Progress: X% -> Y%

Backlog Analysis:
1. [Next task] (High priority, ready to start)
2. [Task 2] (Medium priority, blocked by: [blocker])
3. [Task 3] (Low priority)

Recommendation: Start "[next_task]"?
```

## See Also
- Progress tracker: `docs/01_progress.md`
- Session logs: `docs/logs/session_context.md`
- Backlog prioritization: `docs/01_progress.md` Section III
