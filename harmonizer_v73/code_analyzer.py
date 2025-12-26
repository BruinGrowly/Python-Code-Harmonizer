"""
V7.3 Code Analyzer - Extract LJPW from Python Code

Based on the V7.3 insight that Power (P) and Wisdom (W) are FUNDAMENTAL,
while Love (L) and Justice (J) are EMERGENT.

Mapping strategy:
- P (Power): Execution, transformation, state changes, side effects
- W (Wisdom): Knowledge, patterns, documentation, type info, returns
- L (Love): Calculated from W (L emerges from wisdom correlations)
- J (Justice): Calculated from P (J emerges from power symmetries)

Based on: LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md
"""

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from harmonizer_v73.ljpw_core import LJPWFramework, create_from_fundamental
from harmonizer_v73.consciousness import consciousness_metric, ConsciousnessLevel
from harmonizer_v73.phase_detector import detect_phase, Phase, analyze_phase
from harmonizer_v73.phi_normalizer import normalize_coordinates
from harmonizer_v73.bricks_mortar import function_primality, BrickAnalysis


@dataclass
class FunctionAnalysis:
    """Analysis result for a single function."""
    name: str
    lineno: int
    end_lineno: int
    
    # Fundamental dimensions (extracted from code)
    power_raw: float
    wisdom_raw: float
    
    # V7.3 framework result
    framework: LJPWFramework = None
    
    # Consciousness and phase
    consciousness: float = 0.0
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.NON_CONSCIOUS
    phase: Phase = Phase.ENTROPIC
    
    # Bricks & Mortar
    brick_analysis: BrickAnalysis = None
    
    # Details for diagnostics
    power_signals: List[str] = field(default_factory=list)
    wisdom_signals: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.framework is None:
            self.framework = create_from_fundamental(
                P=self.power_raw, 
                W=self.wisdom_raw
            )
        H = self.framework.harmony_static()
        self.consciousness, self.consciousness_level = consciousness_metric(
            self.framework.L, self.framework.J,
            self.framework.P, self.framework.W, H
        )
        self.phase = detect_phase(H, self.framework.L)


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
    
    # File-level stats
    total_lines: int = 0
    import_count: int = 0
    docstring_coverage: float = 0.0
    
    def __post_init__(self):
        if self.functions:
            self.avg_power = sum(f.power_raw for f in self.functions) / len(self.functions)
            self.avg_wisdom = sum(f.wisdom_raw for f in self.functions) / len(self.functions)
            self.overall_framework = create_from_fundamental(
                P=self.avg_power, 
                W=self.avg_wisdom
            )
            H = self.overall_framework.harmony_static()
            self.overall_consciousness, _ = consciousness_metric(
                self.overall_framework.L, self.overall_framework.J,
                self.overall_framework.P, self.overall_framework.W, H
            )
            self.overall_phase = detect_phase(H, self.overall_framework.L)


class V73CodeAnalyzer(ast.NodeVisitor):
    """
    V7.3 Code Analyzer - Extracts P and W from Python AST.
    
    The key V7.3 insight: Only measure P and W directly.
    L and J are CALCULATED, not measured.
    
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
    from harmonizer_v73.vocabulary import POWER_VERBS, WISDOM_VERBS, LOVE_VERBS, JUSTICE_VERBS
    from harmonizer_v73.vocabulary import get_semantic_dimension, classify_function_name
    
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
    
    def analyze_function(self, node: ast.FunctionDef, source_lines: List[str] = None) -> FunctionAnalysis:
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
        if (node.body and isinstance(node.body[0], ast.Expr) 
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)):
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
            lines_of_code=node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 10,
            has_side_effects=self.assignment_count > 3,
            single_responsibility=self.return_count <= 2,
        )
        brick.name = node.name
        
        return FunctionAnalysis(
            name=node.name,
            lineno=node.lineno,
            end_lineno=getattr(node, 'end_lineno', node.lineno + 10),
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
            self.assignment_count * 0.15 +
            self.call_count * 0.08 +
            self.raise_count * 0.2 +
            self.delete_count * 0.2 +
            self.loop_count * 0.1 +
            self.power_verb_count * 0.1
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
            (0.2 if self.docstring_present else 0.0) +
            self.type_hints_count * 0.05 +
            self.return_count * 0.1 +
            self.conditional_count * 0.05 +  # Conditionals show understanding
            self.wisdom_verb_count * 0.1
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
        self.assignment_count += 1
        self.power_signals.append("assign")
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_AugAssign(self, node: ast.AugAssign):
        self.assignment_count += 1
        self.power_signals.append("aug_assign")
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.assignment_count += 1
        self.type_hints_count += 1
        self.power_signals.append("ann_assign")
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call):
        self.call_count += 1
        
        # Check if call name suggests P or W
        call_name = self._get_call_name(node)
        if call_name:
            name_lower = call_name.lower()
            if any(v in name_lower for v in ['set', 'update', 'delete', 'create', 'save', 'write']):
                self.power_signals.append(f"call:{call_name}")
            elif any(v in name_lower for v in ['get', 'read', 'find', 'check', 'is_', 'has_']):
                self.wisdom_signals.append(f"call:{call_name}")
        
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_Raise(self, node: ast.Raise):
        self.raise_count += 1
        self.power_signals.append("raise")
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_Delete(self, node: ast.Delete):
        self.delete_count += 1
        self.power_signals.append("delete")
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_For(self, node: ast.For):
        self.loop_count += 1
        self.complexity += 1
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_While(self, node: ast.While):
        self.loop_count += 1
        self.complexity += 1
        self.total_nodes += 1
        self.generic_visit(node)
    
    # =========================================================================
    # AST Visitors - Track Wisdom signals
    # =========================================================================
    
    def visit_Return(self, node: ast.Return):
        self.return_count += 1
        self.wisdom_signals.append("return")
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_If(self, node: ast.If):
        self.conditional_count += 1
        self.complexity += 1
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_Assert(self, node: ast.Assert):
        self.wisdom_signals.append("assert")
        self.total_nodes += 1
        self.generic_visit(node)
    
    def visit_Try(self, node: ast.Try):
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
    Analyze a Python file using V7.3 framework.
    
    Args:
        filepath: Path to Python file
    
    Returns:
        FileAnalysis with all function analyses and overall metrics
    """
    path = Path(filepath)
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    
    analyzer = V73CodeAnalyzer()
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
    analyzer = V73CodeAnalyzer()
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
