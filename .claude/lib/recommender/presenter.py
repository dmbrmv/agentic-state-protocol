"""
Recommendation presentation module.

Formats and displays skill recommendations.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from .models import ProjectContext, CapabilityGap, SkillRecommendation


class RecommendationPresenter:
    """Formats and presents skill recommendations."""

    def __init__(self, context: ProjectContext, gaps: list[CapabilityGap]):
        """
        Initialize the presenter.

        Args:
            context: Project context for display
            gaps: Identified gaps for display
        """
        self.context = context
        self.gaps = gaps

    def format_full_report(
        self,
        recommendations: list[SkillRecommendation],
    ) -> str:
        """
        Format a full recommendation report.

        Args:
            recommendations: Scored recommendations

        Returns:
            Formatted report string
        """
        lines = []

        # Header
        lines.append("SKILL RECOMMENDATIONS")
        lines.append("=" * 70)
        lines.append("")

        # Context summary
        lines.append("Project Context:")
        lines.append(f"  Language: {self.context.primary_language}")
        if self.context.frameworks:
            lines.append(f"  Frameworks: {', '.join(self.context.frameworks[:5])}")
        lines.append(f"  Existing Skills: {len(self.context.existing_skills)}")
        lines.append(f"  Identified Gaps: {len(self.gaps)}")
        lines.append("")

        # Gap summary
        if self.gaps:
            lines.append("Capability Gaps Detected:")
            for gap in self.gaps[:5]:
                severity_icon = _severity_icon(gap.severity)
                lines.append(f"  {severity_icon} [{gap.severity.upper()}] {gap.category}: {gap.description}")
            if len(self.gaps) > 5:
                lines.append(f"  ... and {len(self.gaps) - 5} more")
            lines.append("")

        lines.append("-" * 70)

        if not recommendations:
            lines.append("")
            lines.append("No matching skills found.")
            lines.append("")
            lines.append("Suggestions:")
            lines.append("  - Try refreshing the registry: /discover --refresh")
            lines.append("  - Browse manually: https://claude-plugins.dev/")
            lines.append("")
            return "\n".join(lines)

        # Group by priority
        critical = [r for r in recommendations if r.priority == "critical"]
        recommended = [r for r in recommendations if r.priority == "recommended"]
        optional = [r for r in recommendations if r.priority == "optional"]

        if critical:
            lines.append("")
            lines.append("## CRITICAL (Score > 0.8)")
            lines.append("")
            for i, rec in enumerate(critical, 1):
                lines.extend(self._format_recommendation(i, rec))

        if recommended:
            lines.append("")
            lines.append("## RECOMMENDED (Score 0.6-0.8)")
            lines.append("")
            for i, rec in enumerate(recommended, len(critical) + 1):
                lines.extend(self._format_recommendation(i, rec))

        if optional:
            lines.append("")
            lines.append("## OPTIONAL (Score 0.5-0.6)")
            lines.append("")
            for i, rec in enumerate(optional, len(critical) + len(recommended) + 1):
                lines.extend(self._format_recommendation(i, rec))

        # Footer
        lines.append("")
        lines.append("=" * 70)
        lines.append("")
        lines.append("Actions:")
        lines.append("  - Install specific: Enter number (1, 2, 3...)")
        lines.append("  - Install all critical: 'install critical'")
        lines.append("  - Skip: 'none' or 'skip'")
        lines.append("  - More details: 'details [number]'")
        lines.append("")

        return "\n".join(lines)

    def _format_recommendation(
        self,
        index: int,
        rec: SkillRecommendation,
    ) -> list[str]:
        """Format a single recommendation."""
        lines = []

        skill = rec.skill
        score_bar = _score_bar(rec.total_score)

        lines.append(f"### {index}. {skill.name} {score_bar} ({rec.total_score:.2f})")
        lines.append(f"    Package: {skill.identifier}")
        lines.append(f"    Category: {skill.category}")

        # Quality signals
        quality_parts = []
        if skill.stars > 0:
            quality_parts.append(f"{_format_number(skill.stars)} stars")
        if skill.installs > 0:
            quality_parts.append(f"{_format_number(skill.installs)} installs")
        if skill.verified:
            quality_parts.append("verified")
        if quality_parts:
            lines.append(f"    Quality: {' | '.join(quality_parts)}")

        # Reasons
        if rec.reasons:
            lines.append(f"    Why: {'; '.join(rec.reasons)}")

        # Addressed needs
        if rec.addresses_needs:
            lines.append(f"    Addresses: {', '.join(rec.addresses_needs)}")

        # Conflicts warning
        if rec.potential_conflicts:
            lines.append(f"    Warning: {'; '.join(rec.potential_conflicts)}")

        # Install command
        lines.append(f"    Install: {skill.install_command}")
        lines.append("")

        return lines

    def format_compact(
        self,
        recommendations: list[SkillRecommendation],
        limit: int = 5,
    ) -> str:
        """
        Format a compact recommendation list.

        Args:
            recommendations: Scored recommendations
            limit: Max items to show

        Returns:
            Compact formatted string
        """
        if not recommendations:
            return "No skill recommendations available."

        lines = ["Top Skill Recommendations:", ""]

        for i, rec in enumerate(recommendations[:limit], 1):
            score_bar = _score_bar(rec.total_score)
            lines.append(
                f"  {i}. {rec.skill.name} {score_bar} "
                f"({rec.total_score:.2f}) - {rec.priority}"
            )

        if len(recommendations) > limit:
            lines.append(f"  ... and {len(recommendations) - limit} more")

        lines.append("")
        lines.append("Run /discover for full details")

        return "\n".join(lines)

    def format_json(
        self,
        recommendations: list[SkillRecommendation],
    ) -> dict[str, Any]:
        """
        Format recommendations as JSON-serializable dict.

        Args:
            recommendations: Scored recommendations

        Returns:
            JSON-serializable dictionary
        """
        return {
            "generated_at": datetime.now().isoformat(),
            "context": {
                "primary_language": self.context.primary_language,
                "frameworks": self.context.frameworks,
                "existing_skills": self.context.existing_skills,
                "project_type": self.context.project_type,
            },
            "gaps": [
                {
                    "category": g.category,
                    "description": g.description,
                    "severity": g.severity,
                }
                for g in self.gaps
            ],
            "recommendations": [
                {
                    "rank": i + 1,
                    "identifier": rec.skill.identifier,
                    "name": rec.skill.name,
                    "category": rec.skill.category,
                    "total_score": rec.total_score,
                    "scores": {
                        "relevance": rec.relevance_score,
                        "quality": rec.quality_score,
                        "need": rec.need_score,
                        "compatibility": rec.compatibility_score,
                    },
                    "priority": rec.priority,
                    "reasons": rec.reasons,
                    "addresses": rec.addresses_needs,
                    "conflicts": rec.potential_conflicts,
                    "install_command": rec.install_command,
                }
                for i, rec in enumerate(recommendations)
            ],
        }

    def format_skill_detail(
        self,
        rec: SkillRecommendation,
    ) -> str:
        """
        Format detailed view of a single skill.

        Args:
            rec: The recommendation to detail

        Returns:
            Detailed formatted string
        """
        skill = rec.skill
        lines = []

        lines.append("=" * 70)
        lines.append(f"SKILL DETAILS: {skill.name}")
        lines.append("=" * 70)
        lines.append("")

        lines.append(f"Identifier: {skill.identifier}")
        lines.append(f"Category: {skill.category}")
        lines.append("")

        if skill.description:
            lines.append("Description:")
            lines.append(f"  {skill.description}")
            lines.append("")

        lines.append("Scores:")
        lines.append(f"  Total:         {_score_bar(rec.total_score)} {rec.total_score:.3f}")
        lines.append(f"  Relevance:     {_score_bar(rec.relevance_score)} {rec.relevance_score:.3f}")
        lines.append(f"  Quality:       {_score_bar(rec.quality_score)} {rec.quality_score:.3f}")
        lines.append(f"  Need:          {_score_bar(rec.need_score)} {rec.need_score:.3f}")
        lines.append(f"  Compatibility: {_score_bar(rec.compatibility_score)} {rec.compatibility_score:.3f}")
        lines.append("")

        lines.append("Quality Signals:")
        lines.append(f"  Stars: {_format_number(skill.stars)}")
        lines.append(f"  Installs: {_format_number(skill.installs)}")
        lines.append(f"  Verified: {'Yes' if skill.verified else 'No'}")
        if skill.last_updated:
            lines.append(f"  Last Updated: {skill.last_updated.strftime('%Y-%m-%d')}")
        lines.append("")

        if skill.tags:
            lines.append(f"Tags: {', '.join(skill.tags)}")
            lines.append("")

        if skill.supported_languages:
            lines.append(f"Languages: {', '.join(skill.supported_languages)}")
            lines.append("")

        if skill.dependencies:
            lines.append(f"Dependencies: {', '.join(skill.dependencies)}")
            lines.append("")

        if rec.reasons:
            lines.append("Why Recommended:")
            for reason in rec.reasons:
                lines.append(f"  - {reason}")
            lines.append("")

        if rec.addresses_needs:
            lines.append("Addresses Gaps:")
            for gap in rec.addresses_needs:
                lines.append(f"  - {gap}")
            lines.append("")

        if rec.potential_conflicts:
            lines.append("Potential Conflicts:")
            for conflict in rec.potential_conflicts:
                lines.append(f"  - {conflict}")
            lines.append("")

        lines.append(f"Install Command:")
        lines.append(f"  {skill.install_command}")
        lines.append("")

        if skill.source_url:
            lines.append(f"Source: {skill.source_url}")
        if skill.readme_url:
            lines.append(f"Documentation: {skill.readme_url}")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)


def _severity_icon(severity: str) -> str:
    """Get icon for severity level."""
    icons = {
        "critical": "[!]",
        "high": "[H]",
        "medium": "[M]",
        "low": "[L]",
    }
    return icons.get(severity, "[-]")


def _score_bar(score: float, width: int = 10) -> str:
    """Generate ASCII score bar."""
    filled = int(score * width)
    empty = width - filled
    return f"[{'#' * filled}{'-' * empty}]"


def _format_number(num: int) -> str:
    """Format number with K/M suffix."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}k"
    else:
        return str(num)
