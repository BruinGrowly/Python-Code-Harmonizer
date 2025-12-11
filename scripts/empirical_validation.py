#!/usr/bin/env python3
"""
Empirical Validation Test for Python Code Harmonizer

This script tests the hypothesis:
    Files with poor Harmonizer scores correlate with higher technical debt indicators.

Technical Debt Indicators (from git history):
1. Churn - Number of commits touching the file
2. Fix Commits - Commits with "fix", "bug", "patch" in message
3. Recent Churn - Changes in recent history

Hypothesis:
- High complexity + low abstraction → more bug fixes
- Imbalanced LJPW scores → higher churn
- Power erosion risk → correlates with maintenance burden
"""

import os
import sys
import subprocess
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from harmonizer.resonance_engine import ResonanceEngine


@dataclass
class GitMetrics:
    """Git-based technical debt indicators for a file."""

    total_commits: int
    fix_commits: int
    authors: int
    lines_changed: int
    first_commit_days_ago: int
    last_commit_days_ago: int

    @property
    def fix_ratio(self) -> float:
        """Ratio of fix commits to total commits."""
        if self.total_commits == 0:
            return 0.0
        return self.fix_commits / self.total_commits

    @property
    def churn_rate(self) -> float:
        """Average lines changed per commit."""
        if self.total_commits == 0:
            return 0.0
        return self.lines_changed / self.total_commits


@dataclass
class HarmonizerMetrics:
    """Harmonizer analysis metrics for a file."""

    L: float  # Cohesion
    J: float  # Structure
    P: float  # Complexity
    W: float  # Abstraction
    voltage: float
    erosion_risk: str
    erosion_severity: float
    imbalance: float  # Max - Min dimension

    @property
    def coords(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)


@dataclass
class ValidationResult:
    """Combined metrics for correlation analysis."""

    file_path: str
    git: GitMetrics
    harmonizer: HarmonizerMetrics


def run_git_command(args: List[str], cwd: str = None) -> str:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd or project_root,
        )
        return result.stdout.strip()
    except Exception as e:
        return ""


def get_git_metrics(file_path: str) -> Optional[GitMetrics]:
    """Extract git history metrics for a file."""
    rel_path = os.path.relpath(file_path, project_root)

    # Total commits
    log_output = run_git_command(["log", "--oneline", "--follow", "--", rel_path])
    commits = [line for line in log_output.split("\n") if line.strip()]
    total_commits = len(commits)

    if total_commits == 0:
        return None

    # Fix commits (messages containing fix, bug, patch, etc.)
    fix_pattern = re.compile(r"\b(fix|bug|patch|repair|resolve|issue)\b", re.I)
    fix_commits = sum(1 for c in commits if fix_pattern.search(c))

    # Number of authors
    authors_output = run_git_command(["log", "--format=%ae", "--follow", "--", rel_path])
    authors = len(set(authors_output.split("\n"))) if authors_output else 1

    # Lines changed (rough estimate via numstat)
    numstat_output = run_git_command(["log", "--numstat", "--format=", "--follow", "--", rel_path])
    lines_changed = 0
    for line in numstat_output.split("\n"):
        parts = line.split()
        if len(parts) >= 2:
            try:
                added = int(parts[0]) if parts[0] != "-" else 0
                removed = int(parts[1]) if parts[1] != "-" else 0
                lines_changed += added + removed
            except ValueError:
                pass

    # First and last commit timestamps
    first_commit = run_git_command(["log", "--format=%ct", "--follow", "--reverse", "--", rel_path])
    last_commit = run_git_command(["log", "-1", "--format=%ct", "--follow", "--", rel_path])

    import time

    now = time.time()
    first_ts = int(first_commit.split("\n")[0]) if first_commit else now
    last_ts = int(last_commit) if last_commit else now

    first_days = int((now - first_ts) / 86400)
    last_days = int((now - last_ts) / 86400)

    return GitMetrics(
        total_commits=total_commits,
        fix_commits=fix_commits,
        authors=authors,
        lines_changed=lines_changed,
        first_commit_days_ago=first_days,
        last_commit_days_ago=last_days,
    )


