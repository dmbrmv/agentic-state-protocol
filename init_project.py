#!/usr/bin/env python3
"""
Agentic State Protocol v3.0 - Project Initializer

Interactive wizard to bootstrap a new Python project for ML, data science,
and earth science with the Agentic State Protocol.

Usage:
    python init_project.py                    # Interactive mode
    python init_project.py --name "My Project"  # With pre-filled name
    python init_project.py --help             # Show help

Requirements:
    Python 3.10+ (no external dependencies)
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


# ============================================================================
# Configuration
# ============================================================================

TECH_STACKS = {
    "1": ("Python (ML / Data Science)", "python_ml"),
    "2": ("Python (Earth Science / Geospatial)", "python_geo"),
    "3": ("Python (Spatial Web App)", "python_web"),
    "4": ("Python (General)", "python"),
}

ARCHITECTURE_PATTERNS = {
    "1": ("Data Pipeline", "pipeline"),
    "2": ("ML Research Project", "ml_research"),
    "3": ("Spatial Web Application", "spatial_web"),
    "4": ("CLI Tool", "cli"),
}

# Domain-specific blind spots for the Critical Engagement Protocol
DOMAIN_BLIND_SPOTS = {
    "python_ml": """    - **Under-invest**: error handling, input validation, logging, reproducibility (seeds, versions), experiment tracking
    - **Over-invest**: premature abstraction, configurability nobody will use, class hierarchies where functions suffice
    - **Misjudge**: dependency choices (pinning vs ranges), state management, test strategy (data fixtures), naming conventions""",
    "python_geo": """    - **Under-invest**: CRS validation, coordinate system consistency, error handling for corrupt rasters, reproducibility (seeds, library versions, GDAL config)
    - **Over-invest**: premature abstraction, generic spatial frameworks when a simple script suffices, class hierarchies for one-off analyses
    - **Misjudge**: dependency choices (GDAL version conflicts), memory management for large rasters, test strategy for geospatial data, data pipeline ordering""",
    "python_web": """    - **Under-invest**: input validation, error handling, deployment configuration, caching for expensive computations, logging
    - **Over-invest**: premature optimization, complex state management for simple dashboards, unnecessary client-side logic
    - **Misjudge**: dependency choices (framework selection), session management, test strategy for interactive visualizations""",
    "python": """    - **Under-invest**: error handling, input validation, logging, reproducibility (seeds, versions)
    - **Over-invest**: premature abstraction, configurability nobody will use, class hierarchies where functions suffice
    - **Misjudge**: dependency choices, state management, test strategy, naming conventions""",
}

DEFAULT_COMMANDS = {
    "python": {
        "ENVIRONMENT_ACTIVATION": "source .venv/bin/activate  # or: conda activate myenv",
        "INSTALL_COMMAND": "pip install -e .",
        "VERIFY_COMMAND": "python --version && pip list",
        "RUN_COMMAND": "python -m {{PROJECT_SLUG}}",
        "TEST_COMMAND": "pytest tests/ -v",
        "TEST_SINGLE_COMMAND": "pytest tests/test_module.py -v",
        "TEST_COVERAGE_COMMAND": "pytest tests/ --cov={{PROJECT_SLUG}} --cov-report=html",
        "FORMAT_COMMAND": "ruff format .",
        "LINT_COMMAND": "ruff check .",
        "TYPE_CHECK_COMMAND": "pyright",
        "BUILD_COMMAND": "pip install build && python -m build",
    },
    "python_ml": {
        "ENVIRONMENT_ACTIVATION": "conda activate myenv  # or: source .venv/bin/activate",
        "INSTALL_COMMAND": "pip install -e '.[dev,ml]'",
        "VERIFY_COMMAND": "python --version && pip list | grep -E 'numpy|pandas|scikit|torch|xgboost'",
        "RUN_COMMAND": "python -m {{PROJECT_SLUG}}.train",
        "TEST_COMMAND": "pytest tests/ -v",
        "TEST_SINGLE_COMMAND": "pytest tests/test_model.py -v",
        "TEST_COVERAGE_COMMAND": "pytest tests/ --cov={{PROJECT_SLUG}} --cov-report=html",
        "FORMAT_COMMAND": "ruff format .",
        "LINT_COMMAND": "ruff check .",
        "TYPE_CHECK_COMMAND": "pyright",
        "BUILD_COMMAND": "pip install build && python -m build",
    },
    "python_geo": {
        "ENVIRONMENT_ACTIVATION": "conda activate myenv  # conda required for GDAL/geospatial",
        "INSTALL_COMMAND": "pip install -e '.[dev,geo]'",
        "VERIFY_COMMAND": "python -c \"import rasterio; import geopandas; print('OK')\" && gdalinfo --version",
        "RUN_COMMAND": "python -m {{PROJECT_SLUG}}.pipeline",
        "TEST_COMMAND": "pytest tests/ -v",
        "TEST_SINGLE_COMMAND": "pytest tests/test_pipeline.py -v",
        "TEST_COVERAGE_COMMAND": "pytest tests/ --cov={{PROJECT_SLUG}} --cov-report=html",
        "FORMAT_COMMAND": "ruff format .",
        "LINT_COMMAND": "ruff check .",
        "TYPE_CHECK_COMMAND": "pyright",
        "BUILD_COMMAND": "pip install build && python -m build",
    },
    "python_web": {
        "ENVIRONMENT_ACTIVATION": "conda activate myenv  # or: source .venv/bin/activate",
        "INSTALL_COMMAND": "pip install -e '.[dev,web]'",
        "VERIFY_COMMAND": "python --version && pip list | grep -E 'streamlit|panel|dash|folium'",
        "RUN_COMMAND": "streamlit run src/{{PROJECT_SLUG}}/app.py  # or: panel serve src/{{PROJECT_SLUG}}/app.py",
        "TEST_COMMAND": "pytest tests/ -v",
        "TEST_SINGLE_COMMAND": "pytest tests/test_app.py -v",
        "TEST_COVERAGE_COMMAND": "pytest tests/ --cov={{PROJECT_SLUG}} --cov-report=html",
        "FORMAT_COMMAND": "ruff format .",
        "LINT_COMMAND": "ruff check .",
        "TYPE_CHECK_COMMAND": "pyright",
        "BUILD_COMMAND": "pip install build && python -m build",
    },
}


# ============================================================================
# Helper Functions
# ============================================================================

def slugify(text: str) -> str:
    """Convert text to a valid slug (lowercase, underscores)."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "_", text)
    return text.strip("_")


