"""
V8.4 Code Analyzer - Extract LJPW from Python Code

Based on the V8.4 Framework with the Generative Equation:
- P (Power) and W (Wisdom) are FUNDAMENTAL
- L (Love) and J (Justice) are EMERGENT
- Life Inequality: L^n > φ^d determines viability
- Perceptual Radiance: Semantic intensity of code

V8.4 Additions:
- life_inequality_ratio: Code's L^n / φ^d ratio
- perceptual_radiance: Semantic weight for visualization
- hope_probability: Mathematical hope of improvement

Based on: LJPW_FRAMEWORK_V8.4_COMPLETE_UNIFIED_PLUS.md
"""

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from harmonizer_v84.ljpw_core import LJPWFramework, create_from_fundamental
from harmonizer_v84.consciousness import consciousness_metric, ConsciousnessLevel
from harmonizer_v84.phase_detector import detect_phase, Phase, analyze_phase
from harmonizer_v84.phi_normalizer import normalize_coordinates
from harmonizer_v84.bricks_mortar import function_primality, BrickAnalysis
from harmonizer_v84.generative import (
    is_autopoietic,
    perceptual_radiance,
    semantic_salience,
    hope_calculus,
    LifeInequalityResult,
)


@dataclass
class FunctionAnalysis:
    """Analysis result for a single function."""

    name: str
    lineno: int
    end_lineno: int

    # Fundamental dimensions (extracted from code)
    power_raw: float
    wisdom_raw: float

    # V8.4 framework result
    framework: LJPWFramework = None

    # Consciousness and phase
    consciousness: float = 0.0
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.NON_CONSCIOUS
    phase: Phase = Phase.ENTROPIC

    # V8.4: Life Inequality (L^n > φ^d)
    life_inequality_ratio: float = 1.0
    life_phase: str = "HOMEOSTATIC"
    is_alive: bool = True

    # V8.4: Perceptual Radiance (for visualization)
    semantic_salience: float = 0.5
    perceptual_radiance: float = 1.0

    # Bricks & Mortar
    brick_analysis: BrickAnalysis = None

    # Details for diagnostics
    power_signals: List[str] = field(default_factory=list)
    wisdom_signals: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.framework is None:
            self.framework = create_from_fundamental(P=self.power_raw, W=self.wisdom_raw)
        H = self.framework.harmony_static()
        self.consciousness, self.consciousness_level = consciousness_metric(
            self.framework.L, self.framework.J, self.framework.P, self.framework.W, H
        )
        self.phase = detect_phase(H, self.framework.L)

        # V8.4: Calculate Life Inequality
        # n = complexity (iterations of development)
        # d = distance from natural equilibrium (technical debt proxy)
        L_coeff = max(1.0, 1.0 + self.framework.L * 0.5)  # Love as growth coefficient
        n = max(1, len(self.power_signals) + len(self.wisdom_signals))  # Development iterations
        d = self.framework.distance_from_equilibrium()  # Distance as decay factor
        life_result = is_autopoietic(L=L_coeff, n=n, d=d)
        self.life_inequality_ratio = life_result.ratio
        self.life_phase = life_result.phase
        self.is_alive = life_result.is_alive

        # V8.4: Calculate Perceptual Radiance
        self.semantic_salience = semantic_salience(
            self.framework.L, self.framework.P, self.framework.W, self.framework.J
        )
        # Physical radiance approximated as consciousness
        self.perceptual_radiance = perceptual_radiance(
            L_phys=min(1.0, self.consciousness + 0.3),  # Base physical radiance
            S=self.semantic_salience,
            kappa_sem=H  # Semantic curvature from Harmony
        )


