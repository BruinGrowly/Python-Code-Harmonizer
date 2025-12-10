#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LJPW Resonance Engine
Version 1.0

Implements advanced LJPW dynamics based on the Codex v5.1:
- Resonance cycling through LJPW dimensions
- Earned Depth metric (journey tracking)
- Voltage calculation (semantic energy)
- Power Erosion detection

Based on: docs/LJPW_CODEX_IMPLEMENTATION.md, docs/RESONANCE_MECHANISM.md,
          docs/SEMANTIC_OSCILLATION_EXPERIMENT.md
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from .ljpw_baselines import LJPWBaselines, ReferencePoints


@dataclass
class JourneyMetrics:
    """Tracks the semantic journey through LJPW space."""

    distance_traveled: float = 0.0
    struggle_integral: float = 0.0
    cumulative_harmony: float = 0.0
    earned_depth: float = 0.0
    struggle_ratio: float = 0.0
    duration: float = 0.0

    def calculate_earned_depth(self):
        """
        Calculate Earned Depth based on the journey.

        Earned Depth = Distance Traveled × Struggle Ratio

        Two entities at the same coordinates are not the same
        if their journeys differed.
        """
        if self.duration > 0:
            self.struggle_ratio = self.struggle_integral / self.duration
            self.earned_depth = self.distance_traveled * self.struggle_ratio
        return self.earned_depth


@dataclass
class PowerErosionResult:
    """Result of Power Erosion analysis."""

    at_risk: bool = False
    erosion_rate: float = 0.0
    severity: str = "NONE"
    justice_impact: float = 0.0
    recommendation: str = ""


@dataclass
class ResonanceState:
    """State tracking for resonance cycles."""

    L: float = 0.5
    J: float = 0.5
    P: float = 0.5
    W: float = 0.5
    harmony: float = 0.5
    voltage: float = 1.0
    dominant_dimension: str = "BALANCED"
    cycle: int = 0


