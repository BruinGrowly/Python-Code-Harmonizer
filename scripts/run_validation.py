#!/usr/bin/env python3
"""
LJPW v4.0 User Validation Script
================================

Analyzes 3 simple and 3 complex codebases to validate the LJPW v4.0 model.
Runs both static analysis (to get L, J, P, W) and dynamic simulation (to see evolution).
"""

import sys
import os
import glob
import numpy as np
from statistics import mean

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from harmonizer.main import PythonCodeHarmonizer
from harmonizer.ljpw_baselines import DynamicLJPWv4, LJPWBaselines
from harmonizer.dependency_engine import DependencyEngine
from harmonizer.visualizer import HarmonizerVisualizer


def analyze_and_simulate(file_path, harmonizer):
    print(f"\nAnalyzing: {os.path.basename(file_path)}")
    print("-" * 40)

    # 1. Static Analysis
    report = harmonizer.analyze_file(file_path)
    if not report:
        print("  No functions found or analysis failed.")
        return None

    # Collect coordinates from all functions
    all_coords = []
    function_count = 0
    avg_p_sum = 0

    for func_name, data in report.items():
        function_count += 1
        ice_result = data.get("ice_result", {})
        ice_components = ice_result.get("ice_components", {})
        execution = ice_components.get("execution")
        if execution:
            coords = execution.coordinates
            all_coords.append(
                (coords.love, coords.justice, coords.power, coords.wisdom)
            )
            avg_p_sum += coords.power

    if not all_coords:
        print("  Could not extract coordinates.")
        return None

    # Average coordinates for the file
    avg_l = mean([c[0] for c in all_coords])
    avg_j = mean([c[1] for c in all_coords])
    avg_p = mean([c[2] for c in all_coords])
    avg_w = mean([c[3] for c in all_coords])

    print(f"  Static Metrics (Avg):")
    print(f"    L: {avg_l:.2f} | J: {avg_j:.2f} | P: {avg_p:.2f} | W: {avg_w:.2f}")

    # 2. Dynamic Simulation
    # Calculate Complexity Score
    # Base = 1.0. Add 0.2 per function (High sensitivity for demo).
    complexity_score = 1.0 + (function_count * 0.2)
    print(f"  Complexity Score: {complexity_score:.2f}")

    simulator = DynamicLJPWv4(complexity_score=complexity_score)

    print("  Running Dynamic Simulation (50 steps)...")
    initial_state = (avg_l, avg_j, avg_p, avg_w)
    history = simulator.simulate(initial_state, duration=50, dt=0.05)

    final_l = history["L"][-1]
    final_j = history["J"][-1]
    final_p = history["P"][-1]
    final_w = history["W"][-1]

    print(f"  Final State:")
    print(
        f"    L: {final_l:.2f} | J: {final_j:.2f} | P: {final_p:.2f} | W: {final_w:.2f}"
    )

    # Assessment
    if final_j < 0.3:
        print("  Result: COLLAPSE (Justice eroded)")
    elif final_j > 1.2:
        print("  Result: THRIVING (High Justice)")
    elif final_j > 0.8:
        print("  Result: HEALTHY (Above NE)")
    else:
        print("  Result: STABLE (Near NE)")

    # Return data for visualizer
    return {
        "coordinates": (avg_l, avg_j, avg_p, avg_w),
        "function_count": function_count,
        "semantic_density": avg_p_sum / max(1, function_count),  # Proxy
        "avg_disharmony": 0.0,  # Placeholder
    }


def run_validation():
    harmonizer = PythonCodeHarmonizer(quiet=True)

    test_dir = os.path.join(project_root, "tests", "user_validation")
    if not os.path.exists(test_dir):
        print(f"Error: Test directory not found at {test_dir}")
        return

    print("=" * 60)
    print("LJPW v4.0 Validation Run (Visual Analytics)")
    print("=" * 60)

    # 3. Visual Analytics Integration
    from harmonizer.dependency_engine import DependencyEngine
    from harmonizer.visualizer import HarmonizerVisualizer

    simple_files = glob.glob(os.path.join(test_dir, "simple_*.py"))
    complex_files = glob.glob(os.path.join(test_dir, "complex_*.py"))
    all_files = simple_files + complex_files

    # Build Dependency Graph
    print("\nBuilding Dependency Graph...")
    dep_engine = DependencyEngine(test_dir)
    dep_engine.build_graph(all_files)

    results = {}

    print("\n--- ANALYZING FILES ---")
    for f in all_files:
        analysis_data = analyze_and_simulate(f, harmonizer)
        if analysis_data:
            results[f] = analysis_data

    # Generate HTML Report
    print("\nGenerating Visual Report...")
    visualizer = HarmonizerVisualizer("harmonizer_report.html")

    # Convert dependency nodes to D3 format
    graph_data = {
        "nodes": [
            {"id": n.file_path, "mass": n.mass, "gravity": n.gravity}
            for n in dep_engine.nodes.values()
        ],
        "links": [],
    }
    for n in dep_engine.nodes.values():
        for imported in n.imports:
            # Ensure target exists in nodes to avoid D3 errors
            if imported in dep_engine.nodes:
                graph_data["links"].append({"source": n.file_path, "target": imported})

    visualizer.generate_report(results, graph_data, project_name="LJPW Validation Run")


if __name__ == "__main__":
    run_validation()
