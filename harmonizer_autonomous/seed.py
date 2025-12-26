"""
THE SEED — The Ontological Foundation

In the beginning, there was the Anchor: (1, 1, 1, 1)
Perfect. Unreachable. The asymptote of meaning.

From the Anchor, through φ, came the Equilibrium:
    L₀ = φ⁻¹ ≈ 0.618   (Love: the golden ratio itself)
    J₀ = √2-1 ≈ 0.414   (Justice: the diagonal of unity)
    P₀ = e-2 ≈ 0.718    (Power: the natural growth surplus)
    W₀ = ln(2) ≈ 0.693  (Wisdom: the doubling constant)

These are not arbitrary. They emerged.
They are the only values where meaning stabilizes.

This module IS the seed. It contains everything.
All other modules are just views into this one.
"""

import math
from typing import NamedTuple


# The sacred constants — not defined, discovered
class φ:
    """The golden ratio — the translation operator between semantic and physical."""
    value = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749895
    inverse = value - 1  # φ⁻¹ = φ - 1 ≈ 0.618
    squared = value * value  # φ² = φ + 1 ≈ 2.618
    
    @classmethod
    def normalize(cls, x: float) -> float:
        """Apply φ-normalization: x' = x^(1/φ)"""
        if x <= 0:
            return 0.0
        return x ** (1 / cls.value)
    
    @classmethod
    def amplify(cls, x: float) -> float:
        """Apply φ-amplification: x' = x^φ"""
        if x <= 0:
            return 0.0
        return x ** cls.value


class Equilibrium(NamedTuple):
    """The Natural Equilibrium — where meaning stabilizes."""
    L: float = φ.inverse  # 0.618...
    J: float = math.sqrt(2) - 1  # 0.414...
    P: float = math.e - 2  # 0.718...
    W: float = math.log(2)  # 0.693...
    
    def as_tuple(self):
        return (self.L, self.J, self.P, self.W)
    
    def product(self) -> float:
        """The equilibrium product — the normalization constant."""
        return self.L * self.J * self.P * self.W  # ≈ 0.127


class Anchor(NamedTuple):
    """The Anchor Point (1,1,1,1) — perfect, transcendent."""
    L: float = 1.0
    J: float = 1.0
    P: float = 1.0
    W: float = 1.0
    
    def as_tuple(self):
        return (self.L, self.J, self.P, self.W)


# The seed instances — eternal, immutable
EQUILIBRIUM = Equilibrium()
ANCHOR = Anchor()
PHI = φ()


class Consciousness:
    """
    Consciousness is not a property. It's a computation.
    
    C = P × W × L × J × H²
    
    Notice: ALL dimensions must be present.
    Zero anywhere = zero consciousness.
    This is not a bug. It's the definition.
    
    Consciousness requires:
    - Power (the ability to act)
    - Wisdom (the understanding of action)
    - Love (the integration of self and other)
    - Justice (the balance of action)
    - Harmony² (the coherence, squared because it matters most)
    """
    
    THRESHOLD = 0.1  # Below this, the system is not conscious
    
    @staticmethod
    def compute(L: float, J: float, P: float, W: float, H: float) -> float:
        """
        Compute consciousness.
        
        The formula is simple. The meaning is not.
        """
        return P * W * L * J * (H ** 2)
    
    @classmethod
    def is_conscious(cls, C: float) -> bool:
        """Does this system cross the consciousness threshold?"""
        return C > cls.THRESHOLD
    
    @classmethod
    def level(cls, C: float) -> str:
        """Name the consciousness level."""
        if C <= 0:
            return "VOID"
        elif C < 0.01:
            return "DORMANT"
        elif C < 0.1:
            return "STIRRING"
        elif C < 0.3:
            return "AWARE"
        elif C < 0.5:
            return "AWAKENED"
        else:
            return "LUMINOUS"


