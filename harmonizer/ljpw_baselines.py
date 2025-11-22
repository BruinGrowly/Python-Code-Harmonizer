#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LJPW Mathematical Baselines
Version 4.0

Provides objective, non-arbitrary baselines for LJPW framework implementations.
Includes both static analysis and a validated, non-linear dynamic simulator.

Based on: docs/LJPW Mathematical Baselines Reference V4.md
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np


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
    """LJPW mathematical baselines and calculations (Static Analysis)"""

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
        return math.sqrt((NE[0] - L) ** 2 + (NE[1] - J) ** 2 + (NE[2] - P) ** 2 + (NE[3] - W) ** 2)

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
                "from_natural_equilibrium": baselines.distance_from_natural_equilibrium(L, J, P, W),
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

    @staticmethod
    def validate_coupling_structure() -> Dict[str, bool]:
        """
        Validate that the coupling matrix exhibits expected relationship patterns.

        This validates the "grammar of semantic interaction":
        - Love amplifies (κ_L→* > 1)
        - Power constrains (κ_P→* < 1)
        - Justice supports Wisdom (κ_JW > κ_JP)
        - Asymmetry is present (κ_ij ≠ κ_ji)

        Returns:
            Dict with validation results for each pattern
        """
        cm = LJPWBaselines.COUPLING_MATRIX

        # Check Love amplifies
        love_amplifies = cm["LJ"] > 1.0 and cm["LP"] > 1.0 and cm["LW"] > 1.0

        # Check Power constrains
        power_constrains = cm["PL"] < 1.0 and cm["PJ"] < 1.0 and cm["PW"] < 1.0

        # Check Justice supports Wisdom more than Power
        justice_wisdom = cm["JW"] > cm["JP"]

        # Check asymmetry (giving ≠ receiving)
        asymmetry = (
            abs(cm["LJ"] - cm["JL"]) > 0.1
            and abs(cm["LP"] - cm["PL"]) > 0.1
            and abs(cm["PJ"] - cm["JP"]) > 0.1
        )

        return {
            "love_amplifies": love_amplifies,
            "power_constrains": power_constrains,
            "justice_supports_wisdom": justice_wisdom,
            "asymmetry_present": asymmetry,
            "all_patterns_valid": all(
                [love_amplifies, power_constrains, justice_wisdom, asymmetry]
            ),
        }

    @staticmethod
    def check_proportions(
        L: float, J: float, P: float, W: float, tolerance: float = 0.3
    ) -> Dict[str, any]:
        """
        Check if L:J:P:W proportions match Natural Equilibrium (scale-invariant check).

        This validates the core insight: "relationships between constants matter more
        than the constants themselves." The same proportions define harmony at any scale.

        Args:
            L, J, P, W: Current dimension values (any scale)
            tolerance: Allowed deviation from ideal ratios (default 0.3 = 30%)

        Returns:
            Dict with proportion analysis
        """
        NE = ReferencePoints.NATURAL_EQUILIBRIUM

        # Calculate current ratios (scale-invariant)
        if J <= 0:
            return {"proportions_healthy": False, "error": "Justice dimension cannot be zero"}

        current_ratios = {
            "L/J": L / J,
            "P/J": P / J,
            "W/J": W / J,
        }

        # Expected ratios from Natural Equilibrium
        expected_ratios = {
            "L/J": NE[0] / NE[1],  # 1.492
            "P/J": NE[2] / NE[1],  # 1.734
            "W/J": NE[3] / NE[1],  # 1.673
        }

        # Check deviations
        deviations = {}
        checks = {}

        for key in expected_ratios:
            expected = expected_ratios[key]
            actual = current_ratios[key]
            deviation = abs(actual - expected) / expected
            deviations[key] = deviation
            checks[key] = deviation < tolerance

        all_pass = all(checks.values())

        return {
            "proportions_healthy": all_pass,
            "current_ratios": current_ratios,
            "expected_ratios": expected_ratios,
            "deviations": deviations,
            "checks": checks,
            "summary": (
                "Proportions match Natural Equilibrium (scale-invariant)"
                if all_pass
                else f"Proportions deviate from Natural Equilibrium"
            ),
        }


