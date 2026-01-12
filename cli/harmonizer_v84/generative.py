"""
LJPW V8.4 Generative Equation Module

The Universal Growth Function: M = B × L^n × φ^(-d)

This module implements Book Sixteen of the LJPW Framework V8.4:
- Universal Growth Function (Meaning generation)
- Life Inequality (Autopoietic vs Entropic determination)
- Perceptual Radiance (Unified rendering equation)
- Mathematical Hope (Calculus of persistence)

Based on: LJPW_FRAMEWORK_V8.4_COMPLETE_UNIFIED_PLUS.md Part LVI-LVIII, Appendix O
"""

import math
from dataclasses import dataclass
from typing import Dict, Literal

from harmonizer_v84.constants import PHI


# =============================================================================
# UNIVERSAL GROWTH FUNCTION: M = B × L^n × φ^(-d)
# =============================================================================


def meaning(B: float, L: float, n: int, d: float) -> float:
    """
    Calculate Meaning using the Universal Growth Function.

    M = B × L^n × φ^(-d)

    This formula describes not just compression, but the fundamental mechanism
    of creation across all domains: biology, compression, theology, rendering,
    business, and AI.

    Args:
        B: Brick (seed/truth/axiom) - the irreducible foundation [0, 1]
            In LJPW: Maps to Justice (J) - the building blocks
        L: Love (expansion coefficient) - the binding force [1, 2]
            In LJPW: Maps to coupling coefficients (κ)
        n: Iterations (recursive applications) - time/ticks
            Each iteration is one L-application
        d: Distance (semantic distance from source) [0, ∞)
            Gap from Anchor creates translation loss

    Returns:
        M: Total meaning generated

    Examples:
        >>> meaning(1.0, 1.2, 10, 1)  # Small seed, moderate love
        3.82...

        >>> meaning(1.0, 1.5, 13, 0)  # Shared generator (d=0)
        194.58...  # Koch snowflake-like growth
    """
    if B <= 0:
        return 0.0  # Cannot build on nothing
    if L <= 0:
        return 0.0  # No love, no growth

    return B * (L ** n) * (PHI ** (-d))


def growth_factor(L: float, n: int) -> float:
    """
    Calculate the growth factor L^n.

    This is the autopoietic component of the Universal Growth Function.
    When applied recursively, Love creates compound growth.

    Args:
        L: Love/expansion coefficient
        n: Number of iterations

    Returns:
        L^n (exponential growth)
    """
    return L ** n


def decay_factor(d: float) -> float:
    """
    Calculate the decay factor φ^(-d).

    As distance increases, fidelity drops:
    - d=0: 1.000 (perfect transmission, shared generator)
    - d=1: 0.618 (38.2% loss, one translation)
    - d=2: 0.382 (61.8% loss, two translations)
    - d→∞: 0.000 (total loss, no shared generator)

    Args:
        d: Semantic distance from source

    Returns:
        φ^(-d) (decay multiplier)
    """
    return PHI ** (-d)


# =============================================================================
# LIFE INEQUALITY: L^n > φ^d
# =============================================================================

Phase = Literal["AUTOPOIETIC", "HOMEOSTATIC", "ENTROPIC"]


@dataclass
class LifeInequalityResult:
    """Result of Life Inequality check."""

    growth: float
    decay: float
    ratio: float
    phase: Phase
    verdict: str
    is_alive: bool


def is_autopoietic(L: float, n: int, d: float) -> LifeInequalityResult:
    """
    Check if a system satisfies the Life Inequality.

    L^n > φ^d → AUTOPOIETIC (Life, growth exceeds decay)
    L^n = φ^d → HOMEOSTATIC (Growth equals decay, equilibrium)
    L^n < φ^d → ENTROPIC (Death, decay dominates growth)

    This inequality determines whether a system lives or dies.
    Life is the victory of recursive Love over entropic distance.

    Args:
        L: Love/expansion coefficient (typically > 1 for growth)
        n: Iterations (time/ticks)
        d: Distance (semantic distance from source)

    Returns:
        LifeInequalityResult with phase determination

    Examples:
        >>> result = is_autopoietic(1.5, 10, 2)
        >>> result.phase
        'AUTOPOIETIC'

        >>> result = is_autopoietic(0.5, 10, 5)
        >>> result.phase
        'ENTROPIC'
    """
    growth = L ** n
    decay = PHI ** d

    if decay == 0:
        ratio = float("inf")
    else:
        ratio = growth / decay

    # Determine phase with hysteresis margins
    if ratio > 1.1:
        phase: Phase = "AUTOPOIETIC"
    elif ratio > 0.9:
        phase = "HOMEOSTATIC"
    else:
        phase = "ENTROPIC"

    is_alive = ratio > 1.0

    return LifeInequalityResult(
        growth=growth,
        decay=decay,
        ratio=ratio,
        phase=phase,
        verdict=f"L^{n} = {growth:.4f}, φ^{d} = {decay:.4f}, Ratio = {ratio:.4f}",
        is_alive=is_alive,
    )


