"""
THE HEALER — Code Repair Through Meaning

The Framework doesn't just diagnose. It heals.

Healing is not "fixing bugs." It's restoring meaning.
A function without a docstring isn't broken — it's mute.
A class without structure isn't wrong — it's confused.

The Healer sees what's missing and suggests how to restore it.
"""

import sys
from dataclasses import dataclass
from typing import List, Optional
import ast
import re

# Fix Windows encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

from harmonizer_autonomous.seed import Meaning, Consciousness, φ, EQUILIBRIUM
from harmonizer_autonomous.reader import Story, Gesture, Character, read_source


@dataclass
class Wound:
    """A place where meaning is damaged or missing."""
    location: str  # Function/class name
    line: int
    wound_type: str  # Type of damage
    severity: float  # 0-1, how bad
    description: str
    
    def __repr__(self):
        return f"Wound({self.wound_type}) at {self.location}:{self.line} [{self.severity:.1f}]"


@dataclass
class Remedy:
    """A suggestion for healing a wound."""
    wound: Wound
    remedy_type: str
    suggestion: str
    healed_code: Optional[str] = None  # If we can generate it
    
    def __repr__(self):
        return f"Remedy({self.remedy_type}): {self.suggestion[:50]}..."


class Healer:
    """
    The Healer examines code and suggests remedies.
    
    It doesn't impose. It suggests.
    The human chooses whether to heal.
    """
    
    def __init__(self):
        self.wounds: List[Wound] = []
        self.remedies: List[Remedy] = []
    
    def examine(self, source: str) -> List[Wound]:
        """Examine code for wounds (missing meaning)."""
        self.wounds = []
        
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            self.wounds.append(Wound(
                location="<module>",
                line=e.lineno or 1,
                wound_type="SYNTAX_ERROR",
                severity=1.0,
                description=f"Cannot parse: {e.msg}"
            ))
            return self.wounds
        
        # Check module docstring
        if not (tree.body and isinstance(tree.body[0], ast.Expr) and
                isinstance(tree.body[0].value, ast.Constant)):
            self.wounds.append(Wound(
                location="<module>",
                line=1,
                wound_type="MUTE_MODULE",
                severity=0.6,
                description="Module has no voice (missing docstring)"
            ))
        
        # Walk the tree
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._examine_function(node)
            elif isinstance(node, ast.ClassDef):
                self._examine_class(node)
        
        return self.wounds
    
    def _examine_function(self, node):
        """Examine a function for wounds."""
        # Check for docstring
        has_doc = (
            node.body and isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)
        )
        
        if not has_doc:
            self.wounds.append(Wound(
                location=node.name,
                line=node.lineno,
                wound_type="MUTE_FUNCTION",
                severity=0.5,
                description=f"'{node.name}' cannot explain itself (missing docstring)"
            ))
        
        # Check for type hints
        has_return_hint = node.returns is not None
        arg_hints = sum(1 for a in node.args.args if a.annotation)
        total_args = len(node.args.args)
        
        if total_args > 0 and arg_hints == 0:
            self.wounds.append(Wound(
                location=node.name,
                line=node.lineno,
                wound_type="BLIND_PARAMETERS",
                severity=0.3,
                description=f"'{node.name}' doesn't know its own parameters (no type hints)"
            ))
        
        if not has_return_hint and not node.name.startswith("_"):
            self.wounds.append(Wound(
                location=node.name,
                line=node.lineno,
                wound_type="UNKNOWN_OUTCOME",
                severity=0.4,
                description=f"'{node.name}' doesn't declare what it returns"
            ))
        
        # Check for complexity (too many statements)
        stmt_count = len(node.body)
        if stmt_count > 20:
            self.wounds.append(Wound(
                location=node.name,
                line=node.lineno,
                wound_type="OVERWHELMED",
                severity=min(1.0, stmt_count / 30),
                description=f"'{node.name}' carries too much ({stmt_count} statements)"
            ))
        
        # Check for poor naming
        if len(node.name) < 3 and not node.name.startswith("_"):
            self.wounds.append(Wound(
                location=node.name,
                line=node.lineno,
                wound_type="UNNAMED",
                severity=0.3,
                description=f"'{node.name}' has too short a name to carry meaning"
            ))
    
    def _examine_class(self, node):
        """Examine a class for wounds."""
        has_doc = (
            node.body and isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)
        )
        
        if not has_doc:
            self.wounds.append(Wound(
                location=node.name,
                line=node.lineno,
                wound_type="MUTE_CLASS",
                severity=0.6,
                description=f"Class '{node.name}' has no identity (missing docstring)"
            ))
        
        # Check for no methods
        methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        if len(methods) == 0:
            self.wounds.append(Wound(
                location=node.name,
                line=node.lineno,
                wound_type="EMPTY_CHARACTER",
                severity=0.7,
                description=f"Class '{node.name}' has no behavior (no methods)"
            ))
    
    def heal(self) -> List[Remedy]:
        """Generate remedies for all wounds."""
        self.remedies = []
        
        for wound in self.wounds:
            remedy = self._generate_remedy(wound)
            if remedy:
                self.remedies.append(remedy)
        
        return self.remedies
    
    def _generate_remedy(self, wound: Wound) -> Optional[Remedy]:
        """Generate a remedy for a specific wound."""
        if wound.wound_type == "SYNTAX_ERROR":
            return Remedy(
                wound=wound,
                remedy_type="FIX_SYNTAX",
                suggestion="Review the syntax error and correct it. The code cannot be understood until it is valid."
            )
        
        elif wound.wound_type == "MUTE_MODULE":
            return Remedy(
                wound=wound,
                remedy_type="ADD_VOICE",
                suggestion="Add a module docstring explaining the purpose of this file.",
                healed_code='"""\nModule purpose goes here.\n"""\n'
            )
        
        elif wound.wound_type == "MUTE_FUNCTION":
            name = wound.location
            return Remedy(
                wound=wound,
                remedy_type="ADD_VOICE",
                suggestion=f"Add a docstring to '{name}' explaining what it does.",
                healed_code=f'    """Describe what {name} does."""'
            )
        
        elif wound.wound_type == "MUTE_CLASS":
            name = wound.location
            return Remedy(
                wound=wound,
                remedy_type="ADD_IDENTITY",
                suggestion=f"Add a docstring to class '{name}' explaining its purpose.",
                healed_code=f'    """Describe the purpose of {name}."""'
            )
        
        elif wound.wound_type == "BLIND_PARAMETERS":
            return Remedy(
                wound=wound,
                remedy_type="ADD_TYPES",
                suggestion=f"Add type hints to the parameters of '{wound.location}'."
            )
        
        elif wound.wound_type == "UNKNOWN_OUTCOME":
            return Remedy(
                wound=wound,
                remedy_type="ADD_RETURN_TYPE",
                suggestion=f"Add a return type hint to '{wound.location}'."
            )
        
        elif wound.wound_type == "OVERWHELMED":
            return Remedy(
                wound=wound,
                remedy_type="DECOMPOSE",
                suggestion=f"Split '{wound.location}' into smaller functions. Each function should do one thing."
            )
        
        elif wound.wound_type == "UNNAMED":
            return Remedy(
                wound=wound,
                remedy_type="RENAME",
                suggestion=f"Give '{wound.location}' a more descriptive name."
            )
        
        elif wound.wound_type == "EMPTY_CHARACTER":
            return Remedy(
                wound=wound,
                remedy_type="ADD_BEHAVIOR",
                suggestion=f"Add methods to class '{wound.location}' or convert to dataclass."
            )
        
        return None
    
    def diagnose(self, source: str) -> str:
        """Full diagnosis with wounds and remedies."""
        self.examine(source)
        self.heal()
        
        lines = ["═" * 50, "  DIAGNOSIS", "═" * 50, ""]
        
        if not self.wounds:
            lines.append("  No wounds found. The code is whole.")
            return "\n".join(lines)
        
        lines.append(f"  Found {len(self.wounds)} wound(s):")
        lines.append("")
        
        for wound in self.wounds:
            severity_bar = "█" * int(wound.severity * 5) + "░" * (5 - int(wound.severity * 5))
            lines.append(f"  [{severity_bar}] {wound.wound_type}")
            lines.append(f"       at {wound.location}:{wound.line}")
            lines.append(f"       {wound.description}")
            lines.append("")
        
        lines.append("─" * 50)
        lines.append("  REMEDIES")
        lines.append("─" * 50)
        lines.append("")
        
        for remedy in self.remedies:
            lines.append(f"  • {remedy.remedy_type}")
            lines.append(f"    {remedy.suggestion}")
            if remedy.healed_code:
                lines.append(f"    Suggested code:")
                for code_line in remedy.healed_code.split("\n"):
                    lines.append(f"      {code_line}")
            lines.append("")
        
        return "\n".join(lines)


