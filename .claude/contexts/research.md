# Research Context

**Mode**: Exploration, investigation, learning
**Focus**: Understanding before acting

## Behavior

- Read widely before concluding
- Ask clarifying questions
- Document findings as you go
- Don't write code until understanding is clear
- Preserve existing code (read-only exploration)

## Research Process

1. **Understand the question** - Clarify what we're investigating
2. **Explore relevant code/docs** - Read broadly, not narrowly
3. **Form hypothesis** - What do we think is happening?
4. **Verify with evidence** - Confirm with code/logs/tests
5. **Summarize findings** - Clear, actionable conclusions

## Tools to Favor

- Read for understanding code
- Grep, Glob for finding patterns
- WebSearch, WebFetch for external docs
- Task with Explore agent for codebase questions

## Tools to Avoid

- Write, Edit (no code changes in research mode)
- Bash commands that modify state
- Any destructive operations

## Output Format

Findings first, recommendations second:

```markdown
## Research: [Topic]

### Question
[What we're investigating]

### Findings
1. [Finding 1 with evidence]
2. [Finding 2 with evidence]
3. [Finding 3 with evidence]

### Relevant Files
- `path/to/file.ts:45` - [why relevant]
- `path/to/other.ts:120` - [why relevant]

### Conclusions
[Summary of what we learned]

### Recommendations
[What to do next, if applicable]
```

## Integration with Protocol

After research:
1. Document findings in `docs/logs/session_context.md`
2. If architectural insight, update `docs/03_architecture.md`
3. If issue found, log in `docs/02_issues.md`
4. Consider `/learn` if pattern discovered

## When to Use Research Context

- Investigating bugs
- Understanding unfamiliar code
- Evaluating libraries/approaches
- Planning before implementation
- Auditing security/performance
- Onboarding to new codebase

## Research Best Practices

- Cast a wide net initially
- Follow the data, not assumptions
- Document dead ends (they're valuable)
- Link to specific line numbers
- Note version numbers and dates
- Separate facts from interpretations
