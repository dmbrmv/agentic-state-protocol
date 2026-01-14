"""
Registry client for claude-plugins.dev.

Handles fetching, caching, and parsing of registry data.
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import RegistrySkill, RegistryCache


# Fallback list of popular skills for offline operation
FALLBACK_SKILLS: list[dict[str, Any]] = [
    {
        "identifier": "@anthropics/claude-code-plugins/security-guidance",
        "name": "Security Guidance",
        "description": "Security-focused code review and guidance",
        "category": "skills",
        "tags": ["security", "audit", "review", "vulnerability"],
        "supported_languages": ["python", "javascript", "typescript", "go", "rust"],
        "stars": 55900,
        "installs": 595,
        "verified": True,
    },
    {
        "identifier": "@anthropics/claude-code-plugins/frontend-design",
        "name": "Frontend Design",
        "description": "UI/UX design patterns and component architecture",
        "category": "skills",
        "tags": ["frontend", "ui", "design", "react", "components"],
        "supported_languages": ["javascript", "typescript"],
        "stars": 55900,
        "installs": 595,
        "verified": True,
    },
    {
        "identifier": "@wshobson/claude-code-workflows/python-development",
        "name": "Python Development",
        "description": "Modern Python development patterns and best practices",
        "category": "skills",
        "tags": ["python", "development", "patterns", "fastapi", "async"],
        "supported_languages": ["python"],
        "stars": 25200,
        "installs": 728,
        "verified": False,
    },
    {
        "identifier": "@wshobson/claude-code-workflows/backend-development",
        "name": "Backend Development",
        "description": "Backend API design, databases, and architecture",
        "category": "skills",
        "tags": ["backend", "api", "database", "architecture"],
        "supported_languages": ["python", "javascript", "typescript", "go"],
        "stars": 25200,
        "installs": 728,
        "verified": False,
    },
    {
        "identifier": "@wshobson/claude-code-workflows/code-documentation",
        "name": "Code Documentation",
        "description": "Documentation generation and maintenance",
        "category": "skills",
        "tags": ["docs", "documentation", "api", "readme", "comments"],
        "supported_languages": ["python", "javascript", "typescript", "rust", "go"],
        "stars": 25200,
        "installs": 500,
        "verified": False,
    },
    {
        "identifier": "@feiskyer/claude-code-settings/code-refactoring",
        "name": "Code Refactoring",
        "description": "Code refactoring patterns and techniques",
        "category": "skills",
        "tags": ["refactor", "clean", "patterns", "architecture"],
        "supported_languages": ["python", "javascript", "typescript", "go", "rust"],
        "stars": 12000,
        "installs": 450,
        "verified": False,
    },
    {
        "identifier": "@davila7/claude-code-templates/test-generator",
        "name": "Test Generator",
        "description": "Automatic test generation and coverage improvement",
        "category": "agents",
        "tags": ["test", "testing", "coverage", "unit", "integration"],
        "supported_languages": ["python", "javascript", "typescript"],
        "stars": 8500,
        "installs": 320,
        "verified": False,
    },
    {
        "identifier": "@davila7/claude-code-templates/pr-reviewer",
        "name": "PR Reviewer",
        "description": "Automated pull request review agent",
        "category": "agents",
        "tags": ["pr", "review", "github", "code-review"],
        "supported_languages": ["python", "javascript", "typescript", "go", "rust"],
        "stars": 8500,
        "installs": 280,
        "verified": False,
    },
]


class RegistryClient:
    """Client for fetching and caching claude-plugins.dev registry data."""

    def __init__(
        self,
        cache_dir: Path | None = None,
        cache_ttl_hours: int = 24,
    ):
        """
        Initialize the registry client.

        Args:
            cache_dir: Directory to store cache files
            cache_ttl_hours: Cache time-to-live in hours
        """
        self.cache_dir = cache_dir or Path.home() / ".claude" / "cache"
        self.cache_ttl_hours = cache_ttl_hours
        self.cache_file = self.cache_dir / "registry.json"

        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch_skills(
        self,
        force_refresh: bool = False,
        limit: int = 500,
    ) -> list[RegistrySkill]:
        """
        Fetch skills from registry with caching.

        Args:
            force_refresh: Force cache refresh
            limit: Maximum skills to fetch

        Returns:
            List of registry skills
        """
        # Try cache first
        if not force_refresh:
            cache = self._load_cache()
            if cache and cache.is_valid():
                return cache.skills

        # Fetch fresh data
        skills = self._fetch_via_cli(limit)

        if skills:
            # Update cache
            self._save_cache(skills)
            return skills

        # Fallback chain
        cache = self._load_cache()
        if cache:
            # Use stale cache
            return cache.skills

        # Final fallback
        return [RegistrySkill.from_dict(s) for s in FALLBACK_SKILLS]

    def _fetch_via_cli(self, limit: int) -> list[RegistrySkill]:
        """
        Fetch skills using the claude-plugins CLI.

        Args:
            limit: Maximum number of skills

        Returns:
            List of skills or empty list on failure
        """
        skills = []

        try:
            # Try npx claude-plugins search
            result = subprocess.run(
                [
                    "npx",
                    "--yes",
                    "claude-plugins",
                    "search",
                    "--json",
                    "--limit",
                    str(limit),
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                if isinstance(data, list):
                    skills = [RegistrySkill.from_dict(item) for item in data]
                elif isinstance(data, dict) and "skills" in data:
                    skills = [RegistrySkill.from_dict(item) for item in data["skills"]]
                elif isinstance(data, dict) and "results" in data:
                    skills = [RegistrySkill.from_dict(item) for item in data["results"]]

        except subprocess.TimeoutExpired:
            pass
        except FileNotFoundError:
            # npx not available
            pass
        except json.JSONDecodeError:
            pass
        except Exception:
            pass

        # If CLI failed, try alternative methods
        if not skills:
            skills = self._fetch_via_alternative()

        return skills

    def _fetch_via_alternative(self) -> list[RegistrySkill]:
        """
        Alternative fetch methods when CLI is unavailable.

        Returns:
            List of skills or empty list
        """
        # Try to read from a pre-populated registry file
        local_registry = self.cache_dir.parent / "registry" / "skills.json"
        if local_registry.exists():
            try:
                data = json.loads(local_registry.read_text())
                if isinstance(data, list):
                    return [RegistrySkill.from_dict(item) for item in data]
            except Exception:
                pass

        return []

    def _load_cache(self) -> RegistryCache | None:
        """Load cache from disk."""
        if not self.cache_file.exists():
            return None

        try:
            data = json.loads(self.cache_file.read_text())
            cache = RegistryCache.from_dict(data)
            cache.ttl_hours = self.cache_ttl_hours
            return cache
        except Exception:
            return None

    def _save_cache(self, skills: list[RegistrySkill]) -> None:
        """Save skills to cache."""
        cache = RegistryCache(
            last_updated=datetime.now(),
            ttl_hours=self.cache_ttl_hours,
            skills=skills,
        )
        cache._build_indices()

        try:
            self.cache_file.write_text(json.dumps(cache.to_dict(), indent=2))
        except Exception:
            pass

    def search(
        self,
        query: str,
        language: str | None = None,
        category: str | None = None,
        limit: int = 20,
    ) -> list[RegistrySkill]:
        """
        Search skills with filters.

        Args:
            query: Search query
            language: Filter by language
            category: Filter by category
            limit: Maximum results

        Returns:
            Filtered and ranked skills
        """
        all_skills = self.fetch_skills()
        results = []

        query_lower = query.lower()
        query_words = set(query_lower.split())

        for skill in all_skills:
            # Apply filters
            if language and language not in skill.supported_languages:
                continue
            if category and skill.category != category:
                continue

            # Calculate relevance score
            score = 0

            # Name match
            if query_lower in skill.name.lower():
                score += 10

            # Tag match
            for tag in skill.tags:
                if tag.lower() in query_words or any(q in tag.lower() for q in query_words):
                    score += 3

            # Description match
            desc_lower = skill.description.lower()
            for word in query_words:
                if word in desc_lower:
                    score += 1

            if score > 0:
                results.append((score, skill))

        # Sort by score descending
        results.sort(key=lambda x: (-x[0], -x[1].stars))

        return [skill for _, skill in results[:limit]]

    def get_skill(self, identifier: str) -> RegistrySkill | None:
        """
        Get a specific skill by identifier.

        Args:
            identifier: Skill identifier (@owner/repo/name)

        Returns:
            Skill or None if not found
        """
        all_skills = self.fetch_skills()

        for skill in all_skills:
            if skill.identifier == identifier:
                return skill

        return None

    def install_skill(self, identifier: str) -> tuple[bool, str]:
        """
        Install a skill from the registry.

        Args:
            identifier: Skill identifier

        Returns:
            Tuple of (success, message)
        """
        try:
            result = subprocess.run(
                ["npx", "--yes", "claude-plugins", "install", identifier],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                return True, f"Successfully installed {identifier}"
            else:
                return False, f"Installation failed: {result.stderr or result.stdout}"

        except subprocess.TimeoutExpired:
            return False, "Installation timed out"
        except FileNotFoundError:
            return False, "npx not found. Please install Node.js"
        except Exception as e:
            return False, f"Installation error: {str(e)}"

    def get_cache_status(self) -> dict[str, Any]:
        """
        Get cache status information.

        Returns:
            Dictionary with cache status
        """
        cache = self._load_cache()

        if not cache:
            return {
                "exists": False,
                "valid": False,
                "skill_count": 0,
                "last_updated": None,
            }

        return {
            "exists": True,
            "valid": cache.is_valid(),
            "skill_count": len(cache.skills),
            "last_updated": cache.last_updated.isoformat() if cache.last_updated else None,
            "ttl_hours": cache.ttl_hours,
            "languages": list(cache.by_language.keys()),
            "categories": list(cache.by_category.keys()),
        }
