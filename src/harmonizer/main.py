#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Code Harmonizer (Version 1.2)

This is the main application that integrates the Divine Invitation
Semantic Engine (DIVE-V2) with the AST Semantic Parser.

It is guided by the principle of the "Logical Anchor Point" (S,L,I,E)
and uses the ICE (Intent, Context, Execution) framework to analyze
the "semantic harmony" of Python code.

New in v1.2:
- Exit codes for CI/CD integration (0=harmonious, 1=medium, 2=high, 3=critical)
- JSON output format for tool integration
- Command-line argument parsing with argparse
"""

import argparse
import ast
import json
import os
import sys
from typing import Dict, List

# --- COMPONENT IMPORTS ---
# This script assumes the following two files are in the
# same directory or in Python's path.

try:
    # 1. Import your powerful V2 engine
    # (This assumes 'divine_invitation_engine_V2.py' is the
    # 'Optimized Production-Ready' version)
    from src import divine_invitation_engine_V2 as dive
except ImportError:
    print("FATAL ERROR: 'divine_invitation_engine_V2.py' not found.")
    print("Please place the V2 engine file in the same directory.")
    sys.exit(1)

try:
    # 2. Import our new "Rosetta Stone" parser
    from src.ast_semantic_parser import AST_Semantic_Parser
except ImportError:
    print("FATAL ERROR: 'ast_semantic_parser.py' not found.")
    print("Please place the parser file in the same directory.")
    sys.exit(1)

# --- THE HARMONIZER APPLICATION ---


class PythonCodeHarmonizer:
    """
    Analyzes Python code for "Intent Harmony" using the DIVE-V2
    ICE (Intent, Context, Execution) framework.
    """

    # Severity thresholds
    THRESHOLD_EXCELLENT = 0.3
    THRESHOLD_LOW = 0.5
    THRESHOLD_MEDIUM = 0.8
    THRESHOLD_HIGH = 1.2

    def __init__(self, disharmony_threshold: float = 0.5, quiet: bool = False):
        # 1. Initialize your V2 engine. This is our "compass."
        self.engine = dive.DivineInvitationSemanticEngine()

        # 2. Initialize our "Rosetta Stone" parser.

        # --- HARMONIZATION FIX (v1.1) ---
        # The "Optimized" V2 engine's VocabularyManager stores its
        # word list in the 'all_keywords' set.
        # We now reference the correct attribute.
        self.parser = AST_Semantic_Parser(
            vocabulary=self.engine.vocabulary.all_keywords
        )

        # 3. Set the threshold for flagging disharmony.
        self.disharmony_threshold = disharmony_threshold

        # 4. Quiet mode for JSON output
        self.quiet = quiet

        if not quiet:
            print("=" * 70)
            print("Python Code Harmonizer (v1.2) ONLINE")
            print("Actively guided by the Anchor Point framework.")
            print(f"Powered By: {self.engine.get_engine_version()}")
            print("Logical Anchor Point: (S=1, L=1, I=1, E=1)")
            print(f"Disharmony Threshold: {self.disharmony_threshold}")
            print("=" * 70)

    def analyze_file(self, file_path: str) -> Dict[str, float]:
        """
        Analyzes a single Python file for Intent-Execution-Disharmony.
        Returns a dictionary of {function_name: disharmony_score}
        """
        if not self.quiet:
            print(f"\nAnalyzing file: {file_path}")
            print("-" * 70)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            if not self.quiet:
                print(f"ERROR: File not found at '{file_path}'")
            return {}
        except Exception as e:
            if not self.quiet:
                print(f"ERROR: Could not read file: {e}")
            return {}

        # 1. Use Python's AST to parse the code into a logical tree
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            if not self.quiet:
                print(f"ERROR: Could not parse file. Syntax error on line {e.lineno}")
            return {}

        harmony_report = {}

        # 2. "Walk" the tree and visit every function definition
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                docstring = ast.get_docstring(node)

                # 3. Get INTENT: "The Stated Purpose"
                # We use our parser to get the concepts from the name/docstring
                intent_concepts = self.parser.get_intent_concepts(
                    function_name, docstring
                )

                # 4. Get EXECUTION: "The Actual Action"
                # We use our parser to get the concepts from the function's body
                execution_concepts = self.parser.get_execution_concepts(node.body)

                # 5. THE "A-HA!" MOMENT: Use the V2 ICEAnalyzer
                # We pass our parsed concepts into the V2 engine's
                # built-in ICE framework analyzer.
                ice_result = self.engine.perform_ice_analysis(
                    intent_words=intent_concepts,
                    context_words=[
                        "python",
                        "function",
                        function_name,
                    ],  # Provide context
                    execution_words=execution_concepts,
                )

                # The "bug" is the semantic distance between Intent and Execution
                # This metric *is* returned by the "Optimized" V2 engine.
                disharmony_score = ice_result["ice_metrics"][
                    "intent_execution_disharmony"
                ]

                harmony_report[function_name] = disharmony_score

        return harmony_report

    def get_severity(self, score: float) -> str:
        """Determine severity level based on score."""
        if score < self.THRESHOLD_EXCELLENT:
            return "excellent"
        elif score < self.THRESHOLD_LOW:
            return "low"
        elif score < self.THRESHOLD_MEDIUM:
            return "medium"
        elif score < self.THRESHOLD_HIGH:
            return "high"
        else:
            return "critical"

    def get_highest_severity_code(self, harmony_report: Dict[str, float]) -> int:
        """
        Return exit code based on highest severity found.

        Exit codes:
        0 = All harmonious (excellent or low severity)
        1 = Medium severity found
        2 = High severity found
        3 = Critical severity found
        """
        if not harmony_report:
            return 0

        max_score = max(harmony_report.values())

        if max_score >= self.THRESHOLD_HIGH:
            return 3  # Critical
        elif max_score >= self.THRESHOLD_MEDIUM:
            return 2  # High
        elif max_score >= self.THRESHOLD_LOW:
            return 1  # Medium
        else:
            return 0  # Excellent/Low

    def print_report(self, harmony_report: Dict[str, float]):
        """Prints the final harmony report to the console."""

        print("FUNCTION NAME                | INTENT-EXECUTION DISHARMONY")
        print("-----------------------------|--------------------------------")

        if not harmony_report:
            print("No functions found to analyze.")
            return

        sorted_report = sorted(
            harmony_report.items(), key=lambda item: item[1], reverse=True
        )

        for func_name, score in sorted_report:
            status = "✓ HARMONIOUS"
            if score > self.disharmony_threshold:
                status = f"!! DISHARMONY (Score: {score:.2f})"

            print(f"{func_name:<28} | {status}")

        print("=" * 70)
        print("Analysis Complete.")

    def print_json_report(self, all_reports: Dict[str, Dict[str, float]]):
        """Prints the harmony report in JSON format."""
        output = {
            "version": "1.2",
            "threshold": self.disharmony_threshold,
            "severity_thresholds": {
                "excellent": self.THRESHOLD_EXCELLENT,
                "low": self.THRESHOLD_LOW,
                "medium": self.THRESHOLD_MEDIUM,
                "high": self.THRESHOLD_HIGH,
            },
            "files": [],
        }

        total_functions = 0
        severity_counts = {
            "excellent": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0,
        }

        for file_path, harmony_report in all_reports.items():
            file_data = {"file": file_path, "functions": []}

            for func_name, score in harmony_report.items():
                severity = self.get_severity(score)
                severity_counts[severity] += 1
                total_functions += 1

                function_data = {
                    "name": func_name,
                    "score": round(score, 4),
                    "severity": severity,
                    "disharmonious": score > self.disharmony_threshold,
                }
                file_data["functions"].append(function_data)

            # Sort by score (highest first)
            file_data["functions"].sort(key=lambda x: x["score"], reverse=True)
            output["files"].append(file_data)

        # Add summary
        output["summary"] = {
            "total_files": len(all_reports),
            "total_functions": total_functions,
            "severity_counts": severity_counts,
            "highest_severity": self._get_highest_severity_name(severity_counts),
        }

        print(json.dumps(output, indent=2))

    def _get_highest_severity_name(self, severity_counts: Dict[str, int]) -> str:
        """Get the name of the highest severity level found."""
        for severity in ["critical", "high", "medium", "low", "excellent"]:
            if severity_counts[severity] > 0:
                return severity
        return "excellent"


# --- MAIN EXECUTION ---


def run_cli():
    """Command-line interface entry point."""
    parser = argparse.ArgumentParser(
        description="Python Code Harmonizer - Semantic code analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  harmonizer myfile.py                    # Analyze single file
  harmonizer file1.py file2.py            # Analyze multiple files
  harmonizer --format json myfile.py      # Output JSON format
  harmonizer --threshold 0.7 myfile.py    # Custom threshold

Exit Codes:
  0 = All harmonious (excellent or low severity)
  1 = Medium severity found (0.5-0.8)
  2 = High severity found (0.8-1.2)
  3 = Critical severity found (>= 1.2)
        """,
    )

    parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="Python file(s) to analyze",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        metavar="FLOAT",
        help="Disharmony threshold (default: 0.5)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Python Code Harmonizer v1.2",
    )

    args = parser.parse_args()

    # 1. Initialize the Harmonizer
    quiet = args.format == "json"
    harmonizer = PythonCodeHarmonizer(disharmony_threshold=args.threshold, quiet=quiet)

    # 2. Run the analysis for all provided files
    all_reports = {}
    highest_exit_code = 0

    for file_path in args.files:
        if os.path.exists(file_path):
            report = harmonizer.analyze_file(file_path)
            all_reports[file_path] = report

            # Track highest severity for exit code
            exit_code = harmonizer.get_highest_severity_code(report)
            highest_exit_code = max(highest_exit_code, exit_code)

            # Print text report immediately if not JSON
            if args.format == "text":
                harmonizer.print_report(report)
        else:
            if args.format == "text":
                print(f"\nERROR: File not found: {file_path}")
                print("-" * 70)

    # 3. Print JSON report if requested
    if args.format == "json":
        harmonizer.print_json_report(all_reports)

    # 4. Exit with appropriate code for CI/CD
    sys.exit(highest_exit_code)


if __name__ == "__main__":
    run_cli()
