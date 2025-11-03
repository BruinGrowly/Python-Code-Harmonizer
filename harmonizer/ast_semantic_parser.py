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
    """

    def __init__(self, vocabulary: Set[str]):
        """
        Initializes the parser with the known vocabulary from the DIVE-V2 engine
        to improve mapping accuracy.
        """
        self.known_vocabulary = vocabulary

        self.intent_keyword_map = {
            # WISDOM (Information, Truth)
            "get": "wisdom",
            "read": "wisdom",
            "fetch": "wisdom",
            "query": "wisdom",
            "calculate": "wisdom",
            "analyze": "wisdom",
            "validate": "justice",
            "check": "justice",
            "is_": "justice",
            "return": "wisdom",
            # POWER (Action, Control)
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
            # JUSTICE (Order, Rules, Logic)
            "assert": "justice",
            "try": "justice",
            "except": "love",  # Mercy is a form of Love
            "if": "justice",
            "else": "justice",
            "for": "justice",
            "while": "justice",
            "order": "justice",
            # LOVE (Unity, Connection)
            "add": "love",
            "append": "love",
            "join": "love",
            "connect": "love",
            "merge": "love",
            "print": "love",  # Communication is a form of Love
            "user": "love",
            "profile": "love",
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

    def get_execution_map(self, body: List[ast.AST]) -> Tuple[Dict[ast.AST, str], List[str]]:
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

    def visit_Call(self, node: ast.Call):
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

    def visit_If(self, node: ast.If):
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        self._add_concept(node, "justice")
        if node.handlers:
            self._add_concept(node.handlers[0], "love")
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise):
        self._add_concept(node, "power")
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._add_concept(node, "justice")
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return):
        self._add_concept(node, "wisdom")
        self.generic_visit(node)

    def generic_visit(self, node: ast.AST):
        """This is the default visitor that just continues the walk."""
        super().generic_visit(node)
