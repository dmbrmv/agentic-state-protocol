---
description: Enforce test-driven development workflow. Scaffold interfaces, generate tests FIRST, then implement minimal code to pass. Ensure 80%+ coverage.
---

# /tdd - Test-Driven Development

This command invokes the TDD methodology to enforce test-first development.

## Trigger

Use `/tdd <description>` when implementing new features or fixing bugs.

## The TDD Cycle

```
RED -> GREEN -> REFACTOR -> REPEAT

RED:      Write a failing test
GREEN:    Write minimal code to pass
REFACTOR: Improve code, keep tests passing
REPEAT:   Next feature/scenario
```

## What This Command Does

1. **Scaffold Interfaces** - Define types/interfaces first
2. **Generate Tests First** - Write failing tests (RED)
3. **Implement Minimal Code** - Write just enough to pass (GREEN)
4. **Refactor** - Improve code while keeping tests green
5. **Verify Coverage** - Ensure 80%+ test coverage

## When to Use

- Implementing new features
- Adding new functions/components
- Fixing bugs (write test that reproduces bug first)
- Refactoring existing code
- Building critical business logic

## Process

### Step 1: Define Interface (SCAFFOLD)

```typescript
// Define types before implementation
export interface InputData {
  field1: string
  field2: number
}

export function processData(input: InputData): Result {
  throw new Error('Not implemented')
}
```

### Step 2: Write Failing Test (RED)

```typescript
describe('processData', () => {
  it('should process valid input correctly', () => {
    const input = { field1: 'test', field2: 42 }

    const result = processData(input)

    expect(result.success).toBe(true)
  })

  it('should handle edge case: empty field', () => {
    const input = { field1: '', field2: 0 }

    const result = processData(input)

    expect(result.success).toBe(false)
  })
})
```

### Step 3: Run Tests - Verify FAIL

```bash
npm test path/to/test.ts
# Tests should FAIL - implementation doesn't exist yet
```

### Step 4: Implement Minimal Code (GREEN)

```typescript
export function processData(input: InputData): Result {
  if (!input.field1) {
    return { success: false, error: 'field1 required' }
  }
  return { success: true, data: transform(input) }
}
```

### Step 5: Run Tests - Verify PASS

```bash
npm test path/to/test.ts
# All tests should PASS now
```

### Step 6: Refactor (IMPROVE)

- Extract constants
- Improve naming
- Reduce duplication
- Keep tests green

### Step 7: Check Coverage

```bash
npm test -- --coverage
# Verify 80%+ coverage
```

## Coverage Requirements

| Type | Minimum | Required For |
|------|---------|--------------|
| Unit Tests | 80% | All code |
| Integration | Critical paths | APIs, DB |
| E2E | Happy paths | User flows |

### 100% Coverage Required For:
- Financial calculations
- Authentication logic
- Security-critical code
- Core business logic

## Test Structure (AAA Pattern)

```typescript
it('should do something specific', () => {
  // Arrange - Set up test data
  const input = createTestInput()

  // Act - Execute the code under test
  const result = functionUnderTest(input)

  // Assert - Verify the outcome
  expect(result).toEqual(expectedOutput)
})
```

## TDD Best Practices

### DO:
- Write the test FIRST, before any implementation
- Run tests and verify they FAIL before implementing
- Write minimal code to make tests pass
- Refactor only after tests are green
- Add edge cases and error scenarios
- Test behavior, not implementation details

### DON'T:
- Write implementation before tests
- Skip running tests after each change
- Write too much code at once
- Ignore failing tests
- Mock everything (prefer integration tests)
- Test private methods directly

## Edge Cases to Always Test

1. **Null/Undefined** - What if input is null?
2. **Empty** - What if array/string is empty?
3. **Invalid Types** - What if wrong type passed?
4. **Boundaries** - Min/max values
5. **Errors** - Network failures, database errors
6. **Race Conditions** - Concurrent operations
7. **Large Data** - Performance with many items
8. **Special Characters** - Unicode, SQL characters

## Integration with Protocol

Before marking task as `/done`:
1. Verify 80%+ coverage with `/test-coverage`
2. All tests must pass
3. Log in `docs/logs/session_context.md`: "TDD session complete for [feature]"

## Commit Gate

**STRICT MODE**: Commits are blocked without tests.

```bash
# Pre-commit hook checks:
1. Coverage >= 80%
2. All tests pass
3. No skipped tests (.skip, .only)
```

## Related Commands

- `/test` - Run tests with analysis
- `/test-coverage` - Coverage report with gaps
- `/build-fix` - Fix build errors
- `/review` - Code review with TDD awareness

## Related Agent

This command may invoke the `tdd-guide` agent for complex implementations.
See `.claude/agents/tdd-guide.md`