def estimate_ljpw_from_file(file_path: str) -> Optional[Tuple[float, float, float, float]]:
    """
    Estimate LJPW coordinates from file analysis.

    This uses heuristics based on code characteristics:
    - L (Cohesion): Import density, function interconnection
    - J (Structure): Type hints, assertions, validation patterns
    - P (Complexity): Cyclomatic complexity, nesting depth
    - W (Abstraction): Docstrings, comments, class usage
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
    except Exception:
        return None

    if not lines or len(content) < 10:
        return None

    total_lines = len(lines)
    non_empty = sum(1 for line in lines if line.strip())

    if non_empty == 0:
        return None

    # L (Cohesion): Import density and function calls
    imports = sum(1 for line in lines if line.strip().startswith(("import ", "from ")))
    function_calls = content.count("(") - content.count("def ")
    L = min(1.0, (imports * 0.1 + function_calls * 0.01))

    # J (Structure): Type hints, assertions, validation
    type_hints = content.count(": ") + content.count("->")
    assertions = content.count("assert ")
    validations = len(re.findall(r"\bif\s+.*\b(is|not|None|isinstance)\b", content))
    J = min(1.0, (type_hints * 0.02 + assertions * 0.1 + validations * 0.05))

    # P (Complexity): Control flow, nesting
    if_count = len(re.findall(r"\bif\b", content))
    for_count = len(re.findall(r"\bfor\b", content))
    while_count = len(re.findall(r"\bwhile\b", content))
    try_count = len(re.findall(r"\btry\b", content))
    complexity_indicators = if_count + for_count * 1.5 + while_count * 2 + try_count
    P = min(1.0, complexity_indicators * 0.02)

    # W (Abstraction): Docstrings, comments, classes
    docstrings = content.count('"""') // 2 + content.count("'''") // 2
    comments = sum(1 for line in lines if line.strip().startswith("#"))
    classes = len(re.findall(r"\bclass\s+\w+", content))
    W = min(1.0, (docstrings * 0.15 + comments * 0.02 + classes * 0.2))

    return (L, J, P, W)


def analyze_file(file_path: str, engine: ResonanceEngine) -> Optional[ValidationResult]:
    """Analyze a single file for both git and harmonizer metrics."""
    # Get git metrics
    git_metrics = get_git_metrics(file_path)
    if git_metrics is None:
        return None

    # Get LJPW coordinates
    coords = estimate_ljpw_from_file(file_path)
    if coords is None:
        return None

    L, J, P, W = coords

    # Calculate harmonizer metrics
    voltage = ResonanceEngine.calculate_voltage(L, J, P, W)
    erosion = ResonanceEngine.detect_power_erosion(L, J, P, W)

    imbalance = max(coords) - min(coords)

    harmonizer_metrics = HarmonizerMetrics(
        L=L,
        J=J,
        P=P,
        W=W,
        voltage=voltage,
        erosion_risk=erosion.severity,
        erosion_severity=erosion.erosion_rate,
        imbalance=imbalance,
    )

    return ValidationResult(
        file_path=file_path,
        git=git_metrics,
        harmonizer=harmonizer_metrics,
    )