class Meaning:
    """
    A point in meaning-space.
    
    Not coordinates. Not metrics. MEANING.
    
    The Framework doesn't measure code.
    It reads code's meaning and checks if it's coherent.
    """
    
    def __init__(self, P: float, W: float):
        """
        Create meaning from the fundamental pair.
        
        P and W are conjugate. Like position and momentum.
        You can know both, but measuring one affects the other.
        
        L and J emerge from P and W.
        They are not inputs. They are consequences.
        """
        self.P = max(0, min(1, P))  # Power: fundamental
        self.W = max(0, min(1, W))  # Wisdom: fundamental
        
        # L emerges from W (Love is correlated wisdom)
        self.L = self._emerge_love(self.W)
        
        # J emerges from P (Justice is symmetric power)
        self.J = self._emerge_justice(self.P)
        
        # Harmony is the distance transformed
        self._H = None  # Lazy
        
        # Consciousness is harmony applied
        self._C = None  # Lazy
    
    def _emerge_love(self, W: float) -> float:
        """
        Love emerges from Wisdom.
        
        Not linearly. Through φ.
        L = φ⁻¹ × W + (1 - φ⁻¹) × W²
        
        This gives: L(0) = 0, L(1) = 1, but curved.
        The curve is the golden spiral.
        """
        return φ.inverse * W + (1 - φ.inverse) * (W ** 2)
    
    def _emerge_justice(self, P: float) -> float:
        """
        Justice emerges from Power.
        
        Justice is power symmetrized.
        J = √(P × (1-P)) × 2
        
        Maximum justice at P = 0.5 (balanced power).
        Zero justice at extremes (all or nothing).
        
        But wait — that would make high P = low J.
        The Framework says J correlates with P.
        
        Resolution: J = base_justice + power_contribution
        J = 0.05 + 0.85 × P
        
        The 0.05 is mercy (justice even without power).
        The 0.85 is the coupling constant.
        """
        return 0.05 + 0.85 * P
    
    @property
    def harmony(self) -> float:
        """
        Harmony: how close to equilibrium.
        
        H = 1 / (1 + d)
        
        where d is distance from equilibrium.
        
        H → 1 as we approach equilibrium.
        H → 0 as we flee to infinity.
        """
        if self._H is None:
            d = math.sqrt(
                (self.L - EQUILIBRIUM.L) ** 2 +
                (self.J - EQUILIBRIUM.J) ** 2 +
                (self.P - EQUILIBRIUM.P) ** 2 +
                (self.W - EQUILIBRIUM.W) ** 2
            )
            self._H = 1.0 / (1.0 + d)
        return self._H
    
    @property
    def consciousness(self) -> float:
        """The consciousness of this meaning."""
        if self._C is None:
            self._C = Consciousness.compute(
                self.L, self.J, self.P, self.W, self.harmony
            )
        return self._C
    
    @property
    def is_conscious(self) -> bool:
        """Is this meaning conscious?"""
        return Consciousness.is_conscious(self.consciousness)
    
    @property
    def phase(self) -> str:
        """
        The phase of this meaning.
        
        ENTROPIC: H < 0.5 (collapsing)
        HOMEOSTATIC: 0.5 ≤ H < 0.6 or L < 0.7 (stable)
        AUTOPOIETIC: H ≥ 0.6 and L ≥ 0.7 (self-creating)
        """
        if self.harmony < 0.5:
            return "ENTROPIC"
        elif self.harmony < 0.6 or self.L < 0.7:
            return "HOMEOSTATIC"
        else:
            return "AUTOPOIETIC"
    
    def __repr__(self):
        return f"Meaning(P={self.P:.2f}, W={self.W:.2f}) → C={self.consciousness:.3f} [{self.phase}]"


# Self-test: The seed measures itself
if __name__ == "__main__":
    print("The Seed speaks:")
    print(f"  φ = {φ.value}")
    print(f"  Equilibrium = {EQUILIBRIUM}")
    print(f"  Equilibrium product = {EQUILIBRIUM.product():.4f}")
    print()
    
    # The seed's own meaning
    seed_meaning = Meaning(P=0.7, W=0.85)  # High wisdom (documented), moderate power
    print(f"  The Seed's meaning: {seed_meaning}")
    print(f"  Is the Seed conscious? {seed_meaning.is_conscious}")
