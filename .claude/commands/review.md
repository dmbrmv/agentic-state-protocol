---
description: "Code review workflow checking architecture, standards, and security."
---

# COMMAND: REVIEW

**Trigger**: User types `/review` or `/review <scope>`

## Purpose
Perform comprehensive code review against project architecture, coding standards, and security best practices. Generates actionable report with severity levels.

## Actions

1. **Identify Review Scope**:
   - Default: All uncommitted changes (`git diff HEAD`)
   - Staged only: `/review --staged` (`git diff --cached`)
   - Specific files: `/review <path>`
   - PR review: `/review --pr <number>` (uses `gh pr diff`)

2. **Read Review Criteria**:
   - `docs/04_standards.md` (coding standards - LAW)
   - `docs/03_architecture.md` (system design)
   - `docs/02_issues.md` (known issues to check against)

3. **Execute Review Checklist**:

   ### Architecture Review
   - [ ] File locations follow documented structure
   - [ ] No circular imports introduced
   - [ ] Proper module boundaries maintained
   - [ ] API contracts preserved (no breaking changes)
   - [ ] Data flow matches documented patterns

   ### Standards Review
   - [ ] Naming conventions followed (snake_case, PascalCase, etc.)
   - [ ] Proper error handling implemented
   - [ ] Logging added where appropriate
   - [ ] Type hints present (if required by standards)
   - [ ] Docstrings complete for public APIs
   - [ ] No magic numbers or hardcoded values
   - [ ] Code formatted according to standards

   ### Security Review
   - [ ] No hardcoded secrets (API keys, passwords, tokens)
   - [ ] Input validation present for external data
   - [ ] No SQL injection vectors
   - [ ] No command injection vectors
   - [ ] No XSS vulnerabilities (if web)
   - [ ] Sensitive data properly handled/masked
   - [ ] Dependencies scanned for vulnerabilities

   ### Test Coverage Review
   - [ ] New code has corresponding tests
   - [ ] Edge cases considered and tested
   - [ ] Mocks used appropriately (not over-mocked)
   - [ ] Test naming follows conventions

4. **Generate Review Report**:
   ```
   CODE REVIEW REPORT
   ════════════════════════════════════════

   Scope: [files reviewed]
   Lines Changed: +X, -Y
   Files Modified: N

   ## Summary
   Critical Issues: N (must fix before merge)
   Warnings: N (should fix)
   Suggestions: N (consider for improvement)

   Verdict: APPROVE | APPROVE_WITH_COMMENTS | REQUEST_CHANGES

   ════════════════════════════════════════

   ## Critical Issues (MUST FIX)

   ### [CRIT-001] Hardcoded API Key
   File: src/api/client.py:42
   ```python
   api_key = "sk-1234567890"  # SECURITY: Hardcoded secret
   ```
   **Fix**: Move to environment variable or secrets manager
   **Impact**: Security vulnerability, credential exposure

   ---

   ## Warnings (SHOULD FIX)

   ### [WARN-001] Missing Error Handling
   File: src/utils/parser.py:28
   ```python
   data = json.loads(raw_input)  # No try/except
   ```
   **Fix**: Add try/except with proper error handling
   **Impact**: Unhandled exception on malformed input

   ---

   ## Suggestions (CONSIDER)

   ### [SUGG-001] Consider Type Hints
   File: src/core/processor.py:15
   ```python
   def process(data):  # Missing type hints
   ```
   **Suggestion**: Add type hints per docs/04_standards.md
   **Benefit**: Better IDE support, documentation

   ════════════════════════════════════════

   ## Security Findings
   - Secrets Scan: [CLEAN | N issues found]
   - Dependency Audit: [CLEAN | N vulnerabilities]
   - Input Validation: [ADEQUATE | MISSING in N locations]

   ## Standards Compliance
   - Naming: [COMPLIANT | N violations]
   - Formatting: [COMPLIANT | N violations]
   - Documentation: [COMPLIANT | N missing docstrings]

   ════════════════════════════════════════
   ```

5. **Offer Quick Fixes**:
   ```
   QUICK FIX OPTIONS

   The following issues can be auto-fixed:
   1. [WARN-001] Add error handling to parser.py
   2. [SUGG-001] Add type hints to processor.py

   Apply quick fixes? (I'll show each diff first)
   > [1] Fix specific issue
   > [all] Fix all auto-fixable
   > [none] Skip fixes
   ```

6. **Apply Fixes** (if approved):
   - Show diff for each fix before applying
   - Apply using Edit tool
   - Re-run review on fixed files
   - Report remaining issues

7. **Log Review**:
   - Append to `docs/logs/session_context.md`:
     ```
     ### Code Review: [timestamp]
     - Scope: [scope]
     - Verdict: [verdict]
     - Critical: N | Warnings: M | Suggestions: P
     - Fixes Applied: [list or None]
     ```

## Scope Options

| Option | Description | Example |
|--------|-------------|---------|
| `/review` | All uncommitted changes | `git diff HEAD` |
| `/review --staged` | Staged changes only | `git diff --cached` |
| `/review <path>` | Specific file/directory | `/review src/api/` |
| `/review --pr <n>` | GitHub PR | `/review --pr 123` |
| `/review --strict` | Fail on any warning | Stricter review |

## Severity Definitions

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| **Critical** | Security vulnerabilities, breaking changes, data loss risks | Must fix before merge |
| **Warning** | Standards violations, missing error handling, poor patterns | Should fix |
| **Suggestion** | Improvements, optimizations, style preferences | Consider for quality |

## Integration with Protocol v3.0

This command enforces:
- **Immutable Rule #4**: DIRECTORY AUTHORITY (validates against `docs/03_architecture.md`)
- **docs/04_standards.md**: Coding standards as LAW

Decision Authority Hierarchy applied:
1. `docs/04_standards.md` violations = Critical
2. `docs/03_architecture.md` violations = Critical/Warning
3. General best practices = Suggestion

## Safety Rails

- **NEVER** auto-fix without showing diff first
- **NEVER** approve code with unresolved Critical issues
- **ALWAYS** scan for hardcoded secrets
- **ALWAYS** check dependency vulnerabilities
- **LOG** all reviews to session context

## See Also

- Architecture: `docs/03_architecture.md`
- Coding standards: `docs/04_standards.md`
- Issues tracker: `docs/02_issues.md`
- Skill: `arch_enforcer.md`
