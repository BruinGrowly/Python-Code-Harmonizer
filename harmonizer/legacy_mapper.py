#!/usr/bin/env python3
"""
Legacy Code Mapper - Semantic analysis of entire codebases

Maps files to LJPW space, finds natural clusters, detects architectural smells
"""

import os
import glob
from statistics import mean
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

from harmonizer.main import PythonCodeHarmonizer


@dataclass
class FileAnalysis:
    """Semantic analysis of a single file"""

    path: str
    coordinates: Tuple[float, float, float, float]  # (L, J, P, W)
    function_count: int
    avg_disharmony: float
    dominant_dimension: str


class LegacyCodeMapper:
    """Map entire codebase to semantic space"""

    def __init__(self, codebase_path: str):
        self.codebase_path = codebase_path
        self.harmonizer = PythonCodeHarmonizer()
        self.file_analyses: Dict[str, FileAnalysis] = {}

    def analyze_codebase(self) -> Dict:
        """Analyze entire codebase and generate semantic map"""
        print(f"🔍 Analyzing codebase: {self.codebase_path}")
        print("=" * 70)

        # Find all Python files
        python_files = self._find_python_files()
        print(f"Found {len(python_files)} Python files\n")

        # Analyze each file
        for file_path in python_files:
            try:
                analysis = self._analyze_file(file_path)
                if analysis:
                    self.file_analyses[file_path] = analysis
            except Exception as e:
                print(f"⚠️  Skipped {file_path}: {e}")

        print(f"\n✅ Analyzed {len(self.file_analyses)} files successfully")
        print("=" * 70)

        return self._generate_report()

    def _find_python_files(self) -> List[str]:
        """Find all Python files in codebase"""
        pattern = os.path.join(self.codebase_path, "**/*.py")
        files = glob.glob(pattern, recursive=True)

        # Filter out common directories to skip
        skip_dirs = {"venv", ".venv", "__pycache__", ".git", "build", "dist", ".pytest_cache"}
        filtered = []

        for f in files:
            # Check if any skip_dir is in the path
            if not any(skip in f for skip in skip_dirs):
                filtered.append(f)

        return filtered

    def _analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze single file and compute semantic coordinates"""
        # Analyze file with harmonizer
        results = self.harmonizer.analyze_file(file_path)

        if not results:
            return None

        # Collect execution coordinates from all functions
        all_coords = []
        all_disharmony = []

        # results is Dict[function_name, data]
        for func_name, data in results.items():
            # Get execution coordinates from ice_result
            ice_result = data.get("ice_result", {})
            ice_components = ice_result.get("ice_components", {})

            # execution is a SemanticResult with .coordinates attribute
            execution_result = ice_components.get("execution")

            if execution_result:
                coords = execution_result.coordinates
                all_coords.append((coords.love, coords.justice, coords.power, coords.wisdom))

            disharmony = data.get("score", 0)
            all_disharmony.append(disharmony)

        if not all_coords:
            return None

        # Average coordinates across all functions in file
        avg_l = mean([c[0] for c in all_coords])
        avg_j = mean([c[1] for c in all_coords])
        avg_p = mean([c[2] for c in all_coords])
        avg_w = mean([c[3] for c in all_coords])

        avg_coords = (avg_l, avg_j, avg_p, avg_w)

        # Determine dominant dimension
        dims = {"Love": avg_l, "Justice": avg_j, "Power": avg_p, "Wisdom": avg_w}
        dominant = max(dims, key=dims.get)

        return FileAnalysis(
            path=file_path,
            coordinates=avg_coords,
            function_count=len(results),
            avg_disharmony=mean(all_disharmony) if all_disharmony else 0,
            dominant_dimension=dominant,
        )

    def _generate_report(self) -> Dict:
        """Generate comprehensive semantic map report"""
        # Group by dominant dimension
        clusters = self._cluster_by_dimension()

        # Find outliers (balanced files with no clear purpose)
        outliers = self._find_outliers()

        # Calculate overall metrics
        overall_disharmony = mean([f.avg_disharmony for f in self.file_analyses.values()])

        return {
            "total_files": len(self.file_analyses),
            "clusters": clusters,
            "outliers": outliers,
            "overall_disharmony": overall_disharmony,
        }

    def _cluster_by_dimension(self) -> Dict[str, List[FileAnalysis]]:
        """Group files by dominant semantic dimension"""
        clusters = defaultdict(list)

        for analysis in self.file_analyses.values():
            clusters[analysis.dominant_dimension].append(analysis)

        return dict(clusters)

    def _find_outliers(self, threshold: float = 0.15) -> List[FileAnalysis]:
        """Find files with no clear dominant dimension (semantic confusion)"""
        outliers = []

        for analysis in self.file_analyses.values():
            l, j, p, w = analysis.coordinates

            # Check if all dimensions are roughly equal (balanced = confused)
            max_coord = max(l, j, p, w)
            min_coord = min(l, j, p, w)

            if max_coord - min_coord < threshold:
                outliers.append(analysis)

        return outliers

    def print_report(self, report: Dict):
        """Print human-readable report"""
        print("\n")
        print("=" * 70)
        print("SEMANTIC CODEBASE MAP")
        print("=" * 70)

        clusters = report["clusters"]

        # Print each cluster
        for dimension in ["Love", "Justice", "Power", "Wisdom"]:
            if dimension not in clusters:
                continue

            files = clusters[dimension]
            if not files:
                continue

            # Calculate cluster statistics
            avg_l = mean([f.coordinates[0] for f in files])
            avg_j = mean([f.coordinates[1] for f in files])
            avg_p = mean([f.coordinates[2] for f in files])
            avg_w = mean([f.coordinates[3] for f in files])

            icon = {"Love": "💛", "Justice": "⚖️", "Power": "⚡", "Wisdom": "📚"}[dimension]

            print(f"\n{icon} {dimension.upper()} CLUSTER ({len(files)} files)")
            print(f"   Avg Coordinates: L={avg_l:.2f}, J={avg_j:.2f}, P={avg_p:.2f}, W={avg_w:.2f}")
            print(f"   Files:")

            # Show top files by function count
            sorted_files = sorted(files, key=lambda f: f.function_count, reverse=True)
            for file in sorted_files[:5]:  # Top 5
                rel_path = os.path.relpath(file.path, self.codebase_path)
                print(
                    f"     - {rel_path:40s} "
                    f"({file.function_count} funcs, disharmony: {file.avg_disharmony:.2f})"
                )

            if len(files) > 5:
                print(f"     ... and {len(files) - 5} more")

        # Print outliers
        outliers = report["outliers"]
        if outliers:
            print(f"\n⚠️  OUTLIERS - Semantically Unclear ({len(outliers)} files)")
            print("   Files with no clear dominant dimension:")
            for file in outliers[:5]:
                rel_path = os.path.relpath(file.path, self.codebase_path)
                l, j, p, w = file.coordinates
                print(f"     - {rel_path:40s} L={l:.2f} J={j:.2f} P={p:.2f} W={w:.2f}")

        # Overall metrics
        print(f"\n📊 OVERALL METRICS")
        print(f"   Total files analyzed: {report['total_files']}")
        print(f"   Average disharmony: {report['overall_disharmony']:.2f}")

        # Health assessment
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

        print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        codebase = sys.argv[1]
    else:
        codebase = "harmonizer"  # Default: analyze harmonizer itself

    mapper = LegacyCodeMapper(codebase)
    report = mapper.analyze_codebase()
    mapper.print_report(report)
