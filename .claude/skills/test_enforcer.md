# SKILL: Test Enforcement

**Purpose**: Automatically run relevant tests after code changes and suggest fixes for failures.

---

## Trigger Conditions

Use this skill automatically when:
1. User saves changes to source files (`src/**`)
2. User completes a code modification task
3. User says "Done" with code changes
4. Before `/save` command executes
5. After `/debug` fix is applied
6. When creating new source files

---

## Core Logic

### 1. Change Detection

**Rule**: Track modified files during session to determine test scope.

```text
On file modification:
1. Record modified file path
2. Determine file type (source vs test vs config)
3. If source file:
   a. Find corresponding test files
   b. Add to pending test queue
4. If significant changes accumulated:
   a. Trigger test run
```

**Significance Thresholds**:
- Any modification to `src/**` → Queue tests
- 3+ files modified → Consider running tests
- Before `/done` or `/save` → Must run tests

### 2. Test Selection Strategy

**Direct Mapping** (preferred):
```text
src/module/file.py       → tests/test_file.py
                         → tests/module/test_file.py
                         → tests/test_module_file.py

src/components/Button.tsx → tests/components/Button.test.tsx
                          → __tests__/Button.test.tsx

src/lib.rs               → tests/test_lib.rs (Rust)
                         → src/lib_test.rs (inline tests)

src/handler.go           → src/handler_test.go (Go convention)
```

**Import Analysis** (secondary):
```text
1. Parse modified file for exports
2. Find tests that import the modified module
3. Include those tests in run
```

**Cascade Rules**:
```text
- Core module changed → Run all tests importing it
- Config file changed → Run full test suite
- Test file changed → Run that test
- >5 source files changed → Run full suite
```

### 3. Auto-Run Rules

**ALWAYS run tests after**:
- Creating new source files
- Modifying existing source files
- Refactoring code
- Applying debug fixes
- Before `/save` checkpoint
- Before `/done` task completion

**SKIP tests when**:
- Only documentation changed (`docs/**`, `*.md`)
- Only formatting changes (no logic change)
- Config file formatting only
- User explicitly says "skip tests"

### 4. Failure Analysis

When tests fail, automatically analyze:

```text
TEST FAILURE DETECTED
════════════════════════════════════════

Running failure analysis...

Test: test_function_name
File: tests/test_module.py:42
Framework: [pytest | jest | cargo | go]

## Error Details
Type: AssertionError
Message: "Expected X, got Y"

## Stack Trace Analysis
[Relevant portion highlighting source of error]

## Root Cause Analysis

Likely Cause: [AI analysis]
- [Explanation of what went wrong]
- [Why the assertion failed]

Related Code:
- Source: src/module.py:28-35
- Change: [description of recent change]

## Suggested Fixes

Option 1: Fix Source Code
File: src/module.py:30
```python
# Before
return data.process()

# After
return data.process() if data else None
```
Rationale: Handle None case that test exposes

Option 2: Update Test Expectation
File: tests/test_module.py:42
[Only if test expectation is wrong]

════════════════════════════════════════

Apply suggested fix? (I'll show diff first)
```

### 5. Quality Gates

Before allowing `/done`:
```text
□ Affected tests identified
□ Tests executed
□ All tests pass
  OR failures documented in docs/02_issues.md
□ Coverage not decreased (if tracked)
```

If tests failing at `/done`:
```text
QUALITY GATE: Tests Failing

Cannot mark task as done with failing tests.

Options:
1. Fix the failing tests
2. Document as known issue in docs/02_issues.md
3. Override with explicit approval

Select option:
```

---

## Integration with Protocol v3.0

This skill enforces testing as part of the mandatory loop:

**EXECUTE Phase**:
- After code changes → Run affected tests
- Failure blocks progress until resolved

**COMMIT Phase**:
- Before `/save` → Verify tests pass
- Log test results to `docs/logs/session_context.md`

**Integrates With**:
- `/test` command (shared test execution logic)
- `/done` command (quality gate)
- `/save` command (pre-checkpoint verification)
- `docs/04_standards.md` (coverage requirements)
- `docs/02_issues.md` (failure documentation)

---

## Automation Rules

### Auto-Run (Implicit Permission)
```text
✓ After source file modification → Run affected tests
✓ Show results in session output
✓ Cache results for /status dashboard
```

### Ask Permission Before
```text
? Running full test suite (estimated >2 min)
? Applying suggested fixes
? Modifying test files
? Overriding quality gate
```

### Never Auto
```text
✗ Skip tests on significant code changes
✗ Apply fixes without showing diff
✗ Mark tests as passed when they failed
✗ Delete or disable failing tests
```

---

## Test Framework Detection

**Python**:
```text
Indicators: pytest.ini, pyproject.toml [tool.pytest], conftest.py, setup.cfg [tool:pytest]
Command: pytest {scope} -v --tb=short
Coverage: pytest --cov={package} --cov-report=term-missing
```

**JavaScript/TypeScript**:
```text
Indicators: jest.config.*, package.json:jest, vitest.config.*
Command: npx jest {scope} --verbose OR npx vitest run {scope}
Coverage: --coverage flag
```

**Rust**:
```text
Indicators: Cargo.toml
Command: cargo test {scope} -- --nocapture
Coverage: cargo tarpaulin
```

**Go**:
```text
Indicators: go.mod, *_test.go files
Command: go test {scope} -v
Coverage: go test -coverprofile=coverage.out
```

---

## Enforcement Actions

### Before Task Completion
```text
ENFORCING: Test verification before /done

Status: [BLOCKED | PASSED]

If BLOCKED:
- Failing tests: [count]
- Must resolve or document before completing task

If PASSED:
- All affected tests pass
- Proceeding with task completion
```

### Before Save/Checkpoint
```text
ENFORCING: Test verification before /save

Running quick check on modified files...

Result: [PASS | FAIL]

If FAIL:
- Warning: Saving with failing tests
- Consider fixing before checkpoint
- Continue anyway? [yes/no]
```

---

## Session Integration

**On Session Start**:
- Detect test framework
- Cache framework configuration
- Note any existing test failures

**During Session**:
- Track all file modifications
- Queue tests as changes accumulate
- Run tests at appropriate intervals

**On Session End**:
- Report test status in `/save` output
- Log any unresolved failures
- Update session context with test summary

---

## Quality Metrics Tracking

Track and report:
```text
Session Test Metrics:
- Tests Run: N
- Passed: X
- Failed: Y
- Skipped: Z
- Coverage: XX% (delta: +/-%)
- Failures Fixed: M
```

---

## See Also

- Test command: `/test`
- Progress tracker: `docs/01_progress.md`
- Issues: `docs/02_issues.md`
- Standards: `docs/04_standards.md`
