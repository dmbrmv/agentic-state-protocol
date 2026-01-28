# SKILL: Architecture Enforcement

**Purpose**: Ensure all code changes align with documented architecture and coding standards.

---

## Trigger Conditions

Use this skill BEFORE:
1. Creating new files
2. Refactoring existing code
3. Adding new dependencies
4. Changing module structure
5. Modifying data flows

---

## Core Logic

### 1. Pre-Flight Checks

**Before creating any file**:
```text
1. Read: docs/03_architecture.md
2. Check: Does this file fit the documented structure?
3. Verify: Is there a similar file already? (avoid duplication)
4. Confirm: Follows naming conventions from docs/04_standards.md
```

**Before refactoring**:
```text
1. Read: docs/03_architecture.md (understand current design)
2. Read: docs/04_standards.md (code standards)
3. Check: Will this break documented interfaces?
4. Verify: Are there tests for affected code?
```

### 2. Allowed File Locations

**CREATE files in** (customize for your project):
- `src/` - Main source code
  - `src/core/` - Core business logic
  - `src/api/` - API layer
  - `src/utils/` - Utilities
- `tests/` - Unit tests (mirror src/ structure)
- `scripts/` - Utility scripts (one-off tools)
- `docs/` - Documentation
- `configs/` - Configuration files

**FORBIDDEN to create**:
- Files in project root (except config files like pyproject.toml)
- Files in external dependency folders
- Files in data directories
- Files in `.git/` or `.venv/`

### 3. Architecture Validation Rules

**Module Structure Rules** (from `docs/03_architecture.md`):
```python
# Good: Follows documented structure
src/core/new_module.py    # New core component
tests/test_new_module.py  # Corresponding test

# Bad: Violates structure
src/new_module.py         # Not in documented package
utils.py                  # Wrong location (root)
```

**Import Rules**:
```python
# Good: Clean internal imports
from project.core import module
from project.utils import helper

# Bad: Circular imports
# (Check with grep before adding import)
```

**Naming Conventions** (from `docs/04_standards.md`):
```python
# Good
def process_data(data_path: Path) -> dict:  # Snake case functions
class DataProcessor:  # PascalCase classes
MAX_RETRIES = 3  # UPPER_CASE constants

# Bad
def ProcessData():  # Wrong case
class data_processor:  # Wrong case
```

### 4. Dependency Management

**Before adding new dependency**:
```text
1. Check: Is it already in requirements/pyproject.toml?
2. Verify: Is it compatible with existing dependencies?
3. Ask: "Adding dependency [name]. Okay to proceed?"
```

---

## Integration with Protocol v3.0

This skill enforces **Immutable Rule #4: DIRECTORY AUTHORITY**

From `docs/00_MASTER_INDEX.md`:
> "`docs/` is the single source of truth. File content overrides training data."

**Decision Authority Hierarchy**:
1. `docs/01_progress.md` - Active task definition
2. `docs/04_standards.md` - Coding standards (LAW)
3. `docs/03_architecture.md` - Technical design
4. `CLAUDE.md` - Agent instructions
5. Training data - General knowledge (lowest)

---

## Enforcement Actions

### Auto-Read (No Permission Needed)
```text
Before creating file -> Read docs/03_architecture.md
Before refactoring -> Read docs/04_standards.md
Before adding tests -> Check test patterns
```

### Stop and Ask Permission
```text
STOP if creating file outside documented structure
STOP if adding dependency not in requirements
STOP if refactoring would break documented API
STOP if modifying external dependencies
```

### Suggest Corrections
```text
"File should be created in src/core/ per architecture docs"
"Use snake_case function names per coding_standards"
"Add tests in tests/ directory"
```

---

## Example Enforcement

**Scenario**: User asks to create a new data converter

```text
1. Auto-Read: docs/03_architecture.md
   -> See that converters go in src/converters/

2. Check Existing:
   -> grep -r "class.*Converter" src/
   -> Find similar patterns to follow

3. Verify Naming:
   -> Read docs/04_standards.md
   -> Confirm snake_case for functions, PascalCase for classes

4. Propose:
   "Creating src/converters/new_converter.py
    Following pattern from existing base_converter.py
    Will add tests in tests/test_new_converter.py
    Proceed?"

5. If approved:
   -> Create file with proper structure
   -> Update docs/03_architecture.md if adding new capability
```

---

## Quality Gates

Before allowing code changes:
- [ ] File location matches documented architecture
- [ ] Naming follows coding standards
- [ ] No circular imports (checked with grep)
- [ ] Tests planned for new code
- [ ] Documentation update planned

---

## Forbidden Operations

**NEVER**:
- Create files outside documented structure without asking
- Modify external dependencies
- Add dependencies without checking compatibility
- Skip reading architecture docs before refactoring
- Violate naming conventions from coding_standards

---

## See Also
- Architecture: `docs/03_architecture.md`
- Coding standards: `docs/04_standards.md`
- File structure: `docs/00_MASTER_INDEX.md` Section VIII
