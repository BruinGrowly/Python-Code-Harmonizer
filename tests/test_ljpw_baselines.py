#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for LJPW Mathematical Baselines

Validates the mathematical baseline calculations and interpretations.
"""

import math

import pytest

from harmonizer.ljpw_baselines import (
    LJPWBaselines,
    NumericalEquivalents,
    ReferencePoints,
    get_numerical_equivalents,
    get_reference_points,
)


class TestNumericalEquivalents:
    """Test fundamental mathematical constants"""

    def test_numerical_equivalents_values(self):
        """Verify numerical equivalents match expected values"""
        ne = NumericalEquivalents()

        # Love: Golden ratio inverse
        assert abs(ne.L - 0.618034) < 0.0001

        # Justice: Pythagorean ratio
        assert abs(ne.J - 0.414214) < 0.0001

        # Power: Exponential base
        assert abs(ne.P - 0.718282) < 0.0001

        # Wisdom: Natural log of 2
        assert abs(ne.W - 0.693147) < 0.0001

    def test_get_numerical_equivalents(self):
        """Test convenience function"""
        ne = get_numerical_equivalents()
        assert isinstance(ne, NumericalEquivalents)
        assert ne.L > 0


class TestReferencePoints:
    """Test reference points"""

    def test_anchor_point(self):
        """Verify Anchor Point is (1,1,1,1)"""
        rp = ReferencePoints()
        assert rp.ANCHOR_POINT == (1.0, 1.0, 1.0, 1.0)

    def test_natural_equilibrium(self):
        """Verify Natural Equilibrium matches numerical equivalents"""
        rp = ReferencePoints()
        ne = NumericalEquivalents()

        assert abs(rp.NATURAL_EQUILIBRIUM[0] - ne.L) < 0.0001
        assert abs(rp.NATURAL_EQUILIBRIUM[1] - ne.J) < 0.0001
        assert abs(rp.NATURAL_EQUILIBRIUM[2] - ne.P) < 0.0001
        assert abs(rp.NATURAL_EQUILIBRIUM[3] - ne.W) < 0.0001

    def test_get_reference_points(self):
        """Test convenience function"""
        rp = get_reference_points()
        assert isinstance(rp, ReferencePoints)


class TestEffectiveDimensions:
    """Test coupling-aware effective dimensions"""

    def test_effective_dimensions_no_love(self):
        """With L=0, no amplification occurs"""
        L, J, P, W = 0.0, 0.5, 0.5, 0.5
        eff = LJPWBaselines.effective_dimensions(L, J, P, W)

        assert eff["effective_L"] == 0.0
        assert eff["effective_J"] == 0.5  # No amplification
        assert eff["effective_P"] == 0.5  # No amplification
        assert eff["effective_W"] == 0.5  # No amplification

    def test_effective_dimensions_with_love(self):
        """Love amplifies other dimensions"""
        L, J, P, W = 0.5, 0.5, 0.5, 0.5
        eff = LJPWBaselines.effective_dimensions(L, J, P, W)

        # Justice amplified by 40% per unit Love
        assert eff["effective_J"] == 0.5 * (1 + 1.4 * 0.5)

        # Power amplified by 30% per unit Love
        assert eff["effective_P"] == 0.5 * (1 + 1.3 * 0.5)

        # Wisdom amplified by 50% per unit Love (strongest)
        assert eff["effective_W"] == 0.5 * (1 + 1.5 * 0.5)

    def test_effective_dimensions_high_love(self):
        """High Love creates significant amplification"""
        L, J, P, W = 1.0, 0.5, 0.5, 0.5
        eff = LJPWBaselines.effective_dimensions(L, J, P, W)

        # With max Love, dimensions are amplified significantly
        assert eff["effective_J"] == 0.5 * (1 + 1.4 * 1.0)  # 1.2 (140%)
        assert eff["effective_P"] == 0.5 * (1 + 1.3 * 1.0)  # 1.15 (130%)
        assert eff["effective_W"] == 0.5 * (1 + 1.5 * 1.0)  # 1.25 (150%)


class TestHarmonicMean:
    """Test harmonic mean (robustness metric)"""

    def test_harmonic_mean_zero_handling(self):
        """Harmonic mean returns 0 if any dimension is 0"""
        assert LJPWBaselines.harmonic_mean(0.0, 0.5, 0.5, 0.5) == 0.0
        assert LJPWBaselines.harmonic_mean(0.5, 0.0, 0.5, 0.5) == 0.0

    def test_harmonic_mean_equal_values(self):
        """Harmonic mean equals value when all equal"""
        assert abs(LJPWBaselines.harmonic_mean(0.5, 0.5, 0.5, 0.5) - 0.5) < 0.0001

    def test_harmonic_mean_weakest_link(self):
        """Harmonic mean limited by weakest dimension"""
        # Three high, one low
        result = LJPWBaselines.harmonic_mean(0.2, 0.9, 0.9, 0.9)
        # Should be close to but slightly higher than weakest
        assert result < 0.5  # Much lower than 0.9
        assert result > 0.2  # Higher than weakest


class TestGeometricMean:
    """Test geometric mean (effectiveness metric)"""

    def test_geometric_mean_equal_values(self):
        """Geometric mean equals value when all equal"""
        assert abs(LJPWBaselines.geometric_mean(0.5, 0.5, 0.5, 0.5) - 0.5) < 0.0001

    def test_geometric_mean_natural_equilibrium(self):
        """Geometric mean of Natural Equilibrium"""
        ne = ReferencePoints.NATURAL_EQUILIBRIUM
        result = LJPWBaselines.geometric_mean(ne[0], ne[1], ne[2], ne[3])
        # Should be reasonable value
        assert 0.5 < result < 0.7

    def test_geometric_mean_multiplicative(self):
        """Geometric mean is multiplicative"""
        # Product of dimensions
        L, J, P, W = 0.5, 0.5, 0.5, 0.5
        product = L * J * P * W
        gm = LJPWBaselines.geometric_mean(L, J, P, W)
        assert abs(gm - product**0.25) < 0.0001


class TestCouplingAwareSum:
    """Test coupling-aware sum (growth potential)"""

    def test_coupling_sum_can_exceed_one(self):
        """Coupling sum can exceed 1.0 due to amplification"""
        L, J, P, W = 0.9, 0.9, 0.9, 0.9
        result = LJPWBaselines.coupling_aware_sum(L, J, P, W)
        assert result > 1.0  # Due to Love amplification

    def test_coupling_sum_low_love(self):
        """Low Love limits growth potential"""
        L, J, P, W = 0.1, 0.9, 0.9, 0.9
        result = LJPWBaselines.coupling_aware_sum(L, J, P, W)
        # Limited by low Love despite high others
        assert result < 1.0


class TestHarmonyIndex:
    """Test harmony index (balance metric)"""

    def test_harmony_index_at_anchor(self):
        """Harmony index approaches 1.0 at Anchor Point"""
        L, J, P, W = 1.0, 1.0, 1.0, 1.0
        result = LJPWBaselines.harmony_index(L, J, P, W)
        # At Anchor: distance = 0, so 1/(1+0) = 1.0
        assert abs(result - 1.0) < 0.01

    def test_harmony_index_far_from_anchor(self):
        """Harmony index low when far from Anchor"""
        L, J, P, W = 0.0, 0.0, 0.0, 0.0
        result = LJPWBaselines.harmony_index(L, J, P, W)
        assert result < 0.5  # Far from ideal


class TestCompositeScore:
    """Test composite score (overall performance)"""

    def test_composite_score_range(self):
        """Composite score is in reasonable range"""
        # Various test cases
        test_cases = [
            (0.5, 0.5, 0.5, 0.5),
            (0.8, 0.8, 0.8, 0.8),
            (0.3, 0.7, 0.6, 0.5),
        ]

        for L, J, P, W in test_cases:
            result = LJPWBaselines.composite_score(L, J, P, W)
            assert 0.0 < result < 2.0  # Reasonable range

    def test_composite_score_high_performance(self):
        """High all dimensions = high composite score"""
        L, J, P, W = 0.9, 0.9, 0.9, 0.9
        result = LJPWBaselines.composite_score(L, J, P, W)
        assert result > 1.0  # High performance


class TestDistances:
    """Test distance metrics"""

    def test_distance_from_anchor_at_anchor(self):
        """Distance is 0 at Anchor Point"""
        L, J, P, W = 1.0, 1.0, 1.0, 1.0
        distance = LJPWBaselines.distance_from_anchor(L, J, P, W)
        assert abs(distance) < 0.0001

    def test_distance_from_anchor_at_origin(self):
        """Distance is sqrt(4) = 2 at origin"""
        L, J, P, W = 0.0, 0.0, 0.0, 0.0
        distance = LJPWBaselines.distance_from_anchor(L, J, P, W)
        assert abs(distance - 2.0) < 0.0001

    def test_distance_from_ne_at_ne(self):
        """Distance is 0 at Natural Equilibrium"""
        ne = ReferencePoints.NATURAL_EQUILIBRIUM
        distance = LJPWBaselines.distance_from_natural_equilibrium(
            ne[0], ne[1], ne[2], ne[3]
        )
        assert abs(distance) < 0.0001


class TestFullDiagnostic:
    """Test full diagnostic function"""

    def test_full_diagnostic_structure(self):
        """Full diagnostic returns expected structure"""
        L, J, P, W = 0.5, 0.5, 0.5, 0.5
        diagnostic = LJPWBaselines.full_diagnostic(L, J, P, W)

        # Check structure
        assert "coordinates" in diagnostic
        assert "effective_dimensions" in diagnostic
        assert "distances" in diagnostic
        assert "metrics" in diagnostic

        # Check coordinates
        assert diagnostic["coordinates"]["L"] == 0.5

        # Check effective dimensions
        assert "effective_L" in diagnostic["effective_dimensions"]

        # Check distances
        assert "from_anchor" in diagnostic["distances"]
        assert "from_natural_equilibrium" in diagnostic["distances"]

        # Check metrics
        assert "harmonic_mean" in diagnostic["metrics"]
        assert "geometric_mean" in diagnostic["metrics"]
        assert "coupling_aware_sum" in diagnostic["metrics"]
        assert "harmony_index" in diagnostic["metrics"]
        assert "composite_score" in diagnostic["metrics"]


class TestInterpretations:
    """Test interpretation functions"""

    def test_interpret_distance_from_ne(self):
        """Distance interpretation is reasonable"""
        assert "optimal" in LJPWBaselines.interpret_distance_from_ne(0.1).lower()
        assert "good" in LJPWBaselines.interpret_distance_from_ne(0.3).lower()
        assert "imbalance" in LJPWBaselines.interpret_distance_from_ne(0.6).lower()
        assert "dysfunction" in LJPWBaselines.interpret_distance_from_ne(1.0).lower()

    def test_interpret_composite_score(self):
        """Composite score interpretation is reasonable"""
        assert "critical" in LJPWBaselines.interpret_composite_score(0.4).lower()
        assert "competent" in LJPWBaselines.interpret_composite_score(0.8).lower()
        assert (
            "excellent" in LJPWBaselines.interpret_composite_score(1.2).lower()
            or "strong" in LJPWBaselines.interpret_composite_score(1.2).lower()
        )
        assert "elite" in LJPWBaselines.interpret_composite_score(1.4).lower()


class TestLoveMultiplierEffect:
    """Test Love's amplification effect"""

    def test_love_amplifies_justice(self):
        """Love amplifies Justice by 40% per unit"""
        L1, L2 = 0.0, 1.0
        J = 0.5

        eff1 = LJPWBaselines.effective_dimensions(L1, J, 0.5, 0.5)
        eff2 = LJPWBaselines.effective_dimensions(L2, J, 0.5, 0.5)

        # With L=0, no amplification
        assert eff1["effective_J"] == J

        # With L=1, 140% of J
        assert eff2["effective_J"] == J * (1 + 1.4)

    def test_love_strongest_on_wisdom(self):
        """Love's strongest effect is on Wisdom (+50%)"""
        L = 1.0
        J, P, W = 0.5, 0.5, 0.5

        eff = LJPWBaselines.effective_dimensions(L, J, P, W)

        # Wisdom gets biggest boost
        wisdom_boost = eff["effective_W"] / W - 1
        justice_boost = eff["effective_J"] / J - 1
        power_boost = eff["effective_P"] / P - 1

        assert wisdom_boost > justice_boost
        assert wisdom_boost > power_boost


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
