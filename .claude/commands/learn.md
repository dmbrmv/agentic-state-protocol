# /learn - Extract Reusable Patterns

Extract valuable patterns from the current session and save them to user-global skills.

## Trigger

Run `/learn` at any point during a session when you've solved a non-trivial problem.

## Purpose

The `/learn` command bridges project-level memory (docs/) with user-level memory (~/.claude/skills/learned/). While the Agentic State Protocol maintains project-specific state in documentation, learned patterns are cross-project reusable skills.

## What to Extract

Look for:

### 1. Error Resolution Patterns
- What error occurred?
- What was the root cause?
- What fixed it?
- Is this reusable for similar errors?

### 2. Debugging Techniques
- Non-obvious debugging steps
- Tool combinations that worked
- Diagnostic patterns

### 3. Workarounds
- Library quirks
- API limitations
- Version-specific fixes

### 4. Project-Specific Patterns
- Codebase conventions discovered
- Architecture decisions made
- Integration patterns

## Output Location

Skills are saved to user-global location for cross-project reuse:

```
~/.claude/skills/learned/[pattern-name].md
```

## Output Format

```markdown
# [Descriptive Pattern Name]

**Extracted:** [Date]
**Context:** [Brief description of when this applies]
**Source Project:** [Project name where discovered]

## Problem
[What problem this solves - be specific]

## Solution
[The pattern/technique/workaround]

## Example
[Code example if applicable]

## When to Use
[Trigger conditions - what should activate this skill]

## Related
[Links to docs, issues, or other skills]
```

## Process

1. Review the session for extractable patterns
2. Identify the most valuable/reusable insight
3. Draft the skill file
4. Present to user for confirmation
5. Save to `~/.claude/skills/learned/`
6. Log extraction in `docs/logs/session_context.md`

## Extraction Criteria

### DO Extract:
- Fixes that took significant investigation
- Non-obvious solutions
- Framework/library quirks
- Integration patterns
- Performance optimizations
- Security patterns

### DON'T Extract:
- Trivial fixes (typos, simple syntax errors)
- One-time issues (specific API outages)
- Project-specific business logic
- Temporary workarounds with planned fixes

## Example Usage

```
User: /learn

Agent:
# Session Pattern Analysis

## Extractable Pattern Found

**Pattern**: React 19 + Next.js 15 Server Component Hydration Fix

**Problem**: Server components were causing hydration mismatches when using
Date objects due to timezone differences between server and client.

**Solution**: Convert dates to ISO strings in server components and parse
on client, or use suppressHydrationWarning for purely display timestamps.

**Reusability**: HIGH - This applies to any Next.js 15 + React 19 project
with date handling in server components.

---

Save this pattern to ~/.claude/skills/learned/nextjs15-date-hydration.md?
```

## Integration with Protocol

After extracting a pattern:
1. Log in `docs/logs/session_context.md`: "Extracted pattern: [name]"
2. If pattern reveals architectural insight, consider updating `docs/03_architecture.md`
3. If pattern reveals coding standard, consider updating `docs/04_standards.md`

## Notes

- Keep skills focused - one pattern per skill
- Use descriptive names (nextjs15-date-hydration, not fix-1)
- Include version numbers when relevant
- Update existing skills rather than creating duplicates
