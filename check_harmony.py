#!/usr/bin/env python3
"""
LJPW Harmony Check - CI/CD Gating Script
Enforces semantic quality standards for the codebase.
"""

import sys
import os
import argparse
from harmonizer.legacy_mapper import LegacyCodeMapper


def check_harmony(
    target_dir: str = ".", config_path: str = None, verbose: bool = False
):
    print(f"Running LJPW Harmony Check on: {os.path.abspath(target_dir)}")
    print("=" * 60)

    # If analyzing a subdirectory, find project root for config
    # Otherwise use target_dir
    project_root = os.getcwd() if target_dir != "." else target_dir
    
    # Create mapper - it will load config from project_root
    mapper = LegacyCodeMapper(target_dir, quiet=not verbose)
    
    # If we're in project root, use config from there
    if os.path.exists(os.path.join(project_root, "pyproject.toml")):
        from harmonizer.config import ConfigLoader
        mapper.config = ConfigLoader.load(project_root)
    
    mapper.analyze_codebase(show_progress=True)

    failures = []
    warnings = []

    config = mapper.config
    print("\n--- CONFIGURATION ---")
    print(f"Max Disharmony: {config.max_disharmony}")
    print(f"Max Imbalance:  {config.max_imbalance}")
    print(f"Min Density:    {config.min_density}")

    print("\n--- QUALITY GATES ---")

    for file_path, analysis in mapper.file_analyses.items():
        rel_path = os.path.relpath(file_path, target_dir)

        # 1. Critical Disharmony Gate
        if analysis.avg_disharmony > config.max_disharmony:
            failures.append(
                f"[CRITICAL] {rel_path}: Disharmony {analysis.avg_disharmony:.2f} > {config.max_disharmony}"
            )

    # Check Architectural Smells
    for smell in mapper.architectural_smells:
        if smell.smell_type == "Unnatural Imbalance" and smell.severity == "HIGH":
            failures.append(f"[IMBALANCE] {smell.file_path}: {smell.description}")

        if smell.smell_type == "Anemic Component" and smell.severity == "HIGH":
            # Treat Anemic Components as warnings for now, unless critical
            warnings.append(f"[ANEMIC] {smell.file_path}: {smell.description}")

        if smell.smell_type == "God File" and smell.severity == "HIGH":
            failures.append(f"[GOD FILE] {smell.file_path}: {smell.description}")

    # Report Results
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(w)

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f)
        print("\nHarmony Check FAILED. Please refactor the above files.")
        sys.exit(1)
    else:
        print("\nHarmony Check PASSED. The system is in balance.")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="LJPW Harmony Check")
    parser.add_argument(
        "target", nargs="?", default=".", help="Target directory to analyze"
    )
    parser.add_argument("--config", help="Path to configuration file (optional)")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    check_harmony(args.target, args.config, args.verbose)


if __name__ == "__main__":
    main()
