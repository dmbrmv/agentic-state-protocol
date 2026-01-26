---
description: "Discover and recommend skills from claude-plugins.dev registry based on project context."
---

# COMMAND: DISCOVER

**Trigger**: User types `/discover` or "discover skills" or "recommend plugins"

---

## Purpose

Automatically analyze your project context and recommend relevant skills, agents, and commands from the claude-plugins.dev community registry. The algorithm matches your tech stack, documented issues, and capability gaps to find the most useful additions.

---

## Actions

### 1. Context Detection

Analyze the current project to understand:

```text
DETECTING PROJECT CONTEXT
══════════════════════════════════════════════════════════════

Scanning project structure...

Tech Stack:
- Primary Language: [detected from manifests/files]
- Frameworks: [detected from dependencies]
- Package Manager: [pip/conda/mamba]

Project Structure:
- Has Tests: [yes/no]
- Has CI/CD: [yes/no]
- Project Type: [cli/webapp/library/data-pipeline]

Existing Protocol Elements:
- Skills: [count] installed
- Commands: [count] defined
- Agents: [count] configured

Documentation Analysis:
- Current Goal: [from docs/01_progress.md]
- Open Issues: [count from docs/02_issues.md]
- Architecture: [patterns from docs/03_architecture.md]
```

### 2. Gap Analysis

Identify capability gaps by comparing:

- Existing skills vs standard capabilities for detected tech stack
- Documented issues that could be addressed by skills
- Project type-specific needs not yet covered

```text
CAPABILITY GAP ANALYSIS
══════════════════════════════════════════════════════════════

Standard Capabilities for [Language]:
✓ Test enforcement (test_enforcer.md)
✓ Architecture validation (arch_enforcer.md)
✓ Context management (context_manager.md)
✗ Security auditing - NOT INSTALLED
✗ API documentation - NOT INSTALLED
? Performance profiling - PARTIAL

Needs from docs/02_issues.md:
- ISSUE-042: "Security review process needed" → Gap: security
- ISSUE-045: "API docs incomplete" → Gap: documentation

Identified Gaps: [count]
```

### 3. Registry Fetch

Retrieve available skills from claude-plugins.dev:

```text
FETCHING REGISTRY
══════════════════════════════════════════════════════════════

Cache Status: [valid/stale/missing]
Last Updated: [timestamp or N/A]

[If stale/missing]:
Fetching fresh data via CLI...
Command: pip search claude-plugins --limit 500

Registry Stats:
- Total Plugins: 10,620+
- Total Skills: 52,909+
- Matching Language: [count]

Candidates after language filter: [count]
```

### 4. Match and Rank

Score each candidate skill using weighted algorithm:

| Factor | Weight | Description |
|--------|--------|-------------|
| Relevance | 30% | Tech stack and framework match |
| Quality | 20% | Stars, installs, freshness |
| Need | 35% | Addresses documented gaps/issues |
| Compatibility | 15% | No conflicts, fits protocol |

### 5. Present Recommendations

```text
SKILL RECOMMENDATIONS
══════════════════════════════════════════════════════════════

Based on your project context:
- Language: [detected] ([frameworks])
- Existing Skills: [count]
- Identified Gaps: [count]

## Critical (Score > 0.8)

### 1. [skill-name] (Score: X.XX)
Package: @owner/repo/skill-name
Category: [skill/agent/command/hook]
Stars: XXk | Installs: XXX

Why recommended:
- [Reason based on gap analysis]
- [Reason based on tech stack match]

Addresses:
- [Gap or issue it resolves]

→ pip install claude-plugins-skill-name

---

## Recommended (Score 0.6-0.8)

### 2. [skill-name] (Score: X.XX)
...

---

## Optional (Score 0.5-0.6)

### 3. [skill-name] (Score: X.XX)
...

══════════════════════════════════════════════════════════════

Actions:
- Install specific: Enter number (1, 2, 3...)
- Install all critical: "install critical"
- Install all: "install all"
- Skip: "none" or "skip"
- More details: "details [number]"
```

### 6. Handle Installation

If user approves installation:

```text
INSTALLING SKILL
══════════════════════════════════════════════════════════════

Running: pip install claude-plugins-skill-name

[Installation output]

✓ Skill installed successfully

Post-install:
- Added to .claude/external_skills.json
- Logged to docs/logs/session_context.md
- [If addresses issue]: Updated docs/02_issues.md

Verify with: /status
```

---

## Options

| Option | Description |
|--------|-------------|
| `--refresh` | Force registry cache refresh |
| `--limit N` | Limit recommendations (default: 10) |
| `--min-score X` | Minimum score threshold (default: 0.5) |
| `--category X` | Filter by category (skills/agents/commands/hooks) |
| `--no-cache` | Skip cache, always fetch fresh |
| `--json` | Output as JSON for scripting |

---

## Integration with Protocol v3.0

This command follows the mandatory loop:

| Phase | Action |
|-------|--------|
| STATE CHECK | Read docs/01_progress.md, 02_issues.md, 03_architecture.md |
| ALIGN | Identify capability gaps from documented needs |
| EXECUTE | Fetch registry, score candidates, present recommendations |
| COMMIT | Log recommendations to session_context.md |

---

## Related Commands

- `/status` - View current project health including installed skills
- `/boot` - Wake up sequence that can trigger skill recommendations
- `/save` - Checkpoint that logs skill changes

---

## Automation Rules

### Auto-Trigger (Optional)

Can be configured to run automatically:
- On `/boot` if `auto_fetch_on_boot: true` in settings
- When new critical issues are added to docs/02_issues.md

### Always Ask Before

- Installing any skill
- Removing/disabling skills
- Modifying skill configurations

### Never Auto

- Install skills without user approval
- Modify existing skill files
- Change protocol-critical configurations

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Registry unreachable | Use cached data or static fallback list |
| CLI not installed | Prompt user to install: `pip install claude-plugins` |
| No matching skills | Suggest broadening search or manual registry browse |
| Installation fails | Show error, suggest manual installation steps |
| Conflict detected | Warn user, require explicit override |

---

## Configuration

Settings in `.claude/settings.local.json`:

```json
{
  "skill_recommender": {
    "enabled": true,
    "cache_ttl_hours": 24,
    "max_recommendations": 10,
    "min_score_threshold": 0.5,
    "auto_fetch_on_boot": false,
    "scoring_weights": {
      "relevance": 0.30,
      "quality": 0.20,
      "need": 0.35,
      "compatibility": 0.15
    },
    "preferred_publishers": ["@anthropics", "@wshobson"],
    "excluded_identifiers": [],
    "install_approval": "ask"
  }
}
```

---

## See Also

- Skill: `skill_recommender.md`
- Tracker: `.claude/external_skills.json`
- Cache: `.claude/cache/registry.json`
- Registry: https://claude-plugins.dev/
