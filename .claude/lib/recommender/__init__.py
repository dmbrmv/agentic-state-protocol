"""
Skill Recommender Module

Analyzes project context and recommends relevant skills from claude-plugins.dev
based on tech stack, documented needs, and capability gaps.
"""

from .models import (
    ProjectContext,
    RegistrySkill,
    CapabilityGap,
    SkillRecommendation,
    RegistryCache,
)
from .context_detector import detect_project_context
from .gap_analyzer import analyze_capability_gaps
from .registry_client import RegistryClient
from .scorer import SkillScorer
from .presenter import RecommendationPresenter

__all__ = [
    # Models
    "ProjectContext",
    "RegistrySkill",
    "CapabilityGap",
    "SkillRecommendation",
    "RegistryCache",
    # Functions
    "detect_project_context",
    "analyze_capability_gaps",
    # Classes
    "RegistryClient",
    "SkillScorer",
    "RecommendationPresenter",
    # Main entry point
    "recommend_skills",
]


def recommend_skills(
    project_path: str,
    limit: int = 10,
    min_score: float = 0.5,
    force_refresh: bool = False,
) -> list[SkillRecommendation]:
    """
    Main entry point for skill recommendation algorithm.

    Args:
        project_path: Path to the project root
        limit: Maximum number of recommendations
        min_score: Minimum score threshold
        force_refresh: Force registry cache refresh

    Returns:
        List of scored skill recommendations
    """
    from pathlib import Path

    path = Path(project_path)

    # Phase 1: Context Detection
    context = detect_project_context(path)

    # Phase 2: Gap Analysis
    gaps = analyze_capability_gaps(context)

    # Phase 3: Registry Fetch
    client = RegistryClient(cache_dir=path / ".claude" / "cache")
    skills = client.fetch_skills(force_refresh=force_refresh)

    # Phase 4: Match and Rank
    scorer = SkillScorer(context, gaps)
    recommendations = []

    for skill in skills:
        # Skip already installed
        if skill.identifier in context.existing_skills:
            continue

        # Score the skill
        recommendation = scorer.score_skill(skill)

        if recommendation.total_score >= min_score:
            recommendations.append(recommendation)

    # Sort by score descending
    recommendations.sort(key=lambda r: r.total_score, reverse=True)

    # Apply diversity filter and limit
    recommendations = _apply_diversity_filter(recommendations)
    recommendations = recommendations[:limit]

    return recommendations


def _apply_diversity_filter(
    recommendations: list[SkillRecommendation],
    max_per_category: int = 3,
) -> list[SkillRecommendation]:
    """
    Filter to ensure diversity across categories.

    Prevents too many similar skills from being recommended.
    """
    category_counts: dict[str, int] = {}
    filtered = []

    for rec in recommendations:
        category = rec.skill.category
        count = category_counts.get(category, 0)

        if count < max_per_category:
            filtered.append(rec)
            category_counts[category] = count + 1

    return filtered
