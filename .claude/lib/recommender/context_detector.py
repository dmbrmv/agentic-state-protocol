"""
Project context detection module.

Analyzes project structure, tech stack, and existing protocol elements.
"""

import json
import re
from pathlib import Path
from typing import Any

from .models import ProjectContext, Issue


# Manifest files and their associated languages
MANIFEST_LANGUAGES: dict[str, str] = {
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "setup.py": "python",
    "Pipfile": "python",
    "package.json": "javascript",
    "tsconfig.json": "typescript",
    "Cargo.toml": "rust",
    "go.mod": "go",
    "pom.xml": "java",
    "build.gradle": "java",
    "build.gradle.kts": "kotlin",
    "Gemfile": "ruby",
    "composer.json": "php",
    "mix.exs": "elixir",
    "pubspec.yaml": "dart",
}

# File extensions mapped to languages
EXTENSION_LANGUAGES: dict[str, str] = {
    ".py": "python",
    ".pyx": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".kt": "kotlin",
    ".rb": "ruby",
    ".php": "php",
    ".ex": "elixir",
    ".exs": "elixir",
    ".dart": "dart",
    ".cs": "csharp",
    ".cpp": "cpp",
    ".c": "c",
    ".swift": "swift",
}

# Framework detection patterns
FRAMEWORK_PATTERNS: dict[str, dict[str, Any]] = {
    "python": {
        "fastapi": {"deps": ["fastapi"], "files": []},
        "django": {"deps": ["django"], "files": ["manage.py", "django"]},
        "flask": {"deps": ["flask"], "files": []},
        "sqlalchemy": {"deps": ["sqlalchemy"], "files": []},
        "pydantic": {"deps": ["pydantic"], "files": []},
        "pytest": {"deps": ["pytest"], "files": ["pytest.ini", "conftest.py"]},
        "numpy": {"deps": ["numpy"], "files": []},
        "pandas": {"deps": ["pandas"], "files": []},
        "torch": {"deps": ["torch", "pytorch"], "files": []},
        "tensorflow": {"deps": ["tensorflow"], "files": []},
    },
    "javascript": {
        "react": {"deps": ["react"], "files": []},
        "next": {"deps": ["next"], "files": ["next.config.js", "next.config.mjs"]},
        "vue": {"deps": ["vue"], "files": ["vue.config.js"]},
        "svelte": {"deps": ["svelte"], "files": ["svelte.config.js"]},
        "express": {"deps": ["express"], "files": []},
        "nest": {"deps": ["@nestjs/core"], "files": ["nest-cli.json"]},
        "jest": {"deps": ["jest"], "files": ["jest.config.js", "jest.config.ts"]},
        "vitest": {"deps": ["vitest"], "files": ["vitest.config.ts"]},
    },
    "rust": {
        "tokio": {"deps": ["tokio"], "files": []},
        "actix": {"deps": ["actix-web"], "files": []},
        "axum": {"deps": ["axum"], "files": []},
        "serde": {"deps": ["serde"], "files": []},
    },
    "go": {
        "gin": {"deps": ["github.com/gin-gonic/gin"], "files": []},
        "echo": {"deps": ["github.com/labstack/echo"], "files": []},
        "fiber": {"deps": ["github.com/gofiber/fiber"], "files": []},
    },
}

# Package manager detection
PACKAGE_MANAGERS: dict[str, str] = {
    "pyproject.toml": "pip",
    "requirements.txt": "pip",
    "Pipfile": "pipenv",
    "poetry.lock": "poetry",
    "package.json": "npm",
    "yarn.lock": "yarn",
    "pnpm-lock.yaml": "pnpm",
    "bun.lockb": "bun",
    "Cargo.toml": "cargo",
    "go.mod": "go",
}

# CI/CD config files
CI_CONFIG_FILES: list[str] = [
    ".github/workflows",
    ".gitlab-ci.yml",
    ".circleci/config.yml",
    "Jenkinsfile",
    ".travis.yml",
    "azure-pipelines.yml",
    "bitbucket-pipelines.yml",
]


