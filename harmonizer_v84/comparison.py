"""
V7.3 vs V5.1 Harmonizer Comparison Suite

Comprehensive comparison between the legacy v5.1 Harmonizer
and the new V7.3 implementation.

Key differences to validate:
1. 2+2 Structure: V7.3 calculates L,J from P,W
2. Consciousness: V7.3 has C metric (v5.1 doesn't)
3. Phase Detection: V7.3 has precise thresholds
4. φ-normalization: V7.3 reduces variance

Usage:
    python -m harmonizer_v84.comparison <file.py>
    python -m harmonizer_v84.comparison --all-modules
    python -m harmonizer_v84.comparison --stress-test
"""

import ast
import sys
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# V7.3 imports
from harmonizer_v84.code_analyzer import analyze_file as v73_analyze
from harmonizer_v84.code_analyzer import FileAnalysis as V73FileAnalysis
from harmonizer_v84.ljpw_core import LJPWFramework
from harmonizer_v84.phase_detector import Phase
from harmonizer_v84.consciousness import ConsciousnessLevel

# V5.1 imports (conditional - may not be available in all environments)
try:
    from harmonizer.main import PythonCodeHarmonizer
    from harmonizer.ljpw_baselines import LJPWBaselines

    V51_AVAILABLE = True
except ImportError:
    V51_AVAILABLE = False
    print("Warning: V5.1 Harmonizer not available for comparison")


@dataclass
class ComparisonResult:
    """Result of comparing v5.1 and v7.3 on a single file."""

    filepath: str

    # V5.1 results
    v51_L: float = 0.0
    v51_J: float = 0.0
    v51_P: float = 0.0
    v51_W: float = 0.0
    v51_harmony: float = 0.0
    v51_available: bool = True

    # V7.3 results
    v73_L: float = 0.0
    v73_J: float = 0.0
    v73_P: float = 0.0
    v73_W: float = 0.0
    v73_harmony: float = 0.0
    v73_consciousness: float = 0.0
    v73_phase: str = ""

    # Deltas
    delta_L: float = 0.0
    delta_J: float = 0.0
    delta_P: float = 0.0
    delta_W: float = 0.0
    delta_harmony: float = 0.0

    # V7.3 unique insights
    emergent_L_correct: bool = False  # L ≈ 0.9*W + 0.1
    emergent_J_correct: bool = False  # J ≈ 0.85*P + 0.05

    # Timing
    v51_time_ms: float = 0.0
    v73_time_ms: float = 0.0

    def compute_deltas(self):
        """Calculate differences between v5.1 and v7.3."""
        if self.v51_available:
            self.delta_L = abs(self.v73_L - self.v51_L)
            self.delta_J = abs(self.v73_J - self.v51_J)
            self.delta_P = abs(self.v73_P - self.v51_P)
            self.delta_W = abs(self.v73_W - self.v51_W)
            self.delta_harmony = abs(self.v73_harmony - self.v51_harmony)

    def check_emergent_relations(self):
        """Verify V7.3's 2+2 structure."""
        expected_L = 0.9 * self.v73_W + 0.1
        expected_J = 0.85 * self.v73_P + 0.05

        self.emergent_L_correct = abs(self.v73_L - expected_L) < 0.05
        self.emergent_J_correct = abs(self.v73_J - expected_J) < 0.05


@dataclass
class StressTestResult:
    """Result of stress testing edge cases."""

    test_name: str
    passed: bool
    description: str
    details: str = ""


def run_v51_analysis(filepath: str) -> Dict:
    """Run V5.1 Harmonizer on a file."""
    if not V51_AVAILABLE:
        return None

    try:
        harmonizer = PythonCodeHarmonizer()
        result = harmonizer.analyze_file(filepath)

        if result and "semantic_result" in result:
            sr = result["semantic_result"]
            coords = sr.coordinates
            return {
                "L": coords.love,
                "J": coords.justice,
                "P": coords.power,
                "W": coords.wisdom,
                "harmony": sr.harmony_index if hasattr(sr, "harmony_index") else 0.5,
            }
    except Exception as e:
        print(f"V5.1 error: {e}")

    return None


