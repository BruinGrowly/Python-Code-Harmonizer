#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AST Semantic Parser V2 (Enhanced)
Version 2.0 - Programming Language Semantics Framework Integration

This enhanced parser incorporates insights from PROGRAMMING_LANGUAGE_SEMANTICS.md
to provide comprehensive mapping of code constructs to LJPW dimensions.

Key improvements over v1:
- 200+ programming verbs mapped to dimensions
- Better context-aware recognition
- Compound pattern detection
- Assignment operation tracking
- Enhanced documentation
"""

import ast
import re
from typing import Dict, List, Optional, Set, Tuple

from harmonizer.programming_constructs_vocabulary import (
    COMPOUND_PATTERNS,
    PROGRAMMING_VERBS,
)


class AST_Semantic_Parser_V2(ast.NodeVisitor):
    """
    Enhanced AST parser that translates Python code into LJPW semantic dimensions.

    Based on the programming language semantics framework which proves that:
    - All code operations map to LJPW dimensions
    - All four dimensions necessary for functional code
    - Code quality correlates with semantic harmony
    """

    def __init__(self, vocabulary: Set[str]):
        """
        Initialize parser with comprehensive programming construct mapping.

        Args:
            vocabulary: Known semantic vocabulary from DIVE engine
        """
        self.known_vocabulary = vocabulary

        # Use comprehensive programming verbs vocabulary
        self.intent_keyword_map = PROGRAMMING_VERBS.copy()

        # Add any vocabulary words that aren't already mapped
        for word in vocabulary:
            if word not in self.intent_keyword_map:
                self.intent_keyword_map[word] = word

        self._node_map: Dict[ast.AST, str] = {}
        self._concepts_found: Set[str] = set()
        self._assignment_count = 0
        self._call_count = 0

    def _split_snake_case(self, name: str) -> List[str]:
        """Split 'get_user_by_id' into ['get', 'user', 'by', 'id']"""
        return name.split("_")

    def _split_camel_case(self, name: str) -> List[str]:
        """Split 'getUserById' into ['get', 'User', 'By', 'Id']"""
        return re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+", name)

    def _split_name(self, name: str) -> List[str]:
        """Smart name splitting supporting both snake_case and camelCase"""
        if "_" in name:
            return self._split_snake_case(name)
        else:
            return self._split_camel_case(name)

    def _map_word_to_concept(self, word: str, context: str = "default") -> Optional[str]:
        """
        Map a word to its semantic dimension.

        Args:
            word: The word to map
            context: Additional context for disambiguation

        Returns:
            Semantic dimension or None if not found
        """
        word_lower = word.lower()

        # Check programming verbs first
        if word_lower in self.intent_keyword_map:
            return self.intent_keyword_map[word_lower]

        # Check if it's in known vocabulary
        if word_lower in self.known_vocabulary:
            return word_lower

        # Check for prefix matches
        for prefix, concept in self.intent_keyword_map.items():
            if word_lower.startswith(prefix):
                return concept

        return None

    def _check_compound_pattern(self, words: List[str]) -> Optional[str]:
        """
        Check if a sequence of words matches a compound pattern.

        Args:
            words: List of words from function name

        Returns:
            Semantic dimension if compound pattern found, None otherwise
        """
        # Try combinations of first 2-3 words
        for length in [3, 2]:
            if len(words) >= length:
                compound = "_".join(words[:length]).lower()
                if compound in COMPOUND_PATTERNS:
                    return COMPOUND_PATTERNS[compound]
        return None

    def get_intent_concepts(self, function_name: str, docstring: Optional[str]) -> List[str]:
        """
        Parse function name and docstring to extract semantic intent.

        Args:
            function_name: Name of the function
            docstring: Function docstring (if any)

        Returns:
            List of semantic concepts representing intent
        """
        concepts: Set[str] = set()
        name_words = self._split_name(function_name)

        # Check for compound patterns first
        compound_concept = self._check_compound_pattern(name_words)
        if compound_concept:
            concepts.add(compound_concept)
        else:
            # Map individual words
            for word in name_words:
                concept = self._map_word_to_concept(word)
                if concept:
                    concepts.add(concept)

        # Extract concepts from docstring
        if docstring:
            doc_words = re.findall(r"\b\w+\b", docstring.lower())
            for word in doc_words:
                concept = self._map_word_to_concept(word)
                if concept:
                    concepts.add(concept)

        # Fallback to words in vocabulary
        if not concepts and name_words:
            concepts.update([word for word in name_words if word in self.known_vocabulary])

        return list(concepts)

    def get_execution_map(self, body: List[ast.AST]) -> Tuple[Dict[ast.AST, str], List[str]]:
        """
        Parse function body to map AST nodes to semantic dimensions.

        Args:
            body: List of AST nodes from function body

        Returns:
            Tuple of (node_map, concepts_list)
        """
        self._node_map = {}
        self._concepts_found = set()
        self._assignment_count = 0
        self._call_count = 0

        for node in body:
            self.visit(node)

        return self._node_map, list(self._concepts_found)

    def _add_concept(self, node: ast.AST, concept: str):
        """Add a concept to both the map and the set."""
        self._node_map[node] = concept
        self._concepts_found.add(concept)

    # ========================================================================
    # WISDOM OPERATIONS (Information & Knowledge)
    # ========================================================================

    def visit_Return(self, node: ast.Return):
        """Return statements are WISDOM (providing information)"""
        self._add_concept(node, "wisdom")
        self.generic_visit(node)

    # ========================================================================
    # JUSTICE OPERATIONS (Validation & Correctness)
    # ========================================================================

    def visit_If(self, node: ast.If):
        """Conditionals are JUSTICE (logical structure)"""
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        """Assertions are JUSTICE (enforcing correctness)"""
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        """Loops are JUSTICE (ordered processing)"""
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        """While loops are JUSTICE (conditional iteration)"""
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        """Try blocks are JUSTICE (error boundaries)"""
        self._add_concept(node, "justice")
        # Exception handlers are LOVE (graceful recovery)
        if node.handlers:
            for handler in node.handlers:
                self._add_concept(handler, "love")
        self.generic_visit(node)

    # ========================================================================
    # POWER OPERATIONS (Execution & Transformation)
    # ========================================================================

    def visit_Assign(self, node: ast.Assign):
        """Assignments are POWER (state modification)"""
        self._assignment_count += 1
        self._add_concept(node, "power")
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign):
        """Augmented assignments (+=, -=, etc.) are POWER"""
        self._assignment_count += 1
        self._add_concept(node, "power")
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        """Annotated assignments are POWER (with JUSTICE for type)"""
        self._assignment_count += 1
        self._add_concept(node, "power")
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise):
        """Raising exceptions is POWER (forcing exception flow)"""
        self._add_concept(node, "power")
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete):
        """Delete statements are POWER (destruction)"""
        self._add_concept(node, "power")
        self.generic_visit(node)

    # ========================================================================
    # MIXED OPERATIONS (Context-Dependent)
    # ========================================================================

    def visit_Call(self, node: ast.Call):
        """
        Function/method calls - dimension depends on the operation.

        Common patterns:
        - obj.get_*() → WISDOM (retrieval)
        - obj.save() → POWER (persistence)
        - obj.validate() → JUSTICE (verification)
        - obj.send_*() → LOVE (communication)
        """
        self._call_count += 1
        concept = None

        if isinstance(node.func, ast.Attribute):
            # Method call: obj.method()
            method_name = node.func.attr

            # Special case: self._concepts_found.add() is WISDOM (recording)
            obj_name = self._get_object_name(node.func.value)
            if method_name == "add" and obj_name == "_concepts_found":
                concept = "wisdom"
            else:
                # Use comprehensive verb mapping
                concept = self._map_word_to_concept(method_name)

        elif isinstance(node.func, ast.Name):
            # Direct function call: function()
            func_name = node.func.id
            concept = self._map_word_to_concept(func_name)

        if concept:
            self._add_concept(node, concept)

        self.generic_visit(node)

    def _get_object_name(self, node: ast.AST) -> str:
        """Extract object name from an expression."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "self":
                return node.attr
        return ""

    # ========================================================================
    # LOVE OPERATIONS (Integration & Communication)
    # ========================================================================

    def visit_With(self, node: ast.With):
        """Context managers are LOVE (resource integration)"""
        self._add_concept(node, "love")
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        """Imports are LOVE (connecting external modules)"""
        self._add_concept(node, "love")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """From imports are LOVE (integrating external code)"""
        self._add_concept(node, "love")
        self.generic_visit(node)

    # ========================================================================
    # Generic fallback
    # ========================================================================

    def generic_visit(self, node: ast.AST):
        """Continue traversing the AST."""
        super().generic_visit(node)

    # ========================================================================
    # Statistics and diagnostics
    # ========================================================================

    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about code complexity.

        Returns:
            Dictionary with counts of different operation types
        """
        dimension_counts = {
            "wisdom": 0,
            "justice": 0,
            "power": 0,
            "love": 0,
        }

        for concept in self._concepts_found:
            if concept in dimension_counts:
                dimension_counts[concept] += 1

        return {
            **dimension_counts,
            "total_operations": len(self._concepts_found),
            "assignments": self._assignment_count,
            "calls": self._call_count,
        }