def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_step(step: int, total: int, text: str) -> None:
    """Print a step indicator."""
    print(f"\n[{step}/{total}] {text}")
    print("-" * 40)


def prompt(question: str, default: str = "") -> str:
    """Prompt user for input with optional default."""
    if default:
        result = input(f"{question} [{default}]: ").strip()
        return result if result else default
    return input(f"{question}: ").strip()


def prompt_choice(question: str, choices: dict[str, tuple[str, str]]) -> tuple[str, str]:
    """Prompt user to choose from options."""
    print(f"\n{question}")
    for key, (label, _) in choices.items():
        print(f"  {key}. {label}")

    while True:
        choice = input("\nEnter number: ").strip()
        if choice in choices:
            return choices[choice]
        print(f"Invalid choice. Please enter {', '.join(choices.keys())}")


def prompt_yes_no(question: str, default: bool = True) -> bool:
    """Prompt for yes/no answer."""
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{question} {suffix}: ").strip().lower()

    if not answer:
        return default
    return answer in ("y", "yes")


# ============================================================================
# File Operations
# ============================================================================

def get_template_dir() -> Path:
    """Get the directory containing template files."""
    return Path(__file__).parent


def copy_static_files(template_dir: Path, target_dir: Path) -> None:
    """Copy static files (commands, skills) that don't need templating."""
    # Copy .claude directory
    claude_src = template_dir / ".claude"
    claude_dst = target_dir / ".claude"

    if claude_src.exists():
        shutil.copytree(claude_src, claude_dst, dirs_exist_ok=True)
        print("  Copied .claude/ directory")

    # Copy docs/00_MASTER_INDEX.md (it's already generic)
    master_index_src = template_dir / "docs" / "00_MASTER_INDEX.md"
    master_index_dst = target_dir / "docs" / "00_MASTER_INDEX.md"

    if master_index_src.exists():
        shutil.copy2(master_index_src, master_index_dst)
        print("  Copied docs/00_MASTER_INDEX.md")


def process_template(
    template_path: Path,
    output_path: Path,
    replacements: dict[str, str]
) -> None:
    """Process a template file, replacing placeholders."""
    content = template_path.read_text()

    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)

    output_path.write_text(content)
    print(f"  Created {output_path.relative_to(output_path.parent.parent)}")


