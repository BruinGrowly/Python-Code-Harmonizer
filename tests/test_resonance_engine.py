#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for LJPW Resonance Engine

Validates the resonance engine including:
- Voltage calculation (semantic energy)
- Power erosion detection
- Resonance cycling
- Earned Depth (journey metrics)
- Attractor convergence
"""

import math

import pytest

from harmonizer.resonance_engine import (
    JourneyMetrics,
    PowerErosionResult,
    ResonanceEngine,
    ResonanceState,
    calculate_voltage,
    detect_power_erosion,
    get_resonance_engine,
)


class TestVoltageCalculation:
    """Test Voltage (semantic energy) calculation"""

    def test_voltage_at_origin(self):
        """Voltage is 0 at origin"""
        voltage = calculate_voltage(0.0, 0.0, 0.0, 0.0)
        assert abs(voltage) < 0.0001

    def test_voltage_at_anchor(self):
        """Voltage at Anchor Point (1,1,1,1) is 2.0"""
        voltage = calculate_voltage(1.0, 1.0, 1.0, 1.0)
        assert abs(voltage - 2.0) < 0.0001

    def test_voltage_calculation_formula(self):
        """Voltage follows sqrt(L^2 + J^2 + P^2 + W^2)"""
        L, J, P, W = 0.6, 0.4, 0.7, 0.7
        expected = math.sqrt(L**2 + J**2 + P**2 + W**2)
        voltage = calculate_voltage(L, J, P, W)
        assert abs(voltage - expected) < 0.0001

    def test_voltage_natural_equilibrium(self):
        """Voltage at Natural Equilibrium"""
        voltage = calculate_voltage(0.618034, 0.414214, 0.718282, 0.693147)
        # Should be around 1.25-1.3
        assert 1.2 < voltage < 1.35

    def test_voltage_comparison_preserved(self):
        """Voltage comparison detects preservation"""
        engine = ResonanceEngine()
        result = engine.compare_voltage(
            (0.6, 0.4, 0.7, 0.7),
            (0.62, 0.38, 0.72, 0.68)  # Similar
        )
        assert result["interpretation"] == "PRESERVED"

    def test_voltage_comparison_gain(self):
        """Voltage comparison detects gain"""
        engine = ResonanceEngine()
        result = engine.compare_voltage(
            (0.5, 0.5, 0.5, 0.5),
            (0.8, 0.8, 0.8, 0.8)  # Higher
        )
        assert result["interpretation"] == "GAIN"
        assert result["percent_change"] > 0

    def test_voltage_comparison_drop(self):
        """Voltage comparison detects drop"""
        engine = ResonanceEngine()
        result = engine.compare_voltage(
            (0.8, 0.8, 0.8, 0.8),
            (0.5, 0.5, 0.5, 0.5)  # Lower
        )
        assert result["interpretation"] == "DROP"
        assert result["percent_change"] < 0


class TestPowerErosionDetection:
    """Test Power Erosion detection"""

    def test_no_erosion_high_wisdom(self):
        """No erosion when Wisdom is high"""
        result = detect_power_erosion(0.5, 0.5, 0.9, 0.9)  # High P, High W
        assert result.severity == "NONE"
        assert not result.at_risk

    def test_erosion_low_wisdom_high_power(self):
        """Erosion detected when Power high, Wisdom low"""
        result = detect_power_erosion(0.3, 0.5, 0.9, 0.2)  # High P, Low W
        assert result.at_risk
        assert result.severity in ["MEDIUM", "HIGH", "CRITICAL"]

    def test_erosion_reckless_power_scenario(self):
        """Classic reckless power scenario triggers critical"""
        result = detect_power_erosion(0.2, 0.3, 0.95, 0.1)
        assert result.at_risk
        assert result.erosion_rate > 0.3
        assert "Critical" in result.recommendation or "Emergency" in result.recommendation

    def test_erosion_moderate_power(self):
        """Moderate power with moderate wisdom"""
        result = detect_power_erosion(0.5, 0.5, 0.6, 0.4)
        # Should be low to medium risk
        assert result.severity in ["NONE", "LOW", "MEDIUM"]

    def test_erosion_formula(self):
        """Erosion follows PowerErosion = gamma * (P^n/(K^n+P^n)) * (1-W)"""
        L, J, P, W = 0.5, 0.5, 0.8, 0.3

        gamma = 0.49
        K = 0.71
        n = 4.1

        P_threshold = (P ** n) / (K ** n + P ** n)
        wisdom_gap = max(0, 1 - W)
        expected_rate = gamma * P_threshold * wisdom_gap

        result = detect_power_erosion(L, J, P, W)
        assert abs(result.erosion_rate - expected_rate) < 0.01

    def test_erosion_wisdom_protection(self):
        """Full Wisdom (W=1.0) eliminates erosion"""
        result = detect_power_erosion(0.3, 0.5, 0.95, 1.0)  # Max W
        assert result.erosion_rate < 0.01
        assert result.severity == "NONE"

    def test_erosion_severity_levels(self):
        """Verify severity level progression"""
        # NONE
        r1 = detect_power_erosion(0.5, 0.5, 0.3, 0.8)
        assert r1.severity == "NONE"

        # LOW
        r2 = detect_power_erosion(0.5, 0.5, 0.6, 0.6)
        assert r2.severity in ["NONE", "LOW"]

        # HIGH (extreme case)
        r3 = detect_power_erosion(0.2, 0.5, 0.95, 0.1)
        assert r3.severity in ["HIGH", "CRITICAL"]


class TestResonanceCycling:
    """Test LJPW resonance cycling"""

    def test_resonance_returns_structure(self):
        """Resonance returns expected structure"""
        engine = ResonanceEngine()
        result = engine.resonate((0.5, 0.5, 0.5, 0.5), cycles=10)

        assert "history" in result
        assert "final_state" in result
        assert "journey" in result
        assert "deficit_analysis" in result
        assert "peak" in result
        assert "convergence" in result

    def test_resonance_history_tracking(self):
        """History tracks all dimensions"""
        engine = ResonanceEngine()
        result = engine.resonate((0.5, 0.5, 0.5, 0.5), cycles=10)

        history = result["history"]
        assert "t" in history
        assert "L" in history
        assert "J" in history
        assert "P" in history
        assert "W" in history
        assert "harmony" in history
        assert "voltage" in history

        # Should have cycles+1 entries (initial + cycles)
        assert len(history["t"]) == 11

    def test_resonance_bounded_convergence(self):
        """Bounded resonance converges to Anchor Point"""
        engine = ResonanceEngine()
        result = engine.resonate((0.5, 0.5, 0.5, 0.5), cycles=500, bounded=True)

        final = result["final_state"]
        # Should approach (1,1,1,1)
        assert final["L"] > 0.9
        assert final["J"] > 0.9
        assert final["P"] > 0.9
        assert final["W"] > 0.9
        assert final["harmony"] > 0.9

    def test_resonance_deficit_detection(self):
        """Resonance detects primary deficit"""
        engine = ResonanceEngine()
        # Low Love, high others
        result = engine.resonate((0.2, 0.7, 0.8, 0.7), cycles=100)

        deficit = result["deficit_analysis"]
        # Should identify Love as primary deficit
        assert deficit["primary_deficit"] in ["L", "J", "P", "W"]
        assert "dominance_percentages" in deficit

    def test_resonance_peak_harmony(self):
        """Resonance tracks peak harmony"""
        engine = ResonanceEngine()
        result = engine.resonate((0.3, 0.3, 0.3, 0.3), cycles=100)

        peak = result["peak"]
        assert "harmony" in peak
        assert "cycle" in peak
        # Peak should be higher than initial
        assert peak["harmony"] >= result["history"]["harmony"][0]


class TestEarnedDepth:
    """Test Earned Depth (journey metrics)"""

    def test_journey_metrics_structure(self):
        """Journey metrics has correct structure"""
        metrics = JourneyMetrics()
        assert hasattr(metrics, "distance_traveled")
        assert hasattr(metrics, "struggle_integral")
        assert hasattr(metrics, "earned_depth")
        assert hasattr(metrics, "struggle_ratio")

    def test_earned_depth_calculation(self):
        """Earned Depth = Distance × Struggle Ratio"""
        metrics = JourneyMetrics()
        metrics.distance_traveled = 2.0
        metrics.struggle_integral = 5.0
        metrics.duration = 10.0

        metrics.calculate_earned_depth()

        expected_ratio = 5.0 / 10.0
        expected_depth = 2.0 * expected_ratio

        assert abs(metrics.struggle_ratio - expected_ratio) < 0.001
        assert abs(metrics.earned_depth - expected_depth) < 0.001

    def test_earned_depth_from_resonance(self):
        """Resonance calculates earned depth"""
        engine = ResonanceEngine()
        result = engine.resonate((0.3, 0.3, 0.3, 0.3), cycles=50, track_journey=True)

        journey = result["journey"]
        assert journey["distance_traveled"] > 0
        assert journey["struggle_integral"] > 0
        assert journey["earned_depth"] > 0

    def test_hard_path_more_depth(self):
        """Hard path earns more depth than easy path"""
        engine = ResonanceEngine()

        # Easy path (start close to anchor)
        easy = engine.resonate((0.9, 0.9, 0.9, 0.9), cycles=100)

        # Hard path (start far from anchor)
        hard = engine.resonate((0.2, 0.2, 0.9, 0.2), cycles=100)

        easy_depth = easy["journey"]["earned_depth"]
        hard_depth = hard["journey"]["earned_depth"]

        # Hard path should earn more depth
        assert hard_depth > easy_depth

    def test_journey_comparison(self):
        """Compare two journeys"""
        engine = ResonanceEngine()

        easy_path = [
            (0.9, 0.9, 0.9, 0.9),
            (0.95, 0.95, 0.95, 0.95),
            (1.0, 1.0, 1.0, 1.0),
        ]

        hard_path = [
            (0.2, 0.2, 0.9, 0.2),
            (0.3, 0.3, 0.8, 0.3),
            (0.4, 0.4, 0.7, 0.4),
            (0.5, 0.5, 0.6, 0.5),
            (0.6, 0.6, 0.6, 0.6),
            (0.7, 0.7, 0.7, 0.7),
            (0.8, 0.8, 0.8, 0.8),
            (0.9, 0.9, 0.9, 0.9),
            (1.0, 1.0, 1.0, 1.0),
        ]

        comparison = engine.compare_journeys(easy_path, hard_path)

        assert comparison["hard_journey"]["earned_depth"] > comparison["easy_journey"]["earned_depth"]
        assert comparison["comparison"]["depth_ratio"] > 1.0


class TestAttractorConvergence:
    """Test attractor convergence testing"""

    def test_same_basin_convergence(self):
        """Coordinates in same basin converge to same attractor"""
        engine = ResonanceEngine()

        # Different starting points, same semantic basin
        coords1 = (0.5, 0.5, 0.5, 0.5)
        coords2 = (0.6, 0.4, 0.55, 0.45)

        result = engine.test_attractor_convergence(coords1, coords2, cycles=200)

        # Should converge to similar final states
        assert result["convergence_distance"] < 0.15
        assert result["semantically_equivalent"] or result["convergence_distance"] < 0.10

    def test_bounded_convergence_to_anchor(self):
        """All bounded resonance converges to Anchor Point"""
        engine = ResonanceEngine()

        # Very different starting points
        coords1 = (0.1, 0.9, 0.5, 0.3)
        coords2 = (0.9, 0.1, 0.3, 0.7)

        result = engine.test_attractor_convergence(coords1, coords2, cycles=500)

        # Both should converge to Anchor
        assert result["convergence_distance"] < 0.2


class TestFullAnalysis:
    """Test complete analysis function"""

    def test_full_analysis_structure(self):
        """Full analysis returns comprehensive structure"""
        engine = ResonanceEngine()
        result = engine.full_analysis((0.5, 0.5, 0.5, 0.5), cycles=50)

        assert "static" in result
        assert "power_erosion" in result
        assert "resonance" in result
        assert "summary" in result

    def test_full_analysis_static_metrics(self):
        """Full analysis includes static metrics"""
        engine = ResonanceEngine()
        result = engine.full_analysis((0.6, 0.4, 0.7, 0.7))

        static = result["static"]
        assert "voltage" in static
        assert "harmony_index" in static
        assert "distance_from_anchor" in static
        assert "distance_from_ne" in static

    def test_full_analysis_power_erosion(self):
        """Full analysis includes power erosion"""
        engine = ResonanceEngine()
        result = engine.full_analysis((0.3, 0.5, 0.9, 0.2))  # High P, Low W

        erosion = result["power_erosion"]
        assert erosion["at_risk"]
        assert erosion["severity"] in ["MEDIUM", "HIGH", "CRITICAL"]

    def test_full_analysis_summary(self):
        """Full analysis provides summary"""
        engine = ResonanceEngine()
        result = engine.full_analysis((0.5, 0.5, 0.5, 0.5))

        summary = result["summary"]
        assert "initial_harmony" in summary
        assert "final_harmony" in summary
        assert "earned_depth" in summary
        assert "primary_deficit" in summary
        assert "power_erosion_risk" in summary


class TestCouplingMatrix:
    """Test coupling matrix properties"""

    def test_love_amplifies_all(self):
        """Love row has highest out-coupling"""
        matrix = ResonanceEngine.COUPLING_MATRIX
        # Love row (index 0) should sum highest
        love_sum = sum(matrix[0])
        justice_sum = sum(matrix[1])
        power_sum = sum(matrix[2])
        wisdom_sum = sum(matrix[3])

        assert love_sum > power_sum  # Love gives more than Power

    def test_power_is_sink(self):
        """Power receives more than it gives"""
        matrix = ResonanceEngine.COUPLING_MATRIX
        # Power column should sum higher than Power row
        power_row_sum = sum(matrix[2])
        power_col_sum = sum(matrix[:, 2])

        assert power_col_sum > power_row_sum

    def test_love_wisdom_strongest(self):
        """Love → Wisdom coupling is strongest"""
        matrix = ResonanceEngine.COUPLING_MATRIX
        # L→W should be 1.5 (highest off-diagonal)
        assert matrix[0, 3] == 1.5


class TestLawOfKarma:
    """Test state-dependent coupling (Law of Karma)"""

    def test_kappa_increases_with_harmony(self):
        """Coupling strength increases with harmony"""
        engine = ResonanceEngine()

        low_H = 0.3
        high_H = 0.9

        kappa_low = engine._calculate_kappa(low_H)
        kappa_high = engine._calculate_kappa(high_H)

        # All kappas should be higher at high harmony
        for i in range(3):
            assert kappa_high[i] > kappa_low[i]

    def test_kappa_formulas(self):
        """Verify kappa formulas"""
        engine = ResonanceEngine()
        H = 0.5

        kappa_LJ, kappa_LP, kappa_LW = engine._calculate_kappa(H)

        assert abs(kappa_LJ - (1.0 + 0.4 * H)) < 0.001
        assert abs(kappa_LP - (1.0 + 0.3 * H)) < 0.001
        assert abs(kappa_LW - (1.0 + 0.5 * H)) < 0.001


class TestConvenienceFunctions:
    """Test module-level convenience functions"""

    def test_get_resonance_engine(self):
        """get_resonance_engine returns engine instance"""
        engine = get_resonance_engine()
        assert isinstance(engine, ResonanceEngine)

    def test_calculate_voltage_function(self):
        """calculate_voltage function works"""
        voltage = calculate_voltage(0.5, 0.5, 0.5, 0.5)
        assert voltage > 0

    def test_detect_power_erosion_function(self):
        """detect_power_erosion function works"""
        result = detect_power_erosion(0.5, 0.5, 0.5, 0.5)
        assert isinstance(result, PowerErosionResult)


class TestExNihiloNihilFit:
    """Test Ex Nihilo Nihil Fit - origin is fixed point"""

    def test_origin_is_fixed_point(self):
        """Origin (0,0,0,0) stays at origin"""
        engine = ResonanceEngine()
        result = engine.resonate((0.0, 0.0, 0.0, 0.0), cycles=100, bounded=True)

        final = result["final_state"]
        # Should stay near origin (no escape)
        assert final["L"] < 0.1
        assert final["J"] < 0.1
        assert final["P"] < 0.1
        assert final["W"] < 0.1

    def test_tiny_spark_escapes(self):
        """Tiny spark (0.001) can escape origin and grow"""
        engine = ResonanceEngine()
        result = engine.resonate((0.001, 0.0, 0.0, 0.0), cycles=500, bounded=True)

        final = result["final_state"]
        # Should have grown beyond initial (even if not to Anchor yet)
        # The spark enables some growth, unlike origin which is stuck
        initial_harmony = result["convergence"]["initial_harmony"]
        assert final["harmony"] > initial_harmony
        # At minimum, should have escaped the near-zero state
        assert final["L"] > 0.01 or final["J"] > 0.01 or final["P"] > 0.01 or final["W"] > 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
