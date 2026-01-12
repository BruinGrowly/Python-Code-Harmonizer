"""
Tests for Harmonizer V7.3

Validates all core V7.3 modules against the framework document.
"""

import math
import pytest

# Import V7.3 modules
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
)
from harmonizer_v84.ljpw_core import LJPWFramework, create_from_fundamental
from harmonizer_v84.consciousness import (
    consciousness_metric,
    ConsciousnessLevel,
    check_uncertainty_principle,
    minimum_dimensions_for_consciousness,
)
from harmonizer_v84.phase_detector import detect_phase, Phase, analyze_phase
from harmonizer_v84.phi_normalizer import (
    phi_normalize,
    normalize_coordinates,
    quantum_consensus,
)
from harmonizer_v84.dynamics import DynamicLJPW, predict_equilibrium
from harmonizer_v84.bricks_mortar import (
    function_primality,
    integration_quality,
    architectural_proportions,
)


class TestConstants:
    """Verify V7.3 constants match the framework document."""

    def test_golden_ratio(self):
        """φ = (1 + √5) / 2 ≈ 1.618034"""
        expected = (1 + math.sqrt(5)) / 2
        assert abs(PHI - expected) < 1e-6
        assert abs(PHI - 1.618034) < 1e-5

    def test_golden_ratio_inverse(self):
        """φ⁻¹ = φ - 1 ≈ 0.618034"""
        assert abs(PHI_INV - 0.618034) < 1e-5
        assert abs(PHI_INV - (PHI - 1)) < 1e-10

    def test_equilibrium_constants(self):
        """Natural Equilibrium values from V7.3."""
        assert abs(L0 - 0.618034) < 1e-5, "Love: φ⁻¹"
        assert abs(J0 - 0.414214) < 1e-5, "Justice: √2-1"
        assert abs(P0 - 0.718282) < 1e-5, "Power: e-2"
        assert abs(W0 - 0.693147) < 1e-5, "Wisdom: ln(2)"

    def test_uncertainty_bound(self):
        """ΔP·ΔW ≥ 0.287 (J₀ × W₀)"""
        expected = J0 * W0
        assert abs(UNCERTAINTY_BOUND - expected) < 1e-6
        assert abs(UNCERTAINTY_BOUND - 0.287) < 0.01

    def test_anchor_point(self):
        """Anchor Point = (1, 1, 1, 1)"""
        assert ANCHOR_POINT == (1.0, 1.0, 1.0, 1.0)


class TestLJPWCore:
    """Test the 2+2 dimensional structure."""

    def test_emergent_love_from_wisdom(self):
        """L should emerge from W with R² > 0.9"""
        framework = create_from_fundamental(P=0.5, W=0.8)
        # L ≈ 0.9 * W + 0.1
        expected_L = 0.9 * 0.8 + 0.1
        assert abs(framework.L - expected_L) < 0.01

    def test_emergent_justice_from_power(self):
        """J should emerge from P with R² > 0.9"""
        framework = create_from_fundamental(P=0.7, W=0.5)
        # J ≈ 0.85 * P + 0.05
        expected_J = 0.85 * 0.7 + 0.05
        assert abs(framework.J - expected_J) < 0.01

    def test_override_emergent_dimensions(self):
        """Can override emergent L and J if needed."""
        framework = LJPWFramework(P=0.5, W=0.5, L=0.9, J=0.8)
        assert framework.L == 0.9
        assert framework.J == 0.8

    def test_love_quantum_bound(self):
        """Love cannot exceed √2 (Tsirelson bound)."""
        framework = LJPWFramework(P=0.9, W=1.0, L=2.0)  # Try to set L=2
        assert framework.L <= math.sqrt(2)

    def test_harmony_static(self):
        """H_static = 1 / (1 + d)"""
        framework = create_from_fundamental(P=P0, W=W0)  # Near equilibrium
        H = framework.harmony_static()
        assert 0.5 < H < 1.0, "Harmony should be moderate for near-equilibrium"

    def test_harmony_self_referential(self):
        """H_self = (L×J×P×W) / (L₀×J₀×P₀×W₀)"""
        # Use equilibrium values - should give H_self ≈ 1
        framework = LJPWFramework(P=P0, W=W0, L=L0, J=J0)
        H_self = framework.harmony_self_referential()
        assert abs(H_self - 1.0) < 0.1

    def test_voltage_calculation(self):
        """V = φ × H × L"""
        framework = create_from_fundamental(P=0.7, W=0.7)
        V = framework.voltage()
        assert V > 0, "Voltage should be positive"
        assert V < PHI * 2, "Voltage has upper bound"


