"""
Capability gap analysis module.

Identifies missing capabilities by comparing existing setup
against standard expectations for the detected tech stack.
"""

from .models import ProjectContext, CapabilityGap, Issue


# Standard capabilities expected for each language
STANDARD_CAPABILITIES: dict[str, list[dict]] = {
    "python": [
        {
            "category": "testing",
            "description": "Automated test execution and coverage",
            "severity": "high",
            "keywords": ["test", "pytest", "unittest", "coverage", "testing"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["test_enforcer", "pytest", "unittest"],
        },
        {
            "category": "linting",
            "description": "Code style and error checking",
            "severity": "medium",
            "keywords": ["lint", "ruff", "flake8", "pylint", "style"],
            "preferred_types": ["hooks", "commands"],
            "covered_by": ["linter", "ruff", "flake8"],
        },
        {
            "category": "type_checking",
            "description": "Static type analysis",
            "severity": "medium",
            "keywords": ["type", "mypy", "pyright", "typing", "types"],
            "preferred_types": ["hooks", "commands"],
            "covered_by": ["type_checker", "mypy", "pyright"],
        },
        {
            "category": "security",
            "description": "Security vulnerability scanning",
            "severity": "critical",
            "keywords": ["security", "audit", "vulnerability", "bandit", "safety"],
            "preferred_types": ["skills", "agents"],
            "covered_by": ["security_auditor", "bandit", "safety"],
        },
        {
            "category": "formatting",
            "description": "Code formatting automation",
            "severity": "low",
            "keywords": ["format", "black", "ruff", "prettier", "style"],
            "preferred_types": ["hooks"],
            "covered_by": ["formatter", "black", "ruff-format"],
        },
        {
            "category": "documentation",
            "description": "API documentation generation",
            "severity": "medium",
            "keywords": ["docs", "documentation", "sphinx", "mkdocs", "api"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["doc_generator", "sphinx", "mkdocs"],
        },
        {
            "category": "dependency_audit",
            "description": "Dependency vulnerability checking",
            "severity": "high",
            "keywords": ["dependency", "audit", "pip-audit", "vulnerable", "outdated"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["dependency_tracker", "pip-audit"],
        },
    ],
    "javascript": [
        {
            "category": "testing",
            "description": "Automated test execution",
            "severity": "high",
            "keywords": ["test", "jest", "vitest", "mocha", "testing", "coverage"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["test_enforcer", "jest", "vitest"],
        },
        {
            "category": "linting",
            "description": "Code linting and style enforcement",
            "severity": "medium",
            "keywords": ["lint", "eslint", "biome", "style", "errors"],
            "preferred_types": ["hooks", "commands"],
            "covered_by": ["linter", "eslint", "biome"],
        },
        {
            "category": "type_checking",
            "description": "TypeScript type checking",
            "severity": "medium",
            "keywords": ["type", "typescript", "tsc", "types", "strict"],
            "preferred_types": ["hooks"],
            "covered_by": ["type_checker", "typescript"],
        },
        {
            "category": "security",
            "description": "Security scanning",
            "severity": "critical",
            "keywords": ["security", "audit", "npm", "vulnerability", "snyk"],
            "preferred_types": ["skills", "agents"],
            "covered_by": ["security_auditor", "npm-audit", "snyk"],
        },
        {
            "category": "bundling",
            "description": "Build and bundle optimization",
            "severity": "medium",
            "keywords": ["build", "bundle", "webpack", "vite", "esbuild"],
            "preferred_types": ["commands"],
            "covered_by": ["builder", "bundler"],
        },
        {
            "category": "documentation",
            "description": "API documentation",
            "severity": "medium",
            "keywords": ["docs", "jsdoc", "typedoc", "documentation", "api"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["doc_generator", "typedoc"],
        },
    ],
    "typescript": [
        # Same as JavaScript plus stricter type requirements
        {
            "category": "testing",
            "description": "Automated test execution",
            "severity": "high",
            "keywords": ["test", "jest", "vitest", "testing", "coverage"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["test_enforcer", "jest", "vitest"],
        },
        {
            "category": "type_checking",
            "description": "Strict TypeScript checking",
            "severity": "high",
            "keywords": ["type", "typescript", "tsc", "strict", "types"],
            "preferred_types": ["hooks"],
            "covered_by": ["type_checker", "typescript"],
        },
        {
            "category": "linting",
            "description": "TypeScript linting",
            "severity": "medium",
            "keywords": ["lint", "eslint", "biome", "typescript-eslint"],
            "preferred_types": ["hooks", "commands"],
            "covered_by": ["linter", "eslint"],
        },
        {
            "category": "security",
            "description": "Security scanning",
            "severity": "critical",
            "keywords": ["security", "audit", "vulnerability"],
            "preferred_types": ["skills", "agents"],
            "covered_by": ["security_auditor"],
        },
    ],
    "rust": [
        {
            "category": "testing",
            "description": "Cargo test execution",
            "severity": "high",
            "keywords": ["test", "cargo", "testing", "coverage"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["test_enforcer", "cargo-test"],
        },
        {
            "category": "linting",
            "description": "Clippy linting",
            "severity": "medium",
            "keywords": ["lint", "clippy", "warnings", "style"],
            "preferred_types": ["hooks"],
            "covered_by": ["linter", "clippy"],
        },
        {
            "category": "security",
            "description": "Security audit",
            "severity": "critical",
            "keywords": ["security", "audit", "cargo-audit", "vulnerability"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["security_auditor", "cargo-audit"],
        },
        {
            "category": "documentation",
            "description": "Rustdoc generation",
            "severity": "medium",
            "keywords": ["docs", "rustdoc", "documentation", "api"],
            "preferred_types": ["commands"],
            "covered_by": ["doc_generator", "rustdoc"],
        },
    ],
    "go": [
        {
            "category": "testing",
            "description": "Go test execution",
            "severity": "high",
            "keywords": ["test", "go", "testing", "coverage"],
            "preferred_types": ["skills", "commands"],
            "covered_by": ["test_enforcer", "go-test"],
        },
        {
            "category": "linting",
            "description": "golangci-lint checking",
            "severity": "medium",
            "keywords": ["lint", "golangci", "vet", "style"],
            "preferred_types": ["hooks"],
            "covered_by": ["linter", "golangci-lint"],
        },
        {
            "category": "security",
            "description": "Security scanning",
            "severity": "critical",
            "keywords": ["security", "gosec", "audit", "vulnerability"],
            "preferred_types": ["skills", "agents"],
            "covered_by": ["security_auditor", "gosec"],
        },
        {
            "category": "documentation",
            "description": "Go documentation",
            "severity": "medium",
            "keywords": ["docs", "godoc", "documentation", "api"],
            "preferred_types": ["commands"],
            "covered_by": ["doc_generator", "godoc"],
        },
    ],
}

# Issue keyword to capability category mapping
ISSUE_KEYWORD_MAPPING: dict[str, str] = {
    # Security
    "security": "security",
    "vulnerability": "security",
    "audit": "security",
    "xss": "security",
    "injection": "security",
    "auth": "security",
    "authentication": "security",
    "authorization": "security",
    # Testing
    "test": "testing",
    "tests": "testing",
    "coverage": "testing",
    "failing": "testing",
    "broken": "testing",
    "unittest": "testing",
    # Documentation
    "docs": "documentation",
    "documentation": "documentation",
    "readme": "documentation",
    "api": "documentation",
    "swagger": "documentation",
    "openapi": "documentation",
    # Performance
    "slow": "performance",
    "performance": "performance",
    "memory": "performance",
    "leak": "performance",
    "optimization": "performance",
    # DevOps
    "deploy": "devops",
    "ci": "devops",
    "cd": "devops",
    "pipeline": "devops",
    "docker": "devops",
    "kubernetes": "devops",
    # Code quality
    "lint": "linting",
    "format": "formatting",
    "style": "linting",
    "refactor": "refactoring",
}

# Severity mapping for different gap categories
CATEGORY_SEVERITY: dict[str, str] = {
    "security": "critical",
    "testing": "high",
    "dependency_audit": "high",
    "type_checking": "medium",
    "linting": "medium",
    "documentation": "medium",
    "formatting": "low",
    "performance": "high",
    "devops": "medium",
    "refactoring": "low",
}


def analyze_capability_gaps(context: ProjectContext) -> list[CapabilityGap]:
    """
    Analyze project context to identify capability gaps.

    Args:
        context: Detected project context

    Returns:
        List of identified capability gaps
    """
    gaps = []

    # Phase 1: Compare against standard capabilities
    standard_gaps = _find_standard_gaps(context)
    gaps.extend(standard_gaps)

    # Phase 2: Analyze documented issues
    issue_gaps = _analyze_issues(context.documented_issues)
    for gap in issue_gaps:
        if not _gap_exists(gaps, gap):
            gaps.append(gap)

    # Phase 3: Project type specific gaps
    type_gaps = _find_project_type_gaps(context)
    for gap in type_gaps:
        if not _gap_exists(gaps, gap):
            gaps.append(gap)

    # Phase 4: Quality tooling gaps
    quality_gaps = _find_quality_gaps(context)
    for gap in quality_gaps:
        if not _gap_exists(gaps, gap):
            gaps.append(gap)

    # Sort by severity
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    gaps.sort(key=lambda g: severity_order.get(g.severity, 4))

    return gaps


def _find_standard_gaps(context: ProjectContext) -> list[CapabilityGap]:
    """Find gaps compared to standard capabilities for the language."""
    gaps = []

    standard_caps = STANDARD_CAPABILITIES.get(context.primary_language, [])

    for cap in standard_caps:
        # Check if any existing element covers this capability
        is_covered = False

        covered_by = cap.get("covered_by", [])
        all_existing = (
            context.existing_skills
            + context.existing_commands
            + context.existing_agents
            + context.existing_mcps
            + context.dependencies
            + context.dev_dependencies
        )

        for existing in all_existing:
            existing_lower = existing.lower()
            if any(cover.lower() in existing_lower for cover in covered_by):
                is_covered = True
                break

        if not is_covered:
            gaps.append(CapabilityGap(
                category=cap["category"],
                description=cap["description"],
                severity=cap["severity"],
                source="standard",
                keywords=cap["keywords"],
                preferred_types=cap.get("preferred_types", ["skills"]),
            ))

    return gaps


def _analyze_issues(issues: list[Issue]) -> list[CapabilityGap]:
    """Convert documented issues to capability gaps."""
    gaps = []

    for issue in issues:
        # Only consider high severity issues
        if issue.severity not in ("critical", "high"):
            continue

        # Extract category from keywords
        category = None
        issue_text = f"{issue.title} {issue.description}".lower()

        for keyword, cat in ISSUE_KEYWORD_MAPPING.items():
            if keyword in issue_text:
                category = cat
                break

        if category:
            gaps.append(CapabilityGap(
                category=category,
                description=f"From issue: {issue.title}",
                severity=issue.severity,
                source=f"issue-{issue.id}",
                keywords=issue.tags + [category],
                preferred_types=["skills", "agents"],
            ))

    return gaps


def _find_project_type_gaps(context: ProjectContext) -> list[CapabilityGap]:
    """Find gaps specific to project type."""
    gaps = []

    project_type_needs: dict[str, list[dict]] = {
        "webapp": [
            {
                "category": "frontend_testing",
                "description": "Frontend/E2E testing",
                "severity": "high",
                "keywords": ["e2e", "cypress", "playwright", "selenium", "frontend"],
                "check_frameworks": ["react", "vue", "next", "svelte"],
            },
            {
                "category": "accessibility",
                "description": "Accessibility testing",
                "severity": "medium",
                "keywords": ["a11y", "accessibility", "wcag", "aria"],
            },
        ],
        "api": [
            {
                "category": "api_testing",
                "description": "API endpoint testing",
                "severity": "high",
                "keywords": ["api", "endpoint", "integration", "postman"],
            },
            {
                "category": "api_documentation",
                "description": "API documentation (OpenAPI/Swagger)",
                "severity": "medium",
                "keywords": ["openapi", "swagger", "api", "docs", "schema"],
            },
        ],
        "library": [
            {
                "category": "documentation",
                "description": "Library documentation",
                "severity": "high",
                "keywords": ["docs", "readme", "api", "documentation", "examples"],
            },
            {
                "category": "versioning",
                "description": "Semantic versioning",
                "severity": "medium",
                "keywords": ["version", "semver", "changelog", "release"],
            },
        ],
        "cli": [
            {
                "category": "cli_testing",
                "description": "CLI integration testing",
                "severity": "high",
                "keywords": ["cli", "command", "integration", "shell"],
            },
        ],
        "data-pipeline": [
            {
                "category": "data_validation",
                "description": "Data validation and quality",
                "severity": "high",
                "keywords": ["data", "validation", "quality", "schema", "pipeline"],
            },
            {
                "category": "monitoring",
                "description": "Pipeline monitoring",
                "severity": "medium",
                "keywords": ["monitor", "observability", "logging", "metrics"],
            },
        ],
    }

    type_needs = project_type_needs.get(context.project_type, [])

    for need in type_needs:
        # Skip if framework requirement not met
        if "check_frameworks" in need:
            if not any(fw in context.frameworks for fw in need["check_frameworks"]):
                continue

        # Check if already covered
        all_existing = (
            context.existing_skills
            + context.existing_commands
            + context.dependencies
        )

        is_covered = any(
            kw in " ".join(all_existing).lower()
            for kw in need["keywords"][:3]
        )

        if not is_covered:
            gaps.append(CapabilityGap(
                category=need["category"],
                description=need["description"],
                severity=need["severity"],
                source="project_type",
                keywords=need["keywords"],
                preferred_types=["skills", "commands"],
            ))

    return gaps


def _find_quality_gaps(context: ProjectContext) -> list[CapabilityGap]:
    """Find gaps in quality tooling configuration."""
    gaps = []

    # No linter configured
    if not context.lint_configured:
        gaps.append(CapabilityGap(
            category="linting",
            description="No linter configured for code quality",
            severity="medium",
            source="analysis",
            keywords=["lint", "linter", "code", "quality", "style"],
            preferred_types=["hooks", "commands"],
        ))

    # No type checking for typed languages
    typed_languages = {"python", "typescript", "javascript"}
    if context.primary_language in typed_languages and not context.type_checking:
        gaps.append(CapabilityGap(
            category="type_checking",
            description="No type checking configured",
            severity="medium",
            source="analysis",
            keywords=["type", "typing", "mypy", "typescript", "strict"],
            preferred_types=["hooks"],
        ))

    # No tests
    if not context.has_tests:
        gaps.append(CapabilityGap(
            category="testing",
            description="No test directory or test files found",
            severity="high",
            source="analysis",
            keywords=["test", "testing", "coverage", "unit", "integration"],
            preferred_types=["skills", "commands"],
        ))

    # No CI/CD
    if not context.has_ci:
        gaps.append(CapabilityGap(
            category="devops",
            description="No CI/CD configuration found",
            severity="medium",
            source="analysis",
            keywords=["ci", "cd", "pipeline", "github", "actions", "gitlab"],
            preferred_types=["commands"],
        ))

    return gaps


def _gap_exists(gaps: list[CapabilityGap], new_gap: CapabilityGap) -> bool:
    """Check if a similar gap already exists."""
    for gap in gaps:
        if gap.category == new_gap.category:
            return True
        # Check keyword overlap
        overlap = set(gap.keywords) & set(new_gap.keywords)
        if len(overlap) >= 3:
            return True
    return False
