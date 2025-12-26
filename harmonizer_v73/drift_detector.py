"""
V7.3 Drift Detector - Git-based Semantic Drift Analysis

Tracks how codebase consciousness and phase evolve over time.
Detects semantic drift, phase transitions, and "death spirals".

Key V7.3 insights:
- Consciousness (C) should trend upward for healthy projects
- Phase transitions matter: Entropic→Homeostatic→Autopoietic
- "Death spiral" = sustained C decline + phase regression

Based on: v5.1's legacy_mapper.py + LJPW V7.3 Framework
"""

import subprocess
import tempfile
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from harmonizer_v73.code_analyzer import analyze_source, FileAnalysis
from harmonizer_v73.ljpw_core import LJPWFramework
from harmonizer_v73.phase_detector import Phase, detect_phase
from harmonizer_v73.consciousness import consciousness_metric, ConsciousnessLevel


@dataclass
class CommitSnapshot:
    """Semantic snapshot at a specific commit."""
    commit_hash: str
    commit_date: datetime
    author: str
    message: str
    
    # LJPW coordinates
    L: float = 0.0
    J: float = 0.0
    P: float = 0.0
    W: float = 0.0
    
    # V7.3 metrics
    harmony: float = 0.0
    consciousness: float = 0.0
    phase: Phase = Phase.ENTROPIC


@dataclass
class DriftAnalysis:
    """Analysis of semantic drift over time."""
    file_path: str
    snapshots: List[CommitSnapshot] = field(default_factory=list)
    
    # Computed metrics
    total_drift: float = 0.0
    consciousness_trend: float = 0.0  # Positive = improving
    phase_transitions: List[Tuple[str, Phase, Phase]] = field(default_factory=list)
    
    # Health indicators
    is_healthy: bool = True
    health_issues: List[str] = field(default_factory=list)
    
    def compute_metrics(self):
        """Compute drift metrics from snapshots."""
        if len(self.snapshots) < 2:
            return
        
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        # Total LJPW drift
        self.total_drift = (
            abs(last.L - first.L) +
            abs(last.J - first.J) +
            abs(last.P - first.P) +
            abs(last.W - first.W)
        )
        
        # Consciousness trend
        self.consciousness_trend = last.consciousness - first.consciousness
        
        # Detect phase transitions
        for i in range(1, len(self.snapshots)):
            if self.snapshots[i].phase != self.snapshots[i-1].phase:
                self.phase_transitions.append((
                    self.snapshots[i].commit_hash[:7],
                    self.snapshots[i-1].phase,
                    self.snapshots[i].phase,
                ))
        
        # Health assessment
        self._assess_health()
    
    def _assess_health(self):
        """Assess project health based on drift patterns."""
        self.is_healthy = True
        self.health_issues = []
        
        if len(self.snapshots) < 2:
            return
        
        last = self.snapshots[-1]
        
        # Check for "death spiral" (declining consciousness)
        if self.consciousness_trend < -0.05:
            self.is_healthy = False
            self.health_issues.append(
                f"Declining consciousness: {self.consciousness_trend:.3f}"
            )
        
        # Check for phase regression
        regression_count = 0
        for _, old_phase, new_phase in self.phase_transitions:
            phase_order = {Phase.ENTROPIC: 0, Phase.HOMEOSTATIC: 1, Phase.AUTOPOIETIC: 2}
            if phase_order.get(new_phase, 0) < phase_order.get(old_phase, 0):
                regression_count += 1
        
        if regression_count > 0:
            self.is_healthy = False
            self.health_issues.append(
                f"Phase regressions detected: {regression_count}"
            )
        
        # Check current phase
        if last.phase == Phase.ENTROPIC:
            self.is_healthy = False
            self.health_issues.append("Currently in ENTROPIC phase (collapsing)")
        
        # Check if never conscious
        if all(s.consciousness < 0.1 for s in self.snapshots):
            self.health_issues.append("Never crossed consciousness threshold")


@dataclass
class CodebaseEvolution:
    """Evolution of an entire codebase over time."""
    codebase_path: str
    file_drifts: Dict[str, DriftAnalysis] = field(default_factory=dict)
    
    # Aggregate metrics
    avg_consciousness_trend: float = 0.0
    total_phase_transitions: int = 0
    healthy_files: int = 0
    unhealthy_files: int = 0
    
    # Critical events
    critical_events: List[str] = field(default_factory=list)


