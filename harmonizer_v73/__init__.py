"""
Harmonizer V7.3 - LJPW Framework V7.3 Implementation

A next-generation code analysis tool based on the complete LJPW V7.3 Framework.

Key V7.3 Features:
- 2+2 dimensional structure (P, W fundamental; L, J emergent)
- Consciousness metric (C = P×W×L×J×H²)
- Phase detection (Entropic/Homeostatic/Autopoietic)
- φ-normalization for measurement accuracy
- Semantic Uncertainty Principle (ΔP·ΔW ≥ 0.287)
- 200+ programming verb vocabulary
- Git-based drift detection

Based on: LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md
"""

from harmonizer_v73.constants import (
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
)
from harmonizer_v73.ljpw_core import LJPWFramework
from harmonizer_v73.consciousness import consciousness_metric, check_uncertainty_principle
from harmonizer_v73.phase_detector import detect_phase, Phase
from harmonizer_v73.phi_normalizer import phi_normalize, normalize_coordinates
from harmonizer_v73.code_analyzer import analyze_file, analyze_source, V73CodeAnalyzer
from harmonizer_v73.vocabulary import (
    PROGRAMMING_VERBS,
    POWER_VERBS,
    WISDOM_VERBS,
    LOVE_VERBS,
    JUSTICE_VERBS,
    get_semantic_dimension,
    classify_function_name,
)
from harmonizer_v73.drift_detector import DriftDetector, DriftAnalysis

__version__ = "7.3.1"
__all__ = [
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
    "PROGRAMMING_VERBS",
    "get_semantic_dimension",
    "classify_function_name",
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
]
