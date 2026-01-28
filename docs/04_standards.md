# PROJECT_NAME - Coding Standards

**Last Updated**: YYYY-MM-DD
**Status**: LAW (must be followed)

---

## Language Standards

### Python

- **Version**: 3.12+
- **Style**: PEP 8, enforced by Ruff
- **Type Hints**: Required for all public functions
- **Docstrings**: Google style

---

## Code Quality Tools

```bash
# Linting
ruff check src/

# Formatting
ruff format src/

# Type checking
pyright src/

# Testing
pytest tests/
```

---

## Commit Message Format

```
<type>: <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat: Add discharge quality assessment module

- Implement A-F grading system for year-level quality
- Add climatology comparison and anomaly detection
- Create CLI script for batch processing
```

---

## Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Files | snake_case | `quality_grader.py` |
| Classes | PascalCase | `QualityGrader` |
| Functions | snake_case | `calculate_grade()` |
| Constants | UPPER_SNAKE | `MAX_THRESHOLD` |
| Variables | snake_case | `discharge_data` |

---

## Documentation Requirements

1. All public functions must have docstrings
2. Complex logic must have inline comments
3. Module-level docstring explaining purpose
4. Update `docs/` when architecture changes

---

## Testing Requirements

1. All new features must have tests
2. Bug fixes should include regression tests
3. Aim for >80% coverage on critical paths
4. Use pytest fixtures for common setup

---

## Pre-Commit Checklist

- [ ] Code passes `ruff check`
- [ ] Code passes `ruff format --check`
- [ ] Code passes `pyright`
- [ ] Tests pass `pytest`
- [ ] Documentation updated
- [ ] Commit message follows format
