---
description: "Refine a rough prompt into a clear, actionable request."
---

# COMMAND: REFINE

**Trigger**: User types `/refine <rough_prompt>` or "refine: <rough_prompt>"

## Purpose
Takes a rough, vague, or incomplete prompt and transforms it into a clear, specific, actionable request that will produce better results.

## Actions
1. **Analyze the Rough Prompt**:
   - Identify the core intent (what does user actually want?)
   - Detect ambiguities (multiple interpretations possible?)
   - Find missing context (what information is assumed?)
   - Check scope clarity (is the task bounded?)

2. **Read Relevant Context** (if prompt relates to project):
   - `docs/01_progress.md` (current state - may inform intent)
   - `docs/03_architecture.md` (if code-related)

3. **Apply Refinement Checklist**:
   - [ ] **WHAT**: Is the desired outcome explicit?
   - [ ] **WHERE**: Are file paths/locations specified?
   - [ ] **HOW**: Is the approach/method clear?
   - [ ] **SCOPE**: Are boundaries defined (what NOT to do)?
   - [ ] **OUTPUT**: Is the expected deliverable clear?
   - [ ] **CONSTRAINTS**: Are there limitations to consider?

4. **Generate Refined Prompt**:
   ```
   REFINED PROMPT

   Original: "<user's rough prompt>"

   Refined:
   "<improved, specific, actionable prompt>"

   Clarifications Added:
   - <what was clarified/specified>
   - <assumptions made explicit>
   - <scope boundaries added>

   Questions (if still ambiguous):
   - <question 1>?
   - <question 2>?
   ```

5. **Ask User**:
   - "Use this refined prompt? Or adjust something?"
   - If user approves: Execute the refined prompt
   - If user has questions: Answer and re-refine

## Refinement Patterns

### Vague Intent -> Specific Action
- "fix the bug" -> "Fix the TypeError in `src/module.py:142` where `None` is passed to the function"
- "make it faster" -> "Optimize the `process_data()` function by adding caching for repeated lookups"

### Missing Context -> With Context
- "add logging" -> "Add structured logging using the existing logger module, at INFO level for API calls and DEBUG for data transformations"

### Unbounded Scope -> Bounded Scope
- "refactor the code" -> "Refactor `src/utils.py` to extract the validation logic into a separate `Validator` class, without changing the public API"

### Unclear Output -> Explicit Deliverable
- "document this" -> "Add docstrings to all public functions in `src/api.py` following Google style, including Args, Returns, and Examples sections"

## Safety Rails
- NEVER execute the original vague prompt directly
- ALWAYS present refined version for approval
- If prompt is already clear: Say "This prompt is already well-structured. Proceed?"
- If prompt is dangerous/out of scope: Refuse and explain why

## See Also
- Coding standards: `docs/04_standards.md`
- Architecture: `docs/03_architecture.md`
- Progress tracker: `docs/01_progress.md`
