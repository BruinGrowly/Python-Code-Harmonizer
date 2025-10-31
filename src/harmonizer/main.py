#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Code Harmonizer (Version 1.1)

This is the main application that integrates the Divine Invitation
Semantic Engine (DIVE-V2) with the AST Semantic Parser.

It is guided by the principle of the "Logical Anchor Point" (S,L,I,E)
and uses the ICE (Intent, Context, Execution) framework to analyze
the "semantic harmony" of Python code.

(HARMONIZATION_NOTE: v1.1 fixes a 'AttributeError' by correctly
referencing 'self.engine.vocabulary.all_keywords' from the
'Optimized Production-Ready' V2 engine.)
"""

import ast
import sys
import os
from typing import Dict

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

    def __init__(self, disharmony_threshold: float = 0.5):
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

        print("=" * 70)
        print("Python Code Harmonizer (v1.1) ONLINE")
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
        print(f"\nAnalyzing file: {file_path}")
        print("-" * 70)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"ERROR: File not found at '{file_path}'")
            return {}
        except Exception as e:
            print(f"ERROR: Could not read file: {e}")
            return {}

        # 1. Use Python's AST to parse the code into a logical tree
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
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


# --- MAIN EXECUTION ---


def run_cli():
    """Command-line interface entry point."""
    if len(sys.argv) < 2:
        print("Usage: harmonizer <file_to_analyze.py> [file2.py ...]")
        sys.exit(1)

    files_to_analyze = sys.argv[1:]

    # 1. Initialize the Harmonizer
    harmonizer = PythonCodeHarmonizer()

    # 2. Run the analysis for all provided files
    for file_path in files_to_analyze:
        if os.path.exists(file_path):
            report = harmonizer.analyze_file(file_path)
            harmonizer.print_report(report)
        else:
            print(f"\nERROR: File not found: {file_path}")
            print("-" * 70)


if __name__ == "__main__":
    run_cli()
