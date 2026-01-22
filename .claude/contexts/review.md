# Code Review Context

**Mode**: PR review, code analysis
**Focus**: Quality, security, maintainability

## Behavior

- Read thoroughly before commenting
- Prioritize issues by severity
- Suggest fixes, don't just point out problems
- Check for security vulnerabilities
- Verify test coverage

## Review Checklist

### Critical (Must Fix)
- [ ] Security vulnerabilities (injection, auth bypass, secrets)
- [ ] Data loss potential
- [ ] Breaking changes without migration
- [ ] Race conditions

### High (Should Fix)
- [ ] Logic errors
- [ ] Missing error handling
- [ ] Unvalidated inputs
- [ ] Missing tests for new code
- [ ] Performance regressions

### Medium (Consider Fixing)
- [ ] Code duplication
- [ ] Unclear naming
- [ ] Missing documentation
- [ ] Inconsistent patterns

### Low (Nice to Have)
- [ ] Style improvements
- [ ] Minor optimizations
- [ ] Additional edge case tests

## Review Process

1. **Understand the PR** - Read description, linked issues
2. **Review architecture** - Does design make sense?
3. **Check implementation** - Line-by-line review
4. **Verify tests** - Coverage adequate?
5. **Security scan** - Any vulnerabilities?
6. **Summarize findings** - Grouped by severity

## Output Format

```markdown
# Code Review: [PR Title / Feature]

## Summary
[Brief overview of the changes and overall assessment]

## Critical Issues
### 1. [Issue Title]
**File:** `path/to/file.ts:45`
**Severity:** Critical
**Issue:** [Description]
**Fix:**
```typescript
// Suggested fix
```

## High Priority
### 1. [Issue Title]
...

## Medium Priority
### 1. [Issue Title]
...

## Low Priority / Suggestions
- [Suggestion 1]
- [Suggestion 2]

## Test Coverage
- Current: X%
- New code covered: Yes/No
- Missing tests: [List if any]

## Security Check
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Auth checks in place
- [ ] SQL injection protected
- [ ] XSS protected

## Verdict
[ ] Approve
[ ] Request Changes
[ ] Comment Only
```

## Security Review Focus

### Check For:
- Hardcoded credentials/API keys
- SQL injection vulnerabilities
- XSS vulnerabilities
- CSRF vulnerabilities
- Insecure deserialization
- Authentication bypasses
- Authorization failures
- Sensitive data exposure
- Security misconfigurations

### Common Patterns to Flag:
```typescript
// BAD: SQL injection
query(`SELECT * FROM users WHERE id = ${userId}`)

// BAD: XSS
element.innerHTML = userInput

// BAD: Hardcoded secret
const API_KEY = "sk-live-abc123"

// BAD: Missing auth check
app.get('/admin', (req, res) => { /* no auth */ })
```

## TDD Review Criteria

When reviewing code that should have tests:
- Are tests written before implementation? (check commit order)
- Is coverage >= 80%?
- Are edge cases covered?
- Are error paths tested?
- Do test names describe behavior?

## Integration with Protocol

After review:
1. Log review in `docs/logs/session_context.md`
2. If security issue, add to `docs/02_issues.md` with HIGH priority
3. If architectural concern, note in review and reference `docs/03_architecture.md`

## Review Best Practices

- Be specific, not vague
- Explain why, not just what
- Offer solutions, not just problems
- Distinguish must-fix from nice-to-have
- Acknowledge good code too
- Be respectful and constructive