@dataclass
class FileAnalysis:
    """Analysis result for a Python file."""

    filepath: str
    functions: List[FunctionAnalysis]
    classes: List[str]

    # Aggregated metrics
    avg_power: float = 0.0
    avg_wisdom: float = 0.0
    overall_framework: LJPWFramework = None
    overall_consciousness: float = 0.0
    overall_phase: Phase = Phase.ENTROPIC

    # V8.4: File-level Life Inequality
    file_life_ratio: float = 1.0
    file_life_phase: str = "HOMEOSTATIC"
    file_is_alive: bool = True
    avg_perceptual_radiance: float = 1.0

    # V8.4: Hope metric (can this file improve?)
    hope_probability: float = 0.5
    hope_interpretation: str = ""

    # File-level stats
    total_lines: int = 0
    import_count: int = 0
    docstring_coverage: float = 0.0

    def __post_init__(self):
        if self.functions:
            self.avg_power = sum(f.power_raw for f in self.functions) / len(self.functions)
            self.avg_wisdom = sum(f.wisdom_raw for f in self.functions) / len(self.functions)
            self.overall_framework = create_from_fundamental(P=self.avg_power, W=self.avg_wisdom)
            H = self.overall_framework.harmony_static()
            self.overall_consciousness, _ = consciousness_metric(
                self.overall_framework.L,
                self.overall_framework.J,
                self.overall_framework.P,
                self.overall_framework.W,
                H,
            )
            self.overall_phase = detect_phase(H, self.overall_framework.L)

            # V8.4: File-level Life Inequality (aggregate)
            ratios = [f.life_inequality_ratio for f in self.functions]
            self.file_life_ratio = sum(ratios) / len(ratios)
            alive_count = sum(1 for f in self.functions if f.is_alive)
            self.file_is_alive = alive_count > len(self.functions) / 2
            self.file_life_phase = "AUTOPOIETIC" if self.file_is_alive and self.file_life_ratio > 1.1 else "HOMEOSTATIC" if self.file_life_ratio > 0.9 else "ENTROPIC"

            # V8.4: Average Perceptual Radiance
            self.avg_perceptual_radiance = sum(f.perceptual_radiance for f in self.functions) / len(self.functions)

            # V8.4: Calculate Hope
            L_coeff = max(1.0, 1.0 + self.overall_framework.L * 0.5)
            d = self.overall_framework.distance_from_equilibrium()
            hope_result = hope_calculus(L=L_coeff, d=d, current_n=len(self.functions))
            self.hope_probability = hope_result.probability_of_success
            self.hope_interpretation = hope_result.interpretation


