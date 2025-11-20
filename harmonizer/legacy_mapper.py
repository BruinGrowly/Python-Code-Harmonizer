#!/usr/bin/env python3
"""
Legacy Code Mapper - Advanced semantic analysis of entire codebases

Maps files to LJPW space, finds natural clusters, detects architectural smells,
generates complexity heatmaps, and provides refactoring recommendations.
"""

import os
import subprocess
from datetime import datetime
from statistics import mean
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

from harmonizer.main import PythonCodeHarmonizer
from harmonizer.ljpw_baselines import LJPWBaselines, DynamicLJPWv3
from harmonizer.config import ConfigLoader


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
    semantic_density: float = 0.0  # Action per Line of Code


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


@dataclass
class GitCommitSnapshot:
    """Semantic coordinates at a specific commit"""

    commit_hash: str
    commit_date: datetime
    author: str
    coordinates: Tuple[float, float, float, float]  # (L, J, P, W)
    disharmony: float


@dataclass
class FunctionGenealogy:
    """Evolution of a function over time"""

    function_name: str
    file_path: str
    snapshots: List[GitCommitSnapshot] = field(default_factory=list)
    total_drift: float = 0.0  # Total semantic drift
    drift_rate: float = 0.0  # Drift per commit
    major_changes: List[Tuple[str, str, float]] = field(
        default_factory=list
    )  # (hash, date, drift)


@dataclass
class SemanticDrift:
    """Measure of semantic drift over time"""

    file_path: str
    first_commit: str
    last_commit: str
    time_span_days: int
    total_drift: float
    drift_per_day: float
    dimension_drifts: Dict[str, float] = field(
        default_factory=dict
    )  # L, J, P, W individual drifts
    stability_score: float = 1.0  # 1.0 = stable, 0.0 = highly volatile


@dataclass
class ArchitectureDoc:
    """Documented architecture vs reality"""

    component_name: str
    documented_purpose: str
    documented_coordinates: Optional[Tuple[float, float, float, float]]
    actual_coordinates: Tuple[float, float, float, float]
    alignment_score: float  # 0-1, how well docs match reality
    discrepancies: List[str] = field(default_factory=list)


@dataclass
class ArchitecturalDebt:
    """Estimated architectural debt"""

    file_path: str
    debt_score: float  # 0-1
    estimated_hours: float
    estimated_cost_usd: float
    debt_type: str  # "High Disharmony", "God File", "Mixed Concerns", etc.
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str


