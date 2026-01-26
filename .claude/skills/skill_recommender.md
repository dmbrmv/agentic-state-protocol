# SKILL: Skill Recommender

**Purpose**: Analyze project context and recommend relevant skills from claude-plugins.dev registry based on tech stack, documented needs, and capability gaps.

---

## Trigger Conditions

Use this skill when:
1. User runs `/discover` command
2. User asks "what skills should I install?"
3. User mentions "find plugins" or "recommend skills"
4. During `/boot` if `auto_fetch_on_boot` is enabled
5. When new critical issues are added to `docs/02_issues.md`

---

## Core Logic

### 1. Project Context Detection

**Rule**: Build comprehensive understanding of project before querying registry.

```text
CONTEXT DETECTION STRATEGY
══════════════════════════════════════════════════════════════

Priority 1 - Manifest Files (highest confidence):
┌─────────────────────┬────────────────┬─────────────┐
│ File                │ Language       │ Confidence  │
├─────────────────────┼────────────────┼─────────────┤
│ pyproject.toml      │ Python         │ High        │
│ requirements.txt    │ Python         │ High        │
│ setup.py            │ Python         │ High        │
│ Pipfile             │ Python         │ High        │
│ environment.yml     │ Python (conda) │ High        │
└─────────────────────┴────────────────┴─────────────┘

Priority 2 - File Extension Analysis:
- Count files by extension
- Weight by lines of code
- Weight by recent modifications
- Map extensions to languages

Priority 3 - Documentation Analysis:
- Parse docs/03_architecture.md for tech stack mentions
- Check docs/04_standards.md for language-specific rules
- Review docs/02_issues.md for technology references

Priority 4 - Framework Detection:
- Parse dependency files for known frameworks
- Check for framework config files:
  - django/settings.py → Django
  - fastapi patterns → FastAPI
  - conftest.py → pytest
  - marimo notebooks → marimo
```

**Detection Output Structure**:
```python
ProjectContext(
    primary_language: str,           # "python"
    secondary_languages: list[str],  # Other detected languages
    frameworks: list[str],           # ["fastapi", "sqlalchemy", "pydantic", "xarray"]
    package_manager: str,            # "pip", "conda", "mamba"

    has_tests: bool,                 # tests/ or *_test.* exist
    has_docs: bool,                  # docs/ exists
    has_ci: bool,                    # CI config detected
    project_type: str,               # "cli", "webapp", "library", "api"

    existing_skills: list[str],      # From .claude/skills/
    existing_commands: list[str],    # From .claude/commands/
    existing_agents: list[str],      # From .claude/agents/

    documented_issues: list[Issue],  # From docs/02_issues.md
    architecture: str,               # From docs/03_architecture.md
    current_goal: str,               # From docs/01_progress.md
)
```

### 2. Capability Gap Analysis

**Rule**: Compare existing capabilities against standard expectations for detected stack.

```text
STANDARD CAPABILITIES BY LANGUAGE
══════════════════════════════════════════════════════════════

Python:
├── testing (pytest, unittest)
├── linting (ruff, flake8, pylint)
├── type_checking (mypy, pyright)
├── formatting (black, ruff format)
├── security (bandit, safety)
├── documentation (sphinx, mkdocs)
├── dependency_audit (pip-audit)
├── geospatial (rasterio, geopandas, shapely, fiona)
├── scientific (xarray, numpy, scipy, pandas)
├── notebooks (marimo, jupyter)
└── environment (conda, mamba)
```

**Gap Detection Algorithm**:
```text
For each standard capability:
  1. Check if existing skill covers it
  2. Check if MCP config provides it
  3. Check if hook implements it

  If not covered:
    → Add to gaps list with severity:
      - "critical" if security-related
      - "high" if testing-related
      - "medium" if documentation-related
      - "low" if formatting-related
```

**Issue-Based Gap Detection**:
```text
For each issue in docs/02_issues.md:
  1. Extract keywords from title and description
  2. Map keywords to capability categories:
     - "security", "vulnerability", "audit" → security gap
     - "test", "coverage", "failing" → testing gap
     - "docs", "api", "readme" → documentation gap
     - "slow", "performance", "memory" → profiling gap
     - "deploy", "ci", "pipeline" → devops gap

  3. If severity is critical/high:
     → Create CapabilityGap with high priority
```

### 3. Registry Fetching