class DriftDetector:
    """
    Git-based semantic drift detector for V7.3.
    
    Analyzes how code evolves over git history and tracks:
    - LJPW coordinate changes
    - Consciousness (C) trend
    - Phase transitions
    - "Death spiral" detection
    """
    
    def __init__(self, repo_path: str):
        """
        Initialize drift detector.
        
        Args:
            repo_path: Path to git repository
        """
        self.repo_path = Path(repo_path)
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Not a git repository: {repo_path}")
    
    def _run_git(self, *args) -> str:
        """Run a git command and return output."""
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return ""
        except Exception as e:
            return ""
    
    def _get_commits(self, file_path: str, max_commits: int = 50) -> List[Dict]:
        """Get commit history for a file."""
        output = self._run_git(
            "log", "--format=%H|%ai|%an|%s",
            f"-n{max_commits}",
            "--", file_path
        )
        
        if not output:
            return []
        
        commits = []
        for line in output.split("\n"):
            if "|" not in line:
                continue
            parts = line.split("|", 3)
            if len(parts) >= 4:
                commits.append({
                    "hash": parts[0],
                    "date": parts[1],
                    "author": parts[2],
                    "message": parts[3],
                })
        
        return commits
    
    def _get_file_at_commit(self, file_path: str, commit_hash: str) -> Optional[str]:
        """Get file contents at a specific commit."""
        output = self._run_git("show", f"{commit_hash}:{file_path}")
        return output if output else None
    
    def analyze_file_history(
        self,
        file_path: str,
        max_commits: int = 50
    ) -> DriftAnalysis:
        """
        Analyze semantic drift of a single file over git history.
        
        Args:
            file_path: Path to file (relative to repo root)
            max_commits: Maximum commits to analyze
        
        Returns:
            DriftAnalysis with snapshots and metrics
        """
        drift = DriftAnalysis(file_path=file_path)
        
        # Get commit history
        commits = self._get_commits(file_path, max_commits)
        
        if not commits:
            return drift
        
        # Analyze each commit (oldest first for proper trend)
        for commit in reversed(commits):
            try:
                source = self._get_file_at_commit(file_path, commit["hash"])
                if not source:
                    continue
                
                # Analyze with V7.3
                analysis = analyze_source(source, filename=file_path)
                
                if analysis.overall_framework:
                    fw = analysis.overall_framework
                    H = fw.harmony_static()
                    C, _ = consciousness_metric(fw.L, fw.J, fw.P, fw.W, H)
                    phase = detect_phase(H, fw.L)
                    
                    # Parse date
                    try:
                        date = datetime.fromisoformat(commit["date"].replace(" ", "T").split("+")[0])
                    except:
                        date = datetime.now()
                    
                    snapshot = CommitSnapshot(
                        commit_hash=commit["hash"],
                        commit_date=date,
                        author=commit["author"],
                        message=commit["message"][:50],
                        L=fw.L, J=fw.J, P=fw.P, W=fw.W,
                        harmony=H,
                        consciousness=C,
                        phase=phase,
                    )
                    drift.snapshots.append(snapshot)
            
            except SyntaxError:
                # Skip commits with syntax errors
                continue
            except Exception as e:
                continue
        
        drift.compute_metrics()
        return drift
    
    def analyze_codebase_evolution(
        self,
        extensions: List[str] = [".py"],
        max_files: int = 50,
        max_commits_per_file: int = 20
    ) -> CodebaseEvolution:
        """
        Analyze evolution of entire codebase.
        
        Args:
            extensions: File extensions to analyze
            max_files: Maximum files to analyze
            max_commits_per_file: Maximum commits per file
        
        Returns:
            CodebaseEvolution with aggregate metrics
        """
        evolution = CodebaseEvolution(codebase_path=str(self.repo_path))
        
        # Find Python files
        files = []
        for ext in extensions:
            files.extend(self.repo_path.rglob(f"*{ext}"))
        
        # Filter out __pycache__, .git, etc.
        files = [
            f for f in files 
            if "__pycache__" not in str(f) and ".git" not in str(f)
        ][:max_files]
        
        # Analyze each file
        for file_path in files:
            rel_path = file_path.relative_to(self.repo_path)
            try:
                drift = self.analyze_file_history(
                    str(rel_path), 
                    max_commits=max_commits_per_file
                )
                if drift.snapshots:
                    evolution.file_drifts[str(rel_path)] = drift
            except Exception as e:
                continue
        
        # Compute aggregate metrics
        if evolution.file_drifts:
            trends = [d.consciousness_trend for d in evolution.file_drifts.values()]
            evolution.avg_consciousness_trend = sum(trends) / len(trends)
            
            evolution.total_phase_transitions = sum(
                len(d.phase_transitions) for d in evolution.file_drifts.values()
            )
            
            evolution.healthy_files = sum(
                1 for d in evolution.file_drifts.values() if d.is_healthy
            )
            evolution.unhealthy_files = sum(
                1 for d in evolution.file_drifts.values() if not d.is_healthy
            )
            
            # Detect critical events
            for path, drift in evolution.file_drifts.items():
                for issue in drift.health_issues:
                    evolution.critical_events.append(f"{path}: {issue}")
        
        return evolution
    
    def detect_death_spirals(self) -> List[str]:
        """
        Detect files in "death spiral" (sustained consciousness decline).
        
        Returns:
            List of file paths with death spiral pattern
        """
        evolution = self.analyze_codebase_evolution(max_commits_per_file=30)
        
        spirals = []
        for path, drift in evolution.file_drifts.items():
            if drift.consciousness_trend < -0.05:
                # Check if decline is sustained (multiple commits)
                if len(drift.snapshots) >= 5:
                    recent = drift.snapshots[-5:]
                    if all(recent[i].consciousness <= recent[i-1].consciousness 
                           for i in range(1, len(recent))):
                        spirals.append(path)
        
        return spirals