def detect_project_context(project_path: Path) -> ProjectContext:
    """
    Detect project context by analyzing files and structure.

    Args:
        project_path: Path to project root

    Returns:
        ProjectContext with detected information
    """
    context = ProjectContext()

    # Detect primary language
    context.primary_language = _detect_primary_language(project_path)
    context.secondary_languages = _detect_secondary_languages(
        project_path, context.primary_language
    )

    # Detect package manager
    context.package_manager = _detect_package_manager(project_path)

    # Detect frameworks
    context.frameworks = _detect_frameworks(project_path, context.primary_language)

    # Parse dependencies
    deps, dev_deps = _parse_dependencies(project_path, context.package_manager)
    context.dependencies = deps
    context.dev_dependencies = dev_deps

    # Analyze project structure
    context.has_tests = _has_tests(project_path)
    context.has_docs = (project_path / "docs").is_dir()
    context.has_ci = _has_ci(project_path)
    context.project_type = _infer_project_type(project_path, context)

    # Detect existing protocol elements
    context.existing_skills = _list_protocol_elements(project_path / ".claude" / "skills")
    context.existing_commands = _list_protocol_elements(project_path / ".claude" / "commands")
    context.existing_agents = _list_protocol_elements(project_path / ".claude" / "agents")
    context.existing_mcps = _list_mcp_configs(project_path / ".claude" / "mcp")

    # Parse documentation
    context.documented_issues = _parse_issues(project_path / "docs" / "02_issues.md")
    context.architecture_patterns = _parse_architecture(
        project_path / "docs" / "03_architecture.md"
    )
    context.current_goal = _parse_current_goal(project_path / "docs" / "01_progress.md")

    # Detect quality tooling
    context.lint_configured = _has_linter(project_path)
    context.type_checking = _has_type_checking(project_path, context.primary_language)

    return context


def _detect_primary_language(project_path: Path) -> str:
    """Detect primary language from manifest files and file extensions."""
    # Strategy 1: Check manifest files (highest confidence)
    for manifest, language in MANIFEST_LANGUAGES.items():
        if (project_path / manifest).exists():
            return language

    # Strategy 2: Count file extensions
    extension_counts: dict[str, int] = {}
    for ext, lang in EXTENSION_LANGUAGES.items():
        count = len(list(project_path.rglob(f"*{ext}")))
        if count > 0:
            extension_counts[lang] = extension_counts.get(lang, 0) + count

    if extension_counts:
        return max(extension_counts, key=extension_counts.get)

    return "unknown"


def _detect_secondary_languages(project_path: Path, primary: str) -> list[str]:
    """Detect secondary languages in the project."""
    languages = set()

    # Check manifest files
    for manifest, language in MANIFEST_LANGUAGES.items():
        if (project_path / manifest).exists() and language != primary:
            languages.add(language)

    # Check file extensions
    for ext, lang in EXTENSION_LANGUAGES.items():
        if lang != primary and list(project_path.rglob(f"*{ext}")):
            languages.add(lang)

    return list(languages)[:5]  # Limit to top 5


def _detect_package_manager(project_path: Path) -> str:
    """Detect the package manager used."""
    for file, manager in PACKAGE_MANAGERS.items():
        if (project_path / file).exists():
            return manager
    return "unknown"


def _detect_frameworks(project_path: Path, language: str) -> list[str]:
    """Detect frameworks used in the project."""
    frameworks = []
    patterns = FRAMEWORK_PATTERNS.get(language, {})

    # Parse dependency file for framework detection
    deps = set()
    if language == "python":
        deps = _get_python_deps(project_path)
    elif language in ("javascript", "typescript"):
        deps = _get_js_deps(project_path)
    elif language == "rust":
        deps = _get_rust_deps(project_path)
    elif language == "go":
        deps = _get_go_deps(project_path)

    for framework, pattern in patterns.items():
        # Check dependencies
        if any(dep in deps for dep in pattern.get("deps", [])):
            frameworks.append(framework)
            continue

        # Check for framework-specific files
        for file in pattern.get("files", []):
            if (project_path / file).exists():
                frameworks.append(framework)
                break

    return frameworks


def _get_python_deps(project_path: Path) -> set[str]:
    """Extract Python dependencies."""
    deps = set()

    # Try pyproject.toml
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib
            with open(pyproject, "rb") as f:
                data = tomllib.load(f)
            # Poetry style
            poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            deps.update(poetry_deps.keys())
            # PEP 621 style
            pep_deps = data.get("project", {}).get("dependencies", [])
            for dep in pep_deps:
                # Extract package name from requirement string
                match = re.match(r"^([a-zA-Z0-9_-]+)", dep)
                if match:
                    deps.add(match.group(1).lower())
        except Exception:
            pass

    # Try requirements.txt
    requirements = project_path / "requirements.txt"
    if requirements.exists():
        try:
            content = requirements.read_text()
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    match = re.match(r"^([a-zA-Z0-9_-]+)", line)
                    if match:
                        deps.add(match.group(1).lower())
        except Exception:
            pass

    return deps