**Rule**: Use CLI tool with caching to respect rate limits and robots.txt.

```text
FETCH STRATEGY
══════════════════════════════════════════════════════════════

Step 1: Check Cache
├── Location: .claude/cache/registry.json
├── TTL: 24 hours (configurable)
└── If valid → Use cached data

Step 2: CLI Fetch (if cache invalid)
├── Command: npx claude-plugins search --json --limit 500
├── Timeout: 60 seconds
├── Retry: 3 attempts with exponential backoff
└── Parse JSON output into RegistrySkill objects

Step 3: Fallback Chain
├── If CLI fails → Use stale cache with warning
├── If no cache → Use static fallback list
└── If all fail → Prompt user for manual fetch

Step 4: Update Cache
├── Store fetched data with timestamp
├── Build indices for fast lookup:
│   ├── by_language: dict[str, list[Skill]]
│   ├── by_category: dict[str, list[Skill]]
│   └── by_tag: dict[str, list[Skill]]
└── Save to .claude/cache/registry.json
```

**Registry Skill Model**:
```python
RegistrySkill(
    identifier: str,            # "@owner/repo/name"
    name: str,                  # Human-readable name
    description: str,           # Full description
    category: str,              # "skills", "agents", "commands", "hooks"
    tags: list[str],            # ["python", "testing", "security"]
    supported_languages: list[str],

    stars: int,                 # GitHub stars
    installs: int,              # Download count
    last_updated: datetime,     # Freshness
    verified: bool,             # Official/verified

    dependencies: list[str],    # Required packages
    conflicts_with: list[str],  # Known conflicts
    install_command: str,       # "npx claude-plugins install ..."
)
```

### 4. Matching and Scoring Algorithm

**Rule**: Score each candidate using weighted multi-factor algorithm.

```text
SCORING WEIGHTS (configurable)
══════════════════════════════════════════════════════════════

┌─────────────────┬────────┬─────────────────────────────────┐
│ Factor          │ Weight │ What it measures                │
├─────────────────┼────────┼─────────────────────────────────┤
│ Relevance       │ 30%    │ Tech stack & framework match    │
│ Quality         │ 20%    │ Stars, installs, freshness      │
│ Need            │ 35%    │ Addresses documented gaps       │
│ Compatibility   │ 15%    │ No conflicts, fits protocol     │
└─────────────────┴────────┴─────────────────────────────────┘

Total Score = (R × 0.30) + (Q × 0.20) + (N × 0.35) + (C × 0.15)
```

**Relevance Score (0.0 - 1.0)**:
```text
Components:
├── Language match:
│   ├── Primary language match: +0.40
│   ├── Secondary language match: +0.20
│   └── Generic/universal skill: +0.10
├── Framework match:
│   └── Per matching framework: +0.10 (max 0.30)
├── Tag relevance:
│   └── Per overlapping tag: +0.05 (max 0.20)
└── Project type alignment:
    └── If matches project type: +0.10
```

**Quality Score (0.0 - 1.0)**:
```text
Components:
├── Stars (logarithmic normalization):
│   └── log(stars) / log(50000) × 0.30
├── Installs (logarithmic normalization):
│   └── log(installs) / log(10000) × 0.30
├── Freshness:
│   ├── < 30 days: 0.30
│   ├── 30-180 days: 0.21-0.30 (linear decay)
│   ├── 180-365 days: 0.10-0.21 (steeper decay)
│   └── > 365 days: 0.10 minimum
└── Verified bonus:
    └── If verified: +0.10
```

**Need Score (0.0 - 1.0)**:
```text
For each identified gap:
├── Calculate keyword overlap with skill tags/description
├── If overlap >= 2 keywords:
│   ├── Critical gap: +0.25
│   ├── High gap: +0.15
│   ├── Medium gap: +0.08
│   └── Low gap: +0.04
└── If overlap == 1:
    └── +0.02

Cap at 1.0
```

**Compatibility Score (0.0 - 1.0)**:
```text
Base: 0.60 (no known conflicts)

Deductions:
├── Per explicit conflict: -0.20
├── Per category saturation (>3 same type): -0.05
└── Functional overlap with existing: -0.10

Bonuses:
├── Follows protocol structure: +0.10
├── Has "agentic" or "protocol" tag: +0.10
└── All dependencies satisfied: +0.20
```

### 5. Recommendation Generation