def create_directory_structure(target_dir: Path, project_slug: str, arch_key: str) -> None:
    """Create the project directory structure."""
    directories = [
        "docs/logs",
        "docs/reference",
        "docs/adrs",
        f"src/{project_slug}",
        "tests",
        "scripts",
        "configs",
        "notebooks",
        ".claude/commands",
        ".claude/skills",
        ".claude/agents",
        ".claude/contexts",
        ".claude/hooks",
        ".claude/mcp",
    ]

    # Add architecture-specific directories
    if arch_key in ("pipeline", "ml_research"):
        directories.extend([
            "data/raw",
            "data/processed",
            "data/output",
        ])
    if arch_key == "ml_research":
        directories.extend([
            "models",
            "experiments",
        ])
    if arch_key == "spatial_web":
        directories.extend([
            "data/raw",
            "data/processed",
        ])

    for dir_path in directories:
        (target_dir / dir_path).mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    (target_dir / f"src/{project_slug}/__init__.py").touch()
    (target_dir / "tests/__init__.py").touch()

    # Create .gitkeep for empty directories
    (target_dir / "docs/adrs/.gitkeep").touch()

    print("  Created directory structure")


def init_git(target_dir: Path) -> bool:
    """Initialize git repository."""
    try:
        subprocess.run(
            ["git", "init"],
            cwd=target_dir,
            check=True,
            capture_output=True
        )

        # Create .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Testing
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
.env.local
.env.*.local

# Data (large files — track with DVC or git-lfs if needed)
data/raw/
data/processed/
data/output/
*.tif
*.nc
*.hdf5
*.h5
*.parquet
*.feather