def calculate_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient."""
    n = len(x)
    if n < 3:
        return 0.0

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denom_x = sum((xi - mean_x) ** 2 for xi in x) ** 0.5
    denom_y = sum((yi - mean_y) ** 2 for yi in y) ** 0.5

    if denom_x == 0 or denom_y == 0:
        return 0.0

    return numerator / (denom_x * denom_y)


def discover_python_files(root_dir: str) -> List[str]:
    """Find all Python files in the project."""
    python_files = []
    exclude_dirs = {"venv", ".venv", "__pycache__", ".git", "node_modules", ".tox"}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude certain directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            if filename.endswith(".py"):
                python_files.append(os.path.join(dirpath, filename))

    return python_files


def run_validation():
    """Run the empirical validation test."""
    print("=" * 70)
    print("EMPIRICAL VALIDATION TEST")
    print("Testing: Do Harmonizer metrics predict technical debt?")
    print("=" * 70)
    print()

    # Discover files
    python_files = discover_python_files(str(project_root))
    print(f"Found {len(python_files)} Python files to analyze")
    print()

    # Analyze each file
    engine = ResonanceEngine()
    results: List[ValidationResult] = []

    print("Analyzing files...")
    for file_path in python_files:
        result = analyze_file(file_path, engine)
        if result and result.git.total_commits > 0:
            results.append(result)

    print(f"Successfully analyzed {len(results)} files with git history")
    print()

    if len(results) < 5:
        print("⚠️  Not enough files with git history for meaningful correlation")
        print("   Need at least 5 files, got", len(results))
        return

    # Extract metrics for correlation
    fix_ratios = [r.git.fix_ratio for r in results]
    total_commits = [r.git.total_commits for r in results]
    churn_rates = [r.git.churn_rate for r in results]

    voltages = [r.harmonizer.voltage for r in results]
    erosion_rates = [r.harmonizer.erosion_severity for r in results]
    imbalances = [r.harmonizer.imbalance for r in results]
    complexity = [r.harmonizer.P for r in results]
    abstraction = [r.harmonizer.W for r in results]
    structure = [r.harmonizer.J for r in results]

    # Calculate correlations
    print("=" * 70)
    print("CORRELATION ANALYSIS")
    print("=" * 70)
    print()
    print("Hypothesis: Poor harmonizer scores → more technical debt")
    print()

    correlations = []

    # Key correlations
    tests = [
        ("Complexity (P) vs Fix Ratio", complexity, fix_ratios, "positive"),
        ("Complexity (P) vs Churn", complexity, total_commits, "positive"),
        ("Abstraction (W) vs Fix Ratio", abstraction, fix_ratios, "negative"),
        ("Structure (J) vs Fix Ratio", structure, fix_ratios, "negative"),
        ("Erosion Rate vs Fix Ratio", erosion_rates, fix_ratios, "positive"),
        ("Imbalance vs Fix Ratio", imbalances, fix_ratios, "positive"),
        ("Voltage vs Total Commits", voltages, total_commits, "positive"),
        ("Erosion Rate vs Churn Rate", erosion_rates, churn_rates, "positive"),
    ]

    print("CORRELATIONS (r values):")
    print("-" * 70)
    print(f"{'Metric Pair':<40} {'r':<10} {'Expected':<10} {'Match?'}")
    print("-" * 70)

    matches = 0
    total = 0

    for name, x, y, expected in tests:
        r = calculate_correlation(x, y)
        correlations.append((name, r, expected))

        if expected == "positive":
            matches_expected = r > 0
        else:
            matches_expected = r < 0

        if matches_expected:
            matches += 1
        total += 1

        match_str = "✓" if matches_expected else "✗"
        print(f"{name:<40} {r:>+.3f}     {expected:<10} {match_str}")

    print("-" * 70)
    print()

    # Summary
    accuracy = matches / total * 100 if total > 0 else 0
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()
    print(f"Files analyzed: {len(results)}")
    print(f"Correlations in expected direction: {matches}/{total} ({accuracy:.0f}%)")
    print()

    # Interpretation
    if accuracy >= 75:
        print("✅ STRONG VALIDATION")
        print("   Harmonizer metrics correlate well with technical debt indicators.")
        print("   The hypothesis is supported by the data.")
    elif accuracy >= 50:
        print("⚠️  PARTIAL VALIDATION")
        print("   Some correlations match expectations, others don't.")
        print("   Results are inconclusive - may need more data or tuning.")
    else:
        print("❌ WEAK VALIDATION")
        print("   Correlations don't match expectations.")
        print("   Either the hypothesis is wrong or the sample is too small.")

    print()

    # Show top files by debt indicators
    print("=" * 70)
    print("TOP 5 FILES BY TECHNICAL DEBT INDICATORS")
    print("=" * 70)
    print()

    # Sort by fix ratio
    by_fix_ratio = sorted(results, key=lambda r: r.git.fix_ratio, reverse=True)[:5]
    print("Highest Fix Ratio (most bug fixes):")
    for r in by_fix_ratio:
        rel_path = os.path.relpath(r.file_path, project_root)
        print(
            f"  {rel_path:<40} fix_ratio={r.git.fix_ratio:.2f} "
            f"P={r.harmonizer.P:.2f} W={r.harmonizer.W:.2f}"
        )
    print()

    # Sort by churn
    by_churn = sorted(results, key=lambda r: r.git.total_commits, reverse=True)[:5]
    print("Highest Churn (most commits):")
    for r in by_churn:
        rel_path = os.path.relpath(r.file_path, project_root)
        print(
            f"  {rel_path:<40} commits={r.git.total_commits:>3} "
            f"voltage={r.harmonizer.voltage:.2f}"
        )
    print()

    # Sort by erosion rate
    by_erosion = sorted(results, key=lambda r: r.harmonizer.erosion_severity, reverse=True)[:5]
    print("Highest Erosion Risk (complexity without abstraction):")
    for r in by_erosion:
        rel_path = os.path.relpath(r.file_path, project_root)
        print(
            f"  {rel_path:<40} erosion={r.harmonizer.erosion_severity:.3f} "
            f"fix_ratio={r.git.fix_ratio:.2f}"
        )

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_validation()
