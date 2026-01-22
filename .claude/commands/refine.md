---
description: "Refine a rough prompt into a clear, actionable request with recommended commands."
---

# COMMAND: REFINE

**Trigger**: User types `/refine <rough_prompt>` or "refine: <rough_prompt>"

## Purpose
Takes a rough, vague, or incomplete prompt and transforms it into a clear, specific, actionable request that includes recommended `/commands` for the workflow.

## Actions

1. **Analyze the Rough Prompt**:
   - Identify the core intent (what does user actually want?)
   - Detect ambiguities (multiple interpretations possible?)
   - Find missing context (what information is assumed?)
   - Check scope clarity (is the task bounded?)

2. **Read Relevant Context** (if prompt relates to project):
   - `docs/01_progress.md` (current state - may inform intent)
   - `docs/03_architecture.md` (if code-related)
   - `.claude/commands/` (available commands for workflow)

3. **Apply Refinement Checklist**:
   - [ ] **WHAT**: Is the desired outcome explicit?
   - [ ] **WHERE**: Are file paths/locations specified?
   - [ ] **HOW**: Is the approach/method clear?
   - [ ] **SCOPE**: Are boundaries defined (what NOT to do)?
   - [ ] **OUTPUT**: Is the expected deliverable clear?
   - [ ] **CONSTRAINTS**: Are there limitations to consider?
   - [ ] **COMMANDS**: Which /commands should be used?

4. **Match Intent to Commands**:

   | Intent Keywords | Recommended Commands |
   |-----------------|---------------------|
   | implement, build, create, add feature | `/tdd`, `/test` |
   | fix bug, debug, investigate | `/debug`, `/investigate` |
   | test, coverage, verify | `/test`, `/test-coverage` |
   | build error, type error, compile | `/build-fix` |
   | review, check code, audit | `/review` |
   | refactor, clean up, simplify | `/review`, `/test` |
   | deploy, release, commit | `/precommit`, `/commit-push-pr` |
   | status, health, overview | `/status` |
   | document, explain | `/review` |
   | parallel, delegate, split | `/delegate`, `/sync` |
   | start session, begin | `/boot` |
   | finish, complete, done | `/done`, `/save` |
   | learn, extract, pattern | `/learn` |

5. **Generate Refined Prompt**:
   ```
   REFINED PROMPT

   Original: "<user's rough prompt>"

   Refined:
   "<improved, specific, actionable prompt>"

   Clarifications Added:
   - <what was clarified/specified>
   - <assumptions made explicit>
   - <scope boundaries added>

   Recommended Workflow:
   1. <command 1> - <why>
   2. <command 2> - <why>
   3. <command 3> - <why>

   Questions (if still ambiguous):
   - <question 1>?
   - <question 2>?
   ```

6. **Ask User**:
   - "Use this refined prompt with the suggested workflow? Or adjust something?"
   - If user approves: Execute the refined prompt
   - If user has questions: Answer and re-refine

## Available Commands Reference

### Session Management
| Command | Use For |
|---------|---------|
| `/boot` | Start session, load context |
| `/save` | End session, checkpoint state |
| `/done` | Mark task complete |
| `/status` | Project health overview |

### Development
| Command | Use For |
|---------|---------|
| `/feature <name>` | Plan new feature |
| `/tdd <feature>` | Test-driven implementation |
| `/test` | Run tests with analysis |
| `/test-coverage` | Coverage gaps analysis |
| `/build-fix` | Fix build/type errors |
| `/quickfix` | Auto-fix lint issues |
| `/precommit` | Pre-commit validation |

### Quality & Review
| Command | Use For |
|---------|---------|
| `/review` | Code review |
| `/debug <issue>` | Structured debugging |
| `/investigate <topic>` | Deep investigation |
| `/learn` | Extract reusable patterns |

### Collaboration
| Command | Use For |
|---------|---------|
| `/delegate <task>` | Spawn parallel agents |
| `/sync` | Merge parallel work |
| `/commit-push-pr` | Quick commit and PR |

## Refinement Examples

### Example 1: Feature Implementation
**Original**: "add user authentication"

**Refined**:
"Implement user authentication with JWT tokens for the API.
- Add login/logout endpoints
- Create auth middleware
- Store tokens securely
- Follow existing API patterns in `src/api/`"

**Recommended Workflow**:
1. `/feature auth` - Plan the authentication architecture
2. `/tdd auth-endpoints` - Implement with TDD
3. `/test-coverage` - Verify 100% coverage (auth is critical)
4. `/review` - Security review before merge
5. `/done` - Complete task

### Example 2: Bug Fix
**Original**: "fix the login bug"

**Refined**:
"Fix the login failure where users get 401 error after valid credentials.
- Investigate token generation in `src/auth/token.ts`
- Check session handling
- Add regression test"

**Recommended Workflow**:
1. `/debug login-401` - Structured debugging
2. `/tdd login-fix` - Write failing test first
3. `/test` - Verify fix doesn't break other tests
4. `/learn` - Extract pattern if non-obvious fix
5. `/done` - Complete task

### Example 3: Code Quality
**Original**: "clean up the code"

**Refined**:
"Refactor `src/utils/` to reduce complexity.
- Extract repeated patterns
- Improve naming
- Add missing type annotations
- Maintain existing behavior (no functional changes)"

**Recommended Workflow**:
1. `/test` - Ensure tests pass before refactoring
2. `/review` - Identify specific improvements needed
3. `/test` - Run tests after each change
4. `/test-coverage` - Verify coverage maintained
5. `/done` - Complete task

## Safety Rails
- NEVER execute the original vague prompt directly
- ALWAYS present refined version with commands for approval
- If prompt is already clear: Say "This prompt is already well-structured. Proceed with these commands: [list]?"
- If prompt is dangerous/out of scope: Refuse and explain why
- If no commands match: Proceed without command suggestions

## See Also
- Coding standards: `docs/04_standards.md`
- Architecture: `docs/03_architecture.md`
- Progress tracker: `docs/01_progress.md`
- All commands: `.claude/commands/`
