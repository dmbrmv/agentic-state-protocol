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

### Option 1: Use as GitHub Template

1. Click "Use this template" on GitHub
2. Clone your new repository
3. Run the setup wizard:
   ```bash
   python init_project.py
   ```
4. Follow the interactive prompts

### Option 2: Clone and Initialize

```bash
# Clone the template
git clone https://github.com/yourusername/agentic-state-protocol.git my-project
cd my-project

# Run the setup wizard
python init_project.py

# Start your first session
/boot
```

## What You Get

### Documentation Structure
```
docs/
├── 00_MASTER_INDEX.md      # Protocol specification
├── 01_progress.md          # Tasks, backlog, metrics
├── 02_issues.md            # Issue registry
├── 03_architecture.md      # System design
├── 04_standards.md         # Coding standards
├── 05_guides.md            # Environment setup
└── logs/
    └── session_context.md  # Session history
```

### CLI Commands

| Command | Purpose |
|---------|---------|
| `/boot` | Start session: load state, show active task |
| `/save` | End session: update docs, prepare commit |
| `/done` | Mark task complete, suggest next |
| `/feature <name>` | Plan new feature before coding |
| `/refine <prompt>` | Clarify vague requests |

### Skills (Auto-Enforced)

| Skill | Purpose |
|-------|---------|
| `context_manager` | Keep docs synchronized with code |
| `arch_enforcer` | Enforce architecture and standards |

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
- **Python** - ruff, pyright, pytest
- **JavaScript/TypeScript** - prettier, eslint, jest
- **Rust** - rustfmt, clippy, cargo test
- **Go** - gofmt, golangci-lint, go test
- **Other** - customizable templates

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
5. **Portable** - Works across any project, any tech stack

## Files Overview

| File | Purpose |
|------|---------|
| `init_project.py` | Setup wizard (run once) |
| `CLAUDE.md.template` | Agent instructions template |
| `docs/*.template` | Documentation templates |
| `.claude/commands/*` | CLI command definitions |
| `.claude/skills/*` | Auto-enforced behaviors |

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
2. **Tech Stack** - Python, JavaScript/TypeScript, Rust, Go, or Other
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
