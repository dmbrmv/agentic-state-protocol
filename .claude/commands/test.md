---
description: "Run project tests with smart failure analysis and fix suggestions."
---

# COMMAND: TEST

**Trigger**: User types `/test` or `/test <scope>`

## Purpose
Execute project tests, analyze failures with AI, and suggest actionable fixes. Integrates with the project's test framework automatically.

## Actions

1. **Detect Test Framework**:
   - Scan for: `pytest.ini`, `pyproject.toml [tool.pytest]`, `conftest.py` (Python)
   - Scan for: `unittest` test files matching `test_*.py` (Python stdlib)
   - Select appropriate runner: pytest | unittest

2. **Read Test Context**:
   - `docs/01_progress.md` (active task context)
   - `docs/04_standards.md` (test coverage requirements)

3. **Run Tests**:
   ```bash
   # Based on detected framework:
   pytest {scope} -v --tb=short          # Python (pytest)
   python -m unittest {scope}            # Python (unittest)
   ```

4. **Output Results**:
   ```
   TEST RESULTS
   ════════════════════════════════════════

   Framework: [detected framework]
   Scope: [all | path | changed files]

   Status: PASS | FAIL
   Passed: X/Y tests
   Failed: N tests
   Skipped: M tests
   Duration: Xs
   Coverage: X% (if available)

   ════════════════════════════════════════
   ```

5. **If Failures - Analyze Each**:
   ```
   FAILURE ANALYSIS

   Test: test_function_name
   File: tests/test_module.py:42

   Error Type: [AssertionError | TypeError | etc.]

   Expected: [expected value]
   Actual: [actual value]

   Stack Trace:
   [relevant portion of stack trace]

   Root Cause Analysis:
   [AI analysis of why the test failed]

   Suggested Fixes:
   1. [Fix in source code] - if logic error
      File: src/module.py:XX
      Change: [description]

   2. [Fix in test] - if test expectation wrong
      File: tests/test_module.py:XX
      Change: [description]

   Apply fix #1? (I'll show the diff first)
   ```

6. **Apply Fixes** (if approved):
   - Show complete diff before applying
   - Apply changes using Edit tool
   - Re-run affected tests to verify fix
   - Report success or new failures

7. **Log to Session Context**:
   - Append to `docs/logs/session_context.md`:
     ```
     ### Test Run: [timestamp]
     - Scope: [scope]
     - Result: PASS/FAIL (X/Y)
     - Failures fixed: [N or None]
     ```

## Scope Options

| Option | Description | Example |
|--------|-------------|---------|
| `/test` | Run all tests | Full test suite |
| `/test <path>` | Run tests in specific path | `/test tests/test_api.py` |
| `/test --failed` | Re-run only failed tests | Previously failed tests |
| `/test --changed` | Tests for changed files | Based on `git diff` |
| `/test --coverage` | Run with coverage report | Include coverage metrics |
| `/test --watch` | Watch mode (if supported) | Continuous testing |

## Integration with Protocol v3.0

This command follows the mandatory loop:
1. **STATE CHECK**: Read `docs/01_progress.md` to understand active task
2. **ALIGN**: Tests should relate to current work
3. **EXECUTE**: Run tests and analyze results
4. **COMMIT**: Log results to `docs/logs/session_context.md`

Integrates with:
- `test_enforcer.md` skill (auto-triggered after code changes)
- `docs/04_standards.md` (coverage requirements)
- `docs/02_issues.md` (persistent failures logged as issues)

## Safety Rails

- **NEVER** auto-fix without showing diff first
- **NEVER** modify tests to make them pass artificially
- **ALWAYS** re-run tests after applying fixes
- **LOG** all test runs to session context
- **WARN** if tests would modify production data

## Error Handling

If test framework not detected:
```
TEST FRAMEWORK NOT DETECTED

Searched for:
- pytest.ini, pyproject.toml [tool.pytest], conftest.py (Python/pytest)
- test_*.py files (Python/unittest)

Please specify the test command:
> /test --command "your test command"
```

## See Also

- Coding standards: `docs/04_standards.md`
- Issues tracker: `docs/02_issues.md`
- Session logs: `docs/logs/session_context.md`
- Skill: `test_enforcer.md`