def _get_js_deps(project_path: Path) -> set[str]:
    """Extract JavaScript/TypeScript dependencies."""
    deps = set()
    package_json = project_path / "package.json"

    if package_json.exists():
        try:
            data = json.loads(package_json.read_text())
            deps.update(data.get("dependencies", {}).keys())
            deps.update(data.get("devDependencies", {}).keys())
        except Exception:
            pass

    return deps


def _get_rust_deps(project_path: Path) -> set[str]:
    """Extract Rust dependencies."""
    deps = set()
    cargo_toml = project_path / "Cargo.toml"

    if cargo_toml.exists():
        try:
            import tomllib
            with open(cargo_toml, "rb") as f:
                data = tomllib.load(f)
            deps.update(data.get("dependencies", {}).keys())
            deps.update(data.get("dev-dependencies", {}).keys())
        except Exception:
            pass

    return deps


def _get_go_deps(project_path: Path) -> set[str]:
    """Extract Go dependencies."""
    deps = set()
    go_mod = project_path / "go.mod"

    if go_mod.exists():
        try:
            content = go_mod.read_text()
            for line in content.splitlines():
                if line.strip().startswith("require"):
                    continue
                match = re.match(r"^\s*([^\s]+)", line)
                if match:
                    deps.add(match.group(1))
        except Exception:
            pass

    return deps


def _parse_dependencies(
    project_path: Path, package_manager: str
) -> tuple[list[str], list[str]]:
    """Parse both regular and dev dependencies."""
    deps = []
    dev_deps = []

    if package_manager in ("pip", "poetry", "pipenv"):
        all_deps = _get_python_deps(project_path)
        deps = list(all_deps)

    elif package_manager in ("npm", "yarn", "pnpm", "bun"):
        package_json = project_path / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                deps = list(data.get("dependencies", {}).keys())
                dev_deps = list(data.get("devDependencies", {}).keys())
            except Exception:
                pass

    elif package_manager == "cargo":
        cargo_toml = project_path / "Cargo.toml"
        if cargo_toml.exists():
            try:
                import tomllib
                with open(cargo_toml, "rb") as f:
                    data = tomllib.load(f)
                deps = list(data.get("dependencies", {}).keys())
                dev_deps = list(data.get("dev-dependencies", {}).keys())
            except Exception:
                pass

    return deps, dev_deps


def _has_tests(project_path: Path) -> bool:
    """Check if project has test files."""
    test_indicators = [
        project_path / "tests",
        project_path / "test",
        project_path / "__tests__",
        project_path / "spec",
    ]

    if any(d.is_dir() for d in test_indicators):
        return True

    # Check for test files
    test_patterns = ["*_test.py", "test_*.py", "*.test.js", "*.test.ts", "*.spec.js"]
    for pattern in test_patterns:
        if list(project_path.rglob(pattern)):
            return True

    return False


def _has_ci(project_path: Path) -> bool:
    """Check if project has CI/CD configuration."""
    for ci_path in CI_CONFIG_FILES:
        if (project_path / ci_path).exists():
            return True
    return False


def _infer_project_type(project_path: Path, context: ProjectContext) -> str:
    """Infer the type of project."""
    # Check for CLI indicators
    cli_indicators = ["cli.py", "main.py", "__main__.py", "bin/"]
    for indicator in cli_indicators:
        if (project_path / indicator).exists():
            # But also check if it's not a web app
            if not any(fw in context.frameworks for fw in ["fastapi", "django", "flask", "express", "next"]):
                return "cli"

    # Check for web app indicators
    web_frameworks = ["fastapi", "django", "flask", "express", "next", "react", "vue"]
    if any(fw in context.frameworks for fw in web_frameworks):
        return "webapp"

    # Check for API indicators
    api_indicators = ["api/", "routes/", "endpoints/"]
    for indicator in api_indicators:
        if (project_path / indicator).is_dir():
            return "api"

    # Check for library indicators
    if (project_path / "src").is_dir() and not (project_path / "app").is_dir():
        return "library"

    # Check for data pipeline indicators
    data_indicators = ["pipeline/", "etl/", "dags/"]
    for indicator in data_indicators:
        if (project_path / indicator).is_dir():
            return "data-pipeline"

    return "unknown"


