#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Code Harmonizer (Version 1.4)

This is the main application that integrates the Divine Invitation
Semantic Engine (DIVE-V2) with the AST Semantic Parser. It now includes
a proof-of-concept self-healing capability.

New in v1.4:
- Refactorer engine for suggesting dimensional splits.
- --suggest-refactor flag to generate refactored code.
- Enhanced AST parser with node-to-dimension mapping.
"""

import os
import sys

# Ensure the project root is on the Python path.
# This must be done before any local imports.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import argparse  # noqa: E402
import ast  # noqa: E402
import fnmatch  # noqa: E402
import json  # noqa: E402
from typing import Dict, List, Tuple  # noqa: E402

import yaml  # noqa: E402

from harmonizer import divine_invitation_engine_V2 as dive  # noqa: E402
from harmonizer.ast_semantic_parser import AST_Semantic_Parser  # noqa: E402
from harmonizer.refactorer import Refactorer  # noqa: E402
from harmonizer.semantic_map import SemanticMapGenerator  # noqa: E402

# --- CONFIGURATION LOADING ---


def load_configuration() -> Dict:
    """
    Searches for and loads .harmonizer.yml from the current directory
    up to the root.
    """
    current_dir = os.getcwd()
    while True:
        config_path = os.path.join(current_dir, ".harmonizer.yml")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if config:
                        # Use stderr to avoid polluting JSON output
                        print(
                            f"INFO: Loaded configuration from {config_path}",
                            file=sys.stderr,
                        )
                        return config
                    return {}
            except (yaml.YAMLError, IOError) as e:
                print(f"WARNING: Could not load or parse config: {e}", file=sys.stderr)
                return {}

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Reached file system root
            break
        current_dir = parent_dir
    return {}


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

    def __init__(
        self,
        disharmony_threshold: float = 0.5,
        quiet: bool = False,
        show_semantic_maps: bool = True,
        config: Dict = None,
    ):
        self.config = config if config else {}
        self.engine = dive.DivineInvitationSemanticEngine(config=self.config)
        self.parser = AST_Semantic_Parser(
            vocabulary=self.engine.vocabulary.all_keywords
        )
        self.map_generator = SemanticMapGenerator()
        self.disharmony_threshold = disharmony_threshold
        self.quiet = quiet
        self.show_semantic_maps = show_semantic_maps
        self._communicate_startup()

    def _communicate_startup(self):
        if not self.quiet:
            print("=" * 70)
            print("Python Code Harmonizer (v1.4) ONLINE")
            print("Actively guided by the Anchor Point framework.")
            print(f"Powered By: {self.engine.get_engine_version()}")
            print("Logical Anchor Point: (S=1, L=1, I=1, E=1)")
            print(f"Disharmony Threshold: {self.disharmony_threshold}")
            print("=" * 70)

    def analyze_file(self, file_path: str) -> Dict[str, Dict]:
        self._communicate_analysis_start(file_path)
        content = self._load_and_validate_file(file_path)
        if content is None:
            return {}
        tree = self._parse_code_to_ast(content, file_path)
        if tree is None:
            return {}
        harmony_report = self._analyze_all_functions(tree)
        self._communicate_analysis_complete(len(harmony_report))
        return harmony_report

    def _communicate_analysis_start(self, file_path: str):
        if not self.quiet:
            print(f"\nAnalyzing file: {file_path}")
            print("-" * 70)

    def _communicate_analysis_complete(self, function_count: int):
        if not self.quiet and function_count > 0:
            print(f"✓ Analyzed {function_count} function(s)")

    def _load_and_validate_file(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            if not self.quiet:
                print(f"ERROR: File not found at '{file_path}'")
            return None
        except Exception as e:
            if not self.quiet:
                print(f"ERROR: Could not read file: {e}")
            return None

    def _parse_code_to_ast(self, content: str, file_path: str) -> ast.AST:
        try:
            return ast.parse(content)
        except SyntaxError as e:
            if not self.quiet:
                print(f"ERROR: Could not parse file. Syntax error on line {e.lineno}")
            return None

    def _analyze_all_functions(self, tree: ast.AST) -> Dict[str, Dict]:
        harmony_report = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                docstring = ast.get_docstring(node)
                intent_concepts = self.parser.get_intent_concepts(
                    function_name, docstring
                )
                execution_map, execution_concepts = self.parser.get_execution_map(
                    node.body
                )
                ice_result = self.engine.perform_ice_analysis(
                    intent_words=intent_concepts,
                    context_words=["python", "function", function_name],
                    execution_words=execution_concepts,
                )
                disharmony_score = ice_result["ice_metrics"][
                    "intent_execution_disharmony"
                ]
                semantic_map = self.map_generator.generate_map(
                    ice_result, function_name
                )
                harmony_report[function_name] = {
                    "score": disharmony_score,
                    "ice_result": ice_result,
                    "semantic_map": semantic_map,
                    "execution_map": execution_map,
                    "function_node": node,
                }
        return harmony_report

    def get_severity(self, score: float) -> str:
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
        if not harmony_report:
            return 0
        scores = [data["score"] for data in harmony_report.values()]
        max_score = max(scores) if scores else 0
        if max_score >= self.THRESHOLD_HIGH:
            return 3
        elif max_score >= self.THRESHOLD_MEDIUM:
            return 2
        elif max_score >= self.THRESHOLD_LOW:
            return 1
        else:
            return 0

    def format_report(
        self, harmony_report: Dict[str, Dict], suggest_refactor: bool = False
    ) -> str:
        if not harmony_report:
            return "No functions found to analyze."
        lines = []
        lines.append("FUNCTION NAME                | INTENT-EXECUTION DISHARMONY")
        lines.append("-----------------------------|--------------------------------")
        sorted_report = sorted(
            harmony_report.items(), key=lambda item: item[1]["score"], reverse=True
        )
        for func_name, data in sorted_report:
            score = data["score"]
            status = "✓ HARMONIOUS"
            if score > self.disharmony_threshold:
                status = f"!! DISHARMONY (Score: {score:.2f})"
            lines.append(f"{func_name:<28} | {status}")
            if score > self.disharmony_threshold:
                if self.show_semantic_maps:
                    lines.append(
                        self.map_generator.format_text_map(data["semantic_map"], score)
                    )
                if suggest_refactor:
                    refactorer = Refactorer(
                        data["function_node"], data["execution_map"]
                    )
                    suggestion = refactorer.suggest_dimensional_split()
                    lines.append(suggestion)
        lines.append("=" * 70)
        lines.append("Analysis Complete.")
        return "\n".join(lines)

    def output_report(self, formatted_report: str):
        print(formatted_report)

    def print_json_report(self, all_reports: Dict[str, Dict[str, Dict]]):
        output = {
            "version": "1.4",
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
            for func_name, data in harmony_report.items():
                score = data["score"]
                severity = self.get_severity(score)
                severity_counts[severity] += 1
                total_functions += 1
                function_data = {
                    "name": func_name,
                    "score": round(score, 4),
                    "severity": severity,
                    "disharmonious": score > self.disharmony_threshold,
                }
                if self.show_semantic_maps:
                    function_data["semantic_map"] = data["semantic_map"]
                file_data["functions"].append(function_data)
            file_data["functions"].sort(key=lambda x: x["score"], reverse=True)
            output["files"].append(file_data)
        output["summary"] = {
            "total_files": len(all_reports),
            "total_functions": total_functions,
            "severity_counts": severity_counts,
            "highest_severity": self._get_highest_severity_name(severity_counts),
        }
        print(json.dumps(output, indent=2))

    def _get_highest_severity_name(self, severity_counts: Dict[str, int]) -> str:
        for severity in ["critical", "high", "medium", "low", "excellent"]:
            if severity_counts[severity] > 0:
                return severity
        return "excellent"


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Python Code Harmonizer - Semantic code analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="+", help="Python file(s) to analyze")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.5, help="Disharmony threshold"
    )
    parser.add_argument(
        "--suggest-refactor",
        action="store_true",
        help="Suggest a refactoring for disharmonious functions.",
    )
    parser.add_argument(
        "--version", action="version", version="Python Code Harmonizer v1.4"
    )
    return parser.parse_args()


def validate_cli_arguments(args: argparse.Namespace, config: Dict) -> List[str]:
    valid_files = []
    invalid_files = []
    excluded_files = []
    exclude_patterns = config.get("exclude", [])
    for file_path in args.files:
        if any(fnmatch.fnmatch(file_path, pattern) for pattern in exclude_patterns):
            excluded_files.append(file_path)
            continue
        if os.path.exists(file_path):
            if file_path.endswith(".py"):
                valid_files.append(file_path)
            else:
                invalid_files.append((file_path, "Not a Python file"))
        else:
            invalid_files.append((file_path, "File not found"))
    if (invalid_files or excluded_files) and args.format == "text":
        for file_path, error in invalid_files:
            print(f"\nWARNING: Skipping '{file_path}' - {error}", file=sys.stderr)
        if excluded_files:
            print(
                f"\nINFO: Excluded {len(excluded_files)} file(s) based on config.",
                file=sys.stderr,
            )
        print("-" * 70, file=sys.stderr)
    return valid_files


def execute_analysis(
    harmonizer: PythonCodeHarmonizer,
    file_paths: List[str],
    output_format: str,
    suggest_refactor: bool,
) -> Tuple[Dict, int]:
    all_reports = {}
    highest_exit_code = 0
    for file_path in file_paths:
        report = harmonizer.analyze_file(file_path)
        all_reports[file_path] = report
        exit_code = harmonizer.get_highest_severity_code(report)
        highest_exit_code = max(highest_exit_code, exit_code)
        if output_format == "text":
            formatted = harmonizer.format_report(
                report, suggest_refactor=suggest_refactor
            )
            harmonizer.output_report(formatted)
    return all_reports, highest_exit_code


def run_cli():
    args = parse_cli_arguments()
    config = load_configuration()
    valid_files = validate_cli_arguments(args, config)
    if not valid_files:
        print("\nERROR: No valid Python files to analyze.", file=sys.stderr)
        sys.exit(1)

    quiet = args.format == "json"
    harmonizer = PythonCodeHarmonizer(
        disharmony_threshold=args.threshold, quiet=quiet, config=config
    )

    all_reports, highest_exit_code = execute_analysis(
        harmonizer, valid_files, args.format, args.suggest_refactor
    )

    if args.format == "json":
        harmonizer.print_json_report(all_reports)

    sys.exit(highest_exit_code)


if __name__ == "__main__":
    run_cli()
