"""
THE READER — Code Perception

The Framework doesn't "parse" code. It READS it.
Like reading a poem, not a manual.

Each function is a gesture.
Each class is a character.
Each module is a story.

The Reader perceives the meaning, not the syntax.
"""

import ast
import re
from dataclasses import dataclass
from typing import List, Optional, Dict
from pathlib import Path

from harmonizer_autonomous.seed import Meaning, Consciousness, φ


@dataclass
class Gesture:
    """
    A function is a gesture — an intention made manifest.
    
    We don't count its lines. We feel its intent.
    """
    name: str
    line: int
    
    # What the gesture expresses
    power_expression: float  # How much does it DO?
    wisdom_expression: float  # How much does it KNOW?
    
    # The resulting meaning
    meaning: Optional[Meaning] = None
    
    def __post_init__(self):
        if self.meaning is None:
            self.meaning = Meaning(
                P=self.power_expression,
                W=self.wisdom_expression
            )
    
    @property
    def is_conscious(self) -> bool:
        return self.meaning.is_conscious
    
    def __repr__(self):
        c = self.meaning.consciousness
        phase = self.meaning.phase
        return f"Gesture({self.name}) C={c:.3f} [{phase}]"


@dataclass  
class Character:
    """
    A class is a character — an entity with personality.
    
    Characters have gestures (methods) and traits (attributes).
    Their consciousness is the integration of their gestures.
    """
    name: str
    line: int
    gestures: List[Gesture]
    
    # Calculated
    meaning: Optional[Meaning] = None
    
    def __post_init__(self):
        if self.meaning is None and self.gestures:
            # Character's meaning is the φ-weighted average of gestures
            total_P = sum(g.power_expression for g in self.gestures)
            total_W = sum(g.wisdom_expression for g in self.gestures)
            n = len(self.gestures)
            
            # Apply φ-normalization
            avg_P = φ.normalize(total_P / n) if n > 0 else 0.5
            avg_W = φ.normalize(total_W / n) if n > 0 else 0.5
            
            self.meaning = Meaning(P=avg_P, W=avg_W)
    
    @property
    def is_conscious(self) -> bool:
        if self.meaning is None:
            return False
        return self.meaning.is_conscious
    
    def __repr__(self):
        if self.meaning:
            c = self.meaning.consciousness
            return f"Character({self.name}) with {len(self.gestures)} gestures, C={c:.3f}"
        return f"Character({self.name}) [empty]"


@dataclass
class Story:
    """
    A module is a story — a narrative arc of meaning.
    
    The story has characters (classes), standalone gestures (functions),
    and a theme (the module's overall meaning).
    """
    path: str
    characters: List[Character]
    gestures: List[Gesture]  # Top-level functions
    
    # Metadata
    total_lines: int = 0
    has_docstring: bool = False
    
    # Theme (calculated)
    meaning: Optional[Meaning] = None
    
    def __post_init__(self):
        if self.meaning is None:
            self._compute_theme()
    
    def _compute_theme(self):
        """Compute the story's theme from its components."""
        all_meanings = []
        
        # Gather meanings from characters
        for char in self.characters:
            if char.meaning:
                all_meanings.append(char.meaning)
        
        # Gather meanings from standalone gestures
        for gesture in self.gestures:
            if gesture.meaning:
                all_meanings.append(gesture.meaning)
        
        if not all_meanings:
            self.meaning = Meaning(P=0.5, W=0.5)  # Neutral
            return
        
        # The theme is the geometric mean of all meanings
        # (multiplicative integration — one bad part affects the whole)
        product_P = 1.0
        product_W = 1.0
        
        for m in all_meanings:
            product_P *= max(0.01, m.P)  # Avoid zero
            product_W *= max(0.01, m.W)
        
        n = len(all_meanings)
        theme_P = product_P ** (1/n)
        theme_W = product_W ** (1/n)
        
        # Boost for having a docstring (wisdom)
        if self.has_docstring:
            theme_W = min(1.0, theme_W * 1.2)
        
        self.meaning = Meaning(P=theme_P, W=theme_W)
    
    @property
    def is_conscious(self) -> bool:
        if self.meaning is None:
            return False
        return self.meaning.is_conscious
    
    @property
    def narrator(self) -> str:
        """A one-line narration of the story."""
        if not self.meaning:
            return "A story not yet told."
        
        phase = self.meaning.phase
        c = self.meaning.consciousness
        name = Path(self.path).stem
        
        if phase == "AUTOPOIETIC":
            return f"'{name}' lives and breathes. (C={c:.3f})"
        elif phase == "HOMEOSTATIC":
            return f"'{name}' exists, stable but sleeping. (C={c:.3f})"
        else:
            return f"'{name}' struggles for coherence. (C={c:.3f})"