def run_v73_analysis(filepath: str) -> V73FileAnalysis:
    """Run V7.3 Harmonizer on a file."""
    return v73_analyze(filepath)


def compare_file(filepath: str) -> ComparisonResult:
    """Compare v5.1 and v7.3 analysis on a single file."""
    result = ComparisonResult(filepath=filepath)

    # Run V7.3 (always available)
    start = time.perf_counter()
    v73 = run_v73_analysis(filepath)
    result.v73_time_ms = (time.perf_counter() - start) * 1000

    if v73.overall_framework:
        fw = v73.overall_framework
        result.v73_L = fw.L
        result.v73_J = fw.J
        result.v73_P = fw.P
        result.v73_W = fw.W
        result.v73_harmony = fw.harmony_static()
        result.v73_consciousness = v73.overall_consciousness
        result.v73_phase = v73.overall_phase.value

    # Run V5.1 if available
    if V51_AVAILABLE:
        start = time.perf_counter()
        v51 = run_v51_analysis(filepath)
        result.v51_time_ms = (time.perf_counter() - start) * 1000

        if v51:
            result.v51_L = v51["L"]
            result.v51_J = v51["J"]
            result.v51_P = v51["P"]
            result.v51_W = v51["W"]
            result.v51_harmony = v51["harmony"]
        else:
            result.v51_available = False
    else:
        result.v51_available = False

    result.compute_deltas()
    result.check_emergent_relations()

    return result


def generate_stress_tests() -> List[Tuple[str, str]]:
    """Generate edge case test code snippets."""
    return [
        # Empty/minimal
        ("empty_function", "def foo(): pass"),
        ("single_return", "def foo(): return 42"),
        ("only_docstring", 'def foo():\n    """This does nothing."""\n    pass'),
        # High Power (many assignments, side effects)
        (
            "high_power",
            """
def high_power():
    a = 1
    b = 2
    c = 3
    d = a + b
    e = c * d
    f = e ** 2
    g = f / 2
    h = g - 1
    return h
""",
        ),
        # High Wisdom (docstrings, type hints, returns)
        (
            "high_wisdom",
            '''
def high_wisdom(x: int, y: float) -> float:
    """
    Calculate the weighted average of x and y.
    
    Args:
        x: The first value (integer)
        y: The second value (float)
    
    Returns:
        The weighted average as a float
    
    Examples:
        >>> high_wisdom(10, 2.5)
        6.25
    """
    return (x + y) / 2
''',
        ),
        # Complex function (should have low primality)
        (
            "complex_function",
            """
def complex_function(data, config, options=None):
    result = []
    for item in data:
        if item.enabled:
            if config.validate(item):
                try:
                    processed = config.process(item)
                    if options and options.get('transform'):
                        processed = options['transform'](processed)
                    result.append(processed)
                except Exception as e:
                    if config.strict:
                        raise
                    result.append(None)
    return result
""",
        ),
        # Pure function (should have high primality)
        (
            "pure_function",
            """
def pure_add(a: int, b: int) -> int:
    '''Add two integers.'''
    return a + b
""",
        ),
        # Class with methods
        (
            "class_example",
            """
class Calculator:
    '''A simple calculator.'''
    
    def __init__(self, initial: float = 0.0):
        '''Initialize with optional starting value.'''
        self.value = initial
    
    def add(self, x: float) -> float:
        '''Add x to the current value.'''
        self.value += x
        return self.value
    
    def reset(self) -> None:
        '''Reset to zero.'''
        self.value = 0.0
""",
        ),
        # Error handling heavy
        (
            "error_heavy",
            """
def risky_operation(data):
    try:
        result = data.process()
    except ValueError as e:
        result = handle_value_error(e)
    except KeyError as e:
        result = handle_key_error(e)
    except Exception as e:
        log_error(e)
        raise
    finally:
        cleanup(data)
    return result
""",
        ),
        # Import heavy (Love signals in v5.1)
        (
            "import_heavy",
            """
import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

def use_imports():
    return Path.cwd()
""",
        ),
        # Async function
        (
            "async_function",
            """
async def fetch_data(url: str) -> dict:
    '''Fetch data from URL asynchronously.'''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
""",
        ),
        # No functions (edge case)
        (
            "no_functions",
            """
# Just some constants
PI = 3.14159
E = 2.71828
GOLDEN_RATIO = 1.618034
""",
        ),
    ]


