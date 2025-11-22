import os
import sys
from harmonizer.legacy_mapper import LegacyCodeMapper


def verify_tech_debt():
    print("Verifying Technical Debt Analysis on Test Codebases...")

    # Initialize mapper pointing to the test directory
    test_dir = os.path.abspath("tests/user_validation")
    mapper = LegacyCodeMapper(test_dir, quiet=True)

    # Analyze specific files
    files_to_check = ["complex_clean.py", "complex_spaghetti.py", "complex_god.py"]

    print(f"\nAnalyzing {len(files_to_check)} files in {test_dir}...")

    for filename in files_to_check:
        file_path = os.path.join(test_dir, filename)
        if not os.path.exists(file_path):
            print(f"Skipping {filename} (not found)")
            continue

        print(f"\n--- Analyzing {filename} ---")
        analysis = mapper._analyze_file(file_path)

        if not analysis:
            print("  Analysis failed (returned None)")
            continue

        # Manually register analysis for smell detection
        mapper.file_analyses[file_path] = analysis

        print(
            f"  Coordinates: L={analysis.coordinates[0]:.2f}, J={analysis.coordinates[1]:.2f}, P={analysis.coordinates[2]:.2f}, W={analysis.coordinates[3]:.2f}"
        )
        print(f"  Dominant: {analysis.dominant_dimension}")

        # Run smell detection for this file
        mapper._detect_architectural_smells()
        smells = [s for s in mapper.architectural_smells if s.file_path.endswith(filename)]

        if smells:
            print(f"  Detected {len(smells)} Architectural Smells:")
            for smell in smells:
                print(f"    - [{smell.severity}] {smell.smell_type}: {smell.description}")
        else:
            print("  No Architectural Smells detected.")

        # Run Debt Projection
        projection = mapper.project_debt_trajectory(file_path, months=6)
        if "error" not in projection:
            print(f"  Future Debt Projection (6 months):")
            print(f"    Status: {projection['status']}")
            print(f"    Risk Level: {projection['risk_level']}")
            print(f"    Drift: {projection['drift']:.4f}")
            print(
                f"    Projected Coords: L={projection['projected_coordinates'][0]:.2f}, J={projection['projected_coordinates'][1]:.2f}, P={projection['projected_coordinates'][2]:.2f}, W={projection['projected_coordinates'][3]:.2f}"
            )


if __name__ == "__main__":
    verify_tech_debt()