class LegacyCodeMapper:
    """Advanced codebase semantic analysis"""

    def __init__(self, codebase_path: str, quiet: bool = False):
        self.codebase_path = codebase_path
        self.harmonizer = PythonCodeHarmonizer(quiet=quiet)
        self.config = ConfigLoader.load(codebase_path)
        self.file_analyses: Dict[str, FileAnalysis] = {}
        self.architectural_smells: List[ArchitecturalSmell] = []
        self.refactoring_opportunities: List[RefactoringOpportunity] = []
        self.function_genealogies: Dict[str, FunctionGenealogy] = {}
        self.semantic_drifts: List[SemanticDrift] = []
        self.architecture_docs: List[ArchitectureDoc] = []
        self.architectural_debts: List[ArchitecturalDebt] = []
        self.quiet = quiet

    def analyze_codebase(self, show_progress: bool = True) -> Dict:
        """Analyze entire codebase and generate comprehensive report"""
        if show_progress:
            print(f"Analyzing codebase: {self.codebase_path}")
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
                    print(f"Skipped {file_path}: {e}")

        if show_progress:
            print(f"\nAnalyzed {len(self.file_analyses)} files successfully")
            print("=" * 70)

        # Perform advanced analysis
        self._detect_architectural_smells()
        self._identify_refactoring_opportunities()

        return self.file_analyses

    def _find_python_files(self) -> List[str]:
        """Recursively find all Python files in codebase, respecting ignore patterns"""
        python_files = []

        # Load .harmonizerignore if exists
        ignore_patterns = list(self.config.exclude_patterns)
        ignore_path = os.path.join(self.codebase_path, ".harmonizerignore")
        if os.path.exists(ignore_path):
            try:
                with open(ignore_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            ignore_patterns.append(line)
            except Exception as e:
                if not self.quiet:
                    print(f"Warning: Failed to read .harmonizerignore: {e}")

        import fnmatch

        for root, dirs, files in os.walk(self.codebase_path):
            # Filter directories in-place
            # 1. Check exact match
            dirs[:] = [d for d in dirs if d not in ignore_patterns]
            # 2. Check glob patterns
            dirs[:] = [
                d
                for d in dirs
                if not any(fnmatch.fnmatch(d, p) for p in ignore_patterns)
            ]

            for file in files:
                if file.endswith(".py"):
                    # Check file ignore patterns
                    if any(fnmatch.fnmatch(file, p) for p in ignore_patterns):
                        continue

                    # Check relative path ignore patterns (e.g. "tests/legacy/*.py")
                    rel_path = os.path.relpath(
                        os.path.join(root, file), self.codebase_path
                    )
                    # Normalize path separators for matching
                    rel_path = rel_path.replace(os.sep, "/")

                    if any(fnmatch.fnmatch(rel_path, p) for p in ignore_patterns):
                        continue

                    python_files.append(os.path.join(root, file))

        return python_files

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
                all_coords.append(
                    (coords.love, coords.justice, coords.power, coords.wisdom)
                )

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

        # Calculate Semantic Density (Power / LOC)
        # Note: We don't have exact LOC here, but we can estimate from function count * avg function size
        # Or better, assume 'results' contains LOC info if available.
        # For now, we'll use a proxy: Power Score / Function Count
        # Ideally, we'd want raw Power keywords count.

        # Let's look at how we can get raw counts.
        # The 'results' dict contains 'ice_result' -> 'ice_components' -> 'execution' -> 'coordinates'
        # It doesn't seem to expose raw keyword counts directly.
        # However, 'avg_p' is the average Power score (0-1).
        # Semantic Density = Power Intensity.

        semantic_density = avg_p  # Using avg_p as a proxy for density for now

        return FileAnalysis(
            path=file_path,
            coordinates=avg_coords,
            function_count=len(results),
            avg_disharmony=mean(all_disharmony) if all_disharmony else 0,
            max_disharmony=max(all_disharmony) if all_disharmony else 0,
            min_disharmony=min(all_disharmony) if all_disharmony else 0,
            dominant_dimension=dominant,
            dimension_spread=dimension_spread,
            semantic_density=semantic_density,
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
                        recommendation="Split into smaller, focused modules by semantic dimension",
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
            if analysis.avg_disharmony > self.config.max_disharmony * 0.7:
                self.architectural_smells.append(
                    ArchitecturalSmell(
                        smell_type="High Disharmony",
                        file_path=rel_path,
                        severity=(
                            "CRITICAL"
                            if analysis.avg_disharmony > self.config.max_disharmony
                            else "HIGH"
                        ),
                        description=f"Average disharmony: {analysis.avg_disharmony:.2f} (threshold: {self.config.max_disharmony * 0.7:.2f})",
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
                        description=f"File has multiple active dimensions (L={l:.2f}, J={j:.2f}, P={p:.2f}, W={w:.2f})",
                        impact=0.7,
                        recommendation=f"Split by dimension: L={l:.2f}, J={j:.2f}, P={p:.2f}, W={w:.2f}",
                    )
                )

            # Smell 5: Unnatural Imbalance (LJPW v4.0)
            dist_ne = LJPWBaselines.distance_from_natural_equilibrium(l, j, p, w)
            if dist_ne > 0.5:
                self.architectural_smells.append(
                    ArchitecturalSmell(
                        smell_type="Unnatural Imbalance",
                        file_path=rel_path,
                        severity=(
                            "HIGH" if dist_ne > self.config.max_imbalance else "MEDIUM"
                        ),
                        description=f"Deviates significantly from Natural Equilibrium (distance: {dist_ne:.2f})",
                        impact=min(1.0, dist_ne),
                        recommendation="Rebalance dimensions towards NE (L=0.62, J=0.41, P=0.72, W=0.69)",
                    )
                )

            # Smell 6: Anemic Component (Low Semantic Density)
            # High function count but very low Power (Action)
            if (
                analysis.semantic_density < self.config.min_density
                and analysis.function_count > 10
            ):
                self.architectural_smells.append(
                    ArchitecturalSmell(
                        smell_type="Anemic Component",
                        file_path=rel_path,
                        severity="HIGH",
                        description=f"High complexity ({analysis.function_count} funcs) but low action (Power: {analysis.semantic_density:.2f} < {self.config.min_density})",
                        impact=0.8,
                        recommendation="Component lacks agency. Verify if it's just a data container or if logic leaked elsewhere.",
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
            impact_score = (
                analysis.avg_disharmony * 0.6 + analysis.function_count / 100 * 0.4
            )

            # Estimate complexity reduction
            complexity_reduction = min(80, int((analysis.avg_disharmony - 0.3) * 100))

            suggestions = []

            # Specific suggestions based on analysis
            if analysis.function_count > 20:
                suggestions.append(
                    f"Split into {analysis.function_count // 15 + 1} smaller modules"
                )

            if analysis.dimension_spread < 0.2:
                suggestions.append("Focus file on single semantic dimension")

            l, j, p, w = analysis.coordinates
            dominant_val = max(l, j, p, w)
            if dominant_val < 0.4:
                suggestions.append("Clarify file purpose - currently lacks clear focus")
            else:
                dim_name = analysis.dominant_dimension
                suggestions.append(
                    f"Strengthen {dim_name} focus (currently {dominant_val:.0%})"
                )

            if analysis.max_disharmony > 1.0:
                suggestions.append(
                    "Fix critical disharmony functions first (score > 1.0)"
                )

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
            overall_disharmony = mean(
                [f.avg_disharmony for f in self.file_analyses.values()]
            )
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

            rel_dir = (
                os.path.relpath(dir_name, self.codebase_path)
                if dir_name != "."
                else "."
            )
            heatmap.append(f"\n{rel_dir}/")
            heatmap.append(f"  {bar} ({avg_disharmony:.2f})")

            # Show individual files if directory has few files
            if len(files) <= 5:
                for filename, analysis in sorted(
                    files, key=lambda x: x[1].avg_disharmony, reverse=True
                ):
                    file_bar_length = int(analysis.avg_disharmony * 10)
                    file_bar = "█" * file_bar_length + "░" * (10 - file_bar_length)
                    heatmap.append(
                        f"    {filename:30s} {file_bar} ({analysis.avg_disharmony:.2f})"
                    )

        return "\n".join(heatmap)

    def analyze_git_history(
        self, max_commits: int = 50, show_progress: bool = True
    ) -> bool:
        """Analyze git history to track semantic drift"""
        if show_progress and not self.quiet:
            print(f"\n🕒 Analyzing git history (last {max_commits} commits)...")

        # Check if we're in a git repo
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.codebase_path,
                capture_output=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            if show_progress and not self.quiet:
                print("⚠️  Not a git repository - skipping history analysis")
            return False

        # Get commit history
        try:
            result = subprocess.run(
                ["git", "log", f"-{max_commits}", "--pretty=format:%H|%ai|%an"],
                cwd=self.codebase_path,
                capture_output=True,
                text=True,
                check=True,
            )
            commits = [
                line.split("|") for line in result.stdout.strip().split("\n") if line
            ]
        except subprocess.CalledProcessError:
            if show_progress and not self.quiet:
                print("⚠️  Failed to get git history")
            return False

        if not commits:
            return False

        # Analyze each file's evolution
        for file_path, current_analysis in self.file_analyses.items():
            rel_path = os.path.relpath(file_path, self.codebase_path)
            drift = self._analyze_file_history(rel_path, commits, current_analysis)
            if drift:
                self.semantic_drifts.append(drift)

        if show_progress and not self.quiet:
            print(f"✅ Analyzed {len(self.semantic_drifts)} files with git history")

        return True

    def _analyze_file_history(
        self,
        rel_file_path: str,
        commits: List[List[str]],
        current_analysis: FileAnalysis,
    ) -> Optional[SemanticDrift]:
        """Analyze how a single file evolved over time"""
        snapshots = []

        for commit_hash, commit_date_str, author in commits[:10]:  # Sample 10 commits
            # Get file content at this commit
            try:
                result = subprocess.run(
                    ["git", "show", f"{commit_hash}:{rel_file_path}"],
                    cwd=self.codebase_path,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                if result.returncode != 0:
                    continue  # File didn't exist at this commit

                # Write to temp file and analyze
                import tempfile

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".py", delete=False
                ) as f:
                    f.write(result.stdout)
                    temp_path = f.name

                try:
                    # Analyze this version
                    results = self.harmonizer.analyze_file(temp_path)
                    if results:
                        # Compute average coordinates
                        all_coords = []
                        all_disharmony = []

                        for func_name, data in results.items():
                            ice_result = data.get("ice_result", {})
                            ice_components = ice_result.get("ice_components", {})
                            execution_result = ice_components.get("execution")

                            if execution_result:
                                coords = execution_result.coordinates
                                all_coords.append(
                                    (
                                        coords.love,
                                        coords.justice,
                                        coords.power,
                                        coords.wisdom,
                                    )
                                )

                            all_disharmony.append(data.get("score", 0))

                        if all_coords:
                            avg_l = mean([c[0] for c in all_coords])
                            avg_j = mean([c[1] for c in all_coords])
                            avg_p = mean([c[2] for c in all_coords])
                            avg_w = mean([c[3] for c in all_coords])

                            snapshots.append(
                                GitCommitSnapshot(
                                    commit_hash=commit_hash[:8],
                                    commit_date=datetime.fromisoformat(
                                        commit_date_str.replace(" ", "T")
                                    ),
                                    author=author,
                                    coordinates=(avg_l, avg_j, avg_p, avg_w),
                                    disharmony=(
                                        mean(all_disharmony) if all_disharmony else 0.0
                                    ),
                                )
                            )
                finally:
                    os.unlink(temp_path)

            except Exception:
                continue

        if len(snapshots) < 2:
            return None

        # Calculate drift
        first = snapshots[-1]  # Oldest
        last = snapshots[0]  # Newest

        # Euclidean distance in LJPW space
        drift_l = last.coordinates[0] - first.coordinates[0]
        drift_j = last.coordinates[1] - first.coordinates[1]
        drift_p = last.coordinates[2] - first.coordinates[2]
        drift_w = last.coordinates[3] - first.coordinates[3]

        total_drift = (drift_l**2 + drift_j**2 + drift_p**2 + drift_w**2) ** 0.5

        # Time span
        time_span = (last.commit_date - first.commit_date).days
        drift_per_day = total_drift / max(time_span, 1)

        # Stability score (inverse of drift)
        stability = max(0.0, 1.0 - total_drift)

        return SemanticDrift(
            file_path=rel_file_path,
            first_commit=first.commit_hash,
            last_commit=last.commit_hash,
            time_span_days=time_span,
            total_drift=total_drift,
            drift_per_day=drift_per_day,
            dimension_drifts={"L": drift_l, "J": drift_j, "P": drift_p, "W": drift_w},
            stability_score=stability,
        )

    def project_debt_trajectory(self, file_path: str, months: int = 6) -> Dict:
        """
        Project future technical debt using LJPW v4.0 Dynamic Model.
        Simulates how the file's dimensions will evolve if left unchecked.
        """
        analysis = self.file_analyses.get(file_path)
        if not analysis:
            return {"error": "File not analyzed"}

        # Initialize simulator with complexity score
        # Complexity = 1.0 + (function_count / 20.0) -> 5 functions = 1.25, 20 functions = 2.0
        complexity_score = 1.0 + (analysis.function_count / 20.0)
        simulator = DynamicLJPWv3(complexity_score=complexity_score)

        # Run simulation (1 step approx 1 week, so months * 4 steps)
        duration = months * 4
        history = simulator.simulate(analysis.coordinates, duration=duration, dt=0.1)

        final_l = history["L"][-1]
        final_j = history["J"][-1]
        final_p = history["P"][-1]
        final_w = history["W"][-1]

        # Calculate projected distance from NE
        start_dist = LJPWBaselines.distance_from_natural_equilibrium(
            *analysis.coordinates
        )
        end_dist = LJPWBaselines.distance_from_natural_equilibrium(
            final_l, final_j, final_p, final_w
        )

        drift = end_dist - start_dist

        status = "STABLE"
        if drift > 0.1:
            status = "DEGRADING"
        if drift < -0.1:
            status = "IMPROVING"

        return {
            "current_coordinates": analysis.coordinates,
            "projected_coordinates": (final_l, final_j, final_p, final_w),
            "drift": drift,
            "status": status,
            "risk_level": (
                "HIGH" if end_dist > 0.8 else "MEDIUM" if end_dist > 0.5 else "LOW"
            ),
        }

    def analyze_architecture_docs(self, docs_path: Optional[str] = None) -> bool:
        """Compare documented architecture with actual implementation"""
        if not docs_path:
            # Look for common doc files
            doc_files = []
            for pattern in [
                "ARCHITECTURE.md",
                "docs/ARCHITECTURE.md",
                "README.md",
                "docs/README.md",
            ]:
                path = os.path.join(self.codebase_path, pattern)
                if os.path.exists(path):
                    doc_files.append(path)

            if not doc_files:
                if not self.quiet:
                    print("⚠️  No architecture documentation found")
                return False

            docs_path = doc_files[0]

        if not self.quiet:
            print(
                f"\n📖 Analyzing architecture documentation: {os.path.basename(docs_path)}"
            )

        # Read documentation
        try:
            with open(docs_path, "r") as f:
                doc_content = f.read().lower()
        except Exception as e:
            if not self.quiet:
                print(f"⚠️  Could not read documentation: {e}")
            return False

        # Extract component mentions and their documented purposes
        # Look for patterns like "X handles Y" or "X is responsible for Y"
        import re

        for file_path, analysis in self.file_analyses.items():
            filename = os.path.basename(file_path).replace(".py", "")

            # Check if this component is documented
            if filename.lower() not in doc_content:
                continue

            # Try to extract documented purpose
            patterns = [
                rf"{filename}\s+(?:handles|manages|provides|implements|is responsible for)\s+([^.]+)",
                rf"`{filename}`[:\s]+([^.]+)",
            ]

            documented_purpose = None
            for pattern in patterns:
                match = re.search(pattern, doc_content, re.IGNORECASE)
                if match:
                    documented_purpose = match.group(1).strip()
                    break

            if not documented_purpose:
                documented_purpose = "Mentioned but purpose unclear"

            # Infer documented coordinates from purpose text
            doc_coords = self._infer_coordinates_from_text(documented_purpose)

            # Compare with actual
            actual = analysis.coordinates

            if doc_coords:
                # Calculate alignment (inverse of distance)
                distance = (
                    sum((doc_coords[i] - actual[i]) ** 2 for i in range(4)) ** 0.5
                )
                alignment = max(0.0, 1.0 - distance)

                discrepancies = []
                if abs(doc_coords[0] - actual[0]) > 0.3:
                    discrepancies.append(
                        f"Love dimension mismatch: doc={doc_coords[0]:.2f} vs actual={actual[0]:.2f}"
                    )
                if abs(doc_coords[1] - actual[1]) > 0.3:
                    discrepancies.append(
                        f"Justice dimension mismatch: doc={doc_coords[1]:.2f} vs actual={actual[1]:.2f}"
                    )
                if abs(doc_coords[2] - actual[2]) > 0.3:
                    discrepancies.append(
                        f"Power dimension mismatch: doc={doc_coords[2]:.2f} vs actual={actual[2]:.2f}"
                    )
                if abs(doc_coords[3] - actual[3]) > 0.3:
                    discrepancies.append(
                        f"Wisdom dimension mismatch: doc={doc_coords[3]:.2f} vs actual={actual[3]:.2f}"
                    )
            else:
                alignment = 0.5  # Unknown
                discrepancies = [
                    "Could not infer semantic coordinates from documentation"
                ]

            self.architecture_docs.append(
                ArchitectureDoc(
                    component_name=filename,
                    documented_purpose=documented_purpose,
                    documented_coordinates=doc_coords,
                    actual_coordinates=actual,
                    alignment_score=alignment,
                    discrepancies=discrepancies,
                )
            )

        if not self.quiet:
            print(
                f"✅ Compared {len(self.architecture_docs)} documented components with reality"
            )

        return True

    def _infer_coordinates_from_text(
        self, text: str
    ) -> Optional[Tuple[float, float, float, float]]:
        """Infer LJPW coordinates from natural language description"""
        text_lower = text.lower()

        # Keywords for each dimension
        love_keywords = [
            "connect",
            "integrate",
            "communicate",
            "coordinate",
            "collaborate",
            "interface",
        ]
        justice_keywords = [
            "validate",
            "verify",
            "check",
            "ensure",
            "enforce",
            "correct",
        ]
        power_keywords = [
            "create",
            "delete",
            "modify",
            "update",
            "execute",
            "control",
            "manage",
        ]
        wisdom_keywords = [
            "analyze",
            "compute",
            "calculate",
            "process",
            "retrieve",
            "query",
            "understand",
        ]

        love_count = sum(1 for kw in love_keywords if kw in text_lower)
        justice_count = sum(1 for kw in justice_keywords if kw in text_lower)
        power_count = sum(1 for kw in power_keywords if kw in text_lower)
        wisdom_count = sum(1 for kw in wisdom_keywords if kw in text_lower)

        total = love_count + justice_count + power_count + wisdom_count
        if total == 0:
            return None

        # Normalize
        return (love_count / total, justice_count / total, power_count / total, wisdom_count / total)

    def estimate_architectural_debt(self, hourly_rate: float = 150.0):
        """Estimate architectural debt in hours and dollars"""
        if not self.quiet:
            print(f"\n💰 Estimating architectural debt (rate: ${hourly_rate}/hr)...")

        for file_path, analysis in self.file_analyses.items():
            rel_path = os.path.relpath(file_path, self.codebase_path)

            # Calculate debt score (0-1)
            debt_factors = []

            # Factor 1: Disharmony
            if analysis.avg_disharmony > 0.5:
                debt_factors.append(analysis.avg_disharmony)

            # Factor 2: Complexity (function count)
            if analysis.function_count > 20:
                debt_factors.append(min(1.0, analysis.function_count / 50))

            # Factor 3: Semantic confusion
            if analysis.dimension_spread < 0.2:
                debt_factors.append(0.6)

            if not debt_factors:
                continue

            debt_score = mean(debt_factors)

            # Estimate hours based on debt factors
            base_hours = 0
            debt_type = []

            if analysis.avg_disharmony > 0.7:
                base_hours += (
                    analysis.function_count * 0.5
                )  # 30 min per function to fix
                debt_type.append("High Disharmony")

            if analysis.function_count > 30:
                base_hours += analysis.function_count * 0.3  # Refactoring time
                debt_type.append("God File")

            if analysis.dimension_spread < 0.2:
                base_hours += 4  # Clarification and restructuring
                debt_type.append("Semantic Confusion")

            if base_hours == 0:
                continue

            # Priority based on impact
            if debt_score > 0.8:
                priority = "CRITICAL"
            elif debt_score > 0.6:
                priority = "HIGH"
            elif debt_score > 0.4:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            self.architectural_debts.append(
                ArchitecturalDebt(
                    file_path=rel_path,
                    debt_score=debt_score,
                    estimated_hours=base_hours,
                    estimated_cost_usd=base_hours * hourly_rate,
                    debt_type=" + ".join(debt_type),
                    priority=priority,
                    description=f"{analysis.function_count} functions, {analysis.avg_disharmony:.2f} avg disharmony",
                )
            )

        if not self.quiet:
            total_hours = sum(d.estimated_hours for d in self.architectural_debts)
            total_cost = sum(d.estimated_cost_usd for d in self.architectural_debts)
            print(f"✅ Total debt: {total_hours:.1f} hours (${total_cost:,.0f})")

    def generate_3d_visualization_data(self) -> Dict:
        """Generate data for 3D visualization of codebase in LJPW space"""
        data = {
            "files": [],
            "clusters": {},
            "dimensions": ["Love", "Justice", "Power", "Wisdom"],
        }

        for file_path, analysis in self.file_analyses.items():
            l, j, p, w = analysis.coordinates
            rel_path = os.path.relpath(file_path, self.codebase_path)

            file_data = {
                "path": rel_path,
                "coordinates": {"L": l, "J": j, "P": p, "W": w},
                "dominant": analysis.dominant_dimension,
                "disharmony": analysis.avg_disharmony,
                "function_count": analysis.function_count,
                "color": self._get_dimension_color(analysis.dominant_dimension),
            }
            data["files"].append(file_data)

            # Add to cluster
            if analysis.dominant_dimension not in data["clusters"]:
                data["clusters"][analysis.dominant_dimension] = []
            data["clusters"][analysis.dominant_dimension].append(file_data)

        return data

    def _get_dimension_color(self, dimension: str) -> str:
        """Get color code for dimension"""
        colors = {
            "Love": "#FFD700",  # Gold
            "Justice": "#4169E1",  # Royal Blue
            "Power": "#DC143C",  # Crimson
            "Wisdom": "#32CD32",  # Lime Green
        }
        return colors.get(dimension, "#808080")

    def generate_semantic_map_ascii(self) -> str:
        """Generate advanced ASCII semantic map showing codebase structure"""
        if not self.file_analyses:
            return "No files analyzed"

        output = []
        output.append("\n" + "=" * 90)
        output.append("3D SEMANTIC SPACE MAP (LJPW Coordinates)")
        output.append("=" * 90)

        # Create 2D projection: Love-Justice (X) vs Power-Wisdom (Y)
        output.append("\n  Power-Wisdom Axis (↑)")
        output.append("  1.0 ┤")

        # Create grid
        grid_size = 20
        grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
        file_map = {}

        for file_path, analysis in self.file_analyses.items():
            l, j, p, w = analysis.coordinates

            # Project to 2D: X = (L + J) / 2, Y = (P + W) / 2
            x_val = (l + j) / 2.0
            y_val = (p + w) / 2.0

            # Map to grid coordinates
            x = int(x_val * (grid_size - 1))
            y = int(y_val * (grid_size - 1))

            # Ensure within bounds
            x = max(0, min(grid_size - 1, x))
            y = max(0, min(grid_size - 1, y))

            # Symbol based on dominant dimension
            symbol = {"Love": "♥", "Justice": "⚖", "Power": "⚡", "Wisdom": "◆"}.get(
                analysis.dominant_dimension, "●"
            )

            if grid[grid_size - 1 - y][x] == " ":
                grid[grid_size - 1 - y][x] = symbol
                file_map[(y, x)] = os.path.basename(file_path)
            else:
                grid[grid_size - 1 - y][x] = "▪"  # Multiple files

        # Print grid
        for i, row in enumerate(grid):
            y_label = f"{1.0 - (i / grid_size):.1f}"
            if i % 5 == 0:
                output.append(f"  {y_label:>4} ┤ {''.join(row)}")
            else:
                output.append(f"       │ {''.join(row)}")

        output.append(f"  0.0  └{'─' * grid_size}")
        output.append(f"        0.0{' ' * (grid_size - 8)}1.0")
        output.append("        Love-Justice Axis (→)")

        output.append("\nLEGEND:")
        output.append("  ♥ Love-dominant    ⚖ Justice-dominant")
        output.append("  ⚡ Power-dominant   ◆ Wisdom-dominant")
        output.append("  ▪ Multiple files at same location")

        return "\n".join(output)

    def generate_drift_timeline(self) -> str:
        """Generate timeline visualization of semantic drift"""
        if not self.semantic_drifts:
            return "No drift data available"

        output = []
        output.append("\n" + "=" * 90)
        output.append("SEMANTIC DRIFT TIMELINE")
        output.append("=" * 90)

        # Sort by drift amount
        sorted_drifts = sorted(
            self.semantic_drifts, key=lambda x: x.total_drift, reverse=True
        )[:10]

        for drift in sorted_drifts:
            output.append(f"\n{drift.file_path}")

            # Create drift bar
            drift_normalized = min(
                1.0, drift.total_drift / 2.0
            )  # Cap at 2.0 for visualization
            bar_length = int(drift_normalized * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)

            stability_icon = (
                "✓"
                if drift.stability_score > 0.7
                else ("⚠" if drift.stability_score > 0.3 else "⚠⚠")
            )

            output.append(f"  Drift: {bar} {drift.total_drift:.3f} {stability_icon}")
            output.append(
                f"  Time: {drift.time_span_days} days | Commits: {drift.first_commit}..{drift.last_commit}"
            )

            # Show dimension-specific drift
            dim_bars = []
            for dim, delta in drift.dimension_drifts.items():
                if abs(delta) > 0.1:
                    sign = "+" if delta > 0 else ""
                    dim_bars.append(f"{dim}{sign}{delta:.2f}")

            if dim_bars:
                output.append(f"  Changes: {' | '.join(dim_bars)}")

        return "\n".join(output)

    def generate_debt_breakdown(self) -> str:
        """Generate detailed debt breakdown visualization"""
        if not self.architectural_debts:
            return "No debt data available"

        output = []
        output.append("\n" + "=" * 90)
        output.append("ARCHITECTURAL DEBT BREAKDOWN")
        output.append("=" * 90)

        total_hours = sum(d.estimated_hours for d in self.architectural_debts)
        total_cost = sum(d.estimated_cost_usd for d in self.architectural_debts)

        output.append(f"\nTotal Debt: {total_hours:.1f} hours | ${total_cost:,.0f}")

        # Debt by type
        by_type = defaultdict(lambda: {"hours": 0, "cost": 0, "count": 0})
        for debt in self.architectural_debts:
            by_type[debt.debt_type]["hours"] += debt.estimated_hours
            by_type[debt.debt_type]["cost"] += debt.estimated_cost_usd
            by_type[debt.debt_type]["count"] += 1

        output.append("\nBy Debt Type:")
        for debt_type, stats in sorted(
            by_type.items(), key=lambda x: x[1]["cost"], reverse=True
        ):
            percentage = (stats["cost"] / total_cost * 100) if total_cost > 0 else 0
            bar_length = int(percentage / 100 * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)

            output.append(f"\n  {debt_type}")
            output.append(f"    {bar} {percentage:.1f}%")
            output.append(
                f"    {stats['count']} files | {stats['hours']:.1f}hrs | ${stats['cost']:,.0f}"
            )

        # Top debt contributors
        output.append("\n\nTop 10 Debt Contributors:")
        sorted_debts = sorted(
            self.architectural_debts, key=lambda x: x.estimated_cost_usd, reverse=True
        )[:10]

        for i, debt in enumerate(sorted_debts, 1):
            cost_bar_length = int((debt.estimated_cost_usd / total_cost) * 50)
            cost_bar = "▓" * cost_bar_length

            output.append(f"\n  {i}. {debt.file_path}")
            output.append(f"     {cost_bar} ${debt.estimated_cost_usd:,.0f}")
            output.append(
                f"     {debt.priority} | {debt.debt_type} | {debt.estimated_hours:.1f}hrs"
            )

        return "\n".join(output)

    def export_visualization_html(self, output_path: str = "semantic_map.html"):
        """Export interactive HTML visualization"""
        viz_data = self.generate_3d_visualization_data()

        html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Semantic Codebase Map</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background: #1e1e1e; color: #d4d4d4; }}
        h1 {{ color: #569cd6; }}
        .file-card {{ background: #2d2d30; border-left: 4px solid; padding: 15px; margin: 10px 0; border-radius: 4px; }}
        .love {{ border-color: #FFD700; }}
        .justice {{ border-color: #4169E1; }}
        .power {{ border-color: #DC143C; }}
        .wisdom {{ border-color: #32CD32; }}
        .coords {{ font-family: monospace; color: #ce9178; }}
        .disharmony {{ color: #f48771; font-weight: bold; }}
        .cluster {{ margin: 20px 0; }}
        .stats {{ display: inline-block; margin-right: 20px; padding: 5px 10px; background: #3e3e42; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>🗺️ Semantic Codebase Map</h1>
    <p>Interactive visualization of codebase in LJPW semantic space</p>

    <h2>📊 Summary</h2>
    <div class="stats">Total Files: {total_files}</div>
    <div class="stats">Love Cluster: {love_count}</div>
    <div class="stats">Justice Cluster: {justice_count}</div>
    <div class="stats">Power Cluster: {power_count}</div>
    <div class="stats">Wisdom Cluster: {wisdom_count}</div>

    {clusters_html}

    <h2>📁 All Files</h2>
    {files_html}
</body>
</html>"""

        # Generate clusters HTML
        clusters_html = ""
        for dimension in ["Love", "Justice", "Power", "Wisdom"]:
            if dimension in viz_data["clusters"]:
                files = viz_data["clusters"][dimension]
                clusters_html += f"<div class='cluster'><h3>{dimension} Cluster ({len(files)} files)</h3>"

                for file_data in files[:5]:  # Top 5
                    clusters_html += f"""
                    <div class='file-card {dimension.lower()}'>
                        <strong>{file_data['path']}</strong><br>
                        <span class='coords'>L:{file_data['coordinates']['L']:.2f} J:{file_data['coordinates']['J']:.2f} P:{file_data['coordinates']['P']:.2f} W:{file_data['coordinates']['W']:.2f}</span><br>
                        <span class='disharmony'>Disharmony: {file_data['disharmony']:.2f}</span> | Functions: {file_data['function_count']}
                    </div>
                    """

                if len(files) > 5:
                    clusters_html += f"<p>... and {len(files) - 5} more files</p>"

                clusters_html += "</div>"

        # Generate files HTML
        files_html = ""
        for file_data in sorted(
            viz_data["files"], key=lambda x: x["disharmony"], reverse=True
        )[:20]:
            dim_class = file_data["dominant"].lower()
            files_html += f"""
            <div class='file-card {dim_class}'>
                <strong>{file_data['path']}</strong><br>
                <span class='coords'>L:{file_data['coordinates']['L']:.2f} J:{file_data['coordinates']['J']:.2f} P:{file_data['coordinates']['P']:.2f} W:{file_data['coordinates']['W']:.2f}</span><br>
                <span class='disharmony'>Disharmony: {file_data['disharmony']:.2f}</span> | Functions: {file_data['function_count']} | Dominant: {file_data['dominant']}
            </div>
            """

        # Fill template
        html_content = html_template.format(
            total_files=len(viz_data["files"]),
            love_count=len(viz_data["clusters"].get("Love", [])),
            justice_count=len(viz_data["clusters"].get("Justice", [])),
            power_count=len(viz_data["clusters"].get("Power", [])),
            wisdom_count=len(viz_data["clusters"].get("Wisdom", [])),
            clusters_html=clusters_html,
            files_html=files_html,
        )

        # Write file
        output_file = os.path.join(self.codebase_path, output_path)
        with open(output_file, "w") as f:
            f.write(html_content)

        if not self.quiet:
            print(f"✅ Exported interactive visualization to {output_file}")

        return output_file

    def print_report(
        self, report: Dict, show_heatmap: bool = True, show_smells: bool = True
    ):
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

            icon = {"Love": "💛", "Justice": "⚖️", "Power": "⚡", "Wisdom": "📚"}[
                dimension
            ]

            print(f"\n{icon} {dimension.upper()} CLUSTER ({len(files)} files)")
            print(
                f"   Avg Coordinates: L={avg_l:.2f}, J={avg_j:.2f}, P={avg_p:.2f}, W={avg_w:.2f}"
            )
            print("   Files:")

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
        print("\n📊 OVERALL METRICS")
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
            print(
                f"\n🚨 ARCHITECTURAL SMELLS ({len(self.architectural_smells)} detected)"
            )
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
            print("\n💡 REFACTORING OPPORTUNITIES (Top 5)")
            print("=" * 70)

            top_opportunities = sorted(
                self.refactoring_opportunities,
                key=lambda x: x.impact_score,
                reverse=True,
            )[:5]

            for i, opp in enumerate(top_opportunities, 1):
                print(f"\n{i}. {opp.file_path}")
                print(
                    f"   Impact: {opp.impact_score:.0%} | Complexity reduction: {opp.complexity_reduction}%"
                )
                print(f"   {opp.description}")
                if opp.suggested_actions:
                    print("   Actions:")
                    for action in opp.suggested_actions:
                        print(f"     → {action}")

        # Git History & Semantic Drift
        if self.semantic_drifts:
            print(f"\n🕒 SEMANTIC DRIFT ANALYSIS ({len(self.semantic_drifts)} files)")
            print("=" * 70)

            # Show top 5 most volatile files
            volatile_files = sorted(
                self.semantic_drifts, key=lambda x: x.total_drift, reverse=True
            )[:5]

            for drift in volatile_files:
                print(f"\n{drift.file_path}")
                print(
                    f"   Time span: {drift.time_span_days} days ({drift.first_commit}..{drift.last_commit})"
                )
                print(
                    f"   Total drift: {drift.total_drift:.3f} | Stability: {drift.stability_score:.0%}"
                )
                print(
                    f"   Dimension changes: L{drift.dimension_drifts['L']:+.2f} J{drift.dimension_drifts['J']:+.2f} P{drift.dimension_drifts['P']:+.2f} W{drift.dimension_drifts['W']:+.2f}"
                )

                if drift.stability_score < 0.3:
                    print("   ⚠️  HIGH VOLATILITY - Semantics changed significantly")
                elif drift.stability_score < 0.7:
                    print("   ⚠️  Moderate volatility - Consider stabilizing")

        # Architecture Documentation Alignment
        if self.architecture_docs:
            print(
                f"\n📖 ARCHITECTURE DOCS VS REALITY ({len(self.architecture_docs)} components)"
            )
            print("=" * 70)

            # Show misalignments
            misaligned = [
                doc for doc in self.architecture_docs if doc.alignment_score < 0.7
            ]

            if misaligned:
                print(f"\n⚠️  {len(misaligned)} components have docs/reality mismatch:")
                for doc in misaligned[:5]:
                    print(
                        f"\n  {doc.component_name} (alignment: {doc.alignment_score:.0%})"
                    )
                    print(f"    Documented: {doc.documented_purpose}")
                    if doc.discrepancies:
                        for disc in doc.discrepancies[:2]:
                            print(f"    ⚠️  {disc}")
            else:
                print("✅ All documented components align with implementation")

        # Architectural Debt
        if self.architectural_debts:
            print("\n💰 ARCHITECTURAL DEBT ESTIMATION")
            print("=" * 70)

            total_hours = sum(d.estimated_hours for d in self.architectural_debts)
            total_cost = sum(d.estimated_cost_usd for d in self.architectural_debts)

            print(
                f"\nTotal Estimated Debt: {total_hours:.1f} hours (${total_cost:,.0f})"
            )

            # Group by priority
            by_priority = defaultdict(list)
            for debt in self.architectural_debts:
                by_priority[debt.priority].append(debt)

            for priority in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                debts = by_priority.get(priority, [])
                if not debts:
                    continue

                priority_hours = sum(d.estimated_hours for d in debts)
                priority_cost = sum(d.estimated_cost_usd for d in debts)

                print(
                    f"\n{priority} ({len(debts)} files) - {priority_hours:.1f}hrs (${priority_cost:,.0f}):"
                )

                for debt in sorted(
                    debts, key=lambda x: x.estimated_cost_usd, reverse=True
                )[:3]:
                    print(f"  • {debt.file_path}")
                    print(f"    Type: {debt.debt_type}")
                    print(
                        f"    Cost: {debt.estimated_hours:.1f}hrs (${debt.estimated_cost_usd:,.0f})"
                    )
                    print(f"    {debt.description}")

                if len(debts) > 3:
                    print(f"  ... and {len(debts) - 3} more {priority} priority items")

        # Heatmap
        if show_heatmap:
            print(self.generate_complexity_heatmap())

        print("\n" + "=" * 70)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Legacy Code Mapper - Complete Semantic Codebase Analysis with Git History, Architecture Docs, and Debt Estimation"
    )
    parser.add_argument(
        "path", nargs="?", default="harmonizer", help="Path to codebase to analyze"
    )
    parser.add_argument(
        "--no-heatmap", action="store_true", help="Skip complexity heatmap"
    )
    parser.add_argument(
        "--no-smells", action="store_true", help="Skip architectural smell detection"
    )
    parser.add_argument(
        "--no-git", action="store_true", help="Skip git history analysis"
    )
    parser.add_argument(
        "--no-docs",
        action="store_true",
        help="Skip architecture documentation analysis",
    )
    parser.add_argument(
        "--no-debt", action="store_true", help="Skip architectural debt estimation"
    )
    parser.add_argument(
        "--git-commits",
        type=int,
        default=50,
        help="Number of commits to analyze (default: 50)",
    )
    parser.add_argument(
        "--hourly-rate",
        type=float,
        default=150.0,
        help="Hourly rate for debt estimation (default: $150)",
    )
    parser.add_argument(
        "--docs-path", type=str, default=None, help="Path to architecture documentation"
    )
    parser.add_argument(
        "--export-html",
        action="store_true",
        help="Export interactive HTML visualization",
    )
    parser.add_argument(
        "--semantic-map", action="store_true", help="Show 3D semantic map (ASCII)"
    )
    parser.add_argument(
        "--drift-timeline",
        action="store_true",
        help="Show drift timeline visualization",
    )
    parser.add_argument(
        "--debt-breakdown", action="store_true", help="Show detailed debt breakdown"
    )
    parser.add_argument(
        "--full", action="store_true", help="Enable all analysis features (default)"
    )
    parser.add_argument("--quiet", action="store_true", help="Minimal output")

    args = parser.parse_args()

    # Full analysis by default
    enable_git = not args.no_git
    enable_docs = not args.no_docs
    enable_debt = not args.no_debt

    if args.full:
        enable_git = enable_docs = enable_debt = True

    # Create mapper and run base analysis
    mapper = LegacyCodeMapper(args.path, quiet=args.quiet)
    report = mapper.analyze_codebase(show_progress=not args.quiet)

    # Advanced analyses
    if enable_git:
        mapper.analyze_git_history(
            max_commits=args.git_commits, show_progress=not args.quiet
        )

    if enable_docs:
        mapper.analyze_architecture_docs(docs_path=args.docs_path)

    if enable_debt:
        mapper.estimate_architectural_debt(hourly_rate=args.hourly_rate)

    # Generate report
    mapper.print_report(
        report, show_heatmap=not args.no_heatmap, show_smells=not args.no_smells
    )

    # Advanced visualizations
    if args.semantic_map or args.full:
        print(mapper.generate_semantic_map_ascii())

    if args.drift_timeline and mapper.semantic_drifts:
        print(mapper.generate_drift_timeline())

    if args.debt_breakdown and mapper.architectural_debts:
        print(mapper.generate_debt_breakdown())

    if args.export_html:
        mapper.export_visualization_html()