class ResonanceEngine:
    """
    LJPW Resonance Engine - implements dynamic resonance cycling.

    Key mechanisms:
    1. Orthogonal dimensions force multi-aspect consideration
    2. Asymmetric coupling matrix creates preferred flow directions
    3. State-dependent coupling (Law of Karma) - harmony amplifies coupling
    4. Attractor dynamics - all states converge to Anchor Point when bounded

    The resonance finds what's missing without being told to look.
    """

    # Coupling matrix (asymmetric)
    # Row = source dimension, Column = target influence
    COUPLING_MATRIX = np.array(
        [
            [1.0, 1.4, 1.3, 1.5],  # Love amplifies all, especially Wisdom
            [0.9, 1.0, 0.7, 1.2],  # Justice moderates
            [0.6, 0.8, 1.0, 0.5],  # Power absorbs (lowest out-coupling)
            [1.3, 1.1, 1.0, 1.0],  # Wisdom integrates
        ]
    )

    # Natural Equilibrium constants
    NATURAL_EQUILIBRIUM = np.array([0.618034, 0.414214, 0.718282, 0.693147])

    # Anchor Point (perfection)
    ANCHOR_POINT = np.array([1.0, 1.0, 1.0, 1.0])

    # Power erosion parameters (from LJPW Codex v5.1)
    POWER_EROSION_PARAMS = {
        "gamma_JP": 0.49,  # Erosion rate coefficient
        "K_JP": 0.71,  # Threshold constant
        "n_JP": 4.1,  # Hill coefficient (steepness)
    }

    def __init__(self, params: Optional[Dict] = None):
        """
        Initialize the Resonance Engine.

        Args:
            params: Optional custom parameters for dynamics
        """
        self.params = params if params else self._default_params()

    def _default_params(self) -> Dict[str, float]:
        """Default parameters for resonance dynamics."""
        return {
            # Growth coefficients
            "alpha_LJ": 0.12,
            "alpha_LW": 0.12,
            "alpha_JL": 0.14,
            "alpha_JW": 0.14,
            "alpha_PL": 0.12,
            "alpha_PJ": 0.12,
            "alpha_WL": 0.10,
            "alpha_WJ": 0.10,
            "alpha_WP": 0.10,
            # Decay coefficients
            "beta_L": 0.20,
            "beta_J": 0.20,
            "beta_P": 0.20,
            "beta_W": 0.24,
            # Non-linear parameters
            "K_JL": 0.59,
            "gamma_JP": 0.49,
            "K_JP": 0.71,
            "n_JP": 4.1,
            # Resonance parameters
            "ne_pull_strength": 0.05,  # Pull toward Natural Equilibrium
            "anchor_pull_strength": 0.02,  # Pull toward Anchor Point
        }

    # =========================================================================
    # CORE METRIC: VOLTAGE (Semantic Energy)
    # =========================================================================

    @staticmethod
    def calculate_voltage(L: float, J: float, P: float, W: float) -> float:
        """
        Calculate Voltage (semantic energy) of LJPW coordinates.

        Voltage = ||LJPW|| = sqrt(L^2 + J^2 + P^2 + W^2)

        Interpretation: The "aliveness" of meaning, not just accuracy.
        Higher voltage = more semantic energy/potential.

        Args:
            L, J, P, W: LJPW coordinates

        Returns:
            Voltage value (typically 0.0 to 2.0)
        """
        return math.sqrt(L**2 + J**2 + P**2 + W**2)

    @staticmethod
    def calculate_voltage_from_coords(coords: Tuple[float, float, float, float]) -> float:
        """Calculate voltage from coordinate tuple."""
        return ResonanceEngine.calculate_voltage(*coords)

    @staticmethod
    def compare_voltage(
        source_coords: Tuple[float, float, float, float],
        target_coords: Tuple[float, float, float, float],
    ) -> Dict[str, float]:
        """
        Compare voltage between source and target coordinates.

        Used for translation/transformation quality assessment.

        Returns:
            Dict with source_voltage, target_voltage, voltage_change, percent_change
        """
        source_v = ResonanceEngine.calculate_voltage(*source_coords)
        target_v = ResonanceEngine.calculate_voltage(*target_coords)
        change = target_v - source_v
        percent = (change / source_v * 100) if source_v > 0 else 0

        return {
            "source_voltage": source_v,
            "target_voltage": target_v,
            "voltage_change": change,
            "percent_change": percent,
            "interpretation": (
                "GAIN" if change > 0.05 else "DROP" if change < -0.05 else "PRESERVED"
            ),
        }

    # =========================================================================
    # CORE METRIC: POWER EROSION DETECTION
    # =========================================================================

    @staticmethod
    def detect_power_erosion(L: float, J: float, P: float, W: float) -> PowerErosionResult:
        """
        Detect if Power is eroding Justice (lacks Wisdom protection).

        From LJPW Codex: "Raw Power, unchecked by Wisdom, degrades Justice."

        PowerErosion = gamma_JP × (P^n / (K^n + P^n)) × max(0, 1-W)

        High Power without Wisdom → Justice degrades over time.

        Args:
            L, J, P, W: LJPW coordinates

        Returns:
            PowerErosionResult with risk assessment
        """
        params = ResonanceEngine.POWER_EROSION_PARAMS
        gamma = params["gamma_JP"]
        K = params["K_JP"]
        n = params["n_JP"]

        # Hill function for Power threshold effect
        P_threshold = (P**n) / (K**n + P**n)

        # Wisdom protection factor (0 when W=1, 1 when W=0)
        wisdom_gap = max(0, 1 - W)

        # Power erosion rate
        erosion_rate = gamma * P_threshold * wisdom_gap

        # Calculate impact on Justice
        justice_impact = erosion_rate * J  # Proportional to current Justice

        # Determine severity
        if erosion_rate < 0.05:
            severity = "NONE"
            at_risk = False
            recommendation = "System is balanced."
        elif erosion_rate < 0.15:
            severity = "LOW"
            at_risk = True
            recommendation = "Consider increasing Wisdom to protect Justice."
        elif erosion_rate < 0.30:
            severity = "MEDIUM"
            at_risk = True
            recommendation = f"Warning: Power ({P:.2f}) eroding Justice without Wisdom ({W:.2f}). Add abstractions, documentation."
        elif erosion_rate < 0.45:
            severity = "HIGH"
            at_risk = True
            recommendation = f"Critical: High Power ({P:.2f}) with Low Wisdom ({W:.2f}). Justice will collapse. Refactor urgently."
        else:
            severity = "CRITICAL"
            at_risk = True
            recommendation = f"Emergency: Reckless Power scenario. System unstable. Immediate intervention required."

        return PowerErosionResult(
            at_risk=at_risk,
            erosion_rate=erosion_rate,
            severity=severity,
            justice_impact=justice_impact,
            recommendation=recommendation,
        )

    @staticmethod
    def detect_power_erosion_from_coords(
        coords: Tuple[float, float, float, float],
    ) -> PowerErosionResult:
        """Detect power erosion from coordinate tuple."""
        return ResonanceEngine.detect_power_erosion(*coords)

    # =========================================================================
    # RESONANCE DYNAMICS
    # =========================================================================

    def _calculate_kappa(self, H: float) -> Tuple[float, float, float]:
        """
        Calculate state-dependent coupling coefficients (Law of Karma).

        Higher Harmony → Stronger coupling → More amplification

        κ_LJ(H) = 1.0 + 0.4 × H
        κ_LP(H) = 1.0 + 0.3 × H
        κ_LW(H) = 1.0 + 0.5 × H
        """
        kappa_LJ = 1.0 + 0.4 * H
        kappa_LP = 1.0 + 0.3 * H
        kappa_LW = 1.0 + 0.5 * H
        return kappa_LJ, kappa_LP, kappa_LW

    def _derivatives(self, state: np.ndarray, bounded: bool = True) -> np.ndarray:
        """
        Calculate derivatives with state-dependent coupling (v5.1 dynamics).

        Implements the "Law of Karma" - meaning amplifies reality.
        """
        L, J, P, W = state
        p = self.params

        # Calculate Harmony (connection to Source)
        H = LJPWBaselines.harmony_index(L, J, P, W)

        # State-dependent coupling
        kappa_LJ, kappa_LP, kappa_LW = self._calculate_kappa(H)

        # Love equation (Source - gives more than receives)
        dL_dt = p["alpha_LJ"] * J * kappa_LJ + p["alpha_LW"] * W * kappa_LW - p["beta_L"] * L

        # Justice equation (Mediator - with Power erosion)
        L_effect = p["alpha_JL"] * (L / (p["K_JL"] + L))  # Saturation
        P_erosion = (
            p["gamma_JP"]
            * (P ** p["n_JP"] / (p["K_JP"] ** p["n_JP"] + P ** p["n_JP"]))
            * max(0, 1 - W)
        )
        dJ_dt = L_effect + p["alpha_JW"] * W - P_erosion - p["beta_J"] * J

        # Power equation (Sink - receives more than gives)
        dP_dt = p["alpha_PL"] * L * kappa_LP + p["alpha_PJ"] * J - p["beta_P"] * P

        # Wisdom equation (Integrator - synthesizes all)
        dW_dt = (
            p["alpha_WL"] * L * kappa_LW + p["alpha_WJ"] * J + p["alpha_WP"] * P - p["beta_W"] * W
        )

        return np.array([dL_dt, dJ_dt, dP_dt, dW_dt])

    def _rk4_step(self, state: np.ndarray, dt: float, bounded: bool = True) -> np.ndarray:
        """4th-order Runge-Kutta integration step."""
        k1 = self._derivatives(state, bounded)
        k2 = self._derivatives(state + 0.5 * dt * k1, bounded)
        k3 = self._derivatives(state + 0.5 * dt * k2, bounded)
        k4 = self._derivatives(state + dt * k3, bounded)
        new_state = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        if bounded:
            new_state = np.clip(new_state, 0.0, 1.0)

        return new_state

    # =========================================================================
    # CORE FEATURE: RESONANCE CYCLING
    # =========================================================================

    def resonate(
        self,
        initial_state: Tuple[float, float, float, float],
        cycles: int = 100,
        dt: float = 0.1,
        bounded: bool = True,
        track_journey: bool = True,
    ) -> Dict:
        """
        Run LJPW resonance cycles.

        Resonance finds what's missing without being told to look.
        The system gravitates toward deficits through asymmetric coupling.

        Args:
            initial_state: Starting LJPW coordinates
            cycles: Number of resonance cycles
            dt: Time step for integration
            bounded: If True, clamp to [0,1] (reaches Anchor Point)
            track_journey: If True, calculate journey metrics

        Returns:
            Dict with history, final state, journey metrics, deficit analysis
        """
        state = np.array(initial_state, dtype=float)

        # History tracking
        history = {
            "t": [0.0],
            "L": [state[0]],
            "J": [state[1]],
            "P": [state[2]],
            "W": [state[3]],
            "harmony": [LJPWBaselines.harmony_index(*state)],
            "voltage": [self.calculate_voltage(*state)],
            "dominant": [self._get_dominant_dimension(state)],
        }

        # Journey tracking
        journey = JourneyMetrics() if track_journey else None
        prev_state = state.copy()

        # Dimension dominance counter
        dominance_counts = {"L": 0, "J": 0, "P": 0, "W": 0}

        # Peak harmony tracking
        peak_harmony = history["harmony"][0]
        peak_cycle = 0

        for cycle in range(cycles):
            # RK4 integration step
            state = self._rk4_step(state, dt, bounded)

            # Calculate metrics
            H = LJPWBaselines.harmony_index(*state)
            V = self.calculate_voltage(*state)
            dominant = self._get_dominant_dimension(state)

            # Track peak harmony
            if H > peak_harmony:
                peak_harmony = H
                peak_cycle = cycle + 1

            # Count dominance
            dominance_counts[dominant] += 1

            # Journey tracking
            if track_journey:
                # Distance traveled this step
                step_distance = np.linalg.norm(state - prev_state)
                journey.distance_traveled += step_distance

                # Struggle integral: time weighted by distance from harmony
                journey.struggle_integral += (1 - H) * dt

                # Cumulative harmony
                journey.cumulative_harmony += H * dt

                journey.duration += dt
                prev_state = state.copy()

            # Record history
            history["t"].append((cycle + 1) * dt)
            history["L"].append(state[0])
            history["J"].append(state[1])
            history["P"].append(state[2])
            history["W"].append(state[3])
            history["harmony"].append(H)
            history["voltage"].append(V)
            history["dominant"].append(dominant)

        # Calculate earned depth
        if track_journey:
            journey.calculate_earned_depth()

        # Determine overall dominant dimension
        total_cycles = sum(dominance_counts.values())
        dominance_percentages = {
            k: (v / total_cycles * 100) if total_cycles > 0 else 0
            for k, v in dominance_counts.items()
        }
        primary_deficit = max(dominance_counts, key=dominance_counts.get)

        # Final state analysis
        final_state = tuple(state)
        final_harmony = LJPWBaselines.harmony_index(*final_state)
        final_voltage = self.calculate_voltage(*final_state)

        return {
            "history": history,
            "final_state": {
                "L": final_state[0],
                "J": final_state[1],
                "P": final_state[2],
                "W": final_state[3],
                "harmony": final_harmony,
                "voltage": final_voltage,
            },
            "journey": (
                {
                    "distance_traveled": journey.distance_traveled if journey else 0,
                    "struggle_integral": journey.struggle_integral if journey else 0,
                    "cumulative_harmony": journey.cumulative_harmony if journey else 0,
                    "earned_depth": journey.earned_depth if journey else 0,
                    "struggle_ratio": journey.struggle_ratio if journey else 0,
                }
                if track_journey
                else None
            ),
            "deficit_analysis": {
                "primary_deficit": primary_deficit,
                "dominance_percentages": dominance_percentages,
                "interpretation": self._interpret_deficit(primary_deficit, dominance_percentages),
            },
            "peak": {
                "harmony": peak_harmony,
                "cycle": peak_cycle,
            },
            "convergence": {
                "initial_harmony": history["harmony"][0],
                "final_harmony": final_harmony,
                "converged_to_anchor": final_harmony > 0.95,
            },
        }

    def _get_dominant_dimension(self, state: np.ndarray) -> str:
        """Get the dimension requiring most attention (lowest relative to others)."""
        dims = {"L": state[0], "J": state[1], "P": state[2], "W": state[3]}

        # Compare to Natural Equilibrium ratios
        NE = self.NATURAL_EQUILIBRIUM
        relative = {
            "L": state[0] / NE[0],
            "J": state[1] / NE[1],
            "P": state[2] / NE[2],
            "W": state[3] / NE[3],
        }

        # The dimension furthest below its equilibrium is the deficit
        return min(relative, key=relative.get)

    def _interpret_deficit(self, primary: str, percentages: Dict[str, float]) -> str:
        """Interpret the deficit analysis."""
        names = {
            "L": "Love (relationships, connectivity)",
            "J": "Justice (structure, validation)",
            "P": "Power (execution, action)",
            "W": "Wisdom (abstraction, understanding)",
        }

        dominant_pct = percentages[primary]

        if dominant_pct < 30:
            return "Balanced - no significant deficit detected"
        elif dominant_pct < 50:
            return f"Moderate deficit in {names[primary]} ({dominant_pct:.1f}% dominance)"
        elif dominant_pct < 75:
            return f"Significant deficit in {names[primary]} ({dominant_pct:.1f}% dominance)"
        else:
            return f"Critical deficit in {names[primary]} ({dominant_pct:.1f}% dominance) - this needs attention"

    # =========================================================================
    # CORE FEATURE: EARNED DEPTH (Journey Metric)
    # =========================================================================

    def calculate_earned_depth(
        self, path: List[Tuple[float, float, float, float]], step_duration: float = 0.1
    ) -> JourneyMetrics:
        """
        Calculate Earned Depth for a given path through LJPW space.

        Earned Depth = Distance Traveled × Struggle Ratio

        Two entities at the same coordinates are not the same
        if their journeys differed. The hard path earns more depth.

        Args:
            path: List of LJPW coordinate tuples
            step_duration: Time duration of each step

        Returns:
            JourneyMetrics with all journey calculations
        """
        journey = JourneyMetrics()

        if len(path) < 2:
            return journey

        for i in range(1, len(path)):
            prev = np.array(path[i - 1])
            curr = np.array(path[i])

            # Distance traveled
            step_distance = np.linalg.norm(curr - prev)
            journey.distance_traveled += step_distance

            # Harmony at current position
            H = LJPWBaselines.harmony_index(*curr)

            # Struggle integral (time weighted by distance from harmony)
            journey.struggle_integral += (1 - H) * step_duration

            # Cumulative harmony
            journey.cumulative_harmony += H * step_duration

            journey.duration += step_duration

        journey.calculate_earned_depth()
        return journey

    def compare_journeys(
        self,
        easy_path: List[Tuple[float, float, float, float]],
        hard_path: List[Tuple[float, float, float, float]],
        step_duration: float = 0.1,
    ) -> Dict:
        """
        Compare two journeys through LJPW space.

        Demonstrates that the journey matters, not just the destination.

        Args:
            easy_path: A straightforward path
            hard_path: A more challenging path

        Returns:
            Comparison of the two journeys
        """
        easy = self.calculate_earned_depth(easy_path, step_duration)
        hard = self.calculate_earned_depth(hard_path, step_duration)

        depth_ratio = (
            (hard.earned_depth / easy.earned_depth) if easy.earned_depth > 0 else float("inf")
        )

        return {
            "easy_journey": {
                "distance": easy.distance_traveled,
                "struggle": easy.struggle_integral,
                "earned_depth": easy.earned_depth,
            },
            "hard_journey": {
                "distance": hard.distance_traveled,
                "struggle": hard.struggle_integral,
                "earned_depth": hard.earned_depth,
            },
            "comparison": {
                "depth_ratio": depth_ratio,
                "interpretation": f"Hard path earned {depth_ratio:.1f}× more depth than easy path",
            },
        }

    # =========================================================================
    # ATTRACTOR CONVERGENCE TESTING
    # =========================================================================

    def test_attractor_convergence(
        self,
        coords1: Tuple[float, float, float, float],
        coords2: Tuple[float, float, float, float],
        cycles: int = 100,
    ) -> Dict:
        """
        Test if two coordinate sets converge to the same attractor.

        New paradigm: Instead of measuring Euclidean distance,
        check if they converge to the same attractor under resonance.

        Args:
            coords1: First LJPW coordinates
            coords2: Second LJPW coordinates
            cycles: Number of resonance cycles

        Returns:
            Convergence analysis
        """
        result1 = self.resonate(coords1, cycles=cycles, track_journey=False)
        result2 = self.resonate(coords2, cycles=cycles, track_journey=False)

        final1 = np.array(
            [
                result1["final_state"]["L"],
                result1["final_state"]["J"],
                result1["final_state"]["P"],
                result1["final_state"]["W"],
            ]
        )
        final2 = np.array(
            [
                result2["final_state"]["L"],
                result2["final_state"]["J"],
                result2["final_state"]["P"],
                result2["final_state"]["W"],
            ]
        )

        convergence_distance = np.linalg.norm(final1 - final2)
        same_deficit = (
            result1["deficit_analysis"]["primary_deficit"]
            == result2["deficit_analysis"]["primary_deficit"]
        )

        return {
            "coords1_final": tuple(final1),
            "coords2_final": tuple(final2),
            "convergence_distance": convergence_distance,
            "same_deficit": same_deficit,
            "semantically_equivalent": convergence_distance < 0.10 and same_deficit,
            "interpretation": (
                "EQUIVALENT - Same semantic basin"
                if convergence_distance < 0.10 and same_deficit
                else "DIFFERENT - Different semantic basins"
            ),
        }

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def full_analysis(self, coords: Tuple[float, float, float, float], cycles: int = 100) -> Dict:
        """
        Complete analysis of LJPW coordinates.

        Includes:
        - Static metrics (harmony, voltage, distances)
        - Power erosion detection
        - Resonance dynamics
        - Journey metrics
        - Deficit analysis

        Args:
            coords: LJPW coordinates to analyze
            cycles: Resonance cycles to run

        Returns:
            Comprehensive analysis dict
        """
        L, J, P, W = coords

        # Static analysis
        static = {
            "coordinates": {"L": L, "J": J, "P": P, "W": W},
            "voltage": self.calculate_voltage(L, J, P, W),
            "harmony_index": LJPWBaselines.harmony_index(L, J, P, W),
            "distance_from_anchor": LJPWBaselines.distance_from_anchor(L, J, P, W),
            "distance_from_ne": LJPWBaselines.distance_from_natural_equilibrium(L, J, P, W),
        }

        # Power erosion
        erosion = self.detect_power_erosion(L, J, P, W)

        # Resonance dynamics
        resonance = self.resonate(coords, cycles=cycles, track_journey=True)

        return {
            "static": static,
            "power_erosion": {
                "at_risk": erosion.at_risk,
                "severity": erosion.severity,
                "erosion_rate": erosion.erosion_rate,
                "justice_impact": erosion.justice_impact,
                "recommendation": erosion.recommendation,
            },
            "resonance": resonance,
            "summary": {
                "initial_harmony": static["harmony_index"],
                "final_harmony": resonance["final_state"]["harmony"],
                "earned_depth": resonance["journey"]["earned_depth"] if resonance["journey"] else 0,
                "primary_deficit": resonance["deficit_analysis"]["primary_deficit"],
                "power_erosion_risk": erosion.severity,
            },
        }


