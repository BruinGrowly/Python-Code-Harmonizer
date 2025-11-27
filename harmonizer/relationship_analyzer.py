#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Relationship Structure Analyzer for LJPW Framework

Based on the insight: "Relationships between constants are more important than constants themselves"

This module provides tools to analyze whether a system exhibits healthy LJPW coupling patterns,
regardless of absolute magnitudes.
"""

from typing import Dict, List
import math
from harmonizer.ljpw_baselines import NumericalEquivalents, ReferencePoints


class RelationshipPatterns:
    """Expected patterns in LJPW coupling structure"""

    # Qualitative expectations for coupling
    LOVE_AMPLIFIES = {
        "LJ": (1.2, 1.6),  # Should be > 1.0 (amplification)
        "LP": (1.1, 1.5),
        "LW": (1.3, 1.7),
    }

    POWER_CONSTRAINS = {
        "PL": (0.4, 0.8),  # Should be < 1.0 (constraint)
        "PJ": (0.6, 1.0),
        "PW": (0.3, 0.7),
    }

    JUSTICE_SUPPORTS_WISDOM = {
        "JW": (1.0, 1.4),  # J→W should be strong
        "JP": (0.5, 0.9),  # J→P should be weaker than J→W
    }

    ASYMMETRY_PATTERNS = [
        ("LJ", "JL", "Love gives more to Justice than receives"),
        ("LP", "PL", "Love gives more to Power than receives"),
        ("LW", "WL", "Love and Wisdom are nearly symmetric"),
        ("PJ", "JP", "Power receives more from Justice than gives"),
    ]


class RelationshipAnalyzer:
    """
    Analyzes whether a system exhibits healthy LJPW relationship patterns.

    This focuses on structural properties (coupling patterns) rather than
    exact numerical values of constants.
    """

    def __init__(self):
        self.NE = ReferencePoints.NATURAL_EQUILIBRIUM
        self.constants = {
            "L": NumericalEquivalents.L,
            "J": NumericalEquivalents.J,
            "P": NumericalEquivalents.P,
            "W": NumericalEquivalents.W,
        }

    def check_proportions(
        self, L: float, J: float, P: float, W: float, tolerance: float = 0.3
    ) -> Dict[str, any]:
        """
        Check if L:J:P:W proportions match Natural Equilibrium (scale-invariant).

        Args:
            L, J, P, W: Current values
            tolerance: Allowed deviation from ideal ratios (default 0.3 = 30%)

        Returns:
            Dict with proportions analysis
        """
        # Calculate current ratios
        current_ratios = {
            "L/J": L / J if J > 0 else float("inf"),
            "P/J": P / J if J > 0 else float("inf"),
            "W/J": W / J if J > 0 else float("inf"),
            "L/P": L / P if P > 0 else float("inf"),
            "L/W": L / W if W > 0 else float("inf"),
            "W/P": W / P if P > 0 else float("inf"),
        }

        # Expected ratios from Natural Equilibrium
        expected_ratios = {
            "L/J": self.NE[0] / self.NE[1],  # 1.492
            "P/J": self.NE[2] / self.NE[1],  # 1.734
            "W/J": self.NE[3] / self.NE[1],  # 1.673
            "L/P": self.NE[0] / self.NE[2],  # 0.860
            "L/W": self.NE[0] / self.NE[3],  # 0.892
            "W/P": self.NE[3] / self.NE[2],  # 0.965
        }

        # Check deviations
        deviations = {}
        checks = {}

        for key in expected_ratios:
            expected = expected_ratios[key]
            actual = current_ratios[key]

            if math.isfinite(actual):
                deviation = abs(actual - expected) / expected
                deviations[key] = deviation
                checks[key] = deviation < tolerance
            else:
                deviations[key] = float("inf")
                checks[key] = False

        all_pass = all(checks.values())

        return {
            "proportions_healthy": all_pass,
            "current_ratios": current_ratios,
            "expected_ratios": expected_ratios,
            "deviations": deviations,
            "checks": checks,
            "summary": (
                "Healthy proportions (scale-invariant)"
                if all_pass
                else "Proportions deviate from Natural Equilibrium"
            ),
        }

    def check_coupling_character(self, coupling_matrix: Dict[str, float]) -> Dict[str, any]:
        """
        Check if coupling matrix exhibits expected qualitative patterns.

        Args:
            coupling_matrix: Dict mapping 'XY' to coupling coefficient κ_XY

        Returns:
            Dict with pattern analysis
        """
        checks = {}

        # Check 1: Love amplifies
        love_amplifies = {}
        for key, (min_val, max_val) in RelationshipPatterns.LOVE_AMPLIFIES.items():
            if key in coupling_matrix:
                κ = coupling_matrix[key]
                love_amplifies[key] = {
                    "value": κ,
                    "expected_range": (min_val, max_val),
                    "healthy": min_val <= κ <= max_val,
                    "character": "amplifies" if κ > 1.0 else "diminishes",
                }

        checks["love_amplifies"] = {
            "pattern": "Love should amplify other dimensions (κ > 1)",
            "results": love_amplifies,
            "pass": all(v["healthy"] for v in love_amplifies.values()),
        }

        # Check 2: Power constrains
        power_constrains = {}
        for key, (min_val, max_val) in RelationshipPatterns.POWER_CONSTRAINS.items():
            if key in coupling_matrix:
                κ = coupling_matrix[key]
                power_constrains[key] = {
                    "value": κ,
                    "expected_range": (min_val, max_val),
                    "healthy": min_val <= κ <= max_val,
                    "character": "constrained" if κ < 1.0 else "amplifies",
                }

        checks["power_constrains"] = {
            "pattern": "Power should be constrained (κ < 1)",
            "results": power_constrains,
            "pass": all(v["healthy"] for v in power_constrains.values()),
        }

        # Check 3: Justice supports Wisdom more than Power
        justice_pattern = {}
        if "JW" in coupling_matrix and "JP" in coupling_matrix:
            κ_JW = coupling_matrix["JW"]
            κ_JP = coupling_matrix["JP"]
            justice_pattern = {
                "JW": κ_JW,
                "JP": κ_JP,
                "healthy": κ_JW > κ_JP,
                "interpretation": (
                    "Justice flows more to Wisdom than Power"
                    if κ_JW > κ_JP
                    else "Justice favors Power over Wisdom (unusual)"
                ),
            }

        checks["justice_supports_wisdom"] = {
            "pattern": "Justice should support Wisdom more than Power (κ_JW > κ_JP)",
            "results": justice_pattern,
            "pass": justice_pattern.get("healthy", False),
        }

        return checks

    def check_asymmetry(self, coupling_matrix: Dict[str, float]) -> Dict[str, any]:
        """
        Check if coupling matrix exhibits proper asymmetry.

        Args:
            coupling_matrix: Dict mapping 'XY' to coupling coefficient κ_XY

        Returns:
            Dict with asymmetry analysis
        """
        asymmetries = []

        for forward, reverse, description in RelationshipPatterns.ASYMMETRY_PATTERNS:
            if forward in coupling_matrix and reverse in coupling_matrix:
                κ_forward = coupling_matrix[forward]
                κ_reverse = coupling_matrix[reverse]

                asymmetries.append(
                    {
                        "forward": forward,
                        "reverse": reverse,
                        "κ_forward": κ_forward,
                        "κ_reverse": κ_reverse,
                        "asymmetry_ratio": κ_forward / κ_reverse if κ_reverse > 0 else float("inf"),
                        "is_asymmetric": abs(κ_forward - κ_reverse) > 0.1,
                        "description": description,
                    }
                )

        # Asymmetry is healthy - symmetric coupling would be unusual
        healthy_asymmetry = (
            sum(1 for a in asymmetries if a["is_asymmetric"]) >= len(asymmetries) * 0.75
        )

        return {
            "asymmetry_healthy": healthy_asymmetry,
            "patterns": asymmetries,
            "summary": (
                "Healthy asymmetric coupling"
                if healthy_asymmetry
                else "Warning: Coupling too symmetric"
            ),
        }

    def full_relationship_diagnostic(
        self, L: float, J: float, P: float, W: float, coupling_matrix: Dict[str, float] = None
    ) -> Dict[str, any]:
        """
        Complete relationship structure analysis.

        Args:
            L, J, P, W: Current dimension values
            coupling_matrix: Optional coupling matrix (uses default if None)

        Returns:
            Comprehensive diagnostic report
        """
        # Use default coupling if not provided
        if coupling_matrix is None:
            from harmonizer.ljpw_baselines import LJPWBaselines

            coupling_matrix = LJPWBaselines.COUPLING_MATRIX

        # Run all checks
        proportions = self.check_proportions(L, J, P, W)
        coupling_character = self.check_coupling_character(coupling_matrix)
        asymmetry = self.check_asymmetry(coupling_matrix)

        # Overall health assessment
        health_scores = {
            "proportions": 1.0 if proportions["proportions_healthy"] else 0.0,
            "love_amplifies": 1.0 if coupling_character["love_amplifies"]["pass"] else 0.0,
            "power_constrains": 1.0 if coupling_character["power_constrains"]["pass"] else 0.0,
            "justice_supports_wisdom": (
                1.0 if coupling_character["justice_supports_wisdom"]["pass"] else 0.0
            ),
            "asymmetry": 1.0 if asymmetry["asymmetry_healthy"] else 0.0,
        }

        overall_health = sum(health_scores.values()) / len(health_scores)

        return {
            "overall_health": overall_health,
            "health_scores": health_scores,
            "proportions_analysis": proportions,
            "coupling_character_analysis": coupling_character,
            "asymmetry_analysis": asymmetry,
            "interpretation": self._interpret_health(overall_health),
            "recommendations": self._generate_recommendations(
                proportions, coupling_character, asymmetry
            ),
        }

    def _interpret_health(self, health: float) -> str:
        """Interpret overall relationship health score"""
        if health >= 0.9:
            return "Excellent: System exhibits all expected LJPW relationship patterns"
        elif health >= 0.7:
            return "Good: Most relationship patterns are healthy, minor deviations"
        elif health >= 0.5:
            return "Moderate: Some relationship patterns need attention"
        else:
            return "Critical: Major deviations from expected LJPW coupling structure"

    def _generate_recommendations(
        self, proportions: Dict, coupling: Dict, asymmetry: Dict
    ) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []

        # Proportion recommendations
        if not proportions["proportions_healthy"]:
            worst_ratio = max(proportions["deviations"].items(), key=lambda x: x[1])
            recommendations.append(
                f"⚠️ Adjust proportions: {worst_ratio[0]} deviates by {worst_ratio[1]:.1%} from Natural Equilibrium"
            )

        # Coupling character recommendations
        if not coupling["love_amplifies"]["pass"]:
            recommendations.append(
                "⚠️ Love is not amplifying properly - increase Love's influence on other dimensions"
            )

        if not coupling["power_constrains"]["pass"]:
            recommendations.append(
                "⚠️ Power is not constrained - reduce Power's direct influence, channel through Love/Wisdom"
            )

        if not coupling["justice_supports_wisdom"]["pass"]:
            recommendations.append(
                "⚠️ Justice should support Wisdom more than Power - strengthen J→W coupling"
            )

        # Asymmetry recommendations
        if not asymmetry["asymmetry_healthy"]:
            recommendations.append(
                "⚠️ Coupling is too symmetric - verify that giving ≠ receiving for each dimension pair"
            )

        if not recommendations:
            recommendations.append(
                "✓ All relationship patterns are healthy - maintain current structure"
            )

        return recommendations


# Convenience function
def analyze_system_relationships(
    L: float, J: float, P: float, W: float, coupling_matrix: Dict[str, float] = None
) -> Dict:
    """
    Analyze if a system has healthy LJPW relationship patterns.

    Args:
        L, J, P, W: Dimension values
        coupling_matrix: Optional custom coupling matrix

    Returns:
        Comprehensive diagnostic report
    """
    analyzer = RelationshipAnalyzer()
    return analyzer.full_relationship_diagnostic(L, J, P, W, coupling_matrix)


if __name__ == "__main__":
    # Example: Analyze Natural Equilibrium
    print("=" * 80)
    print("LJPW Relationship Structure Analyzer")
    print("=" * 80)
    print()

    # Test with Natural Equilibrium (should be perfect)
    NE = ReferencePoints.NATURAL_EQUILIBRIUM

    print("Testing Natural Equilibrium:")
    print(f"  L={NE[0]:.3f}, J={NE[1]:.3f}, P={NE[2]:.3f}, W={NE[3]:.3f}")
    print()

    result = analyze_system_relationships(NE[0], NE[1], NE[2], NE[3])

    print(f"Overall Health: {result['overall_health']:.2%}")
    print(f"Interpretation: {result['interpretation']}")
    print()

    print("Health Breakdown:")
    for aspect, score in result["health_scores"].items():
        status = "✓" if score >= 0.9 else "⚠️" if score >= 0.7 else "✗"
        print(f"  {status} {aspect}: {score:.0%}")
    print()

    print("Recommendations:")
    for rec in result["recommendations"]:
        print(f"  {rec}")
    print()

    # Test with imbalanced system
    print("=" * 80)
    print("Testing Imbalanced System (High Power, Low Love):")
    print("  L=0.2, J=0.3, P=0.9, W=0.4")
    print()

    result2 = analyze_system_relationships(0.2, 0.3, 0.9, 0.4)

    print(f"Overall Health: {result2['overall_health']:.2%}")
    print(f"Interpretation: {result2['interpretation']}")
    print()

    print("Health Breakdown:")
    for aspect, score in result2["health_scores"].items():
        status = "✓" if score >= 0.9 else "⚠️" if score >= 0.7 else "✗"
        print(f"  {status} {aspect}: {score:.0%}")
    print()

    print("Recommendations:")
    for rec in result2["recommendations"]:
        print(f"  {rec}")
