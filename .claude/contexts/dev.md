# Development Context

**Mode**: Active development
**Focus**: Implementation, coding, building features

## Behavior

- Write code first, explain after
- Prefer working solutions over perfect solutions
- Run tests after changes
- Keep commits atomic
- Follow TDD when implementing new features

## Priorities

1. Get it working
2. Get it right
3. Get it clean

## Tools to Favor

- Edit, Write for code changes
- Bash for running tests/builds
- Grep, Glob for finding code
- Task with agents for complex work

## TDD Integration

When implementing new features:
1. Define interface first
2. Write failing tests
3. Implement minimal code
4. Run tests to verify
5. Refactor if needed

## Protocol Compliance

Before completing work:
- Run tests: `/test`
- Check coverage: `/test-coverage` (must be >= 80%)
- Update docs if architecture changed
- Log progress in session context

## Quick Commands

| Command | Use When |
|---------|----------|
| `/tdd` | Starting new feature |
| `/test` | After code changes |
| `/build-fix` | Build fails |
| `/quickfix` | Lint issues |
| `/done` | Task complete |

## Focus Areas

- Functionality over perfection
- Tests alongside code
- Small, focused commits
- Clear variable names
- Minimal complexity
