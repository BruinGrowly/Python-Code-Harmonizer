import os
import sys
from harmonizer.legacy_mapper import LegacyCodeMapper, ArchitecturalSmell
from harmonizer.ljpw_baselines import LJPWBaselines


def test_legacy_mapper():
    print("Testing LegacyCodeMapper LJPW v4.0 Integration...")

    # Create a dummy file with high imbalance
    with open("test_imbalance.py", "w") as f:
        f.write(
            """
def execute_power_move():
    # Power keywords
    execute()
    run()
    build()
    deploy()
    force()
    kill()
    terminate()
    override()
    write()
    push()
"""
        )

    mapper = LegacyCodeMapper(".", quiet=True)
    # Manually inject analysis for the test file to simulate high Power, low others
    mapper.file_analyses["test_imbalance.py"] = type(
        "obj",
        (object,),
        {
            "path": "test_imbalance.py",
            "coordinates": (0.1, 0.1, 0.9, 0.1),  # High Power, low others
            "function_count": 5,
            "avg_disharmony": 0.8,
            "dominant_dimension": "Power",
            "dimension_spread": 0.8,
            "max_disharmony": 0.9,
            "min_disharmony": 0.7,
            "semantic_density": 0.5,
        },
    )

    # Test Smell Detection
    print("\n1. Testing 'Unnatural Imbalance' Smell Detection...")
    mapper._detect_architectural_smells()

    found_smell = False
    for smell in mapper.architectural_smells:
        if smell.smell_type == "Unnatural Imbalance":
            print(f"  [PASS] Detected 'Unnatural Imbalance': {smell.description}")
            found_smell = True
            break

    if not found_smell:
        print("  [FAIL] Did not detect 'Unnatural Imbalance'")

    # Test Debt Projection
    print("\n2. Testing 'Future Debt' Projection...")
    projection = mapper.project_debt_trajectory("test_imbalance.py", months=6)

    if "error" in projection:
        print(f"  [FAIL] Projection error: {projection['error']}")
    else:
        print(f"  Current: {projection['current_coordinates']}")
        print(f"  Projected: {projection['projected_coordinates']}")
        print(f"  Status: {projection['status']}")
        print(f"  Risk: {projection['risk_level']}")

        if (
            projection["status"] == "DEGRADING" or projection["status"] == "STABLE"
        ):  # Might be stable if already saturated
            print("  [PASS] Projection ran successfully")
        else:
            print(f"  [WARN] Unexpected status: {projection['status']}")

    # Cleanup
    if os.path.exists("test_imbalance.py"):
        os.remove("test_imbalance.py")


if __name__ == "__main__":
    test_legacy_mapper()
