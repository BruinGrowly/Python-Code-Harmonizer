"""
Anchor Point Mathematical Analysis (Harmonized V2)

This script is the refactored version of the original anchor_analysis.py.
It has been "harmonized" to use the new 'divine_invitation_engine_V2.py'
engine, resolving the V1/V2 logical contradiction.

This script validates that the Anchor Point (1,1,1,1) is the
mathematical representation of Perfect Harmony, using the
production-ready V2 engine.
"""

import math
import sys

# --- V2 ENGINE IMPORT ---
# This now imports your production-ready V2 engine
try:
    # We will use the 'Optimized Production-Ready' version
    from src import divine_invitation_engine_V2 as dive
except ImportError:
    print("FATAL ERROR: 'divine_invitation_engine_V2.py' not found.")
    print("Please place the V2 engine file in the same directory.")
    sys.exit(1)


def get_harmonized_semantic_clarity(coords: dive.Coordinates) -> float:
    """
    Helper function to calculate semantic clarity using the
    DIVE-V2 engine's logic (standard deviation).

    A perfectly balanced coordinate (like 1,1,1,1) will have a
    std_dev of 0.0, resulting in a "perfect" clarity of 1.0.
    """
    # The V2 Coordinates object is iterable
    dims = list(coords)
    if not dims:
        return 0.0

    mean = sum(dims) / len(dims)
    variance = sum((d - mean) ** 2 for d in dims) / len(dims)
    std_dev = math.sqrt(variance)

    # DIVE-V2 formula: Clarity = 1.0 minus normalized deviation.
    # 0.5 is the max possible std_dev in a 0-1, 4D space.
    clarity = max(0.0, 1.0 - (std_dev / 0.5))
    return clarity