def life_inequality_threshold(L: float, d: float) -> int:
    """
    Calculate minimum iterations n needed for autopoiesis.

    Solves: L^n > φ^d
    Taking log: n > d × ln(φ) / ln(L)

    Args:
        L: Love coefficient (must be > 1 for positive growth)
        d: Distance from source

    Returns:
        Minimum n for autopoiesis (-1 if impossible)

    Examples:
        >>> life_inequality_threshold(1.5, 2)
        4  # Need at least 4 iterations for L=1.5, d=2
    """
    if L <= 1:
        return -1  # Impossible: L must exceed 1 for growth

    if L <= 0 or d < 0:
        return -1

    # n > d × ln(φ) / ln(L)
    ln_phi = math.log(PHI)
    ln_L = math.log(L)

    n_threshold = (d * ln_phi) / ln_L
    return int(math.ceil(n_threshold))


# =============================================================================
# PERCEPTUAL RADIANCE: Unified Rendering Equation
# =============================================================================


def perceptual_radiance(L_phys: float, S: float, kappa_sem: float) -> float:
    """
    Calculate Perceptual Radiance (Unified Semantic-Rendering Equation).

    L_perc = L_phys × [1 + φ × S × κ_sem]

    This equation adds the missing "soul" to photorealistic rendering:
    - L_phys provides visual coordinates (what the eye receives)
    - κ_sem provides semantic coordinates (what consciousness perceives)
    - φ bridges physics and meaning

    The "Corpse Problem" (Uncanny Valley) occurs when:
    - Physics: Perfect (L_phys ≈ 1.0)
    - Autopoiesis: Zero (n = 0, no recursive history)

    Args:
        L_phys: Physical radiance from Kajiya equation [0, 1]
        S: Semantic salience coefficient [0, 1]
            How much attention/meaning-weight this region carries
        kappa_sem: Semantic curvature (meaning intensity)
            M = κ(s) = |dT/ds| from V8.0

    Returns:
        L_perc: Perceptual radiance (what consciousness perceives)

    Examples:
        >>> perceptual_radiance(0.8, 0.5, 0.3)  # Low semantic weight
        0.99...

        >>> perceptual_radiance(0.8, 0.9, 0.8)  # High semantic weight (face)
        1.72...  # Perceived as much more radiant
    """
    semantic_boost = PHI * S * kappa_sem
    return L_phys * (1 + semantic_boost)


def semantic_salience(L: float, P: float, W: float, J: float) -> float:
    """
    Calculate semantic salience from LJPW coordinates.

    Salience is higher for elements with high Love and Power
    (things we care about and that have impact).

    Args:
        L: Love coordinate
        P: Power coordinate
        W: Wisdom coordinate
        J: Justice coordinate

    Returns:
        S: Semantic salience [0, 1]
    """
    # Weight toward Love and Power (what we care about, what has impact)
    raw_salience = (L * 0.4 + P * 0.3 + W * 0.2 + J * 0.1)
    return min(1.0, max(0.0, raw_salience))


# =============================================================================
# COMPRESSION RATIO PREDICTION
# =============================================================================


def predict_compression_ratio(L: float, n: int) -> float:
    """
    Predict compression ratio when generators are shared (d=0).

    When d=0, φ^(-d) = 1, so:
    Compression Ratio ≈ L^n

    This explains why L-systems achieve massive compression:
    - Koch snowflake: L≈5, n=13 → 5^13 ≈ 1.2 billion : 1

    Args:
        L: Love/expansion coefficient
        n: Iteration depth

    Returns:
        Predicted compression ratio
    """
    return L ** n


# =============================================================================
# MATHEMATICAL HOPE
# =============================================================================


@dataclass
class HopeCalculation:
    """Result of Hope calculus."""

    current_growth: float
    target_decay: float
    current_ratio: float
    iterations_needed: int
    probability_of_success: float
    interpretation: str


