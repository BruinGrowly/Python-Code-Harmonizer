#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LJPW Mathematical Baselines
Version 1.0

Provides objective, non-arbitrary baselines for LJPW framework implementations.

Based on: docs/LJPW_MATHEMATICAL_BASELINES.md
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class NumericalEquivalents:
    """Fundamental constants for LJPW dimensions"""

    L: float = (math.sqrt(5) - 1) / 2  # φ⁻¹ ≈ 0.618034
    J: float = math.sqrt(2) - 1  # √2 - 1 ≈ 0.414214
    P: float = math.e - 2  # e - 2 ≈ 0.718282
    W: float = math.log(2)  # ln(2) ≈ 0.693147


@dataclass
class ReferencePoints:
    """Key reference points in LJPW space"""

    ANCHOR_POINT: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    NATURAL_EQUILIBRIUM: Tuple[float, float, float, float] = (
        0.618034,  # L
        0.414214,  # J
        0.718282,  # P
        0.693147,  # W
    )


class LJPWBaselines:
    """LJPW mathematical baselines and calculations"""

    # Coupling matrix - Love amplifies other dimensions
    COUPLING_MATRIX = {
        "LL": 1.0,
        "LJ": 1.4,
        "LP": 1.3,
        "LW": 1.5,
        "JL": 0.9,
        "JJ": 1.0,
        "JP": 0.7,
        "JW": 1.2,
        "PL": 0.6,
        "PJ": 0.8,
        "PP": 1.0,
        "PW": 0.5,
        "WL": 1.3,
        "WJ": 1.1,
        "WP": 1.0,
        "WW": 1.0,
    }

    @staticmethod
    def effective_dimensions(L: float, J: float, P: float, W: float) -> Dict[str, float]:
        """
        Calculate coupling-adjusted effective dimensions.

        Love amplifies other dimensions:
        - Justice: +40% per unit of Love
        - Power: +30% per unit of Love
        - Wisdom: +50% per unit of Love (strongest coupling)

        Args:
            L, J, P, W: Raw dimension values (0.0 to 1.0)

        Returns:
            Dict with effective_L, effective_J, effective_P, effective_W
        """
        return {
            "effective_L": L,  # Love is the source, not amplified
            "effective_J": J * (1 + 1.4 * L),  # Justice amplified by Love
            "effective_P": P * (1 + 1.3 * L),  # Power amplified by Love
            "effective_W": W * (1 + 1.5 * L),  # Wisdom amplified by Love (strongest)
        }

    @staticmethod
    def harmonic_mean(L: float, J: float, P: float, W: float) -> float:
        """
        Harmonic mean - robustness (weakest link).

        Use for: Fault tolerance, minimum guarantees, resilience.
        The system is only as strong as its weakest dimension.

        Returns:
            Harmonic mean (0.0 to 1.0)
        """
        if L <= 0 or J <= 0 or P <= 0 or W <= 0:
            return 0.0
        return 4.0 / (1 / L + 1 / J + 1 / P + 1 / W)

    @staticmethod
    def geometric_mean(L: float, J: float, P: float, W: float) -> float:
        """
        Geometric mean - effectiveness (multiplicative).

        Use for: Overall effectiveness, balanced performance.
        All dimensions contribute multiplicatively.

        Returns:
            Geometric mean (0.0 to 1.0)
        """
        return (L * J * P * W) ** 0.25

    @staticmethod
    def coupling_aware_sum(L: float, J: float, P: float, W: float) -> float:
        """
        Coupling-aware weighted sum - growth potential.

        Uses effective dimensions that account for Love's amplification.
        Can exceed 1.0 due to coupling effects.

        Use for: Growth potential, scalability, future performance.

        Returns:
            Weighted sum (can exceed 1.0)
        """
        J_eff = J * (1 + 1.4 * L)
        P_eff = P * (1 + 1.3 * L)
        W_eff = W * (1 + 1.5 * L)
        return 0.35 * L + 0.25 * J_eff + 0.20 * P_eff + 0.20 * W_eff

    @staticmethod
    def harmony_index(L: float, J: float, P: float, W: float) -> float:
        """
        Harmony index - balance (inverse distance from Anchor).

        Use for: Balance, alignment, proximity to ideal.
        Measures how close to perfect harmony (1,1,1,1).

        Returns:
            Harmony index (0.0 to 1.0, asymptotic to 1.0)
        """
        d_anchor = math.sqrt((1 - L) ** 2 + (1 - J) ** 2 + (1 - P) ** 2 + (1 - W) ** 2)
        return 1.0 / (1.0 + d_anchor)

    @staticmethod
    def composite_score(L: float, J: float, P: float, W: float) -> float:
        """
        Composite score - overall performance.

        Weighted combination:
        - 35% Growth Potential (coupling-aware sum)
        - 25% Effectiveness (geometric mean)
        - 25% Robustness (harmonic mean)
        - 15% Harmony (balance)

        Returns:
            Composite score (typically 0.5 to 1.3)
        """
        baselines = LJPWBaselines
        growth = baselines.coupling_aware_sum(L, J, P, W)
        effectiveness = baselines.geometric_mean(L, J, P, W)
        robustness = baselines.harmonic_mean(L, J, P, W)
        harmony = baselines.harmony_index(L, J, P, W)

        return 0.35 * growth + 0.25 * effectiveness + 0.25 * robustness + 0.15 * harmony

    @staticmethod
    def distance_from_anchor(L: float, J: float, P: float, W: float) -> float:
        """
        Euclidean distance from Anchor Point (1,1,1,1).

        The Anchor Point represents perfect, transcendent ideal.
        Lower distance = closer to perfection.

        Returns:
            Distance (0.0 to ~2.0)
        """
        return math.sqrt((1 - L) ** 2 + (1 - J) ** 2 + (1 - P) ** 2 + (1 - W) ** 2)

    @staticmethod
    def distance_from_natural_equilibrium(L: float, J: float, P: float, W: float) -> float:
        """
        Euclidean distance from Natural Equilibrium.

        Natural Equilibrium (0.618, 0.414, 0.718, 0.693) represents
        physically achievable optimal balance.

        Returns:
            Distance (0.0 to ~2.0)
        """
        NE = ReferencePoints.NATURAL_EQUILIBRIUM
        return math.sqrt(
            (NE[0] - L) ** 2 + (NE[1] - J) ** 2 + (NE[2] - P) ** 2 + (NE[3] - W) ** 2
        )

    @staticmethod
    def full_diagnostic(L: float, J: float, P: float, W: float) -> Dict:
        """
        Complete diagnostic analysis.

        Provides comprehensive view of system health across multiple metrics.

        Args:
            L, J, P, W: Dimension values

        Returns:
            Dict with coordinates, effective dimensions, distances, and all metrics
        """
        baselines = LJPWBaselines
        eff = baselines.effective_dimensions(L, J, P, W)

        return {
            "coordinates": {"L": L, "J": J, "P": P, "W": W},
            "effective_dimensions": eff,
            "distances": {
                "from_anchor": baselines.distance_from_anchor(L, J, P, W),
                "from_natural_equilibrium": baselines.distance_from_natural_equilibrium(
                    L, J, P, W
                ),
            },
            "metrics": {
                "harmonic_mean": baselines.harmonic_mean(L, J, P, W),
                "geometric_mean": baselines.geometric_mean(L, J, P, W),
                "coupling_aware_sum": baselines.coupling_aware_sum(L, J, P, W),
                "harmony_index": baselines.harmony_index(L, J, P, W),
                "composite_score": baselines.composite_score(L, J, P, W),
            },
        }

    @staticmethod
    def interpret_distance_from_ne(distance: float) -> str:
        """
        Interpret distance from Natural Equilibrium.

        Args:
            distance: Distance value

        Returns:
            Human-readable interpretation
        """
        if distance < 0.2:
            return "Near-optimal balance"
        elif distance < 0.5:
            return "Good but improvable"
        elif distance < 0.8:
            return "Moderate imbalance"
        else:
            return "Significant dysfunction"

    @staticmethod
    def interpret_composite_score(score: float) -> str:
        """
        Interpret composite score.

        Args:
            score: Composite score value

        Returns:
            Human-readable interpretation
        """
        if score < 0.5:
            return "Critical - multiple dimensions failing"
        elif score < 0.7:
            return "Struggling - functional but inefficient"
        elif score < 0.9:
            return "Competent - solid baseline performance"
        elif score < 1.1:
            return "Strong - above-average effectiveness"
        elif score < 1.3:
            return "Excellent - high-performing, growth active"
        else:
            return "Elite - exceptional, Love multiplier engaged"