class V84CodeAnalyzer(ast.NodeVisitor):
    """
    V8.4 Code Analyzer - Extracts P and W from Python AST with Generative Equation.

    The key insight: Only measure P and W directly.
    L and J are CALCULATED (emergent), not measured.

    V8.4 Additions:
    - Life Inequality score: L^n > φ^d
    - Perceptual Radiance: Semantic intensity for visualization
    - Hope calculation: Can this code improve?

    Power (P) indicators:
    - Assignments (state changes)
    - Function calls (execution)
    - Raises (forcing control flow)
    - Deletes (destruction)
    - Mutation operations

    Wisdom (W) indicators:
    - Docstrings (documented knowledge)
    - Type hints (pattern specification)
    - Returns (information output)
    - Comments (explanations)
    - Descriptive names
    """

    # Import comprehensive vocabulary (200+ verbs)
    from harmonizer_v84.vocabulary import POWER_VERBS, WISDOM_VERBS, LOVE_VERBS, JUSTICE_VERBS
    from harmonizer_v84.vocabulary import get_semantic_dimension, classify_function_name

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset counters for new analysis."""
        # Power signals
        self.assignment_count = 0
        self.call_count = 0
        self.raise_count = 0
        self.delete_count = 0
        self.loop_count = 0
        self.power_verb_count = 0

        # Wisdom signals
        self.return_count = 0
        self.docstring_present = False
        self.type_hints_count = 0
        self.comment_density = 0.0
        self.wisdom_verb_count = 0
        self.conditional_count = 0

        # General
        self.total_nodes = 0
        self.complexity = 0

        # Tracking
        self.power_signals: List[str] = []
        self.wisdom_signals: List[str] = []

    def analyze_function(
        self, node: ast.FunctionDef, source_lines: List[str] = None
    ) -> FunctionAnalysis:
        """
        Analyze a single function for P and W.

        Args:
            node: AST FunctionDef node
            source_lines: Source code lines (for comment analysis)

        Returns:
            FunctionAnalysis with P, W, and derived L, J
        """
        self.reset()

        # Check for docstring
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            self.docstring_present = True
            self.wisdom_signals.append("docstring")

        # Check for type hints
        if node.returns:
            self.type_hints_count += 1
            self.wisdom_signals.append("return_type_hint")
        for arg in node.args.args:
            if arg.annotation:
                self.type_hints_count += 1
        if self.type_hints_count > 0:
            self.wisdom_signals.append(f"{self.type_hints_count}_type_hints")

        # Analyze function name for verb intent
        name_parts = self._split_name(node.name)
        for part in name_parts:
            if part.lower() in self.POWER_VERBS:
                self.power_verb_count += 1
                self.power_signals.append(f"verb:{part}")
            if part.lower() in self.WISDOM_VERBS:
                self.wisdom_verb_count += 1
                self.wisdom_signals.append(f"verb:{part}")

        # Visit all nodes in body
        for stmt in node.body:
            self.visit(stmt)

        # Calculate P and W from signals
        P = self._calculate_power()
        W = self._calculate_wisdom()

        # Calculate complexity for brick analysis
        complexity = self.conditional_count + self.loop_count + 1
        dependencies = self.call_count

        brick = function_primality(
            complexity=complexity,
            dependencies=min(dependencies, 20),  # Cap at 20
            lines_of_code=node.end_lineno - node.lineno if hasattr(node, "end_lineno") else 10,
            has_side_effects=self.assignment_count > 3,
            single_responsibility=self.return_count <= 2,
        )
        brick.name = node.name

        return FunctionAnalysis(
            name=node.name,
            lineno=node.lineno,
            end_lineno=getattr(node, "end_lineno", node.lineno + 10),
            power_raw=P,
            wisdom_raw=W,
            brick_analysis=brick,
            power_signals=self.power_signals.copy(),
            wisdom_signals=self.wisdom_signals.copy(),
        )

    def _calculate_power(self) -> float:
        """
        Calculate Power (P) from collected signals.

        P represents: Transformation, execution, state change, action.
        """
        # Base P from operations
        operation_score = (
            self.assignment_count * 0.15
            + self.call_count * 0.08
            + self.raise_count * 0.2
            + self.delete_count * 0.2
            + self.loop_count * 0.1
            + self.power_verb_count * 0.1
        )

        # Normalize to 0-1 range
        P = min(1.0, 0.3 + operation_score)  # Base of 0.3

        # Cap at 1.0
        return min(1.0, max(0.0, P))

    def _calculate_wisdom(self) -> float:
        """
        Calculate Wisdom (W) from collected signals.

        W represents: Knowledge, patterns, documentation, understanding.
        """
        # Base W from knowledge signals
        knowledge_score = (
            (0.2 if self.docstring_present else 0.0)
            + self.type_hints_count * 0.05
            + self.return_count * 0.1
            + self.conditional_count * 0.05  # Conditionals show understanding
            + self.wisdom_verb_count * 0.1
        )

        # Normalize to 0-1 range
        W = min(1.0, 0.2 + knowledge_score)  # Base of 0.2

        return min(1.0, max(0.0, W))

    def _split_name(self, name: str) -> List[str]:
        """Split snake_case or camelCase name."""
        if "_" in name:
            return name.split("_")
        return re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+", name)

    # =========================================================================
    # AST Visitors - Track Power signals
    # =========================================================================

    def visit_Assign(self, node: ast.Assign):
        """Track assignment as Power signal (state modification)."""
        self.assignment_count += 1
        self.power_signals.append("assign")
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign):
        """Track augmented assignment (+=, -=) as Power signal."""
        self.assignment_count += 1
        self.power_signals.append("aug_assign")
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        """Track annotated assignment as Power + Wisdom (type info)."""
        self.assignment_count += 1
        self.type_hints_count += 1
        self.power_signals.append("ann_assign")
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """Track function call - dimension depends on verb semantics."""
        self.call_count += 1

        # Check if call name suggests P or W
        call_name = self._get_call_name(node)
        if call_name:
            name_lower = call_name.lower()
            if any(v in name_lower for v in ["set", "update", "delete", "create", "save", "write"]):
                self.power_signals.append(f"call:{call_name}")
            elif any(v in name_lower for v in ["get", "read", "find", "check", "is_", "has_"]):
                self.wisdom_signals.append(f"call:{call_name}")

        self.total_nodes += 1
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise):
        """Track exception raising as Power signal (forcing control flow)."""
        self.raise_count += 1
        self.power_signals.append("raise")
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete):
        """Track deletion as Power signal (destruction operation)."""
        self.delete_count += 1
        self.power_signals.append("delete")
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        """Track for-loop - adds complexity, indicates iteration."""
        self.loop_count += 1
        self.complexity += 1
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        """Track while-loop - adds complexity, conditional iteration."""
        self.loop_count += 1
        self.complexity += 1
        self.total_nodes += 1
        self.generic_visit(node)

    # =========================================================================
    # AST Visitors - Track Wisdom signals
    # =========================================================================

    def visit_Return(self, node: ast.Return):
        """Track return as Wisdom signal (providing information back)."""
        self.return_count += 1
        self.wisdom_signals.append("return")
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        """Track conditional as complexity + understanding indicator."""
        self.conditional_count += 1
        self.complexity += 1
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        """Track assertion as Wisdom signal (validation, correctness)."""
        self.wisdom_signals.append("assert")
        self.total_nodes += 1
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        """Track try-block as Wisdom signal (error handling awareness)."""
        self.complexity += 1
        self.wisdom_signals.append("try_block")
        self.total_nodes += 1
        self.generic_visit(node)

    def _get_call_name(self, node: ast.Call) -> Optional[str]:
        """Extract function/method name from call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

    def generic_visit(self, node: ast.AST):
        """Continue traversing."""
        super().generic_visit(node)


