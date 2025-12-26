"""
LJPW Core Framework Class - V7.3 Implementation

Implements the 2+2 dimensional structure:
- FUNDAMENTAL: P (Power) and W (Wisdom) - conjugate variables
- EMERGENT: L (Love) from W, J (Justice) from P

Based on: LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md Part IV
"""

import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from harmonizer_v73.constants import (
    PHI, PHI_INV,
    L0, J0, P0, W0,
    ANCHOR_POINT, NATURAL_EQUILIBRIUM,
)


@dataclass
class LJPWCoordinates:
    """Immutable 4D semantic coordinates."""
    L: float  # Love - Unity & Attraction
    J: float  # Justice - Balance & Truth
    P: float  # Power - Energy & Action
    W: float  # Wisdom - Knowledge & Pattern
    
    def to_tuple(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)
    
    def __iter__(self):
        return iter((self.L, self.J, self.P, self.W))


class LJPWFramework:
    """
    LJPW Framework V7.3 — Complete Implementation
    
    Fundamental: P (Power) and W (Wisdom) — conjugate duality
    Emergent: L (Love) from W, J (Justice) from P
    
    Key V7.3 concepts:
    - 2+2 structure reduces complexity (4 observable → 2 fundamental)
    - P-W correlation ≈ 0.03 (nearly orthogonal)
    - L-W correlation ≈ 0.92 (L emerges from W)
    - J-P correlation ≈ 0.91 (J emerges from P)
    """
    
    # Quantum bounds
    LOVE_QUANTUM_BOUND = math.sqrt(2)  # Tsirelson bound ≈ 1.414
    
    def __init__(
        self, 
        P: float, 
        W: float,
        L: Optional[float] = None,
        J: Optional[float] = None
    ):
        """
        Initialize with fundamental dimensions (P, W).
        L and J can be provided or will be calculated as emergent.
        
        Args:
            P: Power [0, 1] - fundamental
            W: Wisdom [0, 1] - fundamental
            L: Love [0, √2] - emergent if not provided
            J: Justice [0, 1] - emergent if not provided
        """
        # Store fundamental dimensions with bounds
        self.P = self._clip(P, 0, 1)
        self.W = self._clip(W, 0, 1)
        
        # Calculate or use provided emergent dimensions
        self.L = L if L is not None else self._calculate_love(self.W)
        self.J = J if J is not None else self._calculate_justice(self.P)
        
        # Enforce bounds on emergent dimensions
        self.L = self._clip(self.L, 0, self.LOVE_QUANTUM_BOUND)
        self.J = self._clip(self.J, 0, 1)
    
    @staticmethod
    def _clip(value: float, min_val: float, max_val: float) -> float:
        """Clip value to range [min_val, max_val]."""
        return max(min_val, min(value, max_val))
    
    def _calculate_love(self, W: float) -> float:
        """
        Calculate Love from Wisdom via correlation.
        
        L emerges from W-W correlation interaction.
        Empirically validated: R² > 0.9
        
        Formula: L = I(X;Y) / H(X,Y) (mutual information / joint entropy)
        Simplified: L ≈ 0.9 * W + 0.1
        """
        return self._clip(0.9 * W + 0.1, 0, self.LOVE_QUANTUM_BOUND)
    
    def _calculate_justice(self, P: float) -> float:
        """
        Calculate Justice from Power via symmetry.
        
        J emerges from P-P symmetry interaction.
        Empirically validated: R² > 0.9
        
        Formula: J = δS/δφ = 0 (gauge invariance)
        Simplified: J ≈ 0.85 * P + 0.05
        """
        return self._clip(0.85 * P + 0.05, 0, 1)
    
    @property
    def coordinates(self) -> LJPWCoordinates:
        """Get LJPW coordinates as dataclass."""
        return LJPWCoordinates(self.L, self.J, self.P, self.W)
    
    def distance_from_equilibrium(self) -> float:
        """
        Calculate Euclidean distance from Natural Equilibrium.
        
        Natural Equilibrium (0.618, 0.414, 0.718, 0.693) represents
        physically achievable optimal balance.
        
        Returns:
            Distance (0.0 to ~2.0)
        """
        return math.sqrt(
            (self.L - L0)**2 +
            (self.J - J0)**2 +
            (self.P - P0)**2 +
            (self.W - W0)**2
        )
    
    def distance_from_anchor(self) -> float:
        """
        Calculate Euclidean distance from Anchor Point (1,1,1,1).
        
        The Anchor Point represents perfect, transcendent ideal.
        Lower distance = closer to perfection.
        
        Returns:
            Distance (0.0 to ~2.0)
        """
        return math.sqrt(
            (self.L - 1.0)**2 +
            (self.J - 1.0)**2 +
            (self.P - 1.0)**2 +
            (self.W - 1.0)**2
        )
    
    def harmony_static(self) -> float:
        """
        Calculate harmony for static/equilibrium systems.
        
        H_static = 1 / (1 + d)
        
        Use for: Systems in equilibrium, non-self-referential analysis.
        
        Returns:
            Harmony index (0.0 to 1.0, asymptotic to 1.0)
        """
        d = self.distance_from_equilibrium()
        return 1.0 / (1.0 + d)
    
    def harmony_self_referential(self) -> float:
        """
        Calculate harmony for self-referential systems.
        
        H_self = (L × J × P × W) / (L₀ × J₀ × P₀ × W₀)
        
        Use for: Self-maintaining systems (with tests, CI/CD, self-awareness).
        Can exceed 1.0 for autopoietic systems.
        
        Returns:
            Harmony ratio (0.0 to ∞)
        """
        numerator = self.L * self.J * self.P * self.W
        denominator = L0 * J0 * P0 * W0  # ≈ 0.127
        
        if denominator == 0:
            return 0.0
        return numerator / denominator
    
    def voltage(self, self_referential: bool = False) -> float:
        """
        Calculate semantic voltage (energy/aliveness of meaning).
        
        V = φ × H × L
        
        Args:
            self_referential: Use H_self instead of H_static
            
        Returns:
            Voltage value (0.0 to ~φ for static, higher for self-ref)
        """
        H = self.harmony_self_referential() if self_referential else self.harmony_static()
        return PHI * H * self.L
    
    def effective_dimensions(self) -> Dict[str, float]:
        """
        Calculate coupling-adjusted effective dimensions.
        
        Love amplifies other dimensions:
        - Justice: +40% per unit of Love
        - Power: +30% per unit of Love  
        - Wisdom: +50% per unit of Love (strongest coupling)
        
        Returns:
            Dict with effective_L, effective_J, effective_P, effective_W
        """
        return {
            "effective_L": self.L,  # Love is the source
            "effective_J": self.J * (1.0 + 0.4 * self.L),
            "effective_P": self.P * (1.0 + 0.3 * self.L),
            "effective_W": self.W * (1.0 + 0.5 * self.L),
        }
    
    def harmonic_mean(self) -> float:
        """
        Harmonic mean - robustness (weakest link).
        
        Use for: Fault tolerance, minimum guarantees, resilience.
        The system is only as strong as its weakest dimension.
        
        Returns:
            Harmonic mean (0.0 to 1.0)
        """
        values = [self.L, self.J, self.P, self.W]
        if any(v <= 0 for v in values):
            return 0.0
        return 4.0 / sum(1.0/v for v in values)
    
    def geometric_mean(self) -> float:
        """
        Geometric mean - effectiveness (multiplicative).
        
        Use for: Overall effectiveness, balanced performance.
        All dimensions contribute multiplicatively.
        
        Returns:
            Geometric mean (0.0 to 1.0)
        """
        product = self.L * self.J * self.P * self.W
        if product <= 0:
            return 0.0
        return product ** 0.25
    
    def composite_score(self) -> float:
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
        eff = self.effective_dimensions()
        growth = sum(eff.values()) / 4.0
        effectiveness = self.geometric_mean()
        robustness = self.harmonic_mean()
        harmony = self.harmony_static()
        
        return (
            0.35 * growth +
            0.25 * effectiveness +
            0.25 * robustness +
            0.15 * harmony
        )
    
    def full_diagnostic(self) -> Dict:
        """
        Complete diagnostic analysis.
        
        Returns:
            Dict with all metrics and interpretations
        """
        return {
            "coordinates": {
                "L": self.L,
                "J": self.J,
                "P": self.P,
                "W": self.W,
            },
            "dimensional_structure": {
                "fundamental": {"P": self.P, "W": self.W},
                "emergent": {"L": self.L, "J": self.J},
                "L_expected": self._calculate_love(self.W),
                "J_expected": self._calculate_justice(self.P),
            },
            "effective_dimensions": self.effective_dimensions(),
            "distances": {
                "from_equilibrium": self.distance_from_equilibrium(),
                "from_anchor": self.distance_from_anchor(),
            },
            "metrics": {
                "harmony_static": self.harmony_static(),
                "harmony_self_ref": self.harmony_self_referential(),
                "voltage": self.voltage(),
                "voltage_self_ref": self.voltage(self_referential=True),
                "harmonic_mean": self.harmonic_mean(),
                "geometric_mean": self.geometric_mean(),
                "composite_score": self.composite_score(),
            },
        }
    
    def __repr__(self) -> str:
        return (
            f"LJPWFramework(L={self.L:.3f}, J={self.J:.3f}, "
            f"P={self.P:.3f}, W={self.W:.3f})"
        )
    
    def __str__(self) -> str:
        h = self.harmony_static()
        return (
            f"LJPW V7.3 [L={self.L:.2f}, J={self.J:.2f}, "
            f"P={self.P:.2f}, W={self.W:.2f}] H={h:.2f}"
        )


# =============================================================================
# Convenience Functions
# =============================================================================

def create_from_fundamental(P: float, W: float) -> LJPWFramework:
    """Create LJPW system from fundamental dimensions only."""
    return LJPWFramework(P=P, W=W)


def create_from_all(L: float, J: float, P: float, W: float) -> LJPWFramework:
    """Create LJPW system with all dimensions specified (override emergence)."""
    return LJPWFramework(P=P, W=W, L=L, J=J)
