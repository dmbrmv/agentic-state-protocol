"""
Skill scoring and ranking module.

Implements the weighted multi-factor scoring algorithm.
"""

import math
from datetime import datetime

from .models import (
    ProjectContext,
    RegistrySkill,
    CapabilityGap,
    SkillRecommendation,
)


class SkillScorer:
    """
    Scores skills based on relevance to project context and capability gaps.

    Scoring weights (configurable):
    - Relevance: 30% - Tech stack and framework match
    - Quality: 20% - Stars, installs, freshness
    - Need: 35% - Addresses documented gaps
    - Compatibility: 15% - No conflicts, fits protocol
    """

    # Normalization ceilings
    MAX_STARS = 50000
    MAX_INSTALLS = 10000

    def __init__(
        self,
        context: ProjectContext,
        gaps: list[CapabilityGap],
        weights: dict[str, float] | None = None,
    ):
        """
        Initialize the scorer.

        Args:
            context: Project context
            gaps: Identified capability gaps
            weights: Custom scoring weights (optional)
        """
        self.context = context
        self.gaps = gaps
        self.weights = weights or {
            "relevance": 0.30,
            "quality": 0.20,
            "need": 0.35,
            "compatibility": 0.15,
        }

        # Pre-compute context tags for matching
        self.context_tags = context.get_all_tags()

    def score_skill(self, skill: RegistrySkill) -> SkillRecommendation:
        """
        Score a single skill and generate a recommendation.

        Args:
            skill: The skill to score

        Returns:
            SkillRecommendation with scores and explanations
        """
        # Calculate individual scores
        relevance = self._calculate_relevance(skill)
        quality = self._calculate_quality(skill)
        need = self._calculate_need(skill)
        compatibility = self._calculate_compatibility(skill)

        # Calculate weighted total
        total = (
            relevance * self.weights["relevance"]
            + quality * self.weights["quality"]
            + need * self.weights["need"]
            + compatibility * self.weights["compatibility"]
        )

        # Generate explanations
        reasons = self._generate_reasons(skill, relevance, quality, need, compatibility)
        addresses = self._find_addressed_gaps(skill)
        conflicts = self._find_conflicts(skill)

        # Determine priority and effort
        priority = self._score_to_priority(total, need)
        effort = self._estimate_effort(skill)

        return SkillRecommendation(
            skill=skill,
            total_score=round(total, 3),
            relevance_score=round(relevance, 3),
            quality_score=round(quality, 3),
            need_score=round(need, 3),
            compatibility_score=round(compatibility, 3),
            reasons=reasons,
            addresses_needs=addresses,
            potential_conflicts=conflicts,
            priority=priority,
            estimated_effort=effort,
        )

    def _calculate_relevance(self, skill: RegistrySkill) -> float:
        """
        Calculate relevance score (0.0 - 1.0).

        Components:
        - Language match: up to 0.40
        - Framework match: up to 0.30
        - Tag relevance: up to 0.20
        - Project type alignment: up to 0.10
        """
        score = 0.0

        # Language matching (0.4 max)
        if self.context.primary_language in skill.supported_languages:
            score += 0.40
        elif any(
            lang in skill.supported_languages
            for lang in self.context.secondary_languages
        ):
            score += 0.20
        elif (
            "generic" in skill.supported_languages
            or not skill.supported_languages
        ):
            score += 0.10  # Generic skills get partial credit

        # Framework matching (0.3 max)
        framework_matches = len(
            set(self.context.frameworks) & set(skill.tags)
        )
        score += min(framework_matches * 0.10, 0.30)

        # Tag relevance (0.2 max)
        tag_overlap = len(self.context_tags & set(skill.tags))
        score += min(tag_overlap * 0.05, 0.20)

        # Project type alignment (0.1 max)
        type_tags = {
            "cli": ["cli", "command-line", "terminal"],
            "webapp": ["web", "frontend", "ui", "react", "vue"],
            "api": ["api", "backend", "rest", "graphql"],
            "library": ["library", "package", "module"],
            "data-pipeline": ["data", "pipeline", "etl"],
        }
        if self.context.project_type in type_tags:
            if any(tag in skill.tags for tag in type_tags[self.context.project_type]):
                score += 0.10

        return min(score, 1.0)

    def _calculate_quality(self, skill: RegistrySkill) -> float:
        """
        Calculate quality score (0.0 - 1.0).

        Components:
        - Stars: up to 0.30
        - Installs: up to 0.30
        - Freshness: up to 0.30
        - Verified: up to 0.10
        """
        # Stars component (logarithmic)
        star_score = 0.0
        if skill.stars > 0:
            star_score = min(
                math.log1p(skill.stars) / math.log1p(self.MAX_STARS), 1.0
            ) * 0.30

        # Installs component (logarithmic)
        install_score = 0.0
        if skill.installs > 0:
            install_score = min(
                math.log1p(skill.installs) / math.log1p(self.MAX_INSTALLS), 1.0
            ) * 0.30

        # Freshness component
        freshness = 0.15  # Default for unknown date
        if skill.last_updated:
            days_old = (datetime.now() - skill.last_updated).days
            if days_old <= 30:
                freshness = 0.30
            elif days_old <= 180:
                # Linear decay from 0.30 to 0.21
                freshness = 0.30 - (days_old - 30) / 150 * 0.09
            elif days_old <= 365:
                # Steeper decay from 0.21 to 0.10
                freshness = 0.21 - (days_old - 180) / 185 * 0.11
            else:
                freshness = 0.10

        # Verified bonus
        verified_score = 0.10 if skill.verified else 0.0

        return star_score + install_score + freshness + verified_score

    def _calculate_need(self, skill: RegistrySkill) -> float:
        """
        Calculate need score (0.0 - 1.0).

        Based on how well the skill addresses identified capability gaps.
        """
        score = 0.0

        for gap in self.gaps:
            match_count = gap.matches_skill(skill)

            if match_count >= 2:  # Significant match
                if gap.severity == "critical":
                    score += 0.25
                elif gap.severity == "high":
                    score += 0.15
                elif gap.severity == "medium":
                    score += 0.08
                else:
                    score += 0.04
            elif match_count == 1:  # Partial match
                score += 0.02

        return min(score, 1.0)

    def _calculate_compatibility(self, skill: RegistrySkill) -> float:
        """
        Calculate compatibility score (0.0 - 1.0).

        Based on conflicts, protocol alignment, and dependencies.
        """
        score = 0.60  # Base score

        # Check for explicit conflicts
        for existing in self.context.existing_skills:
            if existing in skill.conflicts_with:
                score -= 0.20
            # Category saturation check
            if _get_skill_category(existing) == skill.category:
                score -= 0.03

        # Protocol alignment bonus
        protocol_tags = ["agentic", "protocol", "claude", "workflow"]
        if any(tag in skill.tags for tag in protocol_tags):
            score += 0.10

        if skill.category in ("skills", "commands", "agents", "hooks"):
            score += 0.10

        # Dependency satisfaction
        if not skill.dependencies:
            score += 0.20
        else:
            all_deps = set(
                self.context.dependencies + self.context.dev_dependencies
            )
            satisfied = sum(
                1 for dep in skill.dependencies
                if any(dep.lower() in d.lower() for d in all_deps)
            )
            if skill.dependencies:
                ratio = satisfied / len(skill.dependencies)
                score += ratio * 0.20

        return max(0.0, min(score, 1.0))

    def _generate_reasons(
        self,
        skill: RegistrySkill,
        relevance: float,
        quality: float,
        need: float,
        compatibility: float,
    ) -> list[str]:
        """Generate human-readable reasons for recommendation."""
        reasons = []

        # Relevance reasons
        if self.context.primary_language in skill.supported_languages:
            reasons.append(f"Supports {self.context.primary_language}")

        framework_matches = set(self.context.frameworks) & set(skill.tags)
        if framework_matches:
            reasons.append(f"Works with {', '.join(list(framework_matches)[:2])}")

        # Quality reasons
        if skill.verified:
            reasons.append("Verified by Anthropic")
        if skill.stars > 10000:
            reasons.append(f"Popular ({skill.stars:,} stars)")
        if skill.installs > 500:
            reasons.append(f"Widely used ({skill.installs:,} installs)")

        # Need reasons
        addressed = self._find_addressed_gaps(skill)
        if addressed:
            reasons.append(f"Addresses: {', '.join(addressed[:2])}")

        # If no specific reasons, add generic ones
        if not reasons:
            if relevance > 0.5:
                reasons.append("Good tech stack match")
            if need > 0.5:
                reasons.append("Fills capability gap")

        return reasons[:4]  # Limit to 4 reasons

    def _find_addressed_gaps(self, skill: RegistrySkill) -> list[str]:
        """Find which gaps this skill addresses."""
        addressed = []

        for gap in self.gaps:
            match_count = gap.matches_skill(skill)
            if match_count >= 2:
                addressed.append(gap.category)

        return addressed

    def _find_conflicts(self, skill: RegistrySkill) -> list[str]:
        """Find potential conflicts with existing skills."""
        conflicts = []

        for existing in self.context.existing_skills:
            if existing in skill.conflicts_with:
                conflicts.append(f"Conflicts with {existing}")

        # Check category saturation
        existing_categories = [
            _get_skill_category(s) for s in self.context.existing_skills
        ]
        if existing_categories.count(skill.category) >= 3:
            conflicts.append(f"Many {skill.category} already installed")

        return conflicts

    def _score_to_priority(self, total: float, need: float) -> str:
        """Convert score to priority level."""
        if total >= 0.80 or (total >= 0.70 and need >= 0.50):
            return "critical"
        elif total >= 0.60:
            return "recommended"
        else:
            return "optional"

    def _estimate_effort(self, skill: RegistrySkill) -> str:
        """Estimate installation/integration effort."""
        if not skill.dependencies:
            return "minimal"
        elif len(skill.dependencies) <= 3:
            return "moderate"
        else:
            return "significant"


def _get_skill_category(skill_name: str) -> str:
    """
    Infer category from skill name.

    Simple heuristic based on naming conventions.
    """
    name_lower = skill_name.lower()

    if "agent" in name_lower:
        return "agents"
    elif "command" in name_lower or "cmd" in name_lower:
        return "commands"
    elif "hook" in name_lower:
        return "hooks"
    else:
        return "skills"
