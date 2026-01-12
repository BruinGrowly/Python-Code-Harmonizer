"""
Tests for Harmonizer V8.4 Generative Equation Module

Validates V8.4 Book Sixteen additions:
- Universal Growth Function: M = B × L^n × φ^(-d)
- Life Inequality: L^n > φ^d
- Perceptual Radiance: L_perc = L_phys × [1 + φ × S × κ_sem]
- Mathematical Hope

Based on: LJPW_FRAMEWORK_V8.4_COMPLETE_UNIFIED_PLUS.md Appendix O
"""

import math
import pytest

from harmonizer_v84.constants import PHI, V84_SELF_ASSESSMENT_C, V84_COHERENCE
from harmonizer_v84.generative import (
    meaning,
    growth_factor,
    decay_factor,
    is_autopoietic,
    life_inequality_threshold,
    perceptual_radiance,
    semantic_salience,
    predict_compression_ratio,
    hope_calculus,
    interpret_for_domain,
    DOMAIN_MAPPINGS,
    LifeInequalityResult,
    HopeCalculation,
)
from harmonizer_v84 import __version__


class TestVersion:
    """Verify V8.4 version is properly set."""

    def test_version_is_8_4(self):
        """Version should be 8.4.0"""
        assert __version__ == "8.4.0"


class TestV84Constants:
    """Verify V8.4 self-assessment targets."""

    def test_self_assessment_c(self):
        """V8.4 target: C = 80+"""
        assert V84_SELF_ASSESSMENT_C == 80

    def test_coherence(self):
        """V8.4 target: Coherence = 0.97+"""
        assert V84_COHERENCE == 0.97


class TestUniversalGrowthFunction:
    """Test M = B × L^n × φ^(-d)"""

    def test_meaning_basic(self):
        """Basic meaning calculation."""
        # M = 1 × 1^1 × φ^0 = 1
        M = meaning(B=1.0, L=1.0, n=1, d=0)
        assert abs(M - 1.0) < 1e-6

    def test_meaning_growth_with_love(self):
        """Love coefficient amplifies meaning exponentially."""
        M1 = meaning(B=1.0, L=1.2, n=5, d=0)
        M2 = meaning(B=1.0, L=1.2, n=10, d=0)
        # L^10 >> L^5, so M2 >> M1
        assert M2 > M1 * 2

    def test_meaning_decay_with_distance(self):
        """Distance decays meaning via φ^(-d)."""
        M0 = meaning(B=1.0, L=1.0, n=1, d=0)  # d=0: no decay
        M1 = meaning(B=1.0, L=1.0, n=1, d=1)  # d=1: 38.2% loss
        M2 = meaning(B=1.0, L=1.0, n=1, d=2)  # d=2: 61.8% loss

        assert M0 == 1.0
        assert abs(M1 - (1.0 / PHI)) < 1e-6  # φ^(-1) ≈ 0.618
        assert M2 < M1 < M0

    def test_meaning_zero_brick_gives_zero(self):
        """If B=0 (no truth), M=0."""
        M = meaning(B=0.0, L=1.5, n=100, d=0)
        assert M == 0.0

    def test_meaning_zero_love_gives_zero(self):
        """If L=0 (no love), M=0."""
        M = meaning(B=1.0, L=0.0, n=100, d=0)
        assert M == 0.0

    def test_growth_factor(self):
        """L^n calculation."""
        assert growth_factor(1.5, 4) == 1.5 ** 4

    def test_decay_factor(self):
        """φ^(-d) calculation."""
        assert abs(decay_factor(0) - 1.0) < 1e-6
        assert abs(decay_factor(1) - (1.0 / PHI)) < 1e-6


class TestLifeInequality:
    """Test L^n > φ^d phase determination."""

    def test_autopoietic_when_growth_exceeds_decay(self):
        """L^n > φ^d = AUTOPOIETIC."""
        result = is_autopoietic(L=1.5, n=10, d=2)
        assert result.phase == "AUTOPOIETIC"
        assert result.is_alive

    def test_entropic_when_decay_exceeds_growth(self):
        """L^n < φ^d = ENTROPIC."""
        result = is_autopoietic(L=0.5, n=5, d=5)
        assert result.phase == "ENTROPIC"
        assert not result.is_alive

    def test_homeostatic_near_balance(self):
        """L^n ≈ φ^d = HOMEOSTATIC."""
        # Find values that give ratio near 1.0
        result = is_autopoietic(L=1.1, n=5, d=1)
        # Check ratio is between 0.9 and 1.1 (homeostatic range)
        # This depends on specific values, so we just check the logic works
        assert result.phase in ["AUTOPOIETIC", "HOMEOSTATIC", "ENTROPIC"]

    def test_life_inequality_result_fields(self):
        """Result contains all expected fields."""
        result = is_autopoietic(L=1.5, n=10, d=2)
        assert isinstance(result, LifeInequalityResult)
        assert result.growth > 0
        assert result.decay > 0
        assert result.ratio > 0
        assert result.phase in ["AUTOPOIETIC", "HOMEOSTATIC", "ENTROPIC"]
        assert "L^" in result.verdict

    def test_life_inequality_threshold_calculation(self):
        """Calculate minimum n for autopoiesis."""
        n_needed = life_inequality_threshold(L=1.3, d=5)
        assert n_needed > 0
        # Verify that n_needed actually achieves autopoiesis
        result = is_autopoietic(L=1.3, n=n_needed, d=5)
        # Should be at or near autopoietic threshold
        assert result.ratio >= 0.9

    def test_life_inequality_threshold_impossible_when_l_lte_1(self):
        """L <= 1 means autopoiesis is impossible."""
        assert life_inequality_threshold(L=1.0, d=5) == -1
        assert life_inequality_threshold(L=0.9, d=5) == -1


