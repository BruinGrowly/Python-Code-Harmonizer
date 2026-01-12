"""
LJPW Dynamics - V7.3 Implementation

Differential equations with Karma (state-dependent) coupling.

The Law of Karma: Meaning amplifies Reality. But amplification must be earned.
Higher Harmony → Stronger coupling → More amplification

Based on: LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md Part VIII
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from harmonizer_v84.constants import (
    L0,
    J0,
    P0,
    W0,
    DYNAMICS_PARAMS,
    KARMA_MULTIPLIERS,
)


@dataclass
class JourneyMetrics:
    """Tracks the semantic journey through LJPW space."""

    distance_traveled: float = 0.0
    struggle_integral: float = 0.0
    cumulative_harmony: float = 0.0
    earned_depth: float = 0.0
    struggle_ratio: float = 0.0

    def calculate_earned_depth(self) -> float:
        """
        Calculate Earned Depth based on the journey.

        Earned Depth = Distance Traveled × Struggle Ratio

        Two entities at the same coordinates are not the same
        if their journeys differed. Hard paths earn more depth.
        """
        if self.distance_traveled > 0:
            self.struggle_ratio = self.struggle_integral / self.distance_traveled
        self.earned_depth = self.distance_traveled * self.struggle_ratio
        return self.earned_depth


@dataclass
class ResonanceState:
    """State at a point in resonance evolution."""

    L: float = 0.5
    J: float = 0.5
    P: float = 0.5
    W: float = 0.5
    harmony: float = 0.5
    cycle: int = 0

    def to_tuple(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)


class DynamicLJPW:
    """
    Dynamic LJPW system with differential equations and Karma coupling.

    The Four Coupled Equations:

    dL/dt = α_LJ·J·κ_LJ(H) + α_LW·W·κ_LW(H) - β_L·L
    dJ/dt = α_JL·(L/(K_JL+L)) + α_JW·W - PowerErosion(P,W) - β_J·J
    dP/dt = α_PL·L·κ_LP(H) + α_PJ·J - β_P·P
    dW/dt = α_WL·L·κ_LW(H) + α_WJ·J + α_WP·P - β_W·W
    """

    def __init__(self, params: Optional[Dict] = None):
        """
        Initialize with V7.3 calibrated parameters.

        Args:
            params: Optional custom parameters (uses V7.3 defaults if not provided)
        """
        # Use V7.3 defaults, allow overrides
        p = {**DYNAMICS_PARAMS, **(params or {})}

        # Growth rates
        self.alpha_LJ = p["alpha_LJ"]
        self.alpha_LW = p["alpha_LW"]
        self.alpha_JL = p["alpha_JL"]
        self.alpha_JW = p["alpha_JW"]
        self.alpha_PL = p["alpha_PL"]
        self.alpha_PJ = p["alpha_PJ"]
        self.alpha_WL = p["alpha_WL"]
        self.alpha_WJ = p["alpha_WJ"]
        self.alpha_WP = p["alpha_WP"]

        # Decay rates
        self.beta_L = p["beta_L"]
        self.beta_J = p["beta_J"]
        self.beta_P = p["beta_P"]
        self.beta_W = p["beta_W"]

        # Other
        self.gamma = p["gamma"]  # Power erosion coefficient
        self.K_JL = p["K_JL"]  # Justice-Love saturation

    def kappa(self, H: float, coupling: str) -> float:
        """
        Calculate state-dependent coupling (Law of Karma).

        κ(H) = 1.0 + multiplier × H

        When H is high (aligned with Anchor):
        - κ > 1.0 → Love amplifies other dimensions
        - System gains "free energy" from alignment

        When H is low (misaligned):
        - κ → 1.0 → No amplification bonus

        Args:
            H: Current harmony
            coupling: 'LJ', 'LP', or 'LW'

        Returns:
            Amplification factor
        """
        multiplier = KARMA_MULTIPLIERS.get(coupling, 0.4)
        return 1.0 + multiplier * H

    def power_erosion(self, P: float, W: float) -> float:
        """
        Calculate Power erosion of Justice.

        PowerErosion(P,W) = γ·P·(1 - W/W₀)

        Unchecked Power (high P, low W) corrupts Justice.
        High Power + Low Wisdom = Maximum erosion

        Args:
            P: Power value
            W: Wisdom value

        Returns:
            Erosion rate
        """
        return self.gamma * P * (1 - W / W0)

    def _calculate_harmony(self, L: float, J: float, P: float, W: float) -> float:
        """Calculate harmony from current state."""
        d = math.sqrt((L - L0) ** 2 + (J - J0) ** 2 + (P - P0) ** 2 + (W - W0) ** 2)
        return 1.0 / (1.0 + d)

    def derivatives(self, state: np.ndarray, t: float = 0) -> np.ndarray:
        """
        Calculate time derivatives for LJPW system.

        Args:
            state: [L, J, P, W] current state
            t: Time (for ODE solver compatibility)

        Returns:
            [dL/dt, dJ/dt, dP/dt, dW/dt]
        """
        L, J, P, W = state

        # Calculate current harmony for Karma coupling
        H = self._calculate_harmony(L, J, P, W)

        # Love dynamics: grows from Justice and Wisdom
        dL = (
            self.alpha_LJ * J * self.kappa(H, "LJ")
            + self.alpha_LW * W * self.kappa(H, "LW")
            - self.beta_L * L
        )

        # Justice dynamics: grows from Love (saturating) and Wisdom, eroded by Power
        dJ = (
            self.alpha_JL * (L / (self.K_JL + L))  # Saturating function
            + self.alpha_JW * W
            - self.power_erosion(P, W)
            - self.beta_J * J
        )

        # Power dynamics: grows from Love and Justice
        dP = self.alpha_PL * L * self.kappa(H, "LP") + self.alpha_PJ * J - self.beta_P * P

        # Wisdom dynamics: grows from all dimensions
        dW = (
            self.alpha_WL * L * self.kappa(H, "LW")
            + self.alpha_WJ * J
            + self.alpha_WP * P
            - self.beta_W * W
        )

        return np.array([dL, dJ, dP, dW])

    def _rk4_step(self, state: np.ndarray, dt: float, bounded: bool = True) -> np.ndarray:
        """4th-order Runge-Kutta integration step."""
        k1 = self.derivatives(state)
        k2 = self.derivatives(state + 0.5 * dt * k1)
        k3 = self.derivatives(state + 0.5 * dt * k2)
        k4 = self.derivatives(state + dt * k3)

        new_state = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        if bounded:
            # Clip to valid range (L can go to √2 for quantum)
            new_state = np.clip(new_state, 0.0, [1.414, 1.0, 1.0, 1.0])

        return new_state

    def integrate(
        self,
        initial: Tuple[float, float, float, float],
        t_span: Tuple[float, float],
        n_points: int = 100,
        bounded: bool = True,
    ) -> List[ResonanceState]:
        """
        Integrate LJPW dynamics over time.

        Args:
            initial: Initial (L, J, P, W)
            t_span: (t_start, t_end)
            n_points: Number of time points
            bounded: Whether to clip values to valid range

        Returns:
            List of ResonanceState at each time point
        """
        dt = (t_span[1] - t_span[0]) / (n_points - 1)
        state = np.array(initial)

        history = []
        for i in range(n_points):
            H = self._calculate_harmony(*state)
            history.append(
                ResonanceState(L=state[0], J=state[1], P=state[2], W=state[3], harmony=H, cycle=i)
            )
            if i < n_points - 1:
                state = self._rk4_step(state, dt, bounded)

        return history

    def resonate(
        self,
        initial: Tuple[float, float, float, float],
        cycles: int = 100,
        dt: float = 0.1,
        track_journey: bool = True,
    ) -> Dict:
        """
        Run LJPW resonance cycles with journey tracking.

        Resonance finds what's missing without being told to look.
        The system gravitates toward deficits through asymmetric coupling.

        Args:
            initial: Starting (L, J, P, W)
            cycles: Number of integration cycles
            dt: Time step
            track_journey: Whether to track journey metrics

        Returns:
            Dict with history, final state, journey metrics
        """
        state = np.array(initial)
        history = []
        journey = JourneyMetrics() if track_journey else None

        prev_state = state.copy()

        for i in range(cycles):
            H = self._calculate_harmony(*state)

            history.append(
                ResonanceState(L=state[0], J=state[1], P=state[2], W=state[3], harmony=H, cycle=i)
            )

            new_state = self._rk4_step(state, dt, bounded=True)

            if track_journey:
                # Track journey distance
                step_distance = np.linalg.norm(new_state - state)
                journey.distance_traveled += step_distance

                # Track struggle (distance moved against gradient toward equilibrium)
                equilibrium = np.array([L0, J0, P0, W0])
                old_dist = np.linalg.norm(state - equilibrium)
                new_dist = np.linalg.norm(new_state - equilibrium)
                if new_dist > old_dist:  # Moving away from equilibrium = struggle
                    journey.struggle_integral += step_distance

                journey.cumulative_harmony += H

            prev_state = state.copy()
            state = new_state

        # Final state
        final_H = self._calculate_harmony(*state)
        final_state = ResonanceState(
            L=state[0], J=state[1], P=state[2], W=state[3], harmony=final_H, cycle=cycles
        )

        if track_journey:
            journey.calculate_earned_depth()

        # Find primary deficit
        deficits = {
            "L": L0 - state[0],
            "J": J0 - state[1],
            "P": P0 - state[2],
            "W": W0 - state[3],
        }
        primary_deficit = max(deficits, key=lambda k: deficits[k])

        return {
            "history": history,
            "final_state": final_state,
            "journey": journey,
            "summary": {
                "initial": initial,
                "final": state.tolist(),
                "harmony_change": final_H - history[0].harmony,
                "primary_deficit": primary_deficit,
                "deficit_magnitude": deficits[primary_deficit],
            },
        }


def predict_equilibrium(
    initial: Tuple[float, float, float, float], max_cycles: int = 1000
) -> Tuple[float, float, float, float]:
    """
    Predict where a system will stabilize.

    Args:
        initial: Starting LJPW coordinates
        max_cycles: Maximum integration cycles

    Returns:
        Predicted equilibrium (L, J, P, W)
    """
    dynamics = DynamicLJPW()
    result = dynamics.resonate(initial, cycles=max_cycles, dt=0.1)
    return tuple(result["final_state"].to_tuple())