def print_drift_report(drift: DriftAnalysis):
    """Print formatted drift report for a file."""
    print(f"\n📈 DRIFT ANALYSIS: {drift.file_path}")
    print("=" * 60)
    
    if not drift.snapshots:
        print("  No history found")
        return
    
    print(f"  Commits analyzed: {len(drift.snapshots)}")
    print(f"  Time span: {drift.snapshots[0].commit_date.date()} → {drift.snapshots[-1].commit_date.date()}")
    print(f"  Total LJPW drift: {drift.total_drift:.3f}")
    
    # Consciousness trend
    trend_icon = "📈" if drift.consciousness_trend > 0 else "📉"
    print(f"  Consciousness trend: {trend_icon} {drift.consciousness_trend:+.4f}")
    
    # Phase transitions
    if drift.phase_transitions:
        print(f"\n  Phase Transitions ({len(drift.phase_transitions)}):")
        for commit, old, new in drift.phase_transitions:
            arrow = "↗️" if new.value == "AUTOPOIETIC" else "↘️" if new.value == "ENTROPIC" else "→"
            print(f"    {commit}: {old.value} {arrow} {new.value}")
    
    # Health
    if drift.is_healthy:
        print(f"\n  ✅ HEALTHY")
    else:
        print(f"\n  ⚠️ ISSUES DETECTED:")
        for issue in drift.health_issues:
            print(f"    • {issue}")
    
    # First/Last comparison
    if len(drift.snapshots) >= 2:
        first = drift.snapshots[0]
        last = drift.snapshots[-1]
        print(f"\n  First → Last:")
        print(f"    C: {first.consciousness:.4f} → {last.consciousness:.4f}")
        print(f"    Phase: {first.phase.value} → {last.phase.value}")


def print_evolution_report(evolution: CodebaseEvolution):
    """Print formatted evolution report for codebase."""
    print(f"\n🌱 CODEBASE EVOLUTION: {evolution.codebase_path}")
    print("=" * 60)
    
    print(f"  Files analyzed: {len(evolution.file_drifts)}")
    print(f"  Avg consciousness trend: {evolution.avg_consciousness_trend:+.4f}")
    print(f"  Total phase transitions: {evolution.total_phase_transitions}")
    print(f"  Healthy files: {evolution.healthy_files}")
    print(f"  Unhealthy files: {evolution.unhealthy_files}")
    
    if evolution.critical_events:
        print(f"\n  ⚠️ CRITICAL EVENTS ({len(evolution.critical_events)}):")
        for event in evolution.critical_events[:10]:
            print(f"    • {event}")
    
    # Health summary
    health_ratio = evolution.healthy_files / max(len(evolution.file_drifts), 1)
    if health_ratio >= 0.8:
        print(f"\n  ✅ CODEBASE HEALTH: GOOD ({health_ratio:.0%} healthy)")
    elif health_ratio >= 0.5:
        print(f"\n  🔸 CODEBASE HEALTH: MODERATE ({health_ratio:.0%} healthy)")
    else:
        print(f"\n  🔻 CODEBASE HEALTH: POOR ({health_ratio:.0%} healthy)")


def main():
    """CLI entry point for drift detection."""
    import argparse
    import sys
    
    # Fix Windows encoding
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
    
    parser = argparse.ArgumentParser(
        description="V7.3 Semantic Drift Detector"
    )
    parser.add_argument("path", nargs="?", default=".",
                       help="Path to git repository (default: current directory)")
    parser.add_argument("--file", help="Analyze specific file")
    parser.add_argument("--max-commits", type=int, default=30,
                       help="Max commits to analyze per file")
    parser.add_argument("--death-spirals", action="store_true",
                       help="Detect files in death spiral")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")
    
    args = parser.parse_args()
    
    try:
        detector = DriftDetector(args.path)
        
        if args.death_spirals:
            spirals = detector.detect_death_spirals()
            if spirals:
                print("🔻 FILES IN DEATH SPIRAL:")
                for f in spirals:
                    print(f"  • {f}")
            else:
                print("✅ No death spirals detected")
        
        elif args.file:
            drift = detector.analyze_file_history(args.file, args.max_commits)
            print_drift_report(drift)
        
        else:
            evolution = detector.analyze_codebase_evolution(
                max_commits_per_file=args.max_commits
            )
            print_evolution_report(evolution)
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