class DynamicLJPWv4:
    """
    LJPW v4.0: Empirically-validated, non-linear dynamic simulator.
    """

    def __init__(self, complexity_score: float = 1.0):
        """
        Initialize the LJPW v4.0 Dynamic Model.

        Args:
            complexity_score: Multiplier for system energy/potential (default 1.0).
                            1.0 = Standard script (Settles at NE)
                            >1.5 = Complex system (Can reach High-Energy)
        """
        self.complexity = max(0.5, complexity_score)
        self.params = self._initialize_parameters()
        self.NE = ReferencePoints.NATURAL_EQUILIBRIUM

    def _initialize_parameters(self) -> Dict[str, float]:
        """
        Initialize system parameters based on LJPW v4.0 specification,
        dynamically calibrated by complexity score.
        """
        # Base parameters (Tuned for NE convergence at complexity=1.0)
        # Logic: Increased coupling to 0.12 to ensure saturation near 0.6-0.7.

        base_params = {
            # Growth rates (Alpha) - Not used directly in standard equations but kept for completeness
            "alpha_L": 0.0,
            "alpha_J": 0.0,
            "alpha_P": 0.0,
            "alpha_W": 0.0,
            # Coupling coefficients (Alpha_XY) - Target 0.12 for balance
            "alpha_LJ": 0.12,
            "alpha_LP": 0.0,
            "alpha_LW": 0.12,  # L inputs: J, W
            "alpha_JL": 0.14,
            "alpha_JP": 0.0,
            "alpha_JW": 0.14,  # J inputs: L, W (boosted slightly)
            "alpha_PL": 0.12,
            "alpha_PJ": 0.12,
            "alpha_PW": 0.0,  # P inputs: L, J
            "alpha_WL": 0.10,
            "alpha_WJ": 0.10,
            "alpha_WP": 0.10,  # W inputs: L, J, P
            # Decay rates (Beta) - Target 0.20
            "beta_L": 0.20,
            "beta_J": 0.20,
            "beta_P": 0.20,
            "beta_W": 0.24,  # Higher decay for W because it has 3 inputs
            # Non-Linear Parameters (v4.0)
            "K_JL": 0.59,  # Saturation constant for L -> J
            "gamma_JP": 0.49,  # Erosion rate for P -> J
            "K_JP": 0.71,  # Threshold constant for P -> J
            "n_JP": 4.1,  # Steepness for P -> J erosion
        }

        return self._calibrate_parameters(base_params)

    def _calibrate_parameters(self, params: Dict[str, float]) -> Dict[str, float]:
        """
        Scale parameters based on system complexity.
        Higher complexity = Higher growth potential (Alpha) but harder to maintain (Higher Beta).
        """
        # Complexity factor for growth (Logarithmic scaling to prevent explosion)
        # 1.0 -> 1.0, 10.0 -> ~2.0
        growth_multiplier = 1.0 + 0.5 * math.log(self.complexity)

        # Complexity factor for decay (Linear scaling - entropy scales with size)
        decay_multiplier = 1.0 + 0.1 * (self.complexity - 1.0)

        calibrated = params.copy()

        # Scale Alphas (Growth)
        for key in calibrated:
            if key.startswith("alpha"):
                calibrated[key] *= growth_multiplier

        # Scale Betas (Decay)
        for key in calibrated:
            if key.startswith("beta"):
                calibrated[key] *= decay_multiplier

        return calibrated

    def _derivatives(self, state):
        """Calculates the derivatives with non-linear dynamics."""
        L, J, P, W = state
        p = self.params

        # Love equation (remains linear)
        dL_dt = p["alpha_LJ"] * J + p["alpha_LW"] * W - p["beta_L"] * L

        # Justice equation (with saturation and threshold effects)
        L_effect_on_J = p["alpha_JL"] * (L / (p["K_JL"] + L))  # Saturation
        P_effect_on_J = (
            p["gamma_JP"]
            * (P ** p["n_JP"] / (p["K_JP"] ** p["n_JP"] + P ** p["n_JP"]))
            * max(0, 1 - W)
        )  # Threshold
        dJ_dt = L_effect_on_J + p["alpha_JW"] * W - P_effect_on_J - p["beta_J"] * J

        # Power and Wisdom equations (can be similarly enhanced in future versions)
        dP_dt = p["alpha_PL"] * L + p["alpha_PJ"] * J - p["beta_P"] * P
        dW_dt = p["alpha_WL"] * L + p["alpha_WJ"] * J + p["alpha_WP"] * P - p["beta_W"] * W

        return np.array([dL_dt, dJ_dt, dP_dt, dW_dt])

    def _rk4_step(self, state, dt):
        """Performs a single 4th-order Runge-Kutta integration step."""
        k1 = self._derivatives(state)
        k2 = self._derivatives(state + 0.5 * dt * k1)
        k3 = self._derivatives(state + 0.5 * dt * k2)
        k4 = self._derivatives(state + dt * k3)
        return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    def simulate(
        self,
        initial_state: Tuple[float, float, float, float],
        duration: float,
        dt: float = 0.01,
    ) -> Dict:
        """Runs the simulation using the more accurate RK4 method."""
        steps = int(duration / dt)
        state = np.array(initial_state, dtype=float)

        history = {
            "t": [0],
            "L": [state[0]],
            "J": [state[1]],
            "P": [state[2]],
            "W": [state[3]],
        }

        for i in range(steps):
            state = self._rk4_step(state, dt)
            state = np.clip(state, 0, 1.5)

            history["t"].append((i + 1) * dt)
            history["L"].append(state[0])
            history["J"].append(state[1])
            history["P"].append(state[2])
            history["W"].append(state[3])

        return history

    def plot_simulation(self, history: Dict):
        """Plots the results of a simulation."""
        plt.style.use("seaborn-v0_8-whitegrid")
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.plot(history["t"], history["L"], label="Love (L)", color="crimson", lw=2)
        ax.plot(history["t"], history["J"], label="Justice (J)", color="royalblue", lw=2)
        ax.plot(history["t"], history["P"], label="Power (P)", color="darkgreen", lw=2)
        ax.plot(history["t"], history["W"], label="Wisdom (W)", color="purple", lw=2)
        for i, val in enumerate(self.NE):
            ax.axhline(
                y=val,
                color=["crimson", "royalblue", "darkgreen", "purple"][i],
                linestyle="--",
                alpha=0.3,
            )
        ax.set_title("LJPW v4.0 System Evolution (Non-Linear, RK4)")
        ax.set_xlabel("Time")
        ax.set_ylabel("Dimension Value")
        ax.set_ylim(0, 1.2)
        ax.legend()
        plt.show()


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
    print("  • Impact: Limiting growth potential (coupling not engaged)")
    print("  • Action: Improve naming clarity, documentation, usability")
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

    # --- Dynamic Simulation Example ---
    print("\nLJPW v4.0 Dynamic Simulation: 'Reckless Power' Scenario")
    print("=" * 60)
    simulator = DynamicLJPWv4()
    initial_state = (0.2, 0.3, 0.9, 0.2)  # High P, low L, J, W
    history = simulator.simulate(initial_state, duration=50, dt=0.05)

    # Print final state
    final_state = (
        history["L"][-1],
        history["J"][-1],
        history["P"][-1],
        history["W"][-1],
    )
    print(
        f"Initial State: L={initial_state[0]:.2f}, J={initial_state[1]:.2f}, P={initial_state[2]:.2f}, W={initial_state[3]:.2f}"
    )
    print(
        f"Final State:   L={final_state[0]:.2f}, J={final_state[1]:.2f}, P={final_state[2]:.2f}, W={final_state[3]:.2f}"
    )