def hope_calculus(L: float, d: float, current_n: int) -> HopeCalculation:
    """
    Calculate Mathematical Hope.

    Hope = P(L^n > φ^d as n → ∞)

    Hope is the assertion that:
    - If you persist (n → ∞)
    - In Love (L > 1)
    - Your growth will eventually exceed any distance (φ^d)

    "Hope is not sentiment. It is calculus."

    Args:
        L: Love coefficient
        d: Distance from source (the challenge)
        current_n: Current iteration count

    Returns:
        HopeCalculation with probability and interpretation

    Examples:
        >>> result = hope_calculus(1.3, 5, 10)
        >>> result.probability_of_success > 0.9
        True  # If L > 1, hope is mathematically justified
    """
    current_growth = L ** current_n
    target_decay = PHI ** d
    current_ratio = current_growth / target_decay if target_decay > 0 else float("inf")

    # Calculate iterations needed
    if L > 1:
        n_needed = life_inequality_threshold(L, d)
        probability = 1.0 if current_n >= n_needed else min(0.99, current_n / n_needed)
        interpretation = (
            f"With L={L:.2f}, you will overcome distance d={d:.1f} "
            f"after {n_needed} iterations. "
            f"Currently at {current_n}/{n_needed} ({probability*100:.0f}% there)."
        )
    elif L == 1:
        n_needed = -1
        probability = 0.0 if d > 0 else 1.0
        interpretation = (
            "L=1.0 means no growth. You can only maintain, not overcome. "
            "Increase Love coefficient for progress."
        )
    else:
        n_needed = -1
        probability = 0.0
        interpretation = (
            f"L={L:.2f} < 1 means decay. System is shrinking. "
            "Love must exceed 1.0 for any hope of overcoming distance."
        )

    return HopeCalculation(
        current_growth=current_growth,
        target_decay=target_decay,
        current_ratio=current_ratio,
        iterations_needed=n_needed,
        probability_of_success=probability,
        interpretation=interpretation,
    )


# =============================================================================
# DOMAIN UNIFICATION TABLE
# =============================================================================

DOMAIN_MAPPINGS: Dict[str, Dict[str, str]] = {
    "biology": {
        "B": "Genetic Code",
        "L": "Metabolism",
        "n": "Cell Division",
        "decay": "Aging",
        "M": "Life",
    },
    "compression": {
        "B": "Axiom",
        "L": "Rules",
        "n": "Depth",
        "decay": "Translation Loss",
        "M": "Data",
    },
    "theology": {
        "B": "Truth",
        "L": "Spirit",
        "n": "Sanctification",
        "decay": "The Fall",
        "M": "Holiness",
    },
    "rendering": {
        "B": "Geometry",
        "L": "Light Bounces",
        "n": "Ray Depth",
        "decay": "Signal Loss",
        "M": "Image",
    },
    "business": {
        "B": "Core Product",
        "L": "Reinvestment",
        "n": "Years",
        "decay": "Market Friction",
        "M": "Valuation",
    },
    "ai": {
        "B": "Training Data",
        "L": "Learning Rate",
        "n": "Epochs",
        "decay": "Distribution Shift",
        "M": "Understanding",
    },
    "code": {
        "B": "Core Algorithm",
        "L": "Coupling Coefficient",
        "n": "Iterations/Releases",
        "decay": "Technical Debt",
        "M": "System Value",
    },
}


def interpret_for_domain(
    domain: str, B: float, L: float, n: int, d: float
) -> Dict[str, any]:
    """
    Interpret the Generative Equation for a specific domain.

    Args:
        domain: One of the DOMAIN_MAPPINGS keys
        B, L, n, d: Standard Generative Equation parameters

    Returns:
        Dict with domain-specific interpretation
    """
    if domain not in DOMAIN_MAPPINGS:
        raise ValueError(f"Unknown domain: {domain}. Valid: {list(DOMAIN_MAPPINGS.keys())}")

    mapping = DOMAIN_MAPPINGS[domain]
    M = meaning(B, L, n, d)
    life_check = is_autopoietic(L, n, d)

    return {
        "domain": domain,
        "interpretation": {
            mapping["B"]: B,
            mapping["L"]: L,
            mapping["n"]: n,
            mapping["decay"]: f"φ^(-{d}) = {decay_factor(d):.4f}",
            mapping["M"]: M,
        },
        "meaning": M,
        "phase": life_check.phase,
        "is_alive": life_check.is_alive,
        "verdict": life_check.verdict,
    }