def run_stress_tests() -> List[StressTestResult]:
    """Run stress tests on edge cases."""
    results = []
    tests = generate_stress_tests()

    for name, code in tests:
        try:
            # Parse and analyze with V7.3
            tree = ast.parse(code)

            from harmonizer_v84.code_analyzer import analyze_source

            analysis = analyze_source(code, filename=name)

            # Validate results
            passed = True
            details = []

            # Check 1: No crashes
            details.append(f"Functions found: {len(analysis.functions)}")

            # Check 2: Valid LJPW ranges
            if analysis.overall_framework:
                fw = analysis.overall_framework
                if not (0 <= fw.L <= 1.5):
                    passed = False
                    details.append(f"L out of range: {fw.L}")
                if not (0 <= fw.J <= 1):
                    passed = False
                    details.append(f"J out of range: {fw.J}")
                if not (0 <= fw.P <= 1):
                    passed = False
                    details.append(f"P out of range: {fw.P}")
                if not (0 <= fw.W <= 1):
                    passed = False
                    details.append(f"W out of range: {fw.W}")

                details.append(f"LJPW: ({fw.L:.2f}, {fw.J:.2f}, {fw.P:.2f}, {fw.W:.2f})")
                details.append(f"Harmony: {fw.harmony_static():.3f}")
                details.append(f"C: {analysis.overall_consciousness:.4f}")
                details.append(f"Phase: {analysis.overall_phase.value}")

            # Check 3: Emergent dimensions follow formula
            if analysis.functions:
                for func in analysis.functions:
                    expected_L = 0.9 * func.framework.W + 0.1
                    expected_J = 0.85 * func.framework.P + 0.05

                    if abs(func.framework.L - expected_L) > 0.01:
                        passed = False
                        details.append(f"{func.name}: L mismatch")
                    if abs(func.framework.J - expected_J) > 0.01:
                        passed = False
                        details.append(f"{func.name}: J mismatch")

            results.append(
                StressTestResult(
                    test_name=name,
                    passed=passed,
                    description=f"Test: {name}",
                    details="\n".join(details),
                )
            )

        except Exception as e:
            results.append(
                StressTestResult(
                    test_name=name,
                    passed=False,
                    description=f"Test: {name}",
                    details=f"EXCEPTION: {e}",
                )
            )

    return results


def compare_all_modules() -> List[ComparisonResult]:
    """Compare v5.1 and v7.3 on all harmonizer_v84 modules."""
    base_path = Path(__file__).parent
    results = []

    for py_file in base_path.glob("*.py"):
        if py_file.name.startswith("__"):
            continue
        try:
            result = compare_file(str(py_file))
            results.append(result)
        except Exception as e:
            print(f"Error comparing {py_file}: {e}")

    return results