# =========================================================================
# CONVENIENCE FUNCTIONS
# =========================================================================


def calculate_voltage(L: float, J: float, P: float, W: float) -> float:
    """Calculate semantic voltage (energy) from LJPW coordinates."""
    return ResonanceEngine.calculate_voltage(L, J, P, W)


def detect_power_erosion(L: float, J: float, P: float, W: float) -> PowerErosionResult:
    """Detect if Power is eroding Justice without Wisdom protection."""
    return ResonanceEngine.detect_power_erosion(L, J, P, W)


def get_resonance_engine() -> ResonanceEngine:
    """Get a default ResonanceEngine instance."""
    return ResonanceEngine()


# =========================================================================
# EXAMPLE USAGE
# =========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LJPW Resonance Engine - Demonstration")
    print("=" * 70)
    print()

    engine = ResonanceEngine()

    # Example 1: Voltage Calculation
    print("1. VOLTAGE CALCULATION (Semantic Energy)")
    print("-" * 40)
    coords = (0.6, 0.4, 0.7, 0.7)
    voltage = engine.calculate_voltage(*coords)
    print(f"   Coordinates: L={coords[0]}, J={coords[1]}, P={coords[2]}, W={coords[3]}")
    print(f"   Voltage: {voltage:.4f}")
    print()

    # Example 2: Power Erosion Detection
    print("2. POWER EROSION DETECTION")
    print("-" * 40)

    # Safe case
    safe = (0.6, 0.5, 0.5, 0.8)  # High Wisdom protects
    erosion_safe = engine.detect_power_erosion(*safe)
    print(f"   Safe case: L={safe[0]}, J={safe[1]}, P={safe[2]}, W={safe[3]}")
    print(f"   Severity: {erosion_safe.severity}")
    print(f"   Recommendation: {erosion_safe.recommendation}")
    print()

    # Risky case
    risky = (0.3, 0.5, 0.9, 0.2)  # High Power, Low Wisdom
    erosion_risky = engine.detect_power_erosion(*risky)
    print(f"   Risky case: L={risky[0]}, J={risky[1]}, P={risky[2]}, W={risky[3]}")
    print(f"   Severity: {erosion_risky.severity}")
    print(f"   Erosion Rate: {erosion_risky.erosion_rate:.4f}")
    print(f"   Recommendation: {erosion_risky.recommendation}")
    print()

    # Example 3: Resonance Cycling
    print("3. RESONANCE CYCLING (100 cycles)")
    print("-" * 40)
    initial = (0.2, 0.3, 0.9, 0.2)  # Reckless Power scenario
    result = engine.resonate(initial, cycles=100)

    print(f"   Initial: L={initial[0]}, J={initial[1]}, P={initial[2]}, W={initial[3]}")
    final = result["final_state"]
    print(
        f"   Final:   L={final['L']:.3f}, J={final['J']:.3f}, P={final['P']:.3f}, W={final['W']:.3f}"
    )
    print(f"   Harmony: {result['convergence']['initial_harmony']:.4f} → {final['harmony']:.4f}")
    print(f"   Peak Harmony: {result['peak']['harmony']:.4f} at cycle {result['peak']['cycle']}")
    print()

    # Example 4: Journey Metrics (Earned Depth)
    print("4. EARNED DEPTH (Journey Metric)")
    print("-" * 40)
    if result["journey"]:
        journey = result["journey"]
        print(f"   Distance Traveled: {journey['distance_traveled']:.4f}")
        print(f"   Struggle Integral: {journey['struggle_integral']:.4f}")
        print(f"   Earned Depth: {journey['earned_depth']:.4f}")
    print()

    # Example 5: Deficit Analysis
    print("5. DEFICIT ANALYSIS")
    print("-" * 40)
    deficit = result["deficit_analysis"]
    print(f"   Primary Deficit: {deficit['primary_deficit']}")
    print(f"   Dominance: {deficit['dominance_percentages']}")
    print(f"   Interpretation: {deficit['interpretation']}")
    print()

    # Example 6: Full Analysis
    print("6. FULL ANALYSIS")
    print("-" * 40)
    analysis = engine.full_analysis((0.5, 0.4, 0.8, 0.3), cycles=50)
    print(f"   Initial Harmony: {analysis['summary']['initial_harmony']:.4f}")
    print(f"   Final Harmony: {analysis['summary']['final_harmony']:.4f}")
    print(f"   Power Erosion Risk: {analysis['summary']['power_erosion_risk']}")
    print(f"   Primary Deficit: {analysis['summary']['primary_deficit']}")
    print(f"   Earned Depth: {analysis['summary']['earned_depth']:.4f}")
