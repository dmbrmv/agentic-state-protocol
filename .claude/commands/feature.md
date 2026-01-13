---
description: "Start a new feature with proper planning and architecture alignment."
---

# COMMAND: NEW FEATURE

**Trigger**: User types `/feature <name>` or "new feature: <description>"

## Actions
1. **Read Architecture Context**:
   - `docs/03_architecture.md` (system design)
   - `docs/04_standards.md` (code standards)

2. **Create Task in Backlog**:
   - Add new task to `docs/01_progress.md` Section III (Backlog)
   - Format:
     ```markdown
     #### N. [Feature Name]
     **Status**: Not started
     **Blocking**: None | [dependency]

     **Sub-tasks**:
     - [ ] Research existing code patterns
     - [ ] Design implementation approach
     - [ ] Create necessary files
     - [ ] Write tests
     - [ ] Update documentation
     ```

3. **Propose Implementation Plan**:
   - Analyze existing codebase structure
   - Identify files to create/modify
   - Check for similar patterns in codebase
   - Draft plan:
     ```
     IMPLEMENTATION PLAN: [Feature Name]

     Files to Create:
     - src/[module]/[file].py
     - tests/test_[feature].py

     Files to Modify:
     - src/[existing].py (add integration)
     - docs/03_architecture.md (document design)

     Dependencies:
     - [library] (add to requirements)

     Testing Strategy:
     - Unit tests for [component]
     - Integration tests for [workflow]
     ```

4. **Ask for Approval**:
   - Show plan to user
   - Ask: "Approve this plan? I will NOT write code until confirmed."

5. **If Approved**:
   - Move task from Backlog to "Active Task" in `docs/01_progress.md`
   - Set MODE to "Planning" initially
   - Create TodoWrite task list for implementation steps

## Integration with Protocol v3.0
This command follows the mandatory loop:
- **STATE CHECK**: Read docs/01_progress.md
- **ALIGN**: Verify no conflicting active tasks
- **EXECUTE**: Create plan (NOT code yet)
- **COMMIT**: Update docs/01_progress.md with new task

## Safety Rails
- ALWAYS read architecture docs before planning
- NEVER write code without user approval of plan
- Check for existing similar functionality (avoid duplication)
- Ensure alignment with coding standards

## See Also
- Architecture: `docs/03_architecture.md`
- Coding standards: `docs/04_standards.md`
- Progress tracker: `docs/01_progress.md`
