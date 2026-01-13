---
description: "Wake up sequence: Loads state and summarizes context."
---

# COMMAND: BOOT

**Trigger**: User types `/boot` or "BOOT"

## Actions
1. **Read Protocol Files**:
   - `docs/00_MASTER_INDEX.md` (protocol specification)
   - `docs/01_progress.md` (current state)
   - `docs/logs/session_context.md` (last 50 lines - recent context)

2. **Output Summary**:
   ```
   BOOT SEQUENCE

   Current Goal: [from docs/01_progress.md]
   Active Task: [from docs/01_progress.md]
   Progress: X%

   Last Session Summary:
   [from docs/logs/session_context.md - most recent checkpoint]

   Blockers: [list or "None"]
   Next Action: [next step from progress tracker]
   ```

3. **Ask**: "Proceed with [Active Task] or switch context?"

## Integration with Protocol v3.0
This command implements the BOOT macro from `docs/00_MASTER_INDEX.md` Section III.

## See Also
- Protocol specification: `docs/00_MASTER_INDEX.md`
- Progress tracker: `docs/01_progress.md`
- Session memory: `docs/logs/session_context.md`
