"""
Data models for the skill recommender system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Issue:
    """Parsed issue from docs/02_issues.md."""

    id: str
    title: str
    severity: str  # "critical", "high", "medium", "low"
    description: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class ProjectContext:
    """Detected project context for skill matching."""

    # Primary tech stack detection
    primary_language: str = "unknown"
    secondary_languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)

    # File structure analysis
    has_tests: bool = False
    has_docs: bool = False
    has_ci: bool = False
    project_type: str = "unknown"  # cli, webapp, library, api, data-pipeline

    # Dependency ecosystem
    package_manager: str = "unknown"
    dependencies: list[str] = field(default_factory=list)
    dev_dependencies: list[str] = field(default_factory=list)

    # Protocol integration
    existing_skills: list[str] = field(default_factory=list)
    existing_commands: list[str] = field(default_factory=list)
    existing_agents: list[str] = field(default_factory=list)
    existing_mcps: list[str] = field(default_factory=list)

    # Needs from documentation
    documented_issues: list[Issue] = field(default_factory=list)
    architecture_patterns: list[str] = field(default_factory=list)
    current_goal: str = ""

    # Quality signals
    test_coverage: float | None = None
    lint_configured: bool = False
    type_checking: bool = False

    def get_all_tags(self) -> set[str]:
        """Get all relevant tags for matching."""
        tags = {self.primary_language}
        tags.update(self.secondary_languages)
        tags.update(self.frameworks)
        tags.update(self.architecture_patterns)
        if self.has_tests:
            tags.add("testing")
        if self.has_ci:
            tags.add("ci-cd")
        if self.project_type != "unknown":
            tags.add(self.project_type)
        return tags


@dataclass
class RegistrySkill:
    """Skill from claude-plugins.dev registry."""

    # Identifiers
    identifier: str  # @owner/repo/name format
    name: str
    description: str = ""

    # Categorization
    category: str = "skills"  # skills, agents, commands, hooks
    tags: list[str] = field(default_factory=list)
    supported_languages: list[str] = field(default_factory=list)

    # Quality signals
    stars: int = 0
    installs: int = 0
    last_updated: datetime | None = None
    verified: bool = False

    # Technical requirements
    dependencies: list[str] = field(default_factory=list)
    conflicts_with: list[str] = field(default_factory=list)
    min_claude_version: str = ""

    # Content
    install_command: str = ""
    readme_url: str | None = None
    source_url: str | None = None

    def __post_init__(self):
        """Set install command if not provided."""
        if not self.install_command and self.identifier:
            self.install_command = f"npx claude-plugins install {self.identifier}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RegistrySkill":
        """Create from dictionary (API response)."""
        last_updated = None
        if data.get("last_updated"):
            try:
                last_updated = datetime.fromisoformat(
                    data["last_updated"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        return cls(
            identifier=data.get("identifier", data.get("id", "")),
            name=data.get("name", ""),
            description=data.get("description", ""),
            category=data.get("category", "skills"),
            tags=data.get("tags", []),
            supported_languages=data.get("supported_languages", data.get("languages", [])),
            stars=data.get("stars", 0),
            installs=data.get("installs", data.get("downloads", 0)),
            last_updated=last_updated,
            verified=data.get("verified", False),
            dependencies=data.get("dependencies", []),
            conflicts_with=data.get("conflicts_with", []),
            readme_url=data.get("readme_url"),
            source_url=data.get("source_url", data.get("repository")),
        )


@dataclass
class CapabilityGap:
    """Identified capability missing from current setup."""

    category: str  # testing, security, docs, linting, etc.
    description: str
    severity: str  # critical, high, medium, low
    source: str  # How detected: "standard", "issue", "analysis"

    # Matching hints
    keywords: list[str] = field(default_factory=list)
    preferred_types: list[str] = field(default_factory=list)  # skill, agent, command

    def matches_skill(self, skill: RegistrySkill) -> int:
        """
        Calculate how well a skill matches this gap.

        Returns:
            Number of keyword matches (0 = no match)
        """
        skill_keywords = set(
            skill.tags
            + [skill.category]
            + skill.name.lower().split()
            + skill.description.lower().split()[:20]
        )
        gap_keywords = set(kw.lower() for kw in self.keywords)

        return len(skill_keywords & gap_keywords)


@dataclass
class SkillRecommendation:
    """A scored skill recommendation."""

    skill: RegistrySkill

    # Scoring breakdown
    total_score: float = 0.0
    relevance_score: float = 0.0
    quality_score: float = 0.0
    need_score: float = 0.0
    compatibility_score: float = 0.0

    # Explanation
    reasons: list[str] = field(default_factory=list)
    addresses_needs: list[str] = field(default_factory=list)
    potential_conflicts: list[str] = field(default_factory=list)

    # Classification
    priority: str = "optional"  # critical, recommended, optional
    estimated_effort: str = "minimal"  # minimal, moderate, significant

    @property
    def install_command(self) -> str:
        """Get the install command for this skill."""
        return self.skill.install_command


@dataclass
class RegistryCache:
    """Cached registry data for efficiency."""

    last_updated: datetime
    ttl_hours: int = 24
    skills: list[RegistrySkill] = field(default_factory=list)

    # Indices for fast lookup
    by_language: dict[str, list[str]] = field(default_factory=dict)
    by_category: dict[str, list[str]] = field(default_factory=dict)
    by_tag: dict[str, list[str]] = field(default_factory=dict)

    def is_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self.last_updated:
            return False
        age = datetime.now() - self.last_updated
        return age.total_seconds() < self.ttl_hours * 3600

    def get_skills_by_language(self, language: str) -> list[RegistrySkill]:
        """Get skills that support a specific language."""
        identifiers = self.by_language.get(language, [])
        identifier_set = set(identifiers)
        return [s for s in self.skills if s.identifier in identifier_set]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RegistryCache":
        """Create from dictionary (loaded from JSON)."""
        last_updated = datetime.fromisoformat(
            data.get("last_updated", datetime.now().isoformat())
        )
        skills = [
            RegistrySkill.from_dict(s)
            for s in data.get("skills", [])
        ]

        cache = cls(
            last_updated=last_updated,
            ttl_hours=data.get("ttl_hours", 24),
            skills=skills,
            by_language=data.get("by_language", {}),
            by_category=data.get("by_category", {}),
            by_tag=data.get("by_tag", {}),
        )

        # Rebuild indices if missing
        if not cache.by_language:
            cache._build_indices()

        return cache

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "last_updated": self.last_updated.isoformat(),
            "ttl_hours": self.ttl_hours,
            "skills": [
                {
                    "identifier": s.identifier,
                    "name": s.name,
                    "description": s.description,
                    "category": s.category,
                    "tags": s.tags,
                    "supported_languages": s.supported_languages,
                    "stars": s.stars,
                    "installs": s.installs,
                    "last_updated": s.last_updated.isoformat() if s.last_updated else None,
                    "verified": s.verified,
                    "dependencies": s.dependencies,
                    "conflicts_with": s.conflicts_with,
                    "source_url": s.source_url,
                }
                for s in self.skills
            ],
            "by_language": self.by_language,
            "by_category": self.by_category,
            "by_tag": self.by_tag,
        }

    def _build_indices(self):
        """Build lookup indices from skills list."""
        self.by_language = {}
        self.by_category = {}
        self.by_tag = {}

        for skill in self.skills:
            # Index by language
            for lang in skill.supported_languages:
                if lang not in self.by_language:
                    self.by_language[lang] = []
                self.by_language[lang].append(skill.identifier)

            # Index by category
            cat = skill.category
            if cat not in self.by_category:
                self.by_category[cat] = []
            self.by_category[cat].append(skill.identifier)

            # Index by tag
            for tag in skill.tags:
                if tag not in self.by_tag:
                    self.by_tag[tag] = []
                self.by_tag[tag].append(skill.identifier)