# Convenience functions for quick access
def get_numerical_equivalents() -> NumericalEquivalents:
    """Get the fundamental LJPW constants"""
    return NumericalEquivalents()


def get_reference_points() -> ReferencePoints:
    """Get Anchor Point and Natural Equilibrium"""
    return ReferencePoints()


# Example usage and testing
if __name__ == "__main__":
    # Example: Analyze a code function's semantic profile
    print("=" * 70)
    print("LJPW Baselines - Example Analysis")
    print("=" * 70)
    print()

    # Example function: validate_and_save_user
    # Low Love (naming clarity), High Justice (validation), Medium Power, High Wisdom
    L, J, P, W = 0.3, 0.8, 0.6, 0.7

    print(f"Function Coordinates: L={L}, J={J}, P={P}, W={W}")
    print()

    baselines = LJPWBaselines()
    diagnostic = baselines.full_diagnostic(L, J, P, W)

    print("Effective Dimensions (coupling-adjusted):")
    for dim, val in diagnostic["effective_dimensions"].items():
        print(f"  {dim}: {val:.3f}")
    print()

    print("Distances:")
    d_anchor = diagnostic["distances"]["from_anchor"]
    d_ne = diagnostic["distances"]["from_natural_equilibrium"]
    print(f"  From Anchor Point: {d_anchor:.3f}")
    print(f"  From Natural Equilibrium: {d_ne:.3f}")
    print(f"    → {baselines.interpret_distance_from_ne(d_ne)}")
    print()

    print("Metrics:")
    for metric, val in diagnostic["metrics"].items():
        print(f"  {metric}: {val:.3f}")

    composite = diagnostic["metrics"]["composite_score"]
    print()
    print(f"Overall Assessment: {baselines.interpret_composite_score(composite)}")
    print()

    print("Recommendations:")
    print(f"  • Primary issue: Low Love (L={L:.2f})")
    print(f"  • Impact: Limiting growth potential (coupling not engaged)")
    print(f"  • Action: Improve naming clarity, documentation, usability")
    print()

    # Show Love's amplification effect
    print("Love Amplification Effect:")
    print(f"  Current (L={L:.1f}):")
    print(
        f"    J_eff = {diagnostic['effective_dimensions']['effective_J']:.2f} "
        f"({(diagnostic['effective_dimensions']['effective_J']/J - 1)*100:.0f}% boost)"
    )

    # Simulate high Love
    L_high = 0.8
    diag_high = baselines.full_diagnostic(L_high, J, P, W)
    print(f"  With High Love (L={L_high:.1f}):")
    print(
        f"    J_eff = {diag_high['effective_dimensions']['effective_J']:.2f} "
        f"({(diag_high['effective_dimensions']['effective_J']/J - 1)*100:.0f}% boost)"
    )
    print(
        f"    Composite: {diag_high['metrics']['composite_score']:.2f} "
        f"(+{(diag_high['metrics']['composite_score']/composite - 1)*100:.0f}% improvement)"
    )
