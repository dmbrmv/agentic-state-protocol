---
description: "Structured debugging workflow with root cause analysis."
---

# COMMAND: DEBUG

**Trigger**: User types `/debug <issue>` or `/debug`

## Purpose
Systematic debugging workflow that gathers context, performs root cause analysis, generates fix options, and tracks resolution. Prevents ad-hoc debugging that loses context.

## Actions

1. **Gather Issue Context**:
   - If `<issue>` provided: Use as starting point
   - If no issue: Ask "What error or behavior are you seeing?"
   - Check `docs/02_issues.md` for related known issues

2. **Information Collection Phase**:
   ```
   DEBUGGING SESSION STARTED
   ════════════════════════════════════════

   Issue: [issue description]
   Started: [timestamp]

   Collecting information...

   1. Error Analysis
      - Error type: [type if available]
      - Stack trace: [parsing...]
      - Error location: [file:line if identified]

   2. Context Gathering
      - Recent changes: [git log --oneline -10]
      - Modified files: [git diff --name-only HEAD~5]
      - Active task: [from docs/01_progress.md]

   3. Related Code
      - [Reading relevant source files...]
      - [Tracing imports and dependencies...]

   4. Environment Check
      - Python version: [version]
      - Key dependencies: [versions]
      - Config files: [relevant configs]

   5. Test Status
      - Related tests: [identifying...]
      - Last test run: [result if available]

   ════════════════════════════════════════
   ```

3. **Root Cause Analysis**:
   ```
   ROOT CAUSE ANALYSIS
   ════════════════════════════════════════

   ## Error Trace
   [Traced path from error to source]

   Call Stack:
   1. [function_a] at file_a.py:10
      └─ calls [function_b]
   2. [function_b] at file_b.py:25
      └─ calls [function_c]
   3. [function_c] at file_c.py:42  <-- ERROR ORIGIN
      └─ [specific operation that fails]

   ## Analysis

   ### What's Happening
   [Clear explanation of the failure mechanism]

   ### Why It's Happening
   [Explanation of the root cause]

   ### When It Started
   - Likely introduced in: [commit or timeframe]
   - Related changes: [list of relevant commits]

   ### Related Known Issues
   [From docs/02_issues.md if any]

   ════════════════════════════════════════
   ```

4. **Generate Solution Options**:
   ```
   SOLUTION OPTIONS
   ════════════════════════════════════════

   ## Option 1: Quick Fix
   Risk: LOW | Effort: LOW | Recommended: [Yes/No]

   Description: [What this fix does]

   Changes:
   - File: src/module.py:42
     ```python
     # Before
     result = process(data)

     # After
     result = process(data) if data else None
     ```

   Pros: Fast, minimal change
   Cons: May not address underlying issue

   ---

   ## Option 2: Proper Fix
   Risk: MEDIUM | Effort: MEDIUM | Recommended: [Yes/No]

   Description: [What this fix does]

   Changes:
   - File: src/module.py:40-50
     [Larger refactoring description]

   Pros: Addresses root cause, more robust
   Cons: Requires more testing

   ---

   ## Option 3: Comprehensive Refactor
   Risk: HIGH | Effort: HIGH | Recommended: [Yes/No]

   Description: [What this refactor does]

   Changes:
   - Multiple files affected
   - [List of changes]

   Pros: Best long-term solution
   Cons: Significant effort, requires thorough testing

   ════════════════════════════════════════

   Recommendation: Option [N] because [rationale]

   Apply Option [N]? (I'll show the complete diff first)
   ```

5. **Apply Fix** (if approved):
   - Show complete diff before any changes
   - Apply using Edit tool
   - Run related tests immediately
   - If tests fail: Show new errors, don't proceed

6. **Verify Resolution**:
   ```
   VERIFICATION
   ════════════════════════════════════════

   Fix Applied: Option [N]

   Test Results:
   - Related tests: PASS/FAIL
   - Regression tests: PASS/FAIL

   Verification Steps:
   1. [Manual check 1]: [DONE/PENDING]
   2. [Manual check 2]: [DONE/PENDING]

   Status: RESOLVED | PARTIALLY_RESOLVED | NOT_RESOLVED

   ════════════════════════════════════════
   ```

7. **Update Documentation**:
   - Add/update entry in `docs/02_issues.md`:
     ```markdown
     ## ISSUE-XXX: [Title]
     - **Status**: RESOLVED
     - **Severity**: [severity]
     - **Root Cause**: [brief description]
     - **Resolution**: [what was done]
     - **Prevention**: [how to avoid in future]
     ```

   - Log to `docs/logs/session_context.md`:
     ```
     ### Debug Session: [timestamp]
     - Issue: [description]
     - Root Cause: [cause]
     - Resolution: Option [N] applied
     - Verification: PASS/FAIL
     ```

## Debug Options

| Option | Description | Example |
|--------|-------------|---------|
| `/debug` | Interactive debug session | Guided debugging |
| `/debug <error>` | Debug specific error | `/debug "TypeError: None"` |
| `/debug --trace <func>` | Trace function execution | `/debug --trace process_data` |
| `/debug --history` | Review past debug sessions | From session_context.md |
| `/debug --issue <id>` | Debug known issue | `/debug --issue ISSUE-001` |

## Debug Checklist

Before concluding debug session:
- [ ] Root cause clearly identified
- [ ] Fix applied and verified
- [ ] Related tests passing
- [ ] docs/02_issues.md updated
- [ ] Session context logged
- [ ] Prevention recommendations noted

## Integration with Protocol v3.0

This command follows the mandatory loop:
1. **STATE CHECK**: Read `docs/01_progress.md` for context
2. **ALIGN**: Verify debugging relates to current work
3. **EXECUTE**: Systematic analysis and fix
4. **COMMIT**: Update `docs/02_issues.md` and session context

## Safety Rails

- **NEVER** apply fixes without showing diff first
- **NEVER** mark resolved without passing tests
- **ALWAYS** run related tests after fix
- **ALWAYS** document resolution in issues tracker
- **WARN** if fix might affect other parts of system

## Error Patterns Database

Common patterns the debugger recognizes:
- `NoneType has no attribute` -> Null check missing
- `IndexError: list index out of range` -> Bounds check missing
- `KeyError` -> Missing key validation
- `ImportError` -> Module path or dependency issue
- `TypeError: cannot unpack` -> Return value mismatch
- `ConnectionError` -> Network/service availability

## See Also

- Issues tracker: `docs/02_issues.md`
- Session logs: `docs/logs/session_context.md`
- Progress tracker: `docs/01_progress.md`
- Test command: `/test`
