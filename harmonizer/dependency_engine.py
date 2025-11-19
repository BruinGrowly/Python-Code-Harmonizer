#!/usr/bin/env python3
"""
Dependency Engine - Analyzes the "Gravity" of code modules.
"""

import ast
import os
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

@dataclass
class DependencyNode:
    """A node in the dependency graph (a file)"""
    file_path: str
    imports: Set[str]  # Files this node imports
    imported_by: Set[str]  # Files that import this node
    gravity: float = 0.0  # Gravitational Pull (In-degree centrality)
    mass: float = 1.0  # Complexity/Size (proxy for mass)

class DependencyEngine:
    """
    Analyzes the dependency structure of the codebase.
    Models the "Gravitational Pull" between modules.
    """
    
    def __init__(self, codebase_path: str):
        self.codebase_path = codebase_path
        self.nodes: Dict[str, DependencyNode] = {}
        
    def build_graph(self, python_files: List[str]):
        """Builds the dependency graph from a list of files"""
        # Initialize nodes
        for file_path in python_files:
            rel_path = os.path.relpath(file_path, self.codebase_path)
            # Normalize path separators
            rel_path = rel_path.replace("\\", "/")
            self.nodes[rel_path] = DependencyNode(
                file_path=rel_path,
                imports=set(),
                imported_by=set()
            )
            
        # Parse imports
        for rel_path, node in self.nodes.items():
            abs_path = os.path.join(self.codebase_path, rel_path)
            try:
                with open(abs_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                    
                for stmt in ast.walk(tree):
                    if isinstance(stmt, (ast.Import, ast.ImportFrom)):
                        self._process_import(node, stmt)
            except Exception:
                continue
                
        # Calculate Gravity
        self._calculate_gravity()
        
    def _process_import(self, source_node: DependencyNode, stmt: ast.AST):
        """Resolves an import statement to a target file"""
        target_module = None
        
        if isinstance(stmt, ast.Import):
            for alias in stmt.names:
                target_module = alias.name
                self._link_nodes(source_node, target_module)
                
        elif isinstance(stmt, ast.ImportFrom):
            if stmt.module:
                target_module = stmt.module
                self._link_nodes(source_node, target_module)
            elif stmt.level > 0:
                # Relative import (simplified handling)
                pass

    def _link_nodes(self, source_node: DependencyNode, target_module: str):
        """Links source node to target module if it exists in the graph"""
        # Convert module path (harmonizer.main) to file path (harmonizer/main.py)
        potential_paths = [
            target_module.replace(".", "/") + ".py",
            target_module.replace(".", "/") + "/__init__.py"
        ]
        
        for path in potential_paths:
            if path in self.nodes:
                target_node = self.nodes[path]
                source_node.imports.add(path)
                target_node.imported_by.add(source_node.file_path)
                return

    def _calculate_gravity(self):
        """
        Calculates Gravitational Pull for each node.
        Gravity = In-degree (number of dependents).
        """
        for node in self.nodes.values():
            node.gravity = len(node.imported_by)

    def get_black_holes(self, threshold: int = 5) -> List[DependencyNode]:
        """Returns nodes with high gravity (many dependents)"""
        return [n for n in self.nodes.values() if n.gravity >= threshold]