**Rule**: Generate actionable recommendations with clear explanations.

```text
RECOMMENDATION STRUCTURE
══════════════════════════════════════════════════════════════

For each recommended skill:

1. Classification:
   ├── CRITICAL: score > 0.80
   ├── RECOMMENDED: score 0.60-0.80
   └── OPTIONAL: score 0.50-0.60

2. Metadata:
   ├── Package identifier
   ├── Category (skill/agent/command/hook)
   ├── Quality signals (stars, installs)
   └── Install command

3. Explanation:
   ├── Why recommended (tech stack match, gap addressed)
   ├── What gaps it addresses
   └── Potential conflicts (if any)

4. Effort estimation:
   ├── minimal: No dependencies, drop-in
   ├── moderate: Some configuration needed
   └── significant: Dependencies to install
```

### 6. Installation Handling

**Rule**: Install only with user approval, track all installations.

```text
INSTALLATION WORKFLOW
══════════════════════════════════════════════════════════════

1. Pre-install validation:
   ├── Check for conflicts with existing
   ├── Verify dependencies available
   └── Confirm user approval

2. Execute installation:
   ├── Run: npx claude-plugins install <identifier>
   ├── Capture output
   └── Check exit code

3. Post-install tracking:
   ├── Add to .claude/external_skills.json
   ├── Log to docs/logs/session_context.md
   └── If addresses issue: Update docs/02_issues.md

4. Verification:
   ├── Check skill file exists in expected location
   ├── Validate skill format
   └── Report success/failure
```

---

## Data Persistence

### External Skills Tracker

Location: `.claude/external_skills.json`

```json
{
  "installed": [
    {
      "identifier": "@owner/repo/skill-name",
      "installed_at": "2025-01-14T10:30:00Z",
      "version": "1.2.0",
      "installed_by": "recommendation",
      "recommendation_score": 0.87,
      "addresses_gaps": ["security_audit"]
    }
  ],
  "rejected": [
    {
      "identifier": "@owner/rejected-skill",
      "rejected_at": "2025-01-13T15:00:00Z",
      "reason": "user_declined"
    }
  ],
  "cache": {
    "last_registry_fetch": "2025-01-14T09:00:00Z",
    "ttl_hours": 24
  }
}
```

### Registry Cache

Location: `.claude/cache/registry.json`

```json
{
  "fetched_at": "2025-01-14T09:00:00Z",
  "ttl_hours": 24,
  "total_skills": 500,
  "skills": [...],
  "indices": {
    "by_language": {...},
    "by_category": {...},
    "by_tag": {...}
  }
}
```

---

## Automation Rules

### Auto-Run (Implicit Permission)
```text
✓ Detect project context from files
✓ Read existing skills and documentation
✓ Fetch registry (respecting cache TTL)
✓ Calculate scores and generate recommendations
✓ Display recommendations to user
```

### Ask Permission Before
```text
? Installing any skill
? Overriding cache to fetch fresh data
? Installing skills with known conflicts
? Installing more than 3 skills at once
```

### Never Auto
```text
✗ Install skills without user approval
✗ Modify existing skill files
✗ Delete or disable installed skills
✗ Bypass conflict warnings
✗ Send project data to external services
```

---

## Integration with Protocol v3.0

This skill follows the mandatory loop:

| Phase | Action |
|-------|--------|
| STATE CHECK | Read docs/, detect tech stack, list existing skills |
| ALIGN | Identify capability gaps, prioritize needs |
| EXECUTE | Fetch registry, score skills, generate recommendations |
| COMMIT | Log to session_context.md, update external_skills.json |

**Integrates With**:
- `/discover` command (primary trigger)
- `/boot` command (optional auto-trigger)
- `/status` command (shows installed skills)
- `docs/02_issues.md` (gap source, update on resolution)
- `docs/03_architecture.md` (tech stack source)

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Language detection fails | Ask user to specify, check docs/ |
| Registry fetch fails | Use cache, then fallback list |
| CLI not available | Prompt installation instructions |
| No matching skills | Suggest broadening criteria |
| Installation fails | Show error, suggest manual steps |
| Conflict detected | Warn and require explicit override |

---

## See Also

- Command: `/discover`
- Tracker: `.claude/external_skills.json`
- Cache: `.claude/cache/registry.json`
- Registry: https://claude-plugins.dev/
- CLI: https://github.com/Kamalnrf/claude-plugins
