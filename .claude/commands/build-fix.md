# /build-fix - Diagnose and Fix Build Errors

Incrementally diagnose and fix build errors with minimal changes.

## Trigger

Use `/build-fix` when build or type check fails.

## What This Command Does

1. **Run Build** - Execute build command and capture errors
2. **Parse Errors** - Group by file, sort by severity
3. **Fix Iteratively** - One error at a time
4. **Verify** - Confirm fix doesn't introduce new errors
5. **Report** - Summary of changes made

## Process

### Step 1: Collect Errors

```bash
# Run type check
npx tsc --noEmit --pretty

# Or full build
npm run build
```

### Step 2: Categorize Errors

| Category | Priority | Example |
|----------|----------|---------|
| Build Blocking | Critical | Module not found |
| Type Errors | High | Type mismatch |
| Import Errors | High | Cannot find module |
| Config Errors | Medium | Invalid tsconfig |
| Warnings | Low | Unused variable |

### Step 3: Fix One at a Time

For each error:
1. Show error context (5 lines before/after)
2. Explain the issue
3. Propose fix
4. Apply fix
5. Re-run build
6. Verify error resolved

### Step 4: Safety Checks

**STOP if:**
- Fix introduces new errors
- Same error persists after 3 attempts
- User requests pause

### Step 5: Report

```markdown
## Build Fix Report

**Initial Errors:** 12
**Errors Fixed:** 12
**New Errors:** 0
**Build Status:** PASSING

### Changes Made
1. `src/utils.ts:45` - Added type annotation
2. `src/api.ts:112` - Fixed import path
3. `src/types.ts:8` - Added missing property
```

## Common Error Patterns

### Type Inference Failure
```typescript
// ERROR: Parameter 'x' implicitly has 'any' type
function add(x, y) { return x + y }

// FIX: Add type annotations
function add(x: number, y: number): number { return x + y }
```

### Null/Undefined Errors
```typescript
// ERROR: Object is possibly 'undefined'
const name = user.name.toUpperCase()

// FIX: Optional chaining
const name = user?.name?.toUpperCase() ?? ''
```

### Missing Properties
```typescript
// ERROR: Property 'age' does not exist
interface User { name: string }
const user: User = { name: 'John', age: 30 }

// FIX: Add property to interface
interface User { name: string; age?: number }
```

### Import Errors
```typescript
// ERROR: Cannot find module '@/lib/utils'

// FIX 1: Check tsconfig paths
// FIX 2: Use relative import
// FIX 3: Install missing package
```

## Minimal Diff Strategy

**CRITICAL: Make smallest possible changes**

### DO:
- Add type annotations where missing
- Add null checks where needed
- Fix imports/exports
- Add missing dependencies
- Update type definitions

### DON'T:
- Refactor unrelated code
- Change architecture
- Rename variables (unless causing error)
- Add new features
- Optimize performance

## Language-Specific Commands

### TypeScript/JavaScript
```bash
npx tsc --noEmit              # Type check
npm run build                 # Full build
npx eslint . --fix           # Auto-fix lint
```

### Python
```bash
pyright                       # Type check
python -m py_compile *.py    # Syntax check
ruff check . --fix           # Auto-fix lint
```

### Rust
```bash
cargo check                   # Type check
cargo build                   # Full build
cargo clippy --fix           # Auto-fix lint
```

### Go
```bash
go vet ./...                  # Type check
go build ./...                # Full build
golangci-lint run --fix      # Auto-fix lint
```

## Integration with Protocol

After fixing build errors:
1. Run tests to verify nothing broke
2. If complex fix, consider `/learn` to extract pattern
3. Log in `docs/logs/session_context.md`: "Fixed N build errors"

## Related Commands

- `/test` - Run tests after build fix
- `/precommit` - Full pre-commit checks
- `/quickfix` - Auto-fix linting issues

## Related Agent

For complex build issues, invoke the `build-error-resolver` agent.
See `.claude/agents/build-error-resolver.md`
