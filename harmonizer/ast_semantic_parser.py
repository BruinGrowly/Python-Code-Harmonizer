#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AST Semantic Parser (The "Rosetta Stone")
Version 1.0

This class is the critical "bridge" in our Python Code Harmonizer.
It walks a Python Abstract Syntax Tree (AST) and translates logical code
structures into the conceptual keywords understood by the
Divine Invitation Semantic Engine (DIVE-V2).
"""

import ast
import re
from typing import List, Optional, Set


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

        # This map translates common function name prefixes and keywords
        # into DIVE-V2 concepts. This is the core "Intent" logic.
        self.intent_keyword_map = {
            # WISDOM (Information, Truth)
            "get": "information",
            "read": "information",
            "fetch": "information",
            "query": "information",
            "calculate": "wisdom",
            "analyze": "wisdom",
            "validate": "truth",
            "check": "truth",
            "is_": "truth",
            "return": "information",
            # POWER (Action, Control)
            "set": "power",
            "update": "power",
            "create": "create",
            "build": "create",
            "write": "manifest",
            "delete": "force",
            "remove": "force",
            "run": "power",
            "execute": "power",
            "raise": "force",
            # JUSTICE (Order, Rules, Logic)
            "assert": "law",
            "try": "logic",
            "except": "mercy",  # (!)
            "if": "logic",
            "else": "logic",
            "for": "process",
            "while": "process",
            "order": "order",
            # LOVE (Unity, Connection)
            "add": "community",
            "append": "community",
            "join": "harmony",
            "connect": "harmony",
            "merge": "togetherness",
        }

        self._concepts_found: Set[str] = set()

    def _split_snake_case(self, name: str) -> List[str]:
        """Splits 'get_user_by_id' into ['get', 'user', 'by', 'id']"""
        return name.split("_")

    def _map_word_to_concept(self, word: str) -> Optional[str]:
        """Finds the base concept for a given word."""
        word_lower = word.lower()

        # Priority 1: Direct match in the map
        if word_lower in self.intent_keyword_map:
            return self.intent_keyword_map[word_lower]

        # Priority 2: Match in the full DIVE-V2 vocabulary
        if word_lower in self.known_vocabulary:
            return word_lower

        # Priority 3: Prefix match in the map
        for prefix, concept in self.intent_keyword_map.items():
            if word_lower.startswith(prefix):
                return concept

        return None

    # --- PHASE 2: "INTENT" PARSING ---

    def get_intent_concepts(
        self, function_name: str, docstring: Optional[str]
    ) -> List[str]:
        """
        Parses the function's name and docstring to find its
        "Stated Purpose" (Intent).
        """
        concepts: Set[str] = set()

        # 1. Parse the function name
        name_words = self._split_snake_case(function_name)
        for word in name_words:
            concept = self._map_word_to_concept(word)
            if concept:
                concepts.add(concept)

        # 2. Parse the docstring (as a simple bag of words)
        if docstring:
            doc_words = re.findall(r"\b\w+\b", docstring.lower())
            for word in doc_words:
                concept = self._map_word_to_concept(word)
                if concept:
                    concepts.add(concept)

        # Fallback: if no concepts found, use the raw words from the name
        if not concepts and name_words:
            return [word for word in name_words if word in self.known_vocabulary]

        return list(concepts)

    # --- PHASE 2: "EXECUTION" PARSING ---

    def get_execution_concepts(self, body: List[ast.AST]) -> List[str]:
        """
        Parses the function's body (a list of AST nodes) to find its
        "Actual Action" (Execution).

        This method "walks" the AST using the ast.NodeVisitor pattern.
        """
        self._concepts_found = set()
        for node in body:
            self.visit(node)
        return list(self._concepts_found)

    # --- AST "ROSETTA STONE" MAPPINGS ---
    # These 'visit_...' methods are called by self.visit()
    # Each one maps a Python logical structure to a DIVE-V2 concept.

    def visit_Call(self, node: ast.Call):
        """
        This is the most important node. It represents an "action"
        (a function call).
        """
        concept = None

        # Check for obj.method() calls (e.g., db.delete)
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            obj_name = ""
            if isinstance(node.func.value, ast.Attribute):
                if (
                    isinstance(node.func.value.value, ast.Name)
                    and node.func.value.value.id == "self"
                ):
                    obj_name = node.func.value.attr

            # --- CONTEXTUAL OVERRIDE (v1.4) ---
            # If we find `self._concepts_found.add()`, this is not a "community"
            # action, but an act of "recording information" (Wisdom).
            if method_name == "add" and obj_name == "_concepts_found":
                concept = "wisdom"
            else:
                concept = self._map_word_to_concept(method_name)

        # Check for simple function() calls (e.g., print)
        elif isinstance(node.func, ast.Name):
            concept = self._map_word_to_concept(node.func.id)

        if concept:
            self._concepts_found.add(concept)

        # Continue walking *inside* the call (e.g., its arguments)
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        """Maps 'if' statements to 'logic' (Justice)"""
        self._concepts_found.add("logic")
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        """Maps 'assert' statements to 'truth' and 'law' (Justice)"""
        self._concepts_found.add("truth")
        self._concepts_found.add("law")
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        """Maps 'try/except' blocks to 'logic' and 'mercy' (Justice/Love)"""
        self._concepts_found.add("logic")
        if node.handlers:  # If there is an 'except' block
            self._concepts_found.add("mercy")
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise):
        """Maps 'raise' to 'power' and 'force' (Power)"""
        self._concepts_found.add("power")
        self._concepts_found.add("force")
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        """Maps 'for' loops to 'process' (Justice)"""
        self._concepts_found.add("process")
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        """Maps 'while' loops to 'process' and 'control' (Justice/Power)"""
        self._concepts_found.add("process")
        self._concepts_found.add("control")
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return):
        """Maps 'return' to 'information' and 'result' (Wisdom)"""
        self._concepts_found.add("information")
        self._concepts_found.add("wisdom")
        self.generic_visit(node)

    def generic_visit(self, node: ast.AST):
        """This is the default visitor that just continues the walk."""
        super().generic_visit(node)
