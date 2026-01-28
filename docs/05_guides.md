# PROJECT_NAME - Guides & Workflows

**Last Updated**: YYYY-MM-DD

---

## Environment Setup

### Prerequisites

- Python 3.12+
- conda or venv
- git

### Installation

```bash
# Clone repository
git clone https://github.com/USER/PROJECT.git
cd PROJECT

# Create environment
conda create -n project_env python=3.12
conda activate project_env

# Install dependencies
pip install -e .

# Verify installation
pytest tests/
```

---

## Development Workflow

### Starting a New Task

1. Check `docs/01_progress.md` for active task
2. Create feature branch if needed: `git checkout -b feature/task-name`
3. Implement changes
4. Run quality checks: `ruff check src/ && pytest tests/`
5. Update documentation
6. Commit with proper message format

### Code Review Workflow

1. Push branch to remote
2. Create pull request
3. Address review comments
4. Squash and merge when approved

---

## Common Commands

```bash
# Development
pip install -e .          # Install in development mode
pytest tests/             # Run tests
ruff check src/           # Lint code
ruff format src/          # Format code

# Git
git status               # Check status
git add -p               # Stage changes interactively
git commit               # Commit with message
git push                 # Push to remote
```

---

## Troubleshooting

### Import Errors

```bash
pip install -e .
```

### Missing Dependencies

```bash
pip install <package>
```

### Type Stub Missing

```bash
pip install types-<package>
```

---

## Data Access

[Document how to access project data]

---

## Deployment

[Document deployment process if applicable]