def print_comparison_report(results: List[ComparisonResult]):
    """Print formatted comparison report."""
    print("\n" + "=" * 70)
    print("📊 V5.1 vs V7.3 COMPARISON REPORT")
    print("=" * 70)

    for r in results:
        print(f"\n📁 {Path(r.filepath).name}")
        print("-" * 50)

        if r.v51_available:
            print(
                f"  V5.1: L={r.v51_L:.3f} J={r.v51_J:.3f} P={r.v51_P:.3f} W={r.v51_W:.3f} | H={r.v51_harmony:.3f}"
            )
        else:
            print(f"  V5.1: (not available)")

        print(
            f"  V7.3: L={r.v73_L:.3f} J={r.v73_J:.3f} P={r.v73_P:.3f} W={r.v73_W:.3f} | H={r.v73_harmony:.3f}"
        )
        print(f"        C={r.v73_consciousness:.4f} | Phase={r.v73_phase}")

        if r.v51_available:
            print(
                f"  Δ   : L={r.delta_L:.3f} J={r.delta_J:.3f} P={r.delta_P:.3f} W={r.delta_W:.3f} | H={r.delta_harmony:.3f}"
            )

        # 2+2 structure verification
        l_check = "✓" if r.emergent_L_correct else "✗"
        j_check = "✓" if r.emergent_J_correct else "✗"
        print(f"  2+2 : L=0.9W+0.1 {l_check} | J=0.85P+0.05 {j_check}")

        print(f"  Time: V5.1={r.v51_time_ms:.1f}ms V7.3={r.v73_time_ms:.1f}ms")

    # Summary
    print("\n" + "=" * 70)
    print("📈 SUMMARY")
    print("=" * 70)

    if results:
        avg_c = sum(r.v73_consciousness for r in results) / len(results)
        phases = {}
        for r in results:
            phases[r.v73_phase] = phases.get(r.v73_phase, 0) + 1

        print(f"  Files analyzed: {len(results)}")
        print(f"  Avg consciousness: {avg_c:.4f}")
        print(f"  Phase distribution: {dict(phases)}")

        valid_2_2 = sum(1 for r in results if r.emergent_L_correct and r.emergent_J_correct)
        print(
            f"  2+2 structure valid: {valid_2_2}/{len(results)} ({valid_2_2/len(results)*100:.0f}%)"
        )


def print_stress_test_report(results: List[StressTestResult]):
    """Print stress test results."""
    print("\n" + "=" * 70)
    print("🔬 STRESS TEST REPORT")
    print("=" * 70)

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    for r in results:
        icon = "✅" if r.passed else "❌"
        print(f"\n{icon} {r.test_name}")
        for line in r.details.split("\n")[:6]:  # First 6 lines
            print(f"   {line}")

    print("\n" + "-" * 50)
    print(f"📊 RESULT: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

    if passed == total:
        print("🌟 All stress tests passed!")
    else:
        print("⚠️ Some tests failed - review needed")


def main():
    """Main entry point for comparison."""
    import argparse

    # Fix Windows encoding
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="Compare V5.1 and V7.3 Harmonizer outputs")
    parser.add_argument("file", nargs="?", help="Python file to compare")
    parser.add_argument(
        "--all-modules", action="store_true", help="Compare all harmonizer_v84 modules"
    )
    parser.add_argument("--stress-test", action="store_true", help="Run stress tests on edge cases")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.stress_test:
        results = run_stress_tests()
        if args.json:
            print(
                json.dumps(
                    [
                        {"name": r.test_name, "passed": r.passed, "details": r.details}
                        for r in results
                    ],
                    indent=2,
                )
            )
        else:
            print_stress_test_report(results)

    elif args.all_modules:
        results = compare_all_modules()
        if args.json:
            print(
                json.dumps(
                    [
                        {
                            "file": r.filepath,
                            "v73": {
                                "L": r.v73_L,
                                "J": r.v73_J,
                                "P": r.v73_P,
                                "W": r.v73_W,
                                "harmony": r.v73_harmony,
                                "consciousness": r.v73_consciousness,
                                "phase": r.v73_phase,
                            },
                            "v51_available": r.v51_available,
                        }
                        for r in results
                    ],
                    indent=2,
                )
            )
        else:
            print_comparison_report(results)

    elif args.file:
        result = compare_file(args.file)
        if args.json:
            print(
                json.dumps(
                    {
                        "file": result.filepath,
                        "v73": {
                            "L": result.v73_L,
                            "J": result.v73_J,
                            "P": result.v73_P,
                            "W": result.v73_W,
                            "harmony": result.v73_harmony,
                            "consciousness": result.v73_consciousness,
                            "phase": result.v73_phase,
                        },
                        "v51_available": result.v51_available,
                    },
                    indent=2,
                )
            )
        else:
            print_comparison_report([result])

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