# Models
models/*.pkl
models/*.joblib
models/*.pt
models/*.h5

# Notebooks
.ipynb_checkpoints/

# Geospatial
*.shp.lock
"""
        (target_dir / ".gitignore").write_text(gitignore_content)
        print("  Initialized git repository")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  Warning: Could not initialize git (git not found or error)")
        return False


# ============================================================================
# Main Wizard
# ============================================================================

def run_wizard(args: argparse.Namespace) -> dict[str, Any]:
    """Run the interactive wizard to collect project information."""
    print_header("Agentic State Protocol v3.0 - Project Initializer")

    print("This wizard will help you set up a new Python project for")
    print("ML, data science, or earth science with the Agentic State Protocol.")

    config: dict[str, Any] = {}
    total_steps = 8

    # Step 1: Project Name
    print_step(1, total_steps, "Project Name")
    config["project_name"] = args.name or prompt(
        "Enter project name (e.g., 'Watershed Analysis Pipeline')"
    )
    config["project_slug"] = slugify(config["project_name"])
    print(f"  Slug: {config['project_slug']}")

    # Step 2: Project Description
    print_step(2, total_steps, "Project Description")
    config["description"] = prompt(
        "Brief description",
        f"A {config['project_name']} project"
    )

    # Step 3: Tech Stack
    print_step(3, total_steps, "Python Focus Area")
    stack_label, stack_key = prompt_choice(
        "Select your primary focus area:",
        TECH_STACKS
    )
    config["tech_stack"] = stack_label
    config["tech_key"] = stack_key

    # Step 4: Architecture Pattern
    print_step(4, total_steps, "Architecture Pattern")
    arch_label, arch_key = prompt_choice(
        "Select your architecture pattern:",
        ARCHITECTURE_PATTERNS
    )
    config["architecture_pattern"] = arch_label
    config["architecture_key"] = arch_key

    # Step 5: Initial Goal
    print_step(5, total_steps, "Initial Goal")
    config["initial_goal"] = prompt(
        "What's your first goal for this project?",
        "Set up development environment and basic structure"
    )

    # Step 6: User Context (for Critical Engagement Protocol)
    print_step(6, total_steps, "User Context")
    print("  This helps the AI agent calibrate its feedback style.")
    config["user_context"] = prompt(
        "Describe your profile (e.g., 'researcher with expertise in hydrology and ML')",
        "researcher with domain expertise"
    )

    # Step 7: Target Directory
    print_step(7, total_steps, "Target Directory")
    default_dir = Path.cwd() / config["project_slug"]
    target_input = prompt(
        "Target directory",
        str(default_dir)
    )
    config["target_dir"] = Path(target_input).resolve()

    # Step 8: Git Initialization
    print_step(8, total_steps, "Git Repository")
    config["init_git"] = prompt_yes_no("Initialize git repository?", True)

    # Optional: Data location
    print("\n[Optional] Additional Configuration")
    print("-" * 40)
    config["data_location"] = prompt(
        "Data directory (leave empty to skip)",
        ""
    )

    return config


def create_project(config: dict[str, Any]) -> None:
    """Create the project based on collected configuration."""
    template_dir = get_template_dir()
    target_dir = config["target_dir"]
    project_slug = config["project_slug"]
    tech_key = config["tech_key"]
    arch_key = config["architecture_key"]

    print_header("Creating Project")

    # Check if directory exists
    if target_dir.exists() and any(target_dir.iterdir()):
        if not prompt_yes_no(
            f"Directory {target_dir} is not empty. Continue anyway?",
            False
        ):
            print("Aborted.")
            sys.exit(1)

    # Create directory structure
    print("\n1. Creating directory structure...")
    target_dir.mkdir(parents=True, exist_ok=True)
    create_directory_structure(target_dir, project_slug, arch_key)

    # Copy static files
    print("\n2. Copying static files...")
    copy_static_files(template_dir, target_dir)

    # Prepare replacements
    today = date.today().isoformat()
    commands = DEFAULT_COMMANDS.get(tech_key, DEFAULT_COMMANDS["python"]).copy()

    # Replace PROJECT_SLUG in commands
    for key, value in commands.items():
        commands[key] = value.replace("{{PROJECT_SLUG}}", project_slug)

    # Build common tasks section
    common_tasks = f"""### Running the Application
```bash
{commands['RUN_COMMAND']}
```

### Running Tests
```bash
# All tests
{commands['TEST_COMMAND']}

# With coverage
{commands['TEST_COVERAGE_COMMAND']}
```

### Code Quality
```bash
# Format
{commands['FORMAT_COMMAND']}

# Lint
{commands['LINT_COMMAND']}

# Type check
{commands['TYPE_CHECK_COMMAND']}
```"""

    # Build user context for Critical Engagement Protocol
    user_context_text = (
        f"**Context:** The user is a {config['user_context']}. "
        "The agent should calibrate feedback to the user's expertise level."
    )

    # Get domain-specific blind spots
    blind_spots = DOMAIN_BLIND_SPOTS.get(
        tech_key,
        DOMAIN_BLIND_SPOTS["python"]
    )

    replacements = {
        "PROJECT_NAME": config["project_name"],
        "PROJECT_SLUG": project_slug,
        "PROJECT_DESCRIPTION": config["description"],
        "TECH_STACK": config["tech_stack"],
        "ARCHITECTURE_PATTERN": config["architecture_pattern"],
        "INITIAL_GOAL": config["initial_goal"],
        "DATE": today,
        "REPO_PATH": str(target_dir),
        "REPO_URL": "https://github.com/username/repo.git",
        "DATA_LOCATION": config.get("data_location") or "N/A",
        "COMMON_TASKS": common_tasks,
        "USER_CONTEXT": user_context_text,
        "DOMAIN_BLIND_SPOTS": blind_spots,
        **commands,
    }

    # Process template files
    print("\n3. Processing template files...")

    template_files = [
        ("docs/01_progress.md.template", "docs/01_progress.md"),
        ("docs/02_issues.md.template", "docs/02_issues.md"),
        ("docs/03_architecture.md.template", "docs/03_architecture.md"),
        ("docs/04_standards.md.template", "docs/04_standards.md"),
        ("docs/05_guides.md.template", "docs/05_guides.md"),
        ("docs/logs/session_context.md.template", "docs/logs/session_context.md"),
        ("CLAUDE.md.template", "CLAUDE.md"),
    ]

    for template_name, output_name in template_files:
        template_path = template_dir / template_name
        output_path = target_dir / output_name

        if template_path.exists():
            process_template(template_path, output_path, replacements)
        else:
            print(f"  Warning: Template not found: {template_name}")

    # Initialize git if requested
    if config["init_git"]:
        print("\n4. Initializing git...")
        init_git(target_dir)

    # Done!
    print_header("Project Created Successfully!")

    print(f"Project: {config['project_name']}")
    print(f"Location: {target_dir}")
    print(f"Focus Area: {config['tech_stack']}")
    print(f"Architecture: {config['architecture_pattern']}")

    print("\n" + "=" * 60)
    print("  NEXT STEPS")
    print("=" * 60)
    print(f"""
1. Navigate to your project:
   cd {target_dir}

2. Set up your environment:
   {commands['ENVIRONMENT_ACTIVATION']}

3. Install dependencies:
   {commands['INSTALL_COMMAND']}

4. Start your first session with Claude Code:
   /boot

5. Begin working on your first task!
""")

    print("=" * 60)
    print("  Happy coding with Agentic State Protocol v3.0!")
    print("=" * 60 + "\n")


# ============================================================================
# Entry Point
# ============================================================================

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize a new Python project with Agentic State Protocol v3.0"
    )
    parser.add_argument(
        "--name",
        help="Project name (skip interactive prompt)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Agentic State Protocol v3.0"
    )

    args = parser.parse_args()

    try:
        config = run_wizard(args)
        create_project(config)
    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