def _list_protocol_elements(path: Path) -> list[str]:
    """List protocol elements (skills, commands, agents) by name."""
    if not path.is_dir():
        return []

    elements = []
    for file in path.glob("*.md"):
        elements.append(file.stem)

    return elements


def _list_mcp_configs(path: Path) -> list[str]:
    """List MCP configurations."""
    if not path.is_dir():
        return []

    configs = []
    for file in path.glob("*.json"):
        configs.append(file.stem)

    return configs


def _parse_issues(path: Path) -> list[Issue]:
    """Parse issues from docs/02_issues.md."""
    issues = []

    if not path.exists():
        return issues

    try:
        content = path.read_text()

        # Pattern to match issue entries
        # Expects format like: ## ISSUE-001: Title
        # or: - [HIGH] Issue description
        issue_pattern = re.compile(
            r"##\s*(?:ISSUE-)?(\d+):?\s*(.+?)(?:\n|$)|"
            r"-\s*\[(\w+)\]\s*(.+?)(?:\n|$)",
            re.IGNORECASE
        )

        for match in issue_pattern.finditer(content):
            if match.group(1):
                # Format: ## ISSUE-001: Title
                issue_id = match.group(1)
                title = match.group(2).strip()
                severity = "medium"  # Default
            else:
                # Format: - [HIGH] Description
                issue_id = str(len(issues) + 1)
                severity = match.group(3).lower()
                title = match.group(4).strip()

            # Extract keywords from title for gap matching
            keywords = [w.lower() for w in title.split() if len(w) > 3]

            issues.append(Issue(
                id=issue_id,
                title=title,
                severity=severity,
                tags=keywords,
            ))

    except Exception:
        pass

    return issues


def _parse_architecture(path: Path) -> list[str]:
    """Parse architecture patterns from docs/03_architecture.md."""
    patterns = []

    if not path.exists():
        return patterns

    try:
        content = path.read_text().lower()

        # Look for common architecture patterns
        pattern_keywords = [
            "microservices", "monolith", "serverless", "event-driven",
            "rest", "graphql", "grpc", "websocket",
            "mvc", "mvvm", "clean architecture", "hexagonal",
            "cqrs", "event-sourcing", "ddd",
        ]

        for kw in pattern_keywords:
            if kw in content:
                patterns.append(kw)

    except Exception:
        pass

    return patterns


def _parse_current_goal(path: Path) -> str:
    """Parse current goal from docs/01_progress.md."""
    if not path.exists():
        return ""

    try:
        content = path.read_text()

        # Look for current/active goal section
        goal_patterns = [
            r"##\s*Current\s+(?:Goal|Task|Focus):?\s*(.+?)(?:\n##|\n\n|$)",
            r"##\s*In\s+Progress:?\s*(.+?)(?:\n##|\n\n|$)",
            r"\*\*Current:\*\*\s*(.+?)(?:\n|$)",
        ]

        for pattern in goal_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:200]  # Limit length

    except Exception:
        pass

    return ""


def _has_linter(project_path: Path) -> bool:
    """Check if linter is configured."""
    linter_configs = [
        ".eslintrc", ".eslintrc.js", ".eslintrc.json",
        "ruff.toml", ".ruff.toml",
        ".flake8", ".pylintrc",
        "biome.json",
        ".golangci.yml",
        "clippy.toml",
    ]

    for config in linter_configs:
        if (project_path / config).exists():
            return True

    # Check pyproject.toml for ruff/black config
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text()
            if "[tool.ruff]" in content or "[tool.black]" in content:
                return True
        except Exception:
            pass

    return False


def _has_type_checking(project_path: Path, language: str) -> bool:
    """Check if type checking is configured."""
    if language == "python":
        type_configs = ["mypy.ini", ".mypy.ini", "pyrightconfig.json"]
        for config in type_configs:
            if (project_path / config).exists():
                return True

        # Check pyproject.toml
        pyproject = project_path / "pyproject.toml"
        if pyproject.exists():
            try:
                content = pyproject.read_text()
                if "[tool.mypy]" in content or "[tool.pyright]" in content:
                    return True
            except Exception:
                pass

    elif language in ("javascript", "typescript"):
        if (project_path / "tsconfig.json").exists():
            return True

    return False