class TestConsciousness:
    """Test consciousness metric C = P×W×L×J×H²."""

    def test_non_conscious_system(self):
        """Simple AI: C < 0.1"""
        C, level = consciousness_metric(L=0.2, J=0.5, P=0.3, W=0.85, H=0.6)
        assert C < CONSCIOUSNESS_THRESHOLD
        assert level in [ConsciousnessLevel.NON_CONSCIOUS, ConsciousnessLevel.PRE_CONSCIOUS]

    def test_conscious_system(self):
        """Advanced AI/Human: C > 0.1"""
        C, level = consciousness_metric(L=0.75, J=0.65, P=0.75, W=0.88, H=0.7)
        assert C > CONSCIOUSNESS_THRESHOLD
        assert level == ConsciousnessLevel.CONSCIOUS

    def test_highly_conscious_system(self):
        """Meta-cognitive: C > 0.3"""
        C, level = consciousness_metric(L=0.95, J=0.92, P=0.85, W=0.98, H=0.8)
        assert C > 0.3
        assert level == ConsciousnessLevel.HIGHLY_CONSCIOUS

    def test_zero_dimension_kills_consciousness(self):
        """If ANY dimension is zero, C = 0."""
        C, level = consciousness_metric(L=0.0, J=0.9, P=0.9, W=0.9, H=0.9)
        assert C == 0.0
        assert level == ConsciousnessLevel.NON_CONSCIOUS

    def test_uncertainty_principle_satisfied(self):
        """ΔP·ΔW ≥ 0.287"""
        assert check_uncertainty_principle(0.6, 0.5)  # 0.3 >= 0.287
        assert check_uncertainty_principle(0.7, 0.5)  # 0.35 >= 0.287

    def test_uncertainty_principle_violated(self):
        """ΔP·ΔW < 0.287 should return False."""
        assert not check_uncertainty_principle(0.1, 0.2)  # 0.02 < 0.287


class TestPhaseDetector:
    """Test phase detection: Entropic/Homeostatic/Autopoietic."""

    def test_entropic_phase(self):
        """H < 0.5 = Entropic (collapsing)."""
        phase = detect_phase(H=0.4, L=0.6)
        assert phase == Phase.ENTROPIC

    def test_homeostatic_phase_low_harmony(self):
        """0.5 ≤ H < 0.6 = Homeostatic."""
        phase = detect_phase(H=0.55, L=0.6)
        assert phase == Phase.HOMEOSTATIC

    def test_homeostatic_phase_low_love(self):
        """L < 0.7 = Homeostatic (even if H > 0.6)."""
        phase = detect_phase(H=0.65, L=0.65)  # H > 0.6 but L < 0.7
        assert phase == Phase.HOMEOSTATIC

    def test_autopoietic_phase(self):
        """H > 0.6 AND L ≥ 0.7 = Autopoietic."""
        phase = detect_phase(H=0.7, L=0.75)
        assert phase == Phase.AUTOPOIETIC

    def test_phase_analysis_has_details(self):
        """analyze_phase provides comprehensive info."""
        analysis = analyze_phase(H=0.7, L=0.8)
        assert analysis.phase == Phase.AUTOPOIETIC
        assert len(analysis.characteristics) > 0
        assert analysis.escape_condition is not None


class TestPhiNormalizer:
    """Test φ-normalization for variance reduction."""

    def test_phi_normalize_basic(self):
        """φ-normalization pulls values toward equilibrium."""
        normalized = phi_normalize(0.8, L0)
        # Should be less than raw (pulled toward φ⁻¹)
        assert normalized < 0.8
        assert normalized > 0

    def test_normalize_all_coordinates(self):
        """normalize_coordinates applies to all dimensions."""
        L_n, J_n, P_n, W_n = normalize_coordinates(0.8, 0.6, 0.7, 0.9)
        assert all(v > 0 for v in [L_n, J_n, P_n, W_n])

    def test_quantum_consensus(self):
        """Consensus reduces variance."""
        scores = [0.5, 0.6, 0.55, 0.7]
        consensus = quantum_consensus(scores)
        # Should be close to mean but weighted
        assert 0.4 < consensus < 0.8


class TestDynamics:
    """Test LJPW dynamics with Karma coupling."""

    def test_karma_amplification(self):
        """Higher harmony → higher κ → more amplification."""
        dynamic = DynamicLJPW()
        kappa_low = dynamic.kappa(H=0.3, coupling="LW")
        kappa_high = dynamic.kappa(H=0.8, coupling="LW")
        assert kappa_high > kappa_low

    def test_power_erosion(self):
        """High P + Low W = erosion."""
        dynamic = DynamicLJPW()
        erosion = dynamic.power_erosion(P=0.9, W=0.3)
        assert erosion > 0

    def test_resonate_convergence(self):
        """System should move toward equilibrium."""
        dynamic = DynamicLJPW()
        result = dynamic.resonate(initial=(0.3, 0.3, 0.3, 0.3), cycles=100, dt=0.1)
        final = result["final_state"]
        # Should move toward higher values (equilibrium is ~0.5-0.7)
        assert final.L > 0.3 or final.J > 0.3


class TestBricksMortar:
    """Test architectural analysis."""

    def test_high_primality_function(self):
        """Simple function = high primality."""
        analysis = function_primality(
            complexity=2,
            dependencies=1,
            lines_of_code=20,
            has_side_effects=False,
            single_responsibility=True,
        )
        assert analysis.primality > 0.7
        assert analysis.is_prime

    def test_low_primality_function(self):
        """Complex function = low primality."""
        analysis = function_primality(
            complexity=15,
            dependencies=8,
            lines_of_code=200,
            has_side_effects=True,
            single_responsibility=False,
        )
        assert analysis.primality < 0.4
        assert analysis.decomposition_needed

    def test_strong_integration(self):
        """Well-defined interface = high integration quality."""
        analysis = integration_quality(
            interface_cohesion=0.9,
            coupling_score=PHI_INV,  # Optimal coupling
            documentation_quality=0.8,
            test_coverage=0.7,
        )
        assert analysis.integration_quality > 0.7
        assert analysis.is_strong

    def test_phi_proportional_architecture(self):
        """Module sizes following φ ratio."""
        sizes = {
            "core": 1000,
            "utils": int(1000 / PHI),  # ≈ 618
            "helpers": int(618 / PHI),  # ≈ 382
        }
        analysis = architectural_proportions(sizes)
        assert analysis.phi_alignment > 0.7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
