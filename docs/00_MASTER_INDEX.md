# Agentic State Protocol v3.1 - Master Index

## Overview

This document defines the **Agentic State Protocol** — a framework for AI-assisted development that maintains context across sessions, enforces quality standards, and enables effective human-AI collaboration.

---

## Document Hierarchy

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CLAUDE.md` | Agent behavior rules, commands, protocols | Rarely (project setup) |
| `00_MASTER_INDEX.md` | This file - protocol overview | Rarely |
| `01_progress.md` | **Current state, active task, backlog** | Every session |
| `02_issues.md` | Known issues, tech debt | As discovered |
| `03_architecture.md` | System design decisions | When architecture changes |
| `04_standards.md` | Coding standards (LAW) | Rarely |
| `05_guides.md` | Environment setup, workflows | As needed |
| `logs/session_context.md` | Session history | Every session |

---

## Core Principles

### 1. State Persistence
AI agents have no memory between sessions. The `docs/` directory IS the memory.

### 2. Single Source of Truth
`docs/01_progress.md` defines what work is active. No work happens without checking it first.

### 3. Critical Engagement
AI must challenge assumptions, flag issues, and resist sycophancy. See CLAUDE.md Section II.

### 4. Documentation = Code
Code changes are incomplete without corresponding documentation updates.

---

## Session Protocol

### Start of Session
```text
1. READ docs/01_progress.md
2. READ docs/02_issues.md (if relevant)
3. VERIFY active task matches user request
4. BEGIN work
```

### End of Session
```text
1. UPDATE docs/01_progress.md with progress
2. LOG session summary to docs/logs/session_context.md
3. COMMIT changes if appropriate
```

---

## Commands Reference

| Command | Action |
|---------|--------|
| `/boot` | Load state, report status, ask to proceed |
| `/done` | Mark task complete, propose next |
| `/save` | Checkpoint all docs |
| `/status` | Quick project status |
| `/review` | Peer review simulation (paper writing) |
| `/verify` | Fact-check current section (paper writing) |

---

## File Templates

All template files are in this directory. Copy and customize for new projects.
