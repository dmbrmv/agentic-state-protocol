# Agentic State Protocol v3.0 - Master Index

**Protocol Version**: 3.0 (Agentic Development)
**Repository**: Initialized with `init_project.py`

---

## I. PROTOCOL MANDATE

**You are the Project State Manager.** Your sole function is to advance the project state stored in `docs/`.

### Core Rules (IMMUTABLE)

1. **NO STATE AMNESIA**: Read `docs/01_progress.md` at the start of EVERY session
2. **NO SILENT ACTIONS**: Verify the "Active Task" before modifying code
3. **DOCS = CODE**: Code changes are incomplete without documentation updates
4. **DIRECTORY AUTHORITY**: `docs/` is the single source of truth

### Mandatory Loop (EXECUTE EVERY REQUEST)

```text
1. STATE CHECK -> Read docs/01_progress.md
2. ALIGN       -> Output: [STATE] Active Task: <name>
                          [MODE] Execution | Planning | Refactoring
3. EXECUTE     -> Perform the work
4. COMMIT      -> Update docs/01_progress.md + docs/logs/session_context.md
```

---

## II. DOCUMENTATION STRUCTURE

```
docs/
├── 00_MASTER_INDEX.md      <- You are here (protocol entry point)
├── 01_progress.md          <- START HERE: Tasks, backlog, metrics
├── 02_issues.md            <- Issues & technical debt registry
├── 03_architecture.md      <- System design & architecture
├── 04_standards.md         <- Coding, git, testing standards (LAW)
├── 05_guides.md            <- Environment setup, workflows
│
├── logs/                   # Session memory
│   └── session_context.md  <- Session history and decisions
│
└── reference/              # Read-only historical docs (optional)
```

### Reading Order

1. **`01_progress.md`** - Current state, active task, backlog
2. **`02_issues.md`** - Known issues and blockers
3. **`03_architecture.md`** - How the system works
4. **`04_standards.md`** - How to write code (LAW)
5. **`05_guides.md`** - How to use the environment

---

## III. MACRO TRIGGERS

When user types these keywords, execute immediately:

### **"BOOT"** or `/boot`
```text
1. READ docs/01_progress.md + docs/02_issues.md
2. REPORT: "Current Goal: [X] | Active Task: [Y] | Open Issues: [N]"
3. ASK: "Proceed?"
```

### **"DONE"** or `/done`
```text
1. UPDATE docs/01_progress.md (mark task complete)
2. LOG to docs/logs/session_context.md
3. PROPOSE next task from Backlog
```

### **"SAVE"** or `/save`
```text
1. SYNC all docs/ files to match current reality
2. WRITE "Checkpoint" entry in docs/logs/session_context.md
```

---

## IV. DECISION AUTHORITY HIERARCHY

When conflicts arise:

1. **`docs/01_progress.md`** - Active task definition
2. **`docs/04_standards.md`** - Coding standards (LAW)
3. **`docs/03_architecture.md`** - Technical design
4. **`CLAUDE.md`** - High-level agent instructions
5. **Training data** - General AI knowledge (lowest)

---

## V. CLI COMMANDS (Claude Code)

Available commands via `.claude/commands/`:

### Core Session Commands
| Command | Purpose |
|---------|---------|
| `/boot` | Wake up: Load state, summarize context |
| `/save` | Shutdown: Update docs, log checkpoint, suggest commit |
| `/done` | Complete task: Mark done, propose next |
| `/feature <name>` | New feature: Plan before coding |
| `/refine <prompt>` | Clarify: Turn vague request into actionable prompt |

### Development Automation
| Command | Purpose |
|---------|---------|
| `/test` | Run tests with smart failure analysis and fix suggestions |
| `/review` | Code review: architecture, standards, security checks |
| `/debug <issue>` | Structured debugging with root cause analysis |
| `/status` | Project health dashboard: git, tests, docs, dependencies |

### Multi-Agent Coordination
| Command | Purpose |
|---------|---------|
| `/delegate <task>` | Spawn parallel Claude agents for subtasks |
| `/sync` | Merge work from parallel agent sessions |

---

## VI. SKILLS (Auto-Enforced)

Available skills via `.claude/skills/`:

### Core Skills
| Skill | Purpose |
|-------|---------|
| `context_manager` | Keep docs synchronized with code changes |
| `arch_enforcer` | Enforce architecture and coding standards |

### Extended Skills
| Skill | Purpose |
|-------|---------|
| `test_enforcer` | Auto-run tests after code changes, suggest fixes |
| `parallel_coordinator` | Manage multi-agent delegation with checkpoints |
| `dependency_tracker` | Track deps, security audit, compatibility check |
| `verifier` | Ensure work quality through verification levels |
| `skill_recommender` | Analyze context and recommend skills from registry |

---

