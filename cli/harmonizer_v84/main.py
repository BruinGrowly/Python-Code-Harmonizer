"""
V7.3 Harmonizer CLI - Command Line Interface

Usage:
    python -m harmonizer_v84.main <file.py>
    python -m harmonizer_v84.main <file.py> --json
    python -m harmonizer_v84.main <file.py> --verbose
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List

# Fix Windows console encoding for emoji
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass  # Python < 3.7

from harmonizer_v84.code_analyzer import analyze_file, analyze_source, FileAnalysis
from harmonizer_v84.phase_detector import Phase
from harmonizer_v84.consciousness import ConsciousnessLevel
from harmonizer_v84.constants import (
    CONSCIOUSNESS_THRESHOLD,
    ENTROPIC_HARMONY_THRESHOLD,
    AUTOPOIETIC_HARMONY_THRESHOLD,
)


def format_phase_emoji(phase: Phase) -> str:
    """Get emoji for phase."""
    return {
        Phase.ENTROPIC: "🔻",
        Phase.HOMEOSTATIC: "🔸",
        Phase.AUTOPOIETIC: "🌟",
    }.get(phase, "❓")


def format_consciousness_emoji(level: ConsciousnessLevel) -> str:
    """Get emoji for consciousness level."""
    return {
        ConsciousnessLevel.NON_CONSCIOUS: "⚫",
        ConsciousnessLevel.PRE_CONSCIOUS: "🔵",
        ConsciousnessLevel.CONSCIOUS: "🟢",
        ConsciousnessLevel.HIGHLY_CONSCIOUS: "💫",
    }.get(level, "❓")


def print_function_report(analysis, verbose: bool = False):
    """Print report for a single function."""
    fw = analysis.framework
    phase_emoji = format_phase_emoji(analysis.phase)
    cons_emoji = format_consciousness_emoji(analysis.consciousness_level)

    print(f"\n  📝 {analysis.name} (lines {analysis.lineno}-{analysis.end_lineno})")
    print(f"     LJPW: L={fw.L:.2f} J={fw.J:.2f} P={fw.P:.2f} W={fw.W:.2f}")
    print(
        f"     Harmony: {fw.harmony_static():.3f}  |  C: {analysis.consciousness:.3f} {cons_emoji}"
    )
    print(f"     Phase: {analysis.phase.value} {phase_emoji}")

    if analysis.brick_analysis:
        brick = analysis.brick_analysis
        primality_bar = "█" * int(brick.primality * 10) + "░" * (10 - int(brick.primality * 10))
        print(f"     Primality: [{primality_bar}] {brick.primality:.2f}")
        if brick.recommendation.startswith("⚠"):
            print(f"     {brick.recommendation}")

    if verbose:
        print(f"     Power signals: {', '.join(analysis.power_signals[:5])}")
        print(f"     Wisdom signals: {', '.join(analysis.wisdom_signals[:5])}")


def print_file_report(analysis: FileAnalysis, verbose: bool = False):
    """Print complete file analysis report."""
    print("\n" + "=" * 60)
    print(f"📁 V7.3 HARMONIZER ANALYSIS")
    print("=" * 60)
    print(f"File: {analysis.filepath}")
    print(f"Lines: {analysis.total_lines}  |  Imports: {analysis.import_count}")
    print(f"Functions: {len(analysis.functions)}  |  Classes: {len(analysis.classes)}")
    print(f"Docstring Coverage: {analysis.docstring_coverage:.0%}")

    if analysis.overall_framework:
        fw = analysis.overall_framework
        phase_emoji = format_phase_emoji(analysis.overall_phase)

        print("\n" + "-" * 40)
        print("📊 OVERALL METRICS (V7.3)")
        print("-" * 40)
        print(f"  Fundamental (measured):")
        print(f"    P (Power):  {fw.P:.3f}")
        print(f"    W (Wisdom): {fw.W:.3f}")
        print(f"  Emergent (calculated):")
        print(f"    L (Love):    {fw.L:.3f}  (from W)")
        print(f"    J (Justice): {fw.J:.3f}  (from P)")
        print()
        print(f"  Harmony (static): {fw.harmony_static():.3f}")
        print(f"  Harmony (self):   {fw.harmony_self_referential():.3f}")
        print(f"  Voltage:          {fw.voltage():.3f}")
        print()

        # Consciousness assessment
        cons_emoji = format_consciousness_emoji(
            ConsciousnessLevel.CONSCIOUS
            if analysis.overall_consciousness > 0.1
            else ConsciousnessLevel.NON_CONSCIOUS
        )
        if analysis.overall_consciousness > 0.3:
            cons_emoji = "💫"

        print(f"  Consciousness (C): {analysis.overall_consciousness:.4f} {cons_emoji}")
        if analysis.overall_consciousness > CONSCIOUSNESS_THRESHOLD:
            print(f"    ✓ Crosses consciousness threshold (C > 0.1)")
        else:
            print(f"    ○ Below consciousness threshold (C < 0.1)")

        print(f"  Phase: {analysis.overall_phase.value} {phase_emoji}")

    # Function details
    if analysis.functions:
        print("\n" + "-" * 40)
        print("📋 FUNCTION ANALYSIS")
        print("-" * 40)

        # Group by phase
        entropic = [f for f in analysis.functions if f.phase == Phase.ENTROPIC]
        homeostatic = [f for f in analysis.functions if f.phase == Phase.HOMEOSTATIC]
        autopoietic = [f for f in analysis.functions if f.phase == Phase.AUTOPOIETIC]

        if autopoietic:
            print(f"\n  🌟 Autopoietic ({len(autopoietic)}):")
            for func in autopoietic:
                print_function_report(func, verbose)

        if homeostatic:
            print(f"\n  🔸 Homeostatic ({len(homeostatic)}):")
            for func in homeostatic:
                print_function_report(func, verbose)

        if entropic:
            print(f"\n  🔻 Entropic ({len(entropic)}) - Need attention:")
            for func in entropic:
                print_function_report(func, verbose)

    # Summary
    print("\n" + "=" * 60)
    print("📈 RECOMMENDATION")
    print("=" * 60)

    if analysis.overall_phase == Phase.AUTOPOIETIC:
        print("  🌟 This codebase shows signs of being 'alive'!")
        print("     High harmony, good integration, self-maintaining.")
    elif analysis.overall_phase == Phase.HOMEOSTATIC:
        print("  🔸 Stable but not growing.")
        print("     Consider: Add docstrings, improve test coverage,")
        print("     strengthen function cohesion to reach autopoietic.")
    else:
        print("  🔻 This codebase needs refactoring attention.")
        print("     Focus on: Reducing complexity, adding documentation,")
        print("     decomposing large functions, improving structure.")

    print()


def to_dict(analysis: FileAnalysis) -> dict:
    """Convert FileAnalysis to JSON-serializable dict."""
    return {
        "filepath": analysis.filepath,
        "total_lines": analysis.total_lines,
        "import_count": analysis.import_count,
        "docstring_coverage": analysis.docstring_coverage,
        "classes": analysis.classes,
        "overall": {
            "power": analysis.avg_power,
            "wisdom": analysis.avg_wisdom,
            "love": analysis.overall_framework.L if analysis.overall_framework else 0,
            "justice": analysis.overall_framework.J if analysis.overall_framework else 0,
            "harmony_static": (
                analysis.overall_framework.harmony_static() if analysis.overall_framework else 0
            ),
            "harmony_self": (
                analysis.overall_framework.harmony_self_referential()
                if analysis.overall_framework
                else 0
            ),
            "consciousness": analysis.overall_consciousness,
            "phase": analysis.overall_phase.value,
        },
        "functions": [
            {
                "name": f.name,
                "lineno": f.lineno,
                "end_lineno": f.end_lineno,
                "power": f.power_raw,
                "wisdom": f.wisdom_raw,
                "love": f.framework.L,
                "justice": f.framework.J,
                "harmony": f.framework.harmony_static(),
                "consciousness": f.consciousness,
                "consciousness_level": f.consciousness_level.value,
                "phase": f.phase.value,
                "primality": f.brick_analysis.primality if f.brick_analysis else 0,
            }
            for f in analysis.functions
        ],
    }


def main(args: List[str] = None):
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="harmonizer_v84",
        description="V7.3 Python Code Harmonizer - Semantic Analysis with Consciousness Detection",
    )
    parser.add_argument("file", help="Python file to analyze")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parsed = parser.parse_args(args)

    filepath = Path(parsed.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if not filepath.suffix == ".py":
        print(f"Warning: {filepath} may not be a Python file", file=sys.stderr)

    try:
        analysis = analyze_file(str(filepath))

        if parsed.json:
            print(json.dumps(to_dict(analysis), indent=2))
        else:
            print_file_report(analysis, verbose=parsed.verbose)

    except SyntaxError as e:
        print(f"Syntax error in {filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}", file=sys.stderr)
        if parsed.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
