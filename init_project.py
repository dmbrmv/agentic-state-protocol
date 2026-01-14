#!/usr/bin/env python3
"""
Agentic State Protocol v3.0 - Project Initializer

Interactive wizard to bootstrap a new project with the Agentic State Protocol.
This script creates a disciplined development environment for AI-assisted coding.

Usage:
    python init_project.py                    # Interactive mode
    python init_project.py --name "My Project"  # With pre-filled name
    python init_project.py --help             # Show help

Requirements:
    Python 3.10+ (no external dependencies)
"""

from __future__ import annotations

import argparse
import os
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
    "1": ("Python", "python"),
    "2": ("JavaScript/TypeScript", "javascript"),
    "3": ("Rust", "rust"),
    "4": ("Go", "go"),
    "5": ("Other", "other"),
}

ARCHITECTURE_PATTERNS = {
    "1": ("Monolithic Application", "monolithic"),
    "2": ("Data Pipeline", "pipeline"),
    "3": ("Microservices / Modular", "microservices"),
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
    "javascript": {
        "ENVIRONMENT_ACTIVATION": "# Node.js environment (nvm use if needed)",
        "INSTALL_COMMAND": "npm install",
        "VERIFY_COMMAND": "node --version && npm --version",
        "RUN_COMMAND": "npm start",
        "TEST_COMMAND": "npm test",
        "TEST_SINGLE_COMMAND": "npm test -- --testPathPattern=module.test",
        "TEST_COVERAGE_COMMAND": "npm test -- --coverage",
        "FORMAT_COMMAND": "npx prettier --write .",
        "LINT_COMMAND": "npx eslint .",
        "TYPE_CHECK_COMMAND": "npx tsc --noEmit",
        "BUILD_COMMAND": "npm run build",
    },
    "rust": {
        "ENVIRONMENT_ACTIVATION": "# Rust environment (rustup default stable)",
        "INSTALL_COMMAND": "cargo build",
        "VERIFY_COMMAND": "rustc --version && cargo --version",
        "RUN_COMMAND": "cargo run",
        "TEST_COMMAND": "cargo test",
        "TEST_SINGLE_COMMAND": "cargo test test_name",
        "TEST_COVERAGE_COMMAND": "cargo tarpaulin",
        "FORMAT_COMMAND": "cargo fmt",
        "LINT_COMMAND": "cargo clippy",
        "TYPE_CHECK_COMMAND": "cargo check",
        "BUILD_COMMAND": "cargo build --release",
    },
    "go": {
        "ENVIRONMENT_ACTIVATION": "# Go environment (go version)",
        "INSTALL_COMMAND": "go mod download",
        "VERIFY_COMMAND": "go version",
        "RUN_COMMAND": "go run .",
        "TEST_COMMAND": "go test ./...",
        "TEST_SINGLE_COMMAND": "go test -run TestName ./...",
        "TEST_COVERAGE_COMMAND": "go test -cover ./...",
        "FORMAT_COMMAND": "gofmt -w .",
        "LINT_COMMAND": "golangci-lint run",
        "TYPE_CHECK_COMMAND": "go vet ./...",
        "BUILD_COMMAND": "go build -o bin/app .",
    },
    "other": {
        "ENVIRONMENT_ACTIVATION": "# Activate your environment",
        "INSTALL_COMMAND": "# Install dependencies",
        "VERIFY_COMMAND": "# Verify installation",
        "RUN_COMMAND": "# Run application",
        "TEST_COMMAND": "# Run tests",
        "TEST_SINGLE_COMMAND": "# Run single test",
        "TEST_COVERAGE_COMMAND": "# Run tests with coverage",
        "FORMAT_COMMAND": "# Format code",
        "LINT_COMMAND": "# Lint code",
        "TYPE_CHECK_COMMAND": "# Type check",
        "BUILD_COMMAND": "# Build project",
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
        print(f"  Copied .claude/ directory")

    # Copy docs/00_MASTER_INDEX.md (it's already generic)
    master_index_src = template_dir / "docs" / "00_MASTER_INDEX.md"
    master_index_dst = target_dir / "docs" / "00_MASTER_INDEX.md"

    if master_index_src.exists():
        shutil.copy2(master_index_src, master_index_dst)
        print(f"  Copied docs/00_MASTER_INDEX.md")


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


def create_directory_structure(target_dir: Path, project_slug: str) -> None:
    """Create the project directory structure."""
    directories = [
        "docs/logs",
        "docs/reference",
        f"src/{project_slug}",
        "tests",
        "scripts",
        "configs",
        ".claude/commands",
        ".claude/skills",
    ]

    for dir_path in directories:
        (target_dir / dir_path).mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    (target_dir / f"src/{project_slug}/__init__.py").touch()
    (target_dir / "tests/__init__.py").touch()

    print(f"  Created directory structure")


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
"""
        (target_dir / ".gitignore").write_text(gitignore_content)
        print(f"  Initialized git repository")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"  Warning: Could not initialize git (git not found or error)")
        return False


# ============================================================================
# Main Wizard
# ============================================================================

def run_wizard(args: argparse.Namespace) -> dict[str, Any]:
    """Run the interactive wizard to collect project information."""
    print_header("Agentic State Protocol v3.0 - Project Initializer")

    print("This wizard will help you set up a new project with the")
    print("Agentic State Protocol for disciplined AI-assisted development.")

    config: dict[str, Any] = {}
    total_steps = 7

    # Step 1: Project Name
    print_step(1, total_steps, "Project Name")
    config["project_name"] = args.name or prompt(
        "Enter project name (e.g., 'My Awesome Project')"
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
    print_step(3, total_steps, "Tech Stack")
    stack_label, stack_key = prompt_choice(
        "Select your primary technology stack:",
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

    # Step 6: Target Directory
    print_step(6, total_steps, "Target Directory")
    default_dir = Path.cwd() / config["project_slug"]
    target_input = prompt(
        f"Target directory",
        str(default_dir)
    )
    config["target_dir"] = Path(target_input).resolve()

    # Step 7: Git Initialization
    print_step(7, total_steps, "Git Repository")
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
    create_directory_structure(target_dir, project_slug)

    # Copy static files
    print("\n2. Copying static files...")
    copy_static_files(template_dir, target_dir)

    # Prepare replacements
    today = date.today().isoformat()
    commands = DEFAULT_COMMANDS.get(tech_key, DEFAULT_COMMANDS["other"])

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
    print(f"Tech Stack: {config['tech_stack']}")
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
        description="Initialize a new project with Agentic State Protocol v3.0"
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
