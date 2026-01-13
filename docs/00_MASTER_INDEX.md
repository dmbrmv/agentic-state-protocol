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

| Command | Purpose |
|---------|---------|
| `/boot` | Wake up: Load state, summarize context |
| `/save` | Shutdown: Update docs, log checkpoint, suggest commit |
| `/done` | Complete task: Mark done, propose next |
| `/feature <name>` | New feature: Plan before coding |
| `/refine <prompt>` | Clarify: Turn vague request into actionable prompt |

---

## VI. SKILLS (Auto-Enforced)

Available skills via `.claude/skills/`:

| Skill | Purpose |
|-------|---------|
| `context_manager` | Keep docs synchronized with code changes |
| `arch_enforcer` | Enforce architecture and coding standards |

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

**REMEMBER**: Before doing ANY work, read `docs/01_progress.md` to verify the active task.

**NEXT STEP**: Read `docs/01_progress.md` now.