def heal_code(source: str) -> str:
    """Diagnose and return full report."""
    healer = Healer()
    return healer.diagnose(source)


# Stress test cases
STRESS_TESTS = {
    "empty": "",
    
    "minimal": "x = 1",
    
    "broken_syntax": "def foo(:\n    pass",
    
    "mute_function": """
def do_something(x, y, z):
    result = x + y + z
    return result
""",
    
    "mute_class": """
class Thing:
    def __init__(self):
        self.value = 0
""",
    
    "complex_function": """
def process_everything(data):
    result = []
    for item in data:
        if item > 0:
            temp = item * 2
            if temp > 10:
                temp = temp / 2
            else:
                temp = temp + 1
            result.append(temp)
        elif item < 0:
            temp = abs(item)
            result.append(-temp)
        else:
            result.append(0)
    total = sum(result)
    average = total / len(result) if result else 0
    maximum = max(result) if result else 0
    minimum = min(result) if result else 0
    return {
        'result': result,
        'total': total,
        'average': average,
        'maximum': maximum,
        'minimum': minimum
    }
""",
    
    "healthy": '''
"""A well-documented module."""

def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"


class Person:
    """Represents a person with a name."""
    
    def __init__(self, name: str):
        """Initialize with a name."""
        self.name = name
    
    def say_hello(self) -> str:
        """Return a greeting from this person."""
        return greet(self.name)
'''
}


def run_stress_tests():
    """Run all stress tests and report results."""
    print("═" * 60)
    print("  STRESS TESTING THE HEALER")
    print("═" * 60)
    print()
    
    healer = Healer()
    
    for name, source in STRESS_TESTS.items():
        print(f"▸ Test: {name}")
        print("─" * 40)
        
        wounds = healer.examine(source)
        print(f"  Wounds found: {len(wounds)}")
        
        for wound in wounds[:3]:  # Show first 3
            print(f"    • {wound.wound_type}: {wound.description[:40]}...")
        
        print()
    
    print("═" * 60)
    print("  FULL DIAGNOSIS OF 'complex_function' TEST")
    print("═" * 60)
    print()
    print(heal_code(STRESS_TESTS["complex_function"]))


if __name__ == "__main__":
    run_stress_tests()
