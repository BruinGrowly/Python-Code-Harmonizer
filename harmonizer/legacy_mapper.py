#!/usr/bin/env python3
"""
Legacy Code Mapper - Advanced semantic analysis of entire codebases

Maps files to LJPW space, finds natural clusters, detects architectural smells,
generates complexity heatmaps, and provides refactoring recommendations.
"""

import os
import glob
import subprocess
from statistics import mean, stdev
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

from harmonizer.main import PythonCodeHarmonizer


@dataclass
class FileAnalysis:
    """Semantic analysis of a single file"""

    path: str
    coordinates: Tuple[float, float, float, float]  # (L, J, P, W)
    function_count: int
    avg_disharmony: float
    dominant_dimension: str
    max_disharmony: float = 0.0
    min_disharmony: float = 0.0
    dimension_spread: float = 0.0  # How evenly distributed across dimensions


@dataclass
class ArchitecturalSmell:
    """Detected architectural problem"""

    smell_type: str
    file_path: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    impact: float  # 0-1 score
    recommendation: str


@dataclass
class RefactoringOpportunity:
    """Suggested refactoring"""

    file_path: str
    opportunity_type: str
    complexity_reduction: float  # Estimated % reduction
    impact_score: float  # 0-1 score
    description: str
    suggested_actions: List[str] = field(default_factory=list)


