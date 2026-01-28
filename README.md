# Agentic State Protocol v3.0

A framework for disciplined AI-assisted software development with persistent state, documentation-as-code, and structured workflows.

## Table of Contents

- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Quick Start](#quick-start)
- [What You Get](#what-you-get)
- [Core Principles](#core-principles)
- [Supported Tech Stacks](#supported-tech-stacks)
- [Architecture Patterns](#architecture-patterns)
- [Example Workflow](#example-workflow)
- [Advanced Features](#advanced-features)
- [Requirements](#requirements)
- [Contributing](#contributing)

## The Problem

AI coding assistants suffer from **context amnesia** - each session starts fresh, losing all project knowledge. This leads to:
- Repeated mistakes across sessions
- Inconsistent code changes
- Documentation that drifts from reality
- Forgotten decisions and their rationale

## The Solution

The Agentic State Protocol solves this by treating **documentation as the persistent memory** for AI agents:

1. **State lives in `docs/`** - A structured documentation folder that the AI reads at the start of every session
2. **Mandatory loop** - Every request follows: STATE CHECK → ALIGN → EXECUTE → COMMIT
3. **Immutable rules** - Core behaviors that cannot be overridden
4. **Macro commands** - Quick triggers for common workflows (/boot, /save, /done)

## Quick Start

### Option 1: Add to Existing Project (Recommended)

**One-liner installation:**
```bash
curl -sL https://raw.githubusercontent.com/dmbrmv/agentic-state-protocol/main/adopt.sh | bash
```

**Or with options:**
```bash
# Minimal: only .claude/ folder (commands, skills, agents)
curl -sL https://raw.githubusercontent.com/dmbrmv/agentic-state-protocol/main/adopt.sh | bash -s -- --minimal

# Full: includes documentation templates (default)
curl -sL https://raw.githubusercontent.com/dmbrmv/agentic-state-protocol/main/adopt.sh | bash -s -- --full
```

### Option 2: Manual Installation

Copy the `.claude/` folder to your existing project:

```bash
# Clone temporarily
git clone --depth 1 https://github.com/dmbrmv/agentic-state-protocol.git /tmp/asp

# Copy .claude folder to your project
cp -r /tmp/asp/.claude /path/to/your/project/

# (Optional) Copy documentation templates
cp -r /tmp/asp/docs /path/to/your/project/
cp /tmp/asp/CLAUDE.md.template /path/to/your/project/

# Clean up
rm -rf /tmp/asp
```

**What you get:**
```
.claude/
├── commands/      # 22 CLI commands (/boot, /tdd, /review, etc.)
├── skills/        # 7 auto-enforced behaviors
├── agents/        # 8 specialized subagents
├── contexts/      # 3 working modes (dev, research, review)
├── hooks/         # 5 automation hooks
└── mcp/           # MCP server configurations
```

### Option 3: New Project from Template

**Use as GitHub Template:**
1. Click "Use this template" on GitHub
2. Clone your new repository
3. Run the setup wizard:
   ```bash
   python init_project.py
   ```
4. Follow the interactive prompts

**Or clone and initialize:**
```bash
git clone https://github.com/dmbrmv/agentic-state-protocol.git my-project
cd my-project
python init_project.py
```

### After Installation

```bash
# Start your first session
/boot

# Check project status
/status

# See all available commands
# (listed in docs/00_MASTER_INDEX.md)
```

## What You Get

### The `.claude/` Folder (Core)

This is the heart of the protocol - works immediately after copying:

```
.claude/
├── commands/           # 22 CLI commands
│   ├── boot.md         # /boot - Start session
│   ├── save.md         # /save - End session
│   ├── done.md         # /done - Complete task
│   ├── tdd.md          # /tdd - Test-driven development
│   ├── test.md         # /test - Run tests
│   ├── review.md       # /review - Code review
│   ├── build-fix.md    # /build-fix - Fix build errors
│   ├── learn.md        # /learn - Extract patterns
│   └── ...             # 14 more commands
│
├── skills/             # Auto-enforced behaviors
├── agents/             # Specialized subagents
├── contexts/           # Working modes (dev/research/review)
├── hooks/              # Automation (format, lint, security)
└── mcp/                # MCP server configs
```

### Documentation Structure (Optional)

If you use `--full` mode or want state persistence:

```
docs/
├── 00_MASTER_INDEX.md      # Protocol specification (start here)
├── 01_progress.md          # Tasks, backlog, metrics
├── 02_issues.md            # Issue registry
├── 03_architecture.md      # System design
├── 04_standards.md         # Coding standards
├── 05_guides.md            # Environment setup
├── adrs/                   # Architecture Decision Records
└── logs/
    └── session_context.md  # Session history
```

### CLI Commands

**Session Management:**
| Command | Purpose |
|---------|---------|
| `/boot` | Start session: load state, show active task |
| `/save` | End session: update docs, prepare commit |
| `/done` | Mark task complete, suggest next |
| `/status` | Project health dashboard |

**Development:**
| Command | Purpose |
|---------|---------|
| `/tdd <feature>` | Test-driven development workflow |
| `/test` | Run tests with failure analysis |
| `/test-coverage` | Coverage analysis with gap identification |
| `/build-fix` | Fix build/type errors |
| `/feature <name>` | Plan new feature before coding |

**Quality:**
| Command | Purpose |
|---------|---------|
| `/review` | Code review with security checks |
| `/refine <prompt>` | Clarify vague requests with command suggestions |
| `/learn` | Extract reusable patterns |
| `/precommit` | Run all pre-commit checks |

### Skills (Auto-Enforced)

| Skill | Purpose |
|-------|---------|
| `context_manager` | Keep docs synchronized with code |
| `arch_enforcer` | Enforce architecture and standards |
| `test_enforcer` | Auto-run tests, enforce coverage |
| `verifier` | Quality gates before commits |

## Core Principles

### The 4 Immutable Rules

1. **NO STATE AMNESIA** - Read `docs/01_progress.md` at session start
2. **NO SILENT ACTIONS** - Verify active task before modifying code
3. **DOCS = CODE** - Code changes are incomplete without doc updates
4. **DIRECTORY AUTHORITY** - `docs/` is the single source of truth

### The Mandatory Loop

Every request follows this pattern:

```
1. STATE CHECK  → Read docs/01_progress.md
2. ALIGN        → Output: [STATE] Active Task: <name>
                          [MODE] Execution | Planning | Refactoring
3. EXECUTE      → Perform the work
4. COMMIT       → Update docs/01_progress.md + session_context.md
```

### Decision Authority Hierarchy

When conflicts arise, this is the priority order:

1. `docs/01_progress.md` - Active task definition
2. `docs/04_standards.md` - Coding standards (LAW)
3. `docs/03_architecture.md` - Technical design
4. `CLAUDE.md` - Agent instructions
5. AI training data - General knowledge (lowest)

## Supported Tech Stacks

The init wizard supports:
- **Python** (ML/Data Science, Earth Science, Spatial Web Apps) - ruff, pyright, pytest

## Architecture Patterns

Choose from three patterns:

1. **Monolithic** - Single-purpose apps, CLIs, scripts
2. **Data Pipeline** - ETL, ML pipelines, scientific computing
3. **Microservices** - Large apps, team projects

## Example Workflow

```bash
# Morning: Start session
/boot
# Output: Current Goal: X | Active Task: Y | Progress: Z%

# Work on the active task
# ... make changes ...

# Check before committing
PRECOMMIT
# Output: Lint ✓ | Tests ✓ | Types ✓

# End of day: Save progress
/save
# Output: Updated docs, ready to commit

# Mark task complete
/done
# Output: Task complete! Next suggestion: Z
```

## Why This Works

1. **Persistent Memory** - State survives between sessions
2. **Transparent Decisions** - Authority hierarchy is explicit
3. **Automatic Sync** - Docs and code stay aligned
4. **Reproducible** - Same workflow for every task
5. **Portable** - Works across any Python project

## Customization After Adoption

### If You Have an Existing CLAUDE.md

Merge the protocol instructions into your existing file:

```markdown
# Your Project Name

## Project-Specific Instructions
[Your existing content]

## Agentic State Protocol
[Copy relevant sections from CLAUDE.md.template]

### Mandatory Loop
1. STATE CHECK → Read docs/01_progress.md
2. ALIGN → Verify active task
3. EXECUTE → Perform the work
4. COMMIT → Update documentation
```

### Minimal Setup (Just Commands)

If you only want the `/commands` without full state management:

1. Copy only `.claude/commands/` and `.claude/contexts/`
2. Skip the `docs/` folder entirely
3. Commands like `/tdd`, `/test`, `/review` work standalone

### Full Setup (Recommended for Teams)

1. Copy everything with `--full` flag
2. Rename `*.template` files and fill in project details
3. Commit the `docs/` folder to git
4. Team members get persistent context across sessions

## Files Overview

| File | Purpose |
|------|---------|
| `adopt.sh` | One-liner adoption script |
| `init_project.py` | Interactive wizard (new projects) |
| `CLAUDE.md.template` | Agent instructions template |
| `docs/*.template` | Documentation templates |
| `.claude/commands/*` | CLI command definitions |
| `.claude/skills/*` | Auto-enforced behaviors |
| `.claude/agents/*` | Specialized subagents |
| `.claude/contexts/*` | Working mode definitions |
| `.claude/hooks/*` | Automation scripts |

## Advanced Features

For advanced usage, see these sections in `docs/00_MASTER_INDEX.md`:

| Feature | Section | Description |
|---------|---------|-------------|
| Multi-Agent Coordination | IX | Spawn parallel Claude agents for complex tasks |
| Inner-Loop Commands | XIV | Fast workflow commands (`/commit-push-pr`, `/quickfix`) |
| Verification Workflows | XV | Automated quality gates before commits |
| Autonomous Execution | XVI | Permission modes for supervised autonomy |

### Template Initialization

The `init_project.py` wizard configures:
1. **Project Name** - Sets the project identifier
2. **Tech Stack** - Python (ML/Data Science, Earth Science, Spatial Web Apps)
3. **Architecture Pattern** - Monolithic, Data Pipeline, or Microservices
4. **Git Setup** - Optional repository initialization

After initialization, the `docs/` folder contains your project-specific configuration.

## Requirements

- Python 3.10+ (for init script only)
- Git (optional, for repository initialization)
- Claude Code or compatible AI assistant

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - feel free to use in any project.

## Credits

Developed as a solution for disciplined AI-assisted development. Inspired by the need for persistent context across AI coding sessions.

---

**Start your journey**: `python init_project.py`

**Questions?** Open an issue or read `docs/00_MASTER_INDEX.md`
