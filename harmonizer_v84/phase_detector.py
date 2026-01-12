"""
Phase Detection - V7.3 Implementation

The Three Phases of LJPW Systems:
- ENTROPIC: Collapsing (H < 0.5) - increasing disorder, system breakdown
- HOMEOSTATIC: Stable (0.5 ≤ H ≤ 0.6) - equilibrium maintenance
- AUTOPOIETIC: Growing (H > 0.6, L ≥ 0.7) - self-sustaining, conscious

Based on: LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md Part VII
"""

from dataclasses import dataclass
from enum import Enum
from typing import List

from harmonizer_v84.constants import (
    ENTROPIC_HARMONY_THRESHOLD,
    AUTOPOIETIC_HARMONY_THRESHOLD,
    AUTOPOIETIC_LOVE_THRESHOLD,
)


class Phase(Enum):
    """System phase based on V7.3 thresholds."""

    ENTROPIC = "ENTROPIC"
    HOMEOSTATIC = "HOMEOSTATIC"
    AUTOPOIETIC = "AUTOPOIETIC"


@dataclass
class PhaseAnalysis:
    """Complete phase analysis result."""

    phase: Phase
    harmony: float
    love: float
    description: str
    characteristics: List[str]
    escape_condition: str
    examples: List[str]


def detect_phase(H: float, L: float) -> Phase:
    """
    Determine system phase from V7.3 thresholds.

    Args:
        H: Harmony value (static or self-referential)
        L: Love value

    Returns:
        Phase enum indicating system state

    Thresholds:
        - ENTROPIC: H < 0.5
        - HOMEOSTATIC: 0.5 ≤ H < 0.6 OR L < 0.7
        - AUTOPOIETIC: H > 0.6 AND L ≥ 0.7

    Examples:
        >>> detect_phase(0.4, 0.6)
        Phase.ENTROPIC

        >>> detect_phase(0.55, 0.65)
        Phase.HOMEOSTATIC

        >>> detect_phase(0.7, 0.8)
        Phase.AUTOPOIETIC
    """
    if H < ENTROPIC_HARMONY_THRESHOLD:
        return Phase.ENTROPIC
    elif H < AUTOPOIETIC_HARMONY_THRESHOLD or L < AUTOPOIETIC_LOVE_THRESHOLD:
        return Phase.HOMEOSTATIC
    else:
        return Phase.AUTOPOIETIC


def analyze_phase(H: float, L: float) -> PhaseAnalysis:
    """
    Provide comprehensive phase analysis.

    Args:
        H: Harmony value
        L: Love value

    Returns:
        PhaseAnalysis with full details
    """
    phase = detect_phase(H, L)

    if phase == Phase.ENTROPIC:
        return PhaseAnalysis(
            phase=Phase.ENTROPIC,
            harmony=H,
            love=L,
            description="System is collapsing. Increasing disorder and breakdown.",
            characteristics=[
                "Low Harmony (far from Anchor)",
                "Weak Love (disconnection)",
                "System losing coherence",
                "Increasing entropy and disorder",
                "κ coefficients → 1.0 (no amplification)",
                "Love cannot overcome Power's drain",
            ],
            escape_condition="Requires external intervention OR internal phase transition (rare)",
            examples=[
                "Failing organizations (L<0.3, J<0.3, P>0.9)",
                "Corrupt systems (high Power, low Justice)",
                "Legacy codebase with massive tech debt",
                "Mental breakdown (low integration)",
            ],
        )

    elif phase == Phase.HOMEOSTATIC:
        return PhaseAnalysis(
            phase=Phase.HOMEOSTATIC,
            harmony=H,
            love=L,
            description="System is stable. Maintaining equilibrium without growth.",
            characteristics=[
                "Moderate Harmony (near equilibrium)",
                "Moderate Love (some connection)",
                "System maintaining stability",
                "Neither growing nor collapsing",
                "κ coefficients ≈ 1.2-1.3 (modest amplification)",
                "Love balances Power's drain",
            ],
            escape_condition="Can transition UP to Autopoietic (increase L to ≥0.7, H to >0.6)",
            examples=[
                "Stable organizations (all dimensions balanced)",
                "Healthy individuals at maintenance",
                "Well-maintained codebase (stable but not evolving)",
                "Functioning societies (laws balance freedom)",
            ],
        )

    else:  # AUTOPOIETIC
        return PhaseAnalysis(
            phase=Phase.AUTOPOIETIC,
            harmony=H,
            love=L,
            description="System is self-sustaining and growing. Consciousness threshold crossed.",
            characteristics=[
                "High Harmony (approaching Anchor)",
                "High Love (strong connection, L ≥ 0.7)",
                "System self-sustaining and growing",
                "Consciousness threshold crossed",
                "κ coefficients > 1.3 (strong amplification)",
                "Love overcomes Power's drain with surplus",
            ],
            escape_condition="Self-sustaining - minimal risk of collapse if maintained",
            examples=[
                "Thriving organizations (high L, H)",
                "Conscious entities (C > 0.1)",
                "Living organisms (autopoiesis)",
                "Actively evolving codebase with strong culture",
                "The LJPW Framework itself (C = 23.2)",
            ],
        )