class LegacyCodeMapper:
    """Advanced codebase semantic analysis"""

    def __init__(self, codebase_path: str, quiet: bool = False):
        self.codebase_path = codebase_path
        self.harmonizer = PythonCodeHarmonizer(quiet=quiet)
        self.file_analyses: Dict[str, FileAnalysis] = {}
        self.architectural_smells: List[ArchitecturalSmell] = []
        self.refactoring_opportunities: List[RefactoringOpportunity] = []

    def analyze_codebase(self, show_progress: bool = True) -> Dict:
        """Analyze entire codebase and generate comprehensive report"""
        if show_progress:
            print(f"🔍 Analyzing codebase: {self.codebase_path}")
            print("=" * 70)

        # Find all Python files
        python_files = self._find_python_files()
        if show_progress:
            print(f"Found {len(python_files)} Python files\n")

        # Analyze each file
        for i, file_path in enumerate(python_files):
            if show_progress and len(python_files) > 10:
                print(f"  [{i+1}/{len(python_files)}] Analyzing...", end="\r")

            try:
                analysis = self._analyze_file(file_path)
                if analysis:
                    self.file_analyses[file_path] = analysis
            except Exception as e:
                if show_progress:
                    print(f"⚠️  Skipped {file_path}: {e}")

        if show_progress:
            print(f"\n✅ Analyzed {len(self.file_analyses)} files successfully")
            print("=" * 70)

        # Perform advanced analysis
        self._detect_architectural_smells()
        self._identify_refactoring_opportunities()

        return self._generate_comprehensive_report()

    def _find_python_files(self) -> List[str]:
        """Find all Python files in codebase"""
        pattern = os.path.join(self.codebase_path, "**/*.py")
        files = glob.glob(pattern, recursive=True)

        # Filter out common directories to skip
        skip_dirs = {"venv", ".venv", "__pycache__", ".git", "build", "dist", ".pytest_cache"}
        filtered = []

        for f in files:
            if not any(skip in f for skip in skip_dirs):
                filtered.append(f)

        return filtered

    def _analyze_file(self, file_path: str) -> Optional[FileAnalysis]:
        """Analyze single file and compute semantic coordinates"""
        results = self.harmonizer.analyze_file(file_path)

        if not results:
            return None

        # Collect execution coordinates from all functions
        all_coords = []
        all_disharmony = []

        for func_name, data in results.items():
            ice_result = data.get("ice_result", {})
            ice_components = ice_result.get("ice_components", {})
            execution_result = ice_components.get("execution")

            if execution_result:
                coords = execution_result.coordinates
                all_coords.append((coords.love, coords.justice, coords.power, coords.wisdom))

            disharmony = data.get("score", 0)
            all_disharmony.append(disharmony)

        if not all_coords:
            return None

        # Average coordinates across all functions
        avg_l = mean([c[0] for c in all_coords])
        avg_j = mean([c[1] for c in all_coords])
        avg_p = mean([c[2] for c in all_coords])
        avg_w = mean([c[3] for c in all_coords])

        avg_coords = (avg_l, avg_j, avg_p, avg_w)

        # Determine dominant dimension
        dims = {"Love": avg_l, "Justice": avg_j, "Power": avg_p, "Wisdom": avg_w}
        dominant = max(dims, key=dims.get)

        # Calculate dimension spread (how balanced)
        dimension_spread = max(dims.values()) - min(dims.values())

        return FileAnalysis(
            path=file_path,
            coordinates=avg_coords,
            function_count=len(results),
            avg_disharmony=mean(all_disharmony) if all_disharmony else 0,
            max_disharmony=max(all_disharmony) if all_disharmony else 0,
            min_disharmony=min(all_disharmony) if all_disharmony else 0,
            dominant_dimension=dominant,
            dimension_spread=dimension_spread,
        )

    def _detect_architectural_smells(self):
        """Detect architectural problems"""
        if not self.file_analyses:
            return

        for file_path, analysis in self.file_analyses.items():
            rel_path = os.path.relpath(file_path, self.codebase_path)

            # Smell 1: God File (too many functions)
            if analysis.function_count > 30:
                self.architectural_smells.append(
                    ArchitecturalSmell(
                        smell_type="God File",
                        file_path=rel_path,
                        severity="HIGH" if analysis.function_count > 50 else "MEDIUM",
                        description=f"File has {analysis.function_count} functions (threshold: 30)",
                        impact=min(1.0, analysis.function_count / 100),
                        recommendation=f"Split into smaller, focused modules by semantic dimension",
                    )
                )

            # Smell 2: Semantic Confusion (no clear purpose)
            if analysis.dimension_spread < 0.15:
                self.architectural_smells.append(
                    ArchitecturalSmell(
                        smell_type="Semantic Confusion",
                        file_path=rel_path,
                        severity="MEDIUM",
                        description=f"File has no clear dominant dimension (spread: {analysis.dimension_spread:.2f})",
                        impact=0.6,
                        recommendation="Refactor to focus on single semantic dimension",
                    )
                )

            # Smell 3: High Disharmony (semantic bugs)
            if analysis.avg_disharmony > 0.7:
                self.architectural_smells.append(
                    ArchitecturalSmell(
                        smell_type="High Disharmony",
                        file_path=rel_path,
                        severity="CRITICAL" if analysis.avg_disharmony > 1.0 else "HIGH",
                        description=f"Average disharmony: {analysis.avg_disharmony:.2f} (threshold: 0.7)",
                        impact=min(1.0, analysis.avg_disharmony / 1.5),
                        recommendation="Review function names - many don't match implementation",
                    )
                )

            # Smell 4: Mixed Concerns (should be multiple files)
            l, j, p, w = analysis.coordinates
            active_dimensions = sum([1 for coord in [l, j, p, w] if coord > 0.2])
            if active_dimensions >= 3 and analysis.function_count > 15:
                self.architectural_smells.append(
                    ArchitecturalSmell(
                        smell_type="Mixed Concerns",
                        file_path=rel_path,
                        severity="MEDIUM",
                        description=f"File operates in {active_dimensions} semantic dimensions with {analysis.function_count} functions",
                        impact=0.65,
                        recommendation=f"Split by dimension: L={l:.2f}, J={j:.2f}, P={p:.2f}, W={w:.2f}",
                    )
                )

    def _identify_refactoring_opportunities(self):
        """Identify high-impact refactoring targets"""
        if not self.file_analyses:
            return

        # Sort by potential impact (disharmony * function count)
        ranked_files = sorted(
            self.file_analyses.items(),
            key=lambda x: x[1].avg_disharmony * x[1].function_count,
            reverse=True,
        )

        for file_path, analysis in ranked_files[:10]:  # Top 10
            rel_path = os.path.relpath(file_path, self.codebase_path)

            if analysis.avg_disharmony < 0.5:
                continue  # Skip well-harmonized files

            # Calculate impact score
            impact_score = (analysis.avg_disharmony * 0.6 + analysis.function_count / 100 * 0.4)

            # Estimate complexity reduction
            complexity_reduction = min(80, int((analysis.avg_disharmony - 0.3) * 100))

            suggestions = []

            # Specific suggestions based on analysis
            if analysis.function_count > 20:
                suggestions.append(f"Split into {analysis.function_count // 15 + 1} smaller modules")

            if analysis.dimension_spread < 0.2:
                suggestions.append("Focus file on single semantic dimension")

            l, j, p, w = analysis.coordinates
            dominant_val = max(l, j, p, w)
            if dominant_val < 0.4:
                suggestions.append("Clarify file purpose - currently lacks clear focus")
            else:
                dim_name = analysis.dominant_dimension
                suggestions.append(f"Strengthen {dim_name} focus (currently {dominant_val:.0%})")

            if analysis.max_disharmony > 1.0:
                suggestions.append("Fix critical disharmony functions first (score > 1.0)")

            self.refactoring_opportunities.append(
                RefactoringOpportunity(
                    file_path=rel_path,
                    opportunity_type="Semantic Realignment",
                    complexity_reduction=complexity_reduction,
                    impact_score=min(1.0, impact_score),
                    description=f"High-impact refactoring target: {analysis.function_count} functions, {analysis.avg_disharmony:.2f} avg disharmony",
                    suggested_actions=suggestions,
                )
            )

    def _generate_comprehensive_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        clusters = self._cluster_by_dimension()
        outliers = self._find_outliers()

        if self.file_analyses:
            overall_disharmony = mean([f.avg_disharmony for f in self.file_analyses.values()])
        else:
            overall_disharmony = 0.0

        return {
            "total_files": len(self.file_analyses),
            "clusters": clusters,
            "outliers": outliers,
            "overall_disharmony": overall_disharmony,
            "architectural_smells": self.architectural_smells,
            "refactoring_opportunities": self.refactoring_opportunities,
        }

    def _cluster_by_dimension(self) -> Dict[str, List[FileAnalysis]]:
        """Group files by dominant semantic dimension"""
        clusters = defaultdict(list)
        for analysis in self.file_analyses.values():
            clusters[analysis.dominant_dimension].append(analysis)
        return dict(clusters)

    def _find_outliers(self, threshold: float = 0.15) -> List[FileAnalysis]:
        """Find files with no clear dominant dimension"""
        outliers = []
        for analysis in self.file_analyses.values():
            if analysis.dimension_spread < threshold:
                outliers.append(analysis)
        return outliers

    def generate_complexity_heatmap(self) -> str:
        """Generate ASCII complexity heatmap"""
        if not self.file_analyses:
            return "No files analyzed"

        heatmap = []
        heatmap.append("\n" + "=" * 70)
        heatmap.append("COMPLEXITY HEATMAP (Darker = Higher Disharmony)")
        heatmap.append("=" * 70)

        # Group by directory
        by_directory = defaultdict(list)
        for file_path, analysis in self.file_analyses.items():
            dir_name = os.path.dirname(file_path)
            if not dir_name:
                dir_name = "."
            by_directory[dir_name].append((os.path.basename(file_path), analysis))

        # Generate heatmap
        for dir_name in sorted(by_directory.keys()):
            files = by_directory[dir_name]
            avg_disharmony = mean([f[1].avg_disharmony for f in files])

            # Visual bar (0-10 blocks)
            bar_length = int(avg_disharmony * 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)

            rel_dir = os.path.relpath(dir_name, self.codebase_path) if dir_name != "." else "."
            heatmap.append(f"\n{rel_dir}/")
            heatmap.append(f"  {bar} ({avg_disharmony:.2f})")

            # Show individual files if directory has few files
            if len(files) <= 5:
                for filename, analysis in sorted(files, key=lambda x: x[1].avg_disharmony, reverse=True):
                    file_bar_length = int(analysis.avg_disharmony * 10)
                    file_bar = "█" * file_bar_length + "░" * (10 - file_bar_length)
                    heatmap.append(f"    {filename:30s} {file_bar} ({analysis.avg_disharmony:.2f})")

        return "\n".join(heatmap)

    def print_report(self, report: Dict, show_heatmap: bool = True, show_smells: bool = True):
        """Print comprehensive human-readable report"""
        print("\n")
        print("=" * 70)
        print("SEMANTIC CODEBASE MAP - COMPREHENSIVE ANALYSIS")
        print("=" * 70)

        # Clusters
        clusters = report["clusters"]
        for dimension in ["Love", "Justice", "Power", "Wisdom"]:
            if dimension not in clusters or not clusters[dimension]:
                continue

            files = clusters[dimension]
            avg_l = mean([f.coordinates[0] for f in files])
            avg_j = mean([f.coordinates[1] for f in files])
            avg_p = mean([f.coordinates[2] for f in files])
            avg_w = mean([f.coordinates[3] for f in files])

            icon = {"Love": "💛", "Justice": "⚖️", "Power": "⚡", "Wisdom": "📚"}[dimension]

            print(f"\n{icon} {dimension.upper()} CLUSTER ({len(files)} files)")
            print(f"   Avg Coordinates: L={avg_l:.2f}, J={avg_j:.2f}, P={avg_p:.2f}, W={avg_w:.2f}")
            print(f"   Files:")

            sorted_files = sorted(files, key=lambda f: f.avg_disharmony, reverse=True)
            for file in sorted_files[:5]:
                rel_path = os.path.relpath(file.path, self.codebase_path)
                print(
                    f"     - {rel_path:40s} "
                    f"({file.function_count:2d} funcs, disharmony: {file.avg_disharmony:.2f})"
                )

            if len(files) > 5:
                print(f"     ... and {len(files) - 5} more")

        # Outliers
        outliers = report["outliers"]
        if outliers:
            print(f"\n⚠️  OUTLIERS - Semantically Unclear ({len(outliers)} files)")
            for file in outliers[:3]:
                rel_path = os.path.relpath(file.path, self.codebase_path)
                l, j, p, w = file.coordinates
                print(f"     - {rel_path:40s} L={l:.2f} J={j:.2f} P={p:.2f} W={w:.2f}")

        # Overall metrics
        print(f"\n📊 OVERALL METRICS")
        print(f"   Total files analyzed: {report['total_files']}")
        print(f"   Average disharmony: {report['overall_disharmony']:.2f}")

        avg_dis = report["overall_disharmony"]
        if avg_dis < 0.3:
            health = "EXCELLENT ✅"
        elif avg_dis < 0.5:
            health = "GOOD ✓"
        elif avg_dis < 0.7:
            health = "MODERATE ⚠️"
        else:
            health = "CONCERNING 🚨"

        print(f"   Codebase health: {health}")

        # Architectural smells
        if show_smells and self.architectural_smells:
            print(f"\n🚨 ARCHITECTURAL SMELLS ({len(self.architectural_smells)} detected)")
            print("=" * 70)

            # Group by severity
            by_severity = defaultdict(list)
            for smell in self.architectural_smells:
                by_severity[smell.severity].append(smell)

            for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                smells = by_severity.get(severity, [])
                if not smells:
                    continue

                print(f"\n{severity} ({len(smells)} issues):")
                for smell in smells[:3]:  # Top 3 per severity
                    print(f"  • {smell.smell_type}: {smell.file_path}")
                    print(f"    {smell.description}")
                    print(f"    → {smell.recommendation}")

                if len(smells) > 3:
                    print(f"  ... and {len(smells) - 3} more {severity} issues")

        # Refactoring opportunities
        if self.refactoring_opportunities:
            print(f"\n💡 REFACTORING OPPORTUNITIES (Top 5)")
            print("=" * 70)

            top_opportunities = sorted(
                self.refactoring_opportunities, key=lambda x: x.impact_score, reverse=True
            )[:5]

            for i, opp in enumerate(top_opportunities, 1):
                print(f"\n{i}. {opp.file_path}")
                print(f"   Impact: {opp.impact_score:.0%} | Complexity reduction: {opp.complexity_reduction}%")
                print(f"   {opp.description}")
                if opp.suggested_actions:
                    print(f"   Actions:")
                    for action in opp.suggested_actions:
                        print(f"     → {action}")

        # Heatmap
        if show_heatmap:
            print(self.generate_complexity_heatmap())

        print("\n" + "=" * 70)


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Legacy Code Mapper - Semantic Codebase Analysis")
    parser.add_argument("path", nargs="?", default="harmonizer", help="Path to codebase to analyze")
    parser.add_argument("--no-heatmap", action="store_true", help="Skip complexity heatmap")
    parser.add_argument("--no-smells", action="store_true", help="Skip architectural smell detection")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")

    args = parser.parse_args()

    mapper = LegacyCodeMapper(args.path, quiet=args.quiet)
    report = mapper.analyze_codebase(show_progress=not args.quiet)
    mapper.print_report(report, show_heatmap=not args.no_heatmap, show_smells=not args.no_smells)
