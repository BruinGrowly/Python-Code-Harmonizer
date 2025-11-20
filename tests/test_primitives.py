#!/usr/bin/env python3
"""
Direct test of the 4 semantic primitives: LOVE, JUSTICE, POWER, WISDOM
"""

from harmonizer.divine_invitation_engine_V2 import (
    Coordinates,
    Dimension,
    DivineInvitationSemanticEngine,
)


def test_primitives():
    """Test each primitive dimension directly"""
    engine = DivineInvitationSemanticEngine()

    print("=" * 70)
    print("TESTING 4 SEMANTIC PRIMITIVES")
    print("=" * 70)

    # Test 1: LOVE primitive
    print("\n1. LOVE PRIMITIVE")
    love_result = engine.analyze_text("love compassion kindness care")
    print("   Text: 'love compassion kindness care'")
    print(f"   Coordinates: {love_result.coordinates}")
    print(f"   LOVE value: {love_result.coordinates.love:.3f}")
    assert love_result.coordinates.love > 0.8, "LOVE dimension should be dominant"
    print("   ✓ LOVE primitive working correctly")

    # Test 2: JUSTICE primitive
    print("\n2. JUSTICE PRIMITIVE")
    justice_result = engine.analyze_text("justice truth fairness law order")
    print("   Text: 'justice truth fairness law order'")
    print(f"   Coordinates: {justice_result.coordinates}")
    print(f"   JUSTICE value: {justice_result.coordinates.justice:.3f}")
    assert (
        justice_result.coordinates.justice > 0.8
    ), "JUSTICE dimension should be dominant"
    print("   ✓ JUSTICE primitive working correctly")

    # Test 3: POWER primitive
    print("\n3. POWER PRIMITIVE")
    power_result = engine.analyze_text("power strength action control execute")
    print("   Text: 'power strength action control execute'")
    print(f"   Coordinates: {power_result.coordinates}")
    print(f"   POWER value: {power_result.coordinates.power:.3f}")
    assert power_result.coordinates.power > 0.8, "POWER dimension should be dominant"
    print("   ✓ POWER primitive working correctly")

    # Test 4: WISDOM primitive
    print("\n4. WISDOM PRIMITIVE")
    wisdom_result = engine.analyze_text("wisdom knowledge understanding analysis")
    print("   Text: 'wisdom knowledge understanding analysis'")
    print(f"   Coordinates: {wisdom_result.coordinates}")
    print(f"   WISDOM value: {wisdom_result.coordinates.wisdom:.3f}")
    assert wisdom_result.coordinates.wisdom > 0.8, "WISDOM dimension should be dominant"
    print("   ✓ WISDOM primitive working correctly")

    # Test 5: Mixed coordinates
    print("\n5. MIXED COORDINATES")
    mixed_result = engine.analyze_text("love justice power wisdom")
    print("   Text: 'love justice power wisdom'")
    print(f"   Coordinates: {mixed_result.coordinates}")
    print(f"   L={mixed_result.coordinates.love:.3f}, ", end="")
    print(f"J={mixed_result.coordinates.justice:.3f}, ", end="")
    print(f"P={mixed_result.coordinates.power:.3f}, ", end="")
    print(f"W={mixed_result.coordinates.wisdom:.3f}")
    expected = 0.25
    tolerance = 0.01
    assert abs(mixed_result.coordinates.love - expected) < tolerance
    assert abs(mixed_result.coordinates.justice - expected) < tolerance
    assert abs(mixed_result.coordinates.power - expected) < tolerance
    assert abs(mixed_result.coordinates.wisdom - expected) < tolerance
    print("   ✓ All primitives balanced at 0.25 each")

    # Test 6: Verify Dimension enum
    print("\n6. DIMENSION ENUM")
    print(f"   LOVE = {Dimension.LOVE.value}")
    print(f"   JUSTICE = {Dimension.JUSTICE.value}")
    print(f"   POWER = {Dimension.POWER.value}")
    print(f"   WISDOM = {Dimension.WISDOM.value}")
    assert Dimension.LOVE.value == "love"
    assert Dimension.JUSTICE.value == "justice"
    assert Dimension.POWER.value == "power"
    assert Dimension.WISDOM.value == "wisdom"
    print("   ✓ All enum values correct")

    # Test 7: Coordinates dataclass
    print("\n7. COORDINATES DATACLASS")
    test_coords = Coordinates(love=0.1, justice=0.2, power=0.3, wisdom=0.4)
    print(f"   Created: {test_coords}")
    assert test_coords.love == 0.1
    assert test_coords.justice == 0.2
    assert test_coords.power == 0.3
    assert test_coords.wisdom == 0.4
    print("   ✓ Coordinates structure working")

    print("\n" + "=" * 70)
    print("ALL 4 SEMANTIC PRIMITIVES VERIFIED AND WORKING")
    print("=" * 70)
    print("\nResult: LOVE, JUSTICE, POWER, WISDOM are functioning correctly")
    print("in the semantic coordinate system.\n")


if __name__ == "__main__":
    test_primitives()
