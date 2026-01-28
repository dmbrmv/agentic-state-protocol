# Example: Python CLI Project

This example shows how to set up a Python CLI project with the Agentic State Protocol.

## Project Type
- **Architecture**: Monolithic Application
- **Tech Stack**: Python
- **Use Case**: Earth science CLI tools, data processing utilities, geospatial workflows

## Initialization

```bash
# From the agentic-state-protocol root directory
python init_project.py

# When prompted:
# - Project name: "My CLI Tool"
# - Tech stack: Python (1)
# - Architecture: Monolithic Application (1)
```

## Resulting Structure

```
my_cli_tool/
├── docs/                      # Protocol documentation
├── src/my_cli_tool/           # Main package
│   ├── __init__.py
│   ├── cli.py                 # CLI entry point (add)
│   └── core.py                # Business logic (add)
├── tests/
│   └── test_core.py           # Tests (add)
├── scripts/
├── configs/
├── .claude/
├── CLAUDE.md
├── pyproject.toml             # Add this
└── README.md                  # Add this
```

## Recommended pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-cli-tool"
version = "0.1.0"
description = "A CLI tool"
requires-python = ">=3.8"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "pyright>=1.1.0",
]

[project.scripts]
mycli = "my_cli_tool.cli:app"

[tool.ruff]
line-length = 88
target-version = "py38"

[tool.pyright]
pythonVersion = "3.8"
typeCheckingMode = "basic"
```

## Sample CLI Code

```python
# src/my_cli_tool/cli.py
import typer
from rich import print

app = typer.Typer(help="My CLI Tool")

@app.command()
def hello(name: str = "World"):
    """Say hello."""
    print(f"[green]Hello, {name}![/green]")

@app.command()
def process(input_file: str, output_file: str):
    """Process a file."""
    # Implementation here
    print(f"Processing {input_file} -> {output_file}")

if __name__ == "__main__":
    app()
```

## Workflow Example

```bash
# Start session
/boot

# Implement feature
/feature add-process-command

# After implementing
/done

# Save and commit
/save
```
