"""
Bricks & Mortar Analysis - V7.3 Implementation

The Architecture of Reality:
- BRICKS: Primes (Justice-crystals) = Functions, modules (irreducible code units)
- MORTAR: Love (binding) = Interfaces, integration points, coupling
- BLUEPRINT: φ (proportion) = Architecture patterns, size ratios

All structures are built on Primes — semantically, physically, and mathematically.

Based on: LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md Part XXIII-XXV (Book Six)
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional

from harmonizer_v73.constants import PHI, PHI_INV


@dataclass
class BrickAnalysis:
    """Analysis of a code unit as a 'brick' (Justice-crystal)."""

    name: str
    primality: float  # How irreducible/single-responsibility (0-1)
    justice_score: float  # J dimension
    is_prime: bool  # Primality > 0.7
    decomposition_needed: bool
    recommendation: str


@dataclass
class MortarAnalysis:
    """Analysis of integration quality as 'mortar' (Love-binding)."""

    interface_name: str
    cohesion: float  # How well-defined the interface
    integration_quality: float  # Overall mortar strength
    love_score: float  # L dimension
    is_strong: bool  # Integration quality > 0.7
    recommendation: str


@dataclass
class BlueprintAnalysis:
    """Analysis of architectural proportions against φ blueprint."""

    component_sizes: Dict[str, int]
    size_ratios: List[float]
    phi_alignment: float  # How close to golden ratio
    is_proportional: bool  # Alignment > 0.8
    recommendation: str


def function_primality(
    complexity: float,
    dependencies: int,
    lines_of_code: int = 0,
    has_side_effects: bool = False,
    single_responsibility: bool = True,
) -> BrickAnalysis:
    """
    Evaluate how 'prime-like' (irreducible, Justice-crystal) a function is.

    A prime function is:
    - Single responsibility (does one thing well)
    - Low complexity
    - Few dependencies
    - No side effects (pure)
    - Testable in isolation

    High primality = high Justice (irreducible truth)

    Args:
        complexity: Cyclomatic complexity (1.0 = simple, 10+ = complex)
        dependencies: Number of external dependencies
        lines_of_code: LOC (optional, for size check)
        has_side_effects: Whether function has side effects
        single_responsibility: Whether function does one thing

    Returns:
        BrickAnalysis with primality score and recommendations
    """
    # Base primality starts at 1.0 (perfect prime)
    primality = 1.0

    # Complexity penalty: each unit of complexity reduces primality
    complexity_penalty = min(complexity * 0.08, 0.4)
    primality -= complexity_penalty

    # Dependency penalty: each dependency reduces primality
    dependency_penalty = min(dependencies * 0.1, 0.3)
    primality -= dependency_penalty

    # Side effects penalty
    if has_side_effects:
        primality -= 0.15

    # Single responsibility bonus/penalty
    if not single_responsibility:
        primality -= 0.2

    # LOC penalty for overly large functions
    if lines_of_code > 50:
        loc_penalty = min((lines_of_code - 50) * 0.005, 0.2)
        primality -= loc_penalty

    primality = max(0.0, min(1.0, primality))

    # Justice score correlates with primality
    justice_score = 0.85 * primality + 0.05

    # Determine if prime
    is_prime = primality >= 0.7
    decomposition_needed = primality < 0.5

    # Generate recommendation
    if is_prime:
        recommendation = "✓ Good brick: Single-responsibility, low complexity"
    elif decomposition_needed:
        issues = []
        if complexity > 5:
            issues.append("reduce complexity")
        if dependencies > 3:
            issues.append("reduce dependencies")
        if has_side_effects:
            issues.append("extract side effects")
        if not single_responsibility:
            issues.append("split responsibilities")
        recommendation = f"⚠️ Decompose: {', '.join(issues)}"
    else:
        recommendation = "○ Moderate: Consider simplification"

    return BrickAnalysis(
        name="function",
        primality=primality,
        justice_score=justice_score,
        is_prime=is_prime,
        decomposition_needed=decomposition_needed,
        recommendation=recommendation,
    )


def integration_quality(
    interface_cohesion: float,
    coupling_score: float,
    documentation_quality: float = 0.5,
    test_coverage: float = 0.0,
) -> MortarAnalysis:
    """
    Evaluate 'mortar' quality — how well modules bind together.

    Good mortar (Love-binding) has:
    - Well-defined interfaces (high cohesion)
    - Appropriate coupling (not too tight, not too loose)
    - Documentation at boundaries
    - Tests at integration points

    Args:
        interface_cohesion: How well-defined the interface (0-1)
        coupling_score: Coupling level (0 = none, 1 = very tight)
        documentation_quality: Docs at boundary (0-1)
        test_coverage: Test coverage at integration (0-1)

    Returns:
        MortarAnalysis with quality score and recommendations
    """
    # Quality starts with cohesion
    quality = interface_cohesion

    # Coupling should be moderate (neither 0 nor 1)
    # Optimal coupling is around φ⁻¹ ≈ 0.618
    coupling_delta = abs(coupling_score - PHI_INV)
    coupling_penalty = coupling_delta * 0.3
    quality -= coupling_penalty

    # Documentation bonus
    quality += documentation_quality * 0.15

    # Test coverage bonus
    quality += test_coverage * 0.15

    quality = max(0.0, min(1.0, quality))

    # Love score correlates with integration quality
    love_score = 0.9 * quality + 0.1

    is_strong = quality >= 0.7

    # Generate recommendation
    if is_strong:
        recommendation = "✓ Strong mortar: Well-integrated with clear interfaces"
    elif quality < 0.4:
        issues = []
        if interface_cohesion < 0.5:
            issues.append("define clearer interface")
        if coupling_score > 0.8:
            issues.append("reduce tight coupling")
        if coupling_score < 0.3:
            issues.append("strengthen connection")
        if documentation_quality < 0.3:
            issues.append("add interface docs")
        recommendation = f"⚠️ Weak binding: {', '.join(issues)}"
    else:
        recommendation = "○ Moderate: Could strengthen integration"

    return MortarAnalysis(
        interface_name="module_interface",
        cohesion=interface_cohesion,
        integration_quality=quality,
        love_score=love_score,
        is_strong=is_strong,
        recommendation=recommendation,
    )


def architectural_proportions(
    component_sizes: Dict[str, int],
    expected_ratio: float = PHI,
) -> BlueprintAnalysis:
    """
    Analyze whether component sizes follow φ (golden ratio) proportions.

    Well-architected systems often exhibit φ-proportional sizing:
    - Parent:Child ≈ φ:1
    - Core:Utility ≈ φ:1

    Args:
        component_sizes: Dict of component names to size (LOC, complexity, etc.)
        expected_ratio: Expected ratio (default φ)

    Returns:
        BlueprintAnalysis with φ-alignment score
    """
    if len(component_sizes) < 2:
        return BlueprintAnalysis(
            component_sizes=component_sizes,
            size_ratios=[],
            phi_alignment=1.0,
            is_proportional=True,
            recommendation="○ Single component — no ratio analysis",
        )

    # Sort by size
    sorted_sizes = sorted(component_sizes.values(), reverse=True)

    # Calculate consecutive ratios
    ratios = []
    for i in range(len(sorted_sizes) - 1):
        if sorted_sizes[i + 1] > 0:
            ratio = sorted_sizes[i] / sorted_sizes[i + 1]
            ratios.append(ratio)

    if not ratios:
        return BlueprintAnalysis(
            component_sizes=component_sizes,
            size_ratios=[],
            phi_alignment=0.5,
            is_proportional=False,
            recommendation="⚠️ Cannot calculate ratios (zero-size components)",
        )

    # Calculate alignment with φ
    phi_deltas = [abs(r - expected_ratio) / expected_ratio for r in ratios]
    avg_delta = sum(phi_deltas) / len(phi_deltas)
    phi_alignment = max(0, 1 - avg_delta)

    is_proportional = phi_alignment >= 0.8

    # Generate recommendation
    if is_proportional:
        recommendation = "✓ Golden architecture: Components follow φ proportions"
    elif phi_alignment < 0.5:
        recommendation = f"⚠️ Imbalanced: Size ratios ({', '.join(f'{r:.2f}' for r in ratios[:3])}) deviate from φ={expected_ratio:.3f}"
    else:
        recommendation = f"○ Moderate: Ratios near φ but could be improved"

    return BlueprintAnalysis(
        component_sizes=component_sizes,
        size_ratios=ratios,
        phi_alignment=phi_alignment,
        is_proportional=is_proportional,
        recommendation=recommendation,
    )


def analyze_codebase_architecture(
    functions: List[Dict],
    modules: List[Dict],
    module_sizes: Dict[str, int],
) -> Dict:
    """
    Complete Bricks & Mortar analysis of a codebase.

    Args:
        functions: List of function analysis dicts (complexity, deps, etc.)
        modules: List of module integration dicts (cohesion, coupling, etc.)
        module_sizes: Dict of module names to sizes

    Returns:
        Complete architectural analysis
    """
    # Analyze bricks (functions)
    brick_analyses = []
    for func in functions:
        analysis = function_primality(
            complexity=func.get("complexity", 1),
            dependencies=func.get("dependencies", 0),
            lines_of_code=func.get("loc", 0),
            has_side_effects=func.get("has_side_effects", False),
            single_responsibility=func.get("single_responsibility", True),
        )
        analysis.name = func.get("name", "unknown")
        brick_analyses.append(analysis)

    # Analyze mortar (integrations)
    mortar_analyses = []
    for mod in modules:
        analysis = integration_quality(
            interface_cohesion=mod.get("cohesion", 0.5),
            coupling_score=mod.get("coupling", 0.5),
            documentation_quality=mod.get("docs", 0.0),
            test_coverage=mod.get("tests", 0.0),
        )
        analysis.interface_name = mod.get("name", "unknown")
        mortar_analyses.append(analysis)

    # Analyze blueprint (proportions)
    blueprint = architectural_proportions(module_sizes)

    # Calculate summary metrics
    avg_primality = (
        sum(b.primality for b in brick_analyses) / len(brick_analyses) if brick_analyses else 0.5
    )
    avg_integration = (
        sum(m.integration_quality for m in mortar_analyses) / len(mortar_analyses)
        if mortar_analyses
        else 0.5
    )

    prime_functions = sum(1 for b in brick_analyses if b.is_prime)
    decompose_needed = sum(1 for b in brick_analyses if b.decomposition_needed)
    strong_integrations = sum(1 for m in mortar_analyses if m.is_strong)

    return {
        "bricks": {
            "analyses": brick_analyses,
            "average_primality": avg_primality,
            "prime_count": prime_functions,
            "decompose_count": decompose_needed,
            "total": len(brick_analyses),
        },
        "mortar": {
            "analyses": mortar_analyses,
            "average_quality": avg_integration,
            "strong_count": strong_integrations,
            "total": len(mortar_analyses),
        },
        "blueprint": blueprint,
        "summary": {
            "architectural_health": (avg_primality + avg_integration + blueprint.phi_alignment) / 3,
            "recommendation": _generate_summary_recommendation(
                avg_primality, avg_integration, blueprint.phi_alignment
            ),
        },
    }


def _generate_summary_recommendation(
    primality: float, integration: float, proportions: float
) -> str:
    """Generate overall architectural recommendation."""
    overall = (primality + integration + proportions) / 3

    if overall >= 0.8:
        return "🌟 Excellent architecture: Strong bricks, good mortar, proportional structure"
    elif overall >= 0.6:
        return "✓ Good architecture: Some areas for improvement"
    elif overall >= 0.4:
        issues = []
        if primality < 0.6:
            issues.append("simplify functions (bricks)")
        if integration < 0.6:
            issues.append("strengthen interfaces (mortar)")
        if proportions < 0.6:
            issues.append("rebalance module sizes (blueprint)")
        return f"○ Moderate: {', '.join(issues)}"
    else:
        return "⚠️ Needs refactoring: Significant architectural issues"