## VII. PROJECT QUICK FACTS

| Item | Value |
|------|-------|
| **Project Name** | (see CLAUDE.md) |
| **Tech Stack** | (see CLAUDE.md) |
| **Environment** | (see docs/05_guides.md) |
| **Current Goal** | (see docs/01_progress.md) |

---

## VIII. FILE SYSTEM MAP

```
project/
├── docs/                   # STATE MANAGEMENT (this folder)
├── src/                    # Source code
├── tests/                  # Test suite
├── scripts/                # Utility scripts
├── configs/                # Configuration files
└── .claude/                # Claude Code commands & skills
    ├── commands/           # CLI commands
    └── skills/             # Auto-enforced behaviors
```

---

## IX. MULTI-AGENT COORDINATION

The protocol supports spawning parallel Claude Task agents for complex work.

### Delegation Model
- **Supervised Autonomy**: All agent work requires human approval before merge
- **Scoped Boundaries**: Each agent has explicit file/module boundaries
- **Checkpoint Requirements**: Agents must checkpoint before completion
- **Conflict Resolution**: Human resolves any conflicts between agents

### Delegation Workflow
```text
1. /delegate <task>  -> Decompose and spawn agents
2. Agents work in parallel on subtasks
3. /sync --status    -> Check agent progress
4. /sync             -> Review and merge completed work
```

### State Files
- `docs/06_multi_agent.md` - Multi-agent coordination overview
- `docs/logs/delegation_registry.md` - Active delegation tracking

---

## X. TESTING AND QUALITY

### Automated Testing
The `test_enforcer` skill automatically:
- Runs affected tests after code changes
- Analyzes failures and suggests fixes
- Enforces coverage thresholds before `/done`

### Code Review
The `/review` command checks:
- Architecture alignment (`docs/03_architecture.md`)
- Coding standards compliance (`docs/04_standards.md`)
- Security best practices (secrets, injection, etc.)
- Test coverage

### Dependency Management
The `dependency_tracker` skill monitors:
- Package vulnerabilities (security audit)
- Outdated dependencies
- License compliance
- Compatibility issues

---

## XI. CRITICAL ENGAGEMENT PROTOCOL

The agent operates under a critical engagement protocol that prioritizes **long-term correctness over short-term agreement**:

- **Challenge before implementing** — if a better approach exists, state it before writing code
- **No sycophancy** — banned phrases include "Excellent!", "Great idea!", "Perfect!"
- **Flag reinvented wheels** — mention standard solutions, even unprompted
- **Resist scope creep** — ask "What does this solve that the simpler version doesn't?"
- **Scale pushback to consequences** — forceful objection for approaches causing data corruption or architectural dead-ends
- **Flag technical debt explicitly** — especially in pipeline code where issues compound

See `CLAUDE.md` Section X for the full 12-rule protocol.

---

## XII. MCP CONFIGURATIONS

MCP server configurations in `.claude/mcp/`:

| Config | Purpose |
|--------|---------|
| `test_runners.json` | pytest, unittest, make test |
| `linters.json` | ruff, pylint, mypy, pyright |
| `dependency_auditors.json` | pip-audit, safety, pip-licenses |

### Test Runners (`test_runners.json`)
Configures test framework integrations with auto-detection:
- **pytest** (Python): Coverage support, verbose output, parallel execution
- **unittest** (Python): Standard library test runner
- **make test**: Generic Makefile-based testing

### Linters (`linters.json`)
Configures linter and formatter integrations:
- **ruff**: Lint + format (primary)
- **pylint**: Deep analysis
- **mypy**: Type checking (gradual typing)
- **pyright**: Type checking (strict)

### Dependency Auditors (`dependency_auditors.json`)
Configures security and dependency management:
- **Security**: pip-audit, safety
- **Outdated**: pip list --outdated
- **Licenses**: pip-licenses

---

## XIII. SUBAGENTS

Specialized agents in `.claude/agents/` for delegated tasks:

| Agent | Purpose | Model |
|-------|---------|-------|
| `code-simplifier` | Simplify and clean up code after implementation | sonnet |
| `verify-app` | End-to-end application verification | sonnet |
| `security-auditor` | Security-focused code review (read-only) | sonnet |
| `background-verifier` | Long-running verification (cost-effective) | haiku |
| `notebook-verifier` | Marimo notebook verification (reproducibility, execution) | sonnet |

### Usage

Subagents are invoked automatically or via commands:
- `verify-app`: Auto-triggered before `/done`
- `security-auditor`: Triggered via `/review --security`
- `background-verifier`: Triggered via `/verify-background`
- `notebook-verifier`: After notebook changes or before publishing
- `code-simplifier`: Manually invoked after feature completion

---

## XIV. HOOKS

Automated behaviors via `.claude/hooks/`:

### PostToolUse Hooks
| Hook | Trigger | Purpose |
|------|---------|---------|
| `format-code.sh` | Edit, Write | Auto-format code after changes |
| `markdown-formatter.py` | Edit, Write | Fix markdown formatting |

### PreToolUse Hooks
| Hook | Trigger | Purpose |
|------|---------|---------|
| `security-check.sh` | Write, Edit, Bash | Block dangerous operations |
| `validate-changes.sh` | Bash (git commit) | Validate before commits |

### Stop Hooks
- Verify all tasks complete before stopping
- Check for unresolved errors

### SubagentStop Hooks
- Evaluate verification agent findings
- Ensure issues are addressed before proceeding

---

## XV. INNER-LOOP COMMANDS

Fast workflow commands with pre-computed context:

| Command | Purpose |
|---------|---------|
| `/commit-push-pr <msg>` | Quick commit, push, and create PR |
| `/quickfix` | Auto-fix linting issues on changed files |
| `/precommit` | Run all pre-commit checks (lint, format, test, type) |
| `/investigate <issue>` | Deep investigation with full context |
| `/verify-background` | Run verification in background |
| `/browser-test <action>` | Test web UI in Chrome browser |

### Pre-computed Context

These commands use inline bash (`!` prefix) to gather context before execution:
```markdown
Current branch: !`git branch --show-current`
Git status: !`git status --short`
```

---

## XVI. VERIFICATION WORKFLOWS

The `verifier` skill ensures work quality:

### Verification Levels
| Level | Files Changed | Checks |
|-------|---------------|--------|
| Minimal | 1-3 | Affected tests only |
| Standard | 4-10 | Build + Tests + Lint + Types |
| Full | 11+ | Everything + Security audit |

### Automatic Triggers
- Before `/done` command
- Before `/commit-push-pr`
- After bug fixes

### Manual Triggers
- `/verify-background` for comprehensive background check
- `/precommit` for pre-commit validation

---

## XVII. AUTONOMOUS EXECUTION

See `docs/07_autonomous.md` for detailed configuration.

### Permission Modes
| Mode | Description |
|------|-------------|
| `default` | Ask for approval on dangerous operations |
| `acceptEdits` | Auto-approve file edits |
| `dontAsk` | Minimal prompts (caution advised) |
| `plan` | Read-only exploration mode |

### Auto-Approved Operations
- Read operations (files, git status)
- Linters and formatters
- Test execution
- Code analysis

### Requires Approval
- Git commits and pushes
- Package installations
- File deletions
- External API calls

---

## XVIII. FILE SYSTEM MAP (EXTENDED)

```
project/
├── docs/                   # STATE MANAGEMENT
│   ├── 00_MASTER_INDEX.md  # Protocol entry point
│   ├── 01_progress.md      # Current state
│   ├── 02_issues.md        # Issue tracking
│   ├── 03_architecture.md  # System design
│   ├── 04_standards.md     # Coding standards
│   ├── 05_guides.md        # Environment guides
│   ├── 06_multi_agent.md   # Multi-agent overview (see Section IX)
│   ├── 07_autonomous.md    # Autonomous execution guide (see Section XVI)
│   └── logs/               # Session memory
│
├── src/                    # Source code
├── tests/                  # Test suite
├── scripts/                # Utility scripts
├── configs/                # Configuration files
│
└── .claude/                # Claude Code configuration
    ├── commands/           # CLI commands (18 total)
    │   ├── boot.md, save.md, done.md
    │   ├── feature.md, refine.md, discover.md
    │   ├── test.md, review.md, debug.md, status.md
    │   ├── delegate.md, sync.md
    │   ├── commit-push-pr.md, quickfix.md, precommit.md
    │   ├── investigate.md, verify-background.md, browser-test.md
    │   │
    ├── skills/             # Auto-enforced behaviors (7 total)
    │   ├── context_manager.md, arch_enforcer.md
    │   ├── test_enforcer.md, parallel_coordinator.md
    │   ├── dependency_tracker.md, verifier.md, skill_recommender.md
    │   │
    ├── agents/             # Specialized subagents (5 total)
    │   ├── code-simplifier.md, verify-app.md
    │   ├── security-auditor.md, background-verifier.md
    │   └── notebook-verifier.md
    │   │
    ├── hooks/              # Automation hooks (4 total)
    │   ├── format-code.sh, markdown-formatter.py
    │   ├── validate-changes.sh, security-check.sh
    │   │
    ├── mcp/                # MCP configurations
    │   ├── test_runners.json
    │   ├── linters.json
    │   └── dependency_auditors.json
    │
    └── settings.local.json # Local settings (from template)
```

---

**REMEMBER**: Before doing ANY work, read `docs/01_progress.md` to verify the active task.

**NEXT STEP**: Read `docs/01_progress.md` now.