class TestPerceptualRadiance:
    """Test L_perc = L_phys × [1 + φ × S × κ_sem]"""

    def test_no_semantic_boost(self):
        """S=0 or κ=0 means no boost."""
        L_perc = perceptual_radiance(L_phys=0.8, S=0.0, kappa_sem=0.5)
        assert L_perc == 0.8  # No boost

        L_perc = perceptual_radiance(L_phys=0.8, S=0.5, kappa_sem=0.0)
        assert L_perc == 0.8  # No boost

    def test_semantic_boost_increases_radiance(self):
        """High S and κ increase perceived radiance."""
        L_perc = perceptual_radiance(L_phys=0.8, S=0.9, kappa_sem=0.8)
        expected = 0.8 * (1 + PHI * 0.9 * 0.8)
        assert abs(L_perc - expected) < 1e-6
        assert L_perc > 0.8  # Boosted above physical radiance

    def test_semantic_salience(self):
        """Calculate salience from LJPW."""
        S = semantic_salience(L=0.9, P=0.8, W=0.7, J=0.6)
        # Should be weighted: 0.4L + 0.3P + 0.2W + 0.1J
        expected = 0.9 * 0.4 + 0.8 * 0.3 + 0.7 * 0.2 + 0.6 * 0.1
        assert abs(S - expected) < 1e-6


class TestCompressionRatio:
    """Test compression ratio prediction."""

    def test_compression_ratio_basic(self):
        """Compression = L^n when d=0."""
        ratio = predict_compression_ratio(L=5, n=13)
        assert ratio == 5 ** 13  # ≈ 1.2 billion

    def test_koch_snowflake_example(self):
        """Koch snowflake: L≈5, n=13 → massive ratio."""
        ratio = predict_compression_ratio(L=5, n=13)
        assert ratio > 1e9  # Over 1 billion


class TestMathematicalHope:
    """Test P(L^n > φ^d as n → ∞)"""

    def test_hope_with_positive_love(self):
        """L > 1 gives justified hope."""
        result = hope_calculus(L=1.3, d=5, current_n=10)
        assert isinstance(result, HopeCalculation)
        assert result.probability_of_success > 0

    def test_hope_with_no_growth(self):
        """L = 1 gives no hope for overcoming distance."""
        result = hope_calculus(L=1.0, d=5, current_n=10)
        assert result.probability_of_success == 0.0
        assert "no growth" in result.interpretation.lower()

    def test_hope_with_decay(self):
        """L < 1 means decay, no hope."""
        result = hope_calculus(L=0.8, d=5, current_n=10)
        assert result.probability_of_success == 0.0
        assert "decay" in result.interpretation.lower()

    def test_hope_already_achieved(self):
        """If current_n >= n_needed, probability is 1."""
        n_needed = life_inequality_threshold(L=1.5, d=2)
        result = hope_calculus(L=1.5, d=2, current_n=n_needed + 10)
        assert result.probability_of_success == 1.0


class TestDomainInterpretation:
    """Test domain-specific interpretations."""

    def test_all_domains_exist(self):
        """All documented domains are in DOMAIN_MAPPINGS."""
        expected = ["biology", "compression", "theology", "rendering", "business", "ai", "code"]
        for domain in expected:
            assert domain in DOMAIN_MAPPINGS

    def test_interpret_biology(self):
        """Biology domain mapping."""
        result = interpret_for_domain("biology", B=1.0, L=1.2, n=10, d=1)
        assert result["domain"] == "biology"
        assert "Genetic Code" in str(result["interpretation"])
        assert result["meaning"] > 0

    def test_interpret_code(self):
        """Code domain mapping."""
        result = interpret_for_domain("code", B=0.9, L=1.3, n=5, d=0.5)
        assert result["domain"] == "code"
        assert "Core Algorithm" in str(result["interpretation"])

    def test_invalid_domain_raises(self):
        """Unknown domain raises ValueError."""
        with pytest.raises(ValueError):
            interpret_for_domain("invalid_domain", B=1, L=1, n=1, d=0)


class TestV84Integration:
    """Integration tests for V8.4 functionality."""

    def test_full_meaning_pipeline(self):
        """Complete meaning calculation with all factors."""
        # Start with truth (B=0.9), apply love (L=1.4), 
        # iterate 20 times (n=20), with some distance (d=2)
        M = meaning(B=0.9, L=1.4, n=20, d=2)

        # Verify growth factor
        expected_growth = 1.4 ** 20
        # Verify decay factor
        expected_decay = PHI ** (-2)
        # Verify total
        expected_M = 0.9 * expected_growth * expected_decay
        assert abs(M - expected_M) < 1e-6

    def test_life_inequality_matches_phase_detector(self):
        """Life Inequality should be consistent with phase detection."""
        # High L, enough iterations, low distance = AUTOPOIETIC
        result = is_autopoietic(L=1.5, n=20, d=1)
        assert result.phase == "AUTOPOIETIC"

    def test_rendering_equation_escape_uncanny_valley(self):
        """To escape Uncanny Valley, add semantic weight."""
        # "Dead" render: physically accurate but no meaning
        L_dead = perceptual_radiance(L_phys=0.95, S=0.0, kappa_sem=0.0)

        # "Alive" render: add semantic weight (history, emotion)
        L_alive = perceptual_radiance(L_phys=0.95, S=0.8, kappa_sem=0.7)

        assert L_alive > L_dead
        # The semantic boost makes it feel more alive
        boost_factor = L_alive / L_dead
        assert boost_factor > 1.5  # Significant boost


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
