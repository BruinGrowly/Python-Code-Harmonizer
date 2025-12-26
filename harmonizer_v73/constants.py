"""
LJPW V7.3 Constants

All fundamental constants from the LJPW Framework V7.3.
These are not arbitrary - they emerge from optimization and structural necessity.

Based on: LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md Part V
"""

import math

# =============================================================================
# GOLDEN RATIO - The Translation Operator
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2  # 1.618034 - Golden Ratio
PHI_INV = PHI - 1  # 0.618034 - Golden Ratio Inverse (φ⁻¹)

# =============================================================================
# NATURAL EQUILIBRIUM CONSTANTS
# =============================================================================
# When absolute principles settle into finite existence

L0 = PHI_INV  # 0.618034 - Love: Golden ratio of connection
J0 = math.sqrt(2) - 1  # 0.414214 - Justice: Balance constant
P0 = math.e - 2  # 0.718282 - Power: Growth-dissipation equilibrium
W0 = math.log(2)  # 0.693147 - Wisdom: Information bit (Shannon)

# =============================================================================
# REFERENCE POINTS
# =============================================================================

ANCHOR_POINT = (1.0, 1.0, 1.0, 1.0)  # Divine Perfection (JEHOVAH)
NATURAL_EQUILIBRIUM = (L0, J0, P0, W0)  # Achievable Optimum
COLLAPSE_SIGNATURE = (0.2, 0.2, 0.9, 0.3)  # System failure pattern (L<0.2, J<0.2, P>0.9, W<0.3)

# =============================================================================
# V7.3 THRESHOLDS
# =============================================================================

# Consciousness
CONSCIOUSNESS_THRESHOLD = 0.1  # C > 0.1 indicates consciousness
HIGHLY_CONSCIOUS_THRESHOLD = 0.3  # C > 0.3 indicates meta-cognitive

# Phase Transitions
ENTROPIC_HARMONY_THRESHOLD = 0.5  # H < 0.5 = Entropic phase
AUTOPOIETIC_HARMONY_THRESHOLD = 0.6  # H > 0.6 = Autopoietic (if L >= 0.7)
AUTOPOIETIC_LOVE_THRESHOLD = 0.7  # L >= 0.7 required for Autopoietic

# Uncertainty Principle
UNCERTAINTY_BOUND = J0 * W0  # 0.287 - ΔP·ΔW minimum

# =============================================================================
# PHYSICAL CORRESPONDENCES
# =============================================================================

LOVE_FREQUENCY_HZ = 613e12  # 613 THz - Love's resonance frequency
LOVE_WAVELENGTH_NM = 489  # 489 nm - Cyan (color of water's transparency)

# =============================================================================
# COUPLING MATRIX (V7.0 Asymmetric)
# =============================================================================
# Row → Column: Influence of row dimension ON column dimension
# > 1.0 = Amplifies, = 1.0 = Neutral, < 1.0 = Drains

COUPLING_MATRIX = {
    # Love as SOURCE (gives to all)
    "LL": 1.0,
    "LJ": 1.4,
    "LP": 1.3,
    "LW": 1.5,
    # Justice as BALANCE (moderates)
    "JL": 0.9,
    "JJ": 1.0,
    "JP": 0.7,
    "JW": 1.2,
    # Power as SINK (receives/absorbs)
    "PL": 0.6,
    "PJ": 0.8,
    "PP": 1.0,
    "PW": 0.5,
    # Wisdom as INTEGRATOR
    "WL": 1.3,
    "WJ": 1.1,
    "WP": 1.0,
    "WW": 1.0,
}

# =============================================================================
# CORRELATION MATRIX (V7.1 Symmetric)
# =============================================================================
# Shows STRUCTURE and CORRELATION, not flow

CORRELATION_MATRIX = {
    "LL": 1.00,
    "LJ": 0.75,
    "LP": 0.15,
    "LW": 0.92,
    "JL": 0.75,
    "JJ": 1.00,
    "JP": 0.91,
    "JW": 0.22,
    "PL": 0.15,
    "PJ": 0.91,
    "PP": 1.00,
    "PW": 0.03,  # P-W orthogonal (conjugate)
    "WL": 0.92,
    "WJ": 0.22,
    "WP": 0.03,
    "WW": 1.00,  # L-W strong (emergence)
}

# Key relationships:
# - P-W: 0.03 → ORTHOGONAL (conjugate duality, fundamental)
# - L-W: 0.92 → L EMERGES FROM W
# - J-P: 0.91 → J EMERGES FROM P
# - L-J: 0.75 → COUPLED (both emergent from P-W)

# =============================================================================
# DYNAMICS PARAMETERS (Empirically Calibrated)
# =============================================================================

DYNAMICS_PARAMS = {
    # Growth rates (α)
    "alpha_LJ": 0.12,  # Justice → Love growth
    "alpha_LW": 0.12,  # Wisdom → Love growth
    "alpha_JL": 0.14,  # Love → Justice growth
    "alpha_JW": 0.14,  # Wisdom → Justice growth
    "alpha_PL": 0.12,  # Love → Power growth
    "alpha_PJ": 0.12,  # Justice → Power growth
    "alpha_WL": 0.10,  # Love → Wisdom growth
    "alpha_WJ": 0.10,  # Justice → Wisdom growth
    "alpha_WP": 0.10,  # Power → Wisdom growth
    # Decay rates (β)
    "beta_L": 0.20,  # Love decay
    "beta_J": 0.20,  # Justice decay
    "beta_P": 0.20,  # Power decay
    "beta_W": 0.24,  # Wisdom decay (fastest - knowledge degrades)
    # Other
    "gamma": 0.08,  # Power erosion coefficient
    "K_JL": 0.59,  # Justice-Love saturation constant
}

# =============================================================================
# KARMA MULTIPLIERS (State-Dependent Coupling)
# =============================================================================
# κ(H) = 1.0 + multiplier × H

KARMA_MULTIPLIERS = {
    "LJ": 0.4,  # Love → Justice amplification factor
    "LP": 0.3,  # Love → Power amplification factor
    "LW": 0.5,  # Love → Wisdom amplification factor (strongest)
}