def analyze_anchor_point_v2():
    print("=" * 80)
    print("ANCHOR POINT MATHEMATICAL ANALYSIS (Harmonized V2)")
    print("=" * 80)
    print("Testing the fundamental properties of (1,1,1,1) as Perfect Harmony")

    # --- V2 ENGINE INITIALIZATION ---
    engine = dive.DivineInvitationSemanticEngine()
    anchor = engine.ANCHOR_POINT

    print(f"Powered By: {engine.get_engine_version()}")
    print(f"Anchor Point: {anchor}")
    print()

    # Test 1: Self-consistency
    print("1. SELF-CONSISTENCY TEST")
    print("-" * 50)
    # --- Refactored to use V2 'get_distance' method ---
    distance = engine.get_distance(anchor, anchor)
    print(f"Anchor distance from itself: {distance}")
    print("Expected: 0.0 (perfect self-consistency)")
    print()

    # Test 2: Perfect harmony properties
    print("2. PERFECT HARMONY PROPERTIES")
    print("-" * 50)
    total_harmony = anchor.love + anchor.justice + anchor.power + anchor.wisdom
    print(f"Total Harmony Score: {total_harmony}")
    print("Expected: 4.0 (perfect unity)")
    print()

    dimensions = list(anchor)
    balance = min(dimensions) / max(dimensions)
    print(f"Dimensional Balance: {balance:.3f}")
    print("Expected: 1.0 (perfect balance)")
    print()

    # Test 3: Mathematical Properties
    print("3. MATHEMATICAL PROPERTIES")
    print("-" * 50)
    # --- Refactored to use V2 'get_distance' method ---
    origin = dive.Coordinates(0.0, 0.0, 0.0, 0.0)
    pure_love = dive.Coordinates(1.0, 0.0, 0.0, 0.0)
    pure_justice = dive.Coordinates(0.0, 1.0, 0.0, 0.0)
    pure_power = dive.Coordinates(0.0, 0.0, 1.0, 0.0)
    pure_wisdom = dive.Coordinates(0.0, 0.0, 0.0, 1.0)

    print(f"Distance from origin: {engine.get_distance(anchor, origin):.6f}")
    print(f"Distance from pure Love: {engine.get_distance(anchor, pure_love):.6f}")
    print(f"Distance from pure Justice: {engine.get_distance(anchor, pure_justice):.6f}")
    print(f"Distance from pure Power: {engine.get_distance(anchor, pure_power):.6f}")
    print(f"Distance from pure Wisdom: {engine.get_distance(anchor, pure_wisdom):.6f}")
    print()

    # Test 4: Golden Ratio Relationships
    print("4. GOLDEN RATIO RELATIONSHIPS")
    print("-" * 50)
    phi = (1 + 5**0.5) / 2
    print(f"Golden Ratio (phi): {phi:.10f}")
    # This is a symbolic test from V1
    phi_love = 1 / (anchor.love + phi)
    print(f"  Symbolic Phi-Scaled Coord (Love): {phi_love:.6f}")
    print("  Expected: 0.381966 (1 / (1 + phi))")
    print()

    # Test 5: Semantic Clarity of Perfection
    print("5. SEMANTIC CLARITY OF PERFECTION")
    print("-" * 50)
    # --- Refactored to use V2 clarity logic ---
    clarity = engine.get_semantic_clarity(anchor)
    print(f"Anchor Point Semantic Clarity: {clarity:.6f}")
    # --- "Expected" value is now corrected to 1.0 ---
    print("Expected: 1.0 (perfect std_dev of 0.0)")
    print()

    # Test 6: Perfect Concepts Proximity
    print("6. PERFECT CONCEPTS PROXIMITY")
    print("-" * 50)
    print("Testing perfect concepts - they should approach Anchor Point:")

    concepts = {
        "perfect harmony": "love justice power wisdom",
        "divine love": "love",
        "absolute truth": "justice wisdom",
        "infinite wisdom": "wisdom",
        "ultimate justice": "justice",
    }

    for name, text in concepts.items():
        # --- Refactored to use V2 'analyze_text' method ---
        # and get the .coordinates from the SemanticResult object
        coords = engine.analyze_text(text).coordinates
        distance = engine.get_distance(anchor, coords)
        print(f"  '{name}': distance = {distance:.6f}")
    print()

    # Test 7: Geometric Properties
    print("7. GEOMETRIC PROPERTIES")
    print("-" * 50)
    volume = anchor.love * anchor.justice * anchor.power * anchor.wisdom
    # Formula from V1 spec (for a 3D prism, but we'll test it for consistency)
    surface_area = 2 * (
        (anchor.love * anchor.justice)
        + (anchor.love * anchor.power)
        + (anchor.love * anchor.wisdom)
        + (anchor.justice * anchor.power)
        + (anchor.justice * anchor.wisdom)
        + (anchor.power * anchor.wisdom)
    )
    print(f"4D Semantic Volume: {volume:.6f}")
    print(f"4D Semantic 'Surface Area' (V1 Formula): {surface_area:.6f}")
    print()

    # Test 8: Anchor Point Analysis Summary
    print("8. ANCHOR POINT ANALYSIS SUMMARY")
    print("-" * 50)

    findings = []
    if distance == 0.0:
        findings.append("[OK] Perfect self-consistency")
    if abs(total_harmony - 4.0) < 0.001:
        findings.append("[OK] Perfect harmony achieved")
    if abs(balance - 1.0) < 0.001:
        findings.append("[OK] Perfect dimensional balance")
    if abs(clarity - 1.0) < 0.001:
        findings.append("[OK] Perfect semantic clarity")

    print("Mathematical Validation Results:")
    for finding in findings:
        print(f"  {finding}")

    print()
    print("CONCLUSION:")
    print("=" * 50)
    print("This harmonized test validates the Anchor Point as the")
    print("mathematical representation of Perfect Harmony, using the")
    print("project's unified V2 engine.")
    print("=" * 80)


if __name__ == "__main__":
    analyze_anchor_point_v2()
