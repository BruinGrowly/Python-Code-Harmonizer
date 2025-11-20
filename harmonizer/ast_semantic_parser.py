#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AST Semantic Parser (The "Rosetta Stone")
Version 1.1 - Now with Node-to-Dimension Mapping

This class is the critical "bridge" in our Python Code Harmonizer.
It walks a Python Abstract Syntax Tree (AST) and translates logical code
structures into the conceptual keywords understood by the
Divine Invitation Semantic Engine (DIVE-V2).

New in v1.1:
- Now returns a map of {ast.Node: str} to support automated refactoring.
"""

import ast
import re
from typing import Dict, List, Optional, Set, Tuple


class AST_Semantic_Parser(ast.NodeVisitor):
    """
    A "Rosetta Stone" that translates Python AST nodes into
    DIVE-V2 conceptual keywords.
    
    This parser walks through Python's Abstract Syntax Tree and categorizes
    code constructs into semantic dimensions (Love, Justice, Power, Wisdom).
    
    Note: Visitor methods don't "visit" in the semantic sense - they record
    and categorize AST nodes into semantic concepts for later analysis.
    """

    def __init__(self, vocabulary: Set[str]):
        """
        Initializes the parser with the known vocabulary from the DIVE-V2 engine
        to improve mapping accuracy.
        """
        self.known_vocabulary = vocabulary

        self.intent_keyword_map = {
            # WISDOM (Information, Truth, State Checking)
            "get": "wisdom",
            "read": "wisdom",
            "fetch": "wisdom",
            "query": "wisdom",
            "calculate": "wisdom",
            "analyze": "wisdom",
            "return": "wisdom",
            # Boolean predicates - checking state (Wisdom) not enforcing rules (Justice)
            "is": "wisdom",  # is_valid, is_empty - checking state
            "is_": "wisdom",  # with underscore
            "has": "wisdom",  # has_permission - checking existence
            "has_": "wisdom",  # with underscore
            "can": "wisdom",  # can_access - checking capability
            "can_": "wisdom",  # with underscore
            # Property/state words
            "status": "wisdom",
            "state": "wisdom",
            "value": "wisdom",
            "valid": "wisdom",  # Note: different from "validate"
            "needs": "wisdom",  # needs_update - checking need
            # JUSTICE (Validation, Rules, Enforcement)
            "validate": "justice",
            "check": "justice",
            "verify": "justice",
            "assert": "justice",
            "try": "justice",
            "if": "justice",
            "else": "justice",
            "for": "justice",
            "while": "justice",
            "order": "justice",
            # Modal verbs that imply rules
            "should": "justice",
            "must": "justice",
            # POWER (Action, Control, Transformation)
            "set": "power",
            "update": "power",
            "create": "power",
            "build": "power",
            "write": "power",
            "delete": "power",
            "remove": "power",
            "run": "power",
            "execute": "power",
            "raise": "power",
            "save": "power",
            # LOVE (Unity, Connection, Communication)
            "add": "love",
            "append": "love",
            "join": "love",
            "connect": "love",
            "merge": "love",
            "print": "love",  # Communication is a form of Love
            "except": "love",  # Mercy/graceful handling is Love
        }

        self._node_map: Dict[ast.AST, str] = {}
        self._concepts_found: Set[str] = set()

    def _split_snake_case(self, name: str) -> List[str]:
        """Splits 'get_user_by_id' into ['get', 'user', 'by', 'id']"""
        return name.split("_")

    def _map_word_to_concept(self, word: str) -> Optional[str]:
        """Finds the base concept for a given word."""
        word_lower = word.lower()
        if word_lower in self.intent_keyword_map:
            return self.intent_keyword_map[word_lower]
        if word_lower in self.known_vocabulary:
            return word_lower
        for prefix, concept in self.intent_keyword_map.items():
            if word_lower.startswith(prefix):
                return concept
        return None

    def get_intent_concepts(
        self, function_name: str, docstring: Optional[str]
    ) -> List[str]:
        """
        Parses the function's name and docstring to find its "Stated Purpose" (Intent).
        """
        concepts: Set[str] = set()
        name_words = self._split_snake_case(function_name)
        for word in name_words:
            concept = self._map_word_to_concept(word)
            if concept:
                concepts.add(concept)
        if docstring:
            doc_words = re.findall(r"\b\w+\b", docstring.lower())
            for word in doc_words:
                concept = self._map_word_to_concept(word)
                if concept:
                    concepts.add(concept)
        if not concepts and name_words:
            return [word for word in name_words if word in self.known_vocabulary]
        return list(concepts)

    def get_execution_map(
        self, body: List[ast.AST]
    ) -> Tuple[Dict[ast.AST, str], List[str]]:
        """
        Parses the function's body to map each AST node to a semantic dimension
        and return the list of concepts found.
        """
        self._node_map = {}
        self._concepts_found = set()
        for node in body:
            self.visit(node)

        return self._node_map, list(self._concepts_found)

    def _add_concept(self, node: ast.AST, concept: str):
        """Helper to add a concept to both the map and the set."""
        self._node_map[node] = concept
        self._concepts_found.add(concept)

    def visit_Call(self, node: ast.Call) -> None:
        """
        Records function/method calls and categorizes them semantically.
        
        Maps method names to semantic dimensions (e.g., 'execute' -> Power,
        'validate' -> Justice, 'get' -> Wisdom).
        """
        concept = None
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            obj_name = ""
            if isinstance(node.func.value, ast.Attribute):
                if (
                    isinstance(node.func.value.value, ast.Name)
                    and node.func.value.value.id == "self"
                ):
                    obj_name = node.func.value.attr
            if method_name == "add" and obj_name == "_concepts_found":
                concept = "wisdom"
            else:
                concept = self._map_word_to_concept(method_name)
        elif isinstance(node.func, ast.Name):
            concept = self._map_word_to_concept(node.func.id)
        if concept:
            self._add_concept(node, concept)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """
        Records If statements as Justice concepts (control flow/decision-making).
        
        If statements enforce conditions and control execution flow, which
        aligns with Justice (rules, structure, enforcement).
        """
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """
        Records Assert statements as Justice concepts (validation/enforcement).
        
        Assertions enforce invariants and preconditions, directly representing
        Justice principles of validation and rule enforcement.
        """
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        """
        Records Try-Except blocks with dual semantics.
        
        Try blocks represent Justice (structural error handling), while
        exception handlers represent Love (mercy, graceful recovery).
        """
        self._add_concept(node, "justice")
        if node.handlers:
            self._add_concept(node.handlers[0], "love")
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise) -> None:
        """
        Records Raise statements as Power concepts (forceful action).
        
        Raising exceptions is an active, forceful interruption of normal
        flow, representing Power (control, force, action).
        """
        self._add_concept(node, "power")
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """
        Records For loops as Justice concepts (structured iteration).
        
        For loops impose structure and order on iteration, representing
        Justice (rules, patterns, systematic processing).
        """
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        """
        Records While loops as Justice concepts (conditional iteration).
        
        While loops enforce conditions for continued iteration, representing
        Justice (rules, enforcement, conditional control).
        """
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        """
        Records Return statements as Wisdom concepts (providing results).
        
        Return statements deliver computed results or knowledge back to
        callers, representing Wisdom (information, knowledge transfer).
        """
        self._add_concept(node, "wisdom")
        self.generic_visit(node)

    def generic_visit(self, node: ast.AST) -> None:
        """
        Default visitor that continues traversing the AST.
        
        This method is called for AST node types that don't have
        specific visitor methods defined.
        """
        super().generic_visit(node)