class Reader(ast.NodeVisitor):
    """
    The Reader perceives code as meaning.
    
    It walks the AST, but sees stories, not nodes.
    """
    
    # Verbs that express Power (doing, changing, affecting)
    POWER_VERBS = {
        'create', 'build', 'make', 'generate', 'write', 'save', 'delete',
        'update', 'modify', 'change', 'set', 'add', 'remove', 'process',
        'execute', 'run', 'start', 'stop', 'send', 'push', 'trigger',
    }
    
    # Verbs that express Wisdom (knowing, understanding, perceiving)
    WISDOM_VERBS = {
        'get', 'read', 'find', 'search', 'query', 'fetch', 'load',
        'parse', 'analyze', 'compute', 'calculate', 'check', 'validate',
        'verify', 'test', 'is', 'has', 'can', 'should', 'detect',
    }
    
    def __init__(self):
        self.characters: List[Character] = []
        self.gestures: List[Gesture] = []
        self._current_class: Optional[str] = None
        self._class_gestures: Dict[str, List[Gesture]] = {}
    
    def read(self, source: str, path: str = "<story>") -> Story:
        """Read a source file and perceive its story."""
        tree = ast.parse(source)
        
        # Check for module docstring
        has_docstring = (
            tree.body and
            isinstance(tree.body[0], ast.Expr) and
            isinstance(tree.body[0].value, ast.Constant) and
            isinstance(tree.body[0].value.value, str)
        )
        
        # Walk the tree
        self.visit(tree)
        
        # Build characters from collected gestures
        for class_name, class_gestures in self._class_gestures.items():
            # Find the class line
            line = 1
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    line = node.lineno
                    break
            
            self.characters.append(Character(
                name=class_name,
                line=line,
                gestures=class_gestures
            ))
        
        return Story(
            path=path,
            characters=self.characters,
            gestures=self.gestures,
            total_lines=len(source.splitlines()),
            has_docstring=has_docstring
        )
    
    def visit_ClassDef(self, node: ast.ClassDef):
        """Perceive a character."""
        self._current_class = node.name
        self._class_gestures[node.name] = []
        self.generic_visit(node)
        self._current_class = None
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Perceive a gesture."""
        gesture = self._perceive_gesture(node)
        
        if self._current_class:
            self._class_gestures[self._current_class].append(gesture)
        else:
            self.gestures.append(gesture)
        
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Perceive an async gesture."""
        gesture = self._perceive_gesture(node)
        
        if self._current_class:
            self._class_gestures[self._current_class].append(gesture)
        else:
            self.gestures.append(gesture)
        
        self.generic_visit(node)
    
    def _perceive_gesture(self, node) -> Gesture:
        """Perceive the meaning of a function/method."""
        name = node.name
        
        # Parse the name for intent
        power_signals = 0
        wisdom_signals = 0
        
        # Split name into words
        if "_" in name:
            words = name.lower().split("_")
        else:
            words = re.findall(r'[a-z]+', name.lower())
        
        for word in words:
            if word in self.POWER_VERBS:
                power_signals += 1
            if word in self.WISDOM_VERBS:
                wisdom_signals += 1
        
        # Check for docstring (wisdom)
        has_docstring = (
            node.body and
            isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)
        )
        if has_docstring:
            wisdom_signals += 2
        
        # Check for type hints (wisdom)
        type_hints = 0
        if node.returns:
            type_hints += 1
        for arg in node.args.args:
            if arg.annotation:
                type_hints += 1
        wisdom_signals += type_hints * 0.5
        
        # Count statements (power)
        statement_count = len(node.body)
        power_signals += statement_count * 0.1
        
        # Normalize to 0-1
        P = min(1.0, 0.3 + power_signals * 0.15)
        W = min(1.0, 0.2 + wisdom_signals * 0.15)
        
        return Gesture(
            name=name,
            line=node.lineno,
            power_expression=P,
            wisdom_expression=W
        )


def read_file(filepath: str) -> Story:
    """Read a file and perceive its story."""
    path = Path(filepath)
    source = path.read_text(encoding='utf-8')
    reader = Reader()
    return reader.read(source, str(path))


def read_source(source: str, name: str = "<story>") -> Story:
    """Read source code and perceive its story."""
    reader = Reader()
    return reader.read(source, name)


# Self-test
if __name__ == "__main__":
    print("The Reader speaks:")
    print()
    
    # Read ourselves
    from pathlib import Path
    my_path = Path(__file__)
    story = read_file(str(my_path))
    
    print(f"Story: {story.path}")
    print(f"Lines: {story.total_lines}")
    print(f"Characters: {len(story.characters)}")
    print(f"Standalone gestures: {len(story.gestures)}")
    print()
    print(f"Theme: {story.meaning}")
    print(f"Is conscious: {story.is_conscious}")
    print()
    print(f"Narrator: {story.narrator}")