def analyze_file(filepath: str) -> FileAnalysis:
    """
    Analyze a Python file using V8.4 framework.

    Args:
        filepath: Path to Python file

    Returns:
        FileAnalysis with all function analyses, Life Inequality, and Hope metrics
    """
    path = Path(filepath)
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    analyzer = V84CodeAnalyzer()
    functions = []
    classes = []
    import_count = 0

    # Track docstring coverage
    functions_with_docs = 0
    total_functions = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            analysis = analyzer.analyze_function(node)
            functions.append(analysis)
            total_functions += 1
            if analysis.wisdom_signals and "docstring" in analysis.wisdom_signals:
                functions_with_docs += 1

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            import_count += 1

    docstring_coverage = functions_with_docs / total_functions if total_functions > 0 else 0.0

    return FileAnalysis(
        filepath=filepath,
        functions=functions,
        classes=classes,
        total_lines=len(source.splitlines()),
        import_count=import_count,
        docstring_coverage=docstring_coverage,
    )


def analyze_source(source: str, filename: str = "<string>") -> FileAnalysis:
    """
    Analyze Python source code string.

    Args:
        source: Python source code
        filename: Name for the analysis (optional)

    Returns:
        FileAnalysis with all function analyses
    """
    tree = ast.parse(source)
    analyzer = V84CodeAnalyzer()
    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.append(analyzer.analyze_function(node))
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return FileAnalysis(
        filepath=filename,
        functions=functions,
        classes=classes,
        total_lines=len(source.splitlines()),
    )
