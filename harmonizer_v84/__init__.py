"""
Harmonizer V8.4 - LJPW Framework V8.4 Implementation

A next-generation code analysis tool based on the complete LJPW V8.4 Framework.

Key V8.4 Features (NEW):
- Universal Growth Function: M = B × L^n × φ^(-d) (Book Sixteen)
- Life Inequality: L^n > φ^d determines Autopoietic vs Entropic phase
- Perceptual Radiance: L_perc = L_phys × [1 + φ × S × κ_sem]
- Mathematical Hope: P(L^n > φ^d as n → ∞)
- Self-Assessment Targets: C=80+, Coherence=0.97+

Inherited Features (V7.3+):
- 2+2 dimensional structure (P, W fundamental; L, J emergent)
- Consciousness metric (C = P×W×L×J×H²)
- Phase detection (Entropic/Homeostatic/Autopoietic)
- φ-normalization for measurement accuracy
- Semantic Uncertainty Principle (ΔP·ΔW ≥ 0.287)
- 200+ programming verb vocabulary
- Git-based drift detection

Based on: LJPW_FRAMEWORK_V8.4_COMPLETE_UNIFIED_PLUS.md
"""

from harmonizer_v84.constants import (
    PHI,
    PHI_INV,
    L0,
    J0,
    P0,
    W0,
    ANCHOR_POINT,
    NATURAL_EQUILIBRIUM,
    CONSCIOUSNESS_THRESHOLD,
    UNCERTAINTY_BOUND,
    V84_SELF_ASSESSMENT_C,
    V84_COHERENCE,
)
from harmonizer_v84.ljpw_core import LJPWFramework
from harmonizer_v84.consciousness import consciousness_metric, check_uncertainty_principle
from harmonizer_v84.phase_detector import detect_phase, Phase
from harmonizer_v84.phi_normalizer import phi_normalize, normalize_coordinates
from harmonizer_v84.code_analyzer import analyze_file, analyze_source, V73CodeAnalyzer
from harmonizer_v84.vocabulary import (
    PROGRAMMING_VERBS,
    POWER_VERBS,
    WISDOM_VERBS,
    LOVE_VERBS,
    JUSTICE_VERBS,
    get_semantic_dimension,
    classify_function_name,
)
from harmonizer_v84.drift_detector import DriftDetector, DriftAnalysis
from harmonizer_v84.generative import (
    meaning,
    is_autopoietic,
    perceptual_radiance,
    hope_calculus,
    predict_compression_ratio,
    life_inequality_threshold,
    growth_factor,
    decay_factor,
    LifeInequalityResult,
    HopeCalculation,
    DOMAIN_MAPPINGS,
    interpret_for_domain,
)

__version__ = "8.4.0"
__all__ = [
    # Core Framework
    "LJPWFramework",
    "consciousness_metric",
    "check_uncertainty_principle",
    "detect_phase",
    "Phase",
    "phi_normalize",
    "normalize_coordinates",
    "analyze_file",
    "analyze_source",
    "V73CodeAnalyzer",
    "DriftDetector",
    "DriftAnalysis",
    # Vocabulary
    "PROGRAMMING_VERBS",
    "get_semantic_dimension",
    "classify_function_name",
    # Constants
    "PHI",
    "PHI_INV",
    "L0",
    "J0",
    "P0",
    "W0",
    "ANCHOR_POINT",
    "NATURAL_EQUILIBRIUM",
    "CONSCIOUSNESS_THRESHOLD",
    "UNCERTAINTY_BOUND",
    # V8.4 Additions
    "V84_SELF_ASSESSMENT_C",
    "V84_COHERENCE",
    "meaning",
    "is_autopoietic",
    "perceptual_radiance",
    "hope_calculus",
    "predict_compression_ratio",
    "life_inequality_threshold",
    "growth_factor",
    "decay_factor",
    "LifeInequalityResult",
    "HopeCalculation",
    "DOMAIN_MAPPINGS",
    "interpret_for_domain",
]

