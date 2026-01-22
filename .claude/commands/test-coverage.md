# /test-coverage - Coverage Analysis and Gap Identification

Analyze test coverage and identify gaps that need tests.

## Trigger

Use `/test-coverage` to analyze coverage and find undertested code.

## What This Command Does

1. **Run Coverage** - Execute tests with coverage reporting
2. **Analyze Report** - Parse coverage data
3. **Identify Gaps** - Find files below 80% threshold
4. **Generate Tests** - Create tests for uncovered paths
5. **Verify** - Ensure coverage meets requirements

## Process

### Step 1: Run Coverage Report

```bash
# JavaScript/TypeScript
npm test -- --coverage

# Python
pytest --cov=src --cov-report=html

# Rust
cargo tarpaulin --out html

# Go
go test -coverprofile=coverage.out ./...
```

### Step 2: Parse Coverage Data

```bash
# Read coverage summary
cat coverage/coverage-summary.json

# Or HTML report
open coverage/lcov-report/index.html
```

### Step 3: Identify Under-Covered Files

```markdown
## Coverage Report

| File | Statements | Branches | Functions | Lines |
|------|------------|----------|-----------|-------|
| src/api.ts | 65% | 50% | 70% | 65% |
| src/utils.ts | 92% | 88% | 95% | 92% |
| src/auth.ts | 45% | 30% | 50% | 45% |

### Files Below 80% Threshold
1. `src/auth.ts` - 45% (CRITICAL - auth code needs 100%)
2. `src/api.ts` - 65%
```

### Step 4: Analyze Uncovered Paths

For each under-covered file:
1. Identify untested functions
2. Find missing branch coverage
3. List error paths not tested
4. Note edge cases not covered

### Step 5: Generate Missing Tests

```typescript
// Identified gap: error handling in auth.ts:45-60

describe('authenticate', () => {
  it('should handle invalid token', async () => {
    const result = await authenticate('invalid-token')
    expect(result.success).toBe(false)
    expect(result.error).toBe('Invalid token')
  })

  it('should handle expired token', async () => {
    const expiredToken = createExpiredToken()
    const result = await authenticate(expiredToken)
    expect(result.success).toBe(false)
    expect(result.error).toBe('Token expired')
  })
})
```

## Coverage Requirements

### Standard Requirements

| Type | Threshold | Notes |
|------|-----------|-------|
| Statements | 80% | All executable statements |
| Branches | 80% | All if/else paths |
| Functions | 80% | All declared functions |
| Lines | 80% | All code lines |

### Critical Code Requirements (100%)

These require 100% coverage:
- Authentication/Authorization
- Financial calculations
- Security validation
- Core business logic
- Data encryption/decryption

## What to Test

### Happy Path
- Normal, expected usage
- Valid inputs
- Successful operations

### Error Handling
- Invalid inputs
- Network failures
- Database errors
- Permission denied

### Edge Cases
- Empty inputs
- Null/undefined
- Boundary values (0, -1, MAX_INT)
- Large datasets

### Security Cases
- SQL injection attempts
- XSS payloads
- Authentication bypass
- Authorization violations

## Output Format

```markdown
# Coverage Analysis Report

**Date:** YYYY-MM-DD
**Overall Coverage:** 78%
**Target:** 80%
**Status:** BELOW THRESHOLD

## Summary

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Statements | 78% | 80% | FAIL |
| Branches | 72% | 80% | FAIL |
| Functions | 85% | 80% | PASS |
| Lines | 78% | 80% | FAIL |

## Files Needing Tests

### 1. src/auth.ts (45% -> needs 100%)

**Untested Functions:**
- `validateSession()` - lines 45-60
- `refreshToken()` - lines 72-85

**Missing Branch Coverage:**
- Line 48: else branch (token invalid)
- Line 75: catch block (refresh failed)

**Recommended Tests:**
```typescript
// Test for validateSession error path
it('should reject invalid session', () => {
  // ...
})
```

### 2. src/api.ts (65% -> needs 80%)

[Similar analysis...]

## Action Items

1. [ ] Add tests for auth.ts validateSession
2. [ ] Add tests for auth.ts refreshToken
3. [ ] Add error path tests for api.ts
4. [ ] Re-run coverage to verify 80%+

## After Coverage Increase

**New Coverage:** 85%
**Status:** PASSING
```

## Integration with Protocol

Before `/done`:
1. Coverage must be >= 80%
2. Critical code must be 100%
3. Log in session context: "Coverage: X% (target: 80%)"

## Configuration

Coverage thresholds are defined in `.claude/settings.local.json`:

```json
{
  "testing": {
    "coverageThreshold": 80,
    "blockDoneOnFailure": true
  }
}
```

## Commit Gate

**STRICT MODE**: Coverage gate blocks commits.

```bash
# Pre-commit hook verifies:
1. Overall coverage >= 80%
2. No file below 60%
3. Critical files at 100%
```

## Related Commands

- `/tdd` - Write tests first
- `/test` - Run tests with analysis
- `/precommit` - Pre-commit checks

## Tips for Improving Coverage

1. **Focus on behavior, not lines** - Cover meaningful scenarios
2. **Test error paths** - They're often missed
3. **Mock external dependencies** - Isolate code under test
4. **Use parameterized tests** - Cover multiple inputs efficiently
5. **Review coverage report** - Red lines show exactly what's missing