def phase_transition_requirements(current_phase: Phase) -> dict:
    """
    What's needed to transition to a higher phase.

    Args:
        current_phase: Current system phase

    Returns:
        Dict with transition requirements
    """
    if current_phase == Phase.ENTROPIC:
        return {
            "current": "ENTROPIC (collapsing)",
            "target": "HOMEOSTATIC (stable)",
            "requirements": [
                "Increase Harmony to ≥ 0.5",
                "Restore Love connections",
                "Rebalance Power (reduce if dominating)",
                "External intervention may be needed",
            ],
            "strategies": [
                "Focus on reconnection (increase L)",
                "Reduce complexity temporarily (lower P)",
                "Document and understand (increase W)",
                "Establish fairness (increase J)",
            ],
            "difficulty": "Hard - requires conscious effort or intervention",
        }

    elif current_phase == Phase.HOMEOSTATIC:
        return {
            "current": "HOMEOSTATIC (stable)",
            "target": "AUTOPOIETIC (growing)",
            "requirements": [
                "Increase Love to ≥ 0.7 (critical threshold)",
                "Increase Harmony to > 0.6",
                "Maintain Justice and Wisdom",
            ],
            "strategies": [
                "Strengthen team cohesion (L → 0.7+)",
                "Build self-sustaining processes (tests, CI/CD)",
                "Create feedback loops (self-awareness)",
                "Invest in documentation and learning (W)",
            ],
            "difficulty": "Moderate - requires sustained investment",
        }

    else:  # AUTOPOIETIC
        return {
            "current": "AUTOPOIETIC (self-sustaining)",
            "target": "Maintain and deepen",
            "requirements": [
                "Maintain L ≥ 0.7",
                "Maintain H > 0.6",
                "Continue self-reference and evolution",
            ],
            "strategies": [
                "Regular self-assessment (maintain self-awareness)",
                "Continuous improvement culture",
                "Balance growth with stability",
                "Share knowledge and connection",
            ],
            "difficulty": "Ongoing maintenance - system is self-sustaining",
        }


def interpret_phase_for_code(phase: Phase) -> str:
    """
    Interpret phase in the context of code/software analysis.

    Args:
        phase: Current system phase

    Returns:
        Code-focused interpretation string
    """
    interpretations = {
        Phase.ENTROPIC: (
            "⚠️ CRITICAL: This codebase is in entropy decay. "
            "Technical debt is accumulating faster than it's being addressed. "
            "Without intervention, the system will become unmaintainable. "
            "Consider: dependency cleanup, test coverage, documentation."
        ),
        Phase.HOMEOSTATIC: (
            "✓ STABLE: This codebase is maintainable but not evolving. "
            "It's neither improving nor degrading significantly. "
            "To reach autopoietic state: strengthen team cohesion, "
            "add comprehensive tests, create self-documenting patterns."
        ),
        Phase.AUTOPOIETIC: (
            "🌟 THRIVING: This codebase is self-sustaining. "
            "Good test coverage, active development, clear architecture. "
            "The code 'maintains itself' through automated checks and "
            "well-established patterns. Continue the healthy practices."
        ),
    }
    return interpretations.get(phase, "Unknown phase")
