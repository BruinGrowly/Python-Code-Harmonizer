#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The Refactorer Engine (v1.0)

This is the "hands" of the self-healing system. It uses the dimensional
map provided by the AST_Semantic_Parser to programmatically refactor
disharmonious code.
"""

import ast
from collections import defaultdict
from typing import Dict, List

import black


class Refactorer:
    """
    Analyzes a function's dimensional map and suggests
    concrete refactoring strategies.
    """

    def __init__(
        self, function_node: ast.FunctionDef, execution_map: Dict[ast.AST, str]
    ):
        self.function_node = function_node
        self.execution_map = execution_map

    def suggest_dimensional_split(self) -> str:
        """
        Analyzes the function for a dimensional split and generates refactored code.
        """
        dimensional_groups = self._group_nodes_by_dimension()
        if len(dimensional_groups) < 2:
            return "# No clear dimensional split found."

        new_functions = []
        new_body_calls = []

        for dimension, nodes in dimensional_groups.items():
            new_func_name = f"_{self.function_node.name}_{dimension}"
            new_func = self._create_new_function(new_func_name, nodes)
            new_functions.append(new_func)
            # Handle 'self' for method calls
            is_method = (
                self.function_node.args.args
                and self.function_node.args.args[0].arg == "self"
            )
            if is_method:
                call_func = ast.Attribute(
                    value=ast.Name(id="self", ctx=ast.Load()),
                    attr=new_func_name,
                    ctx=ast.Load(),
                )
                call_args = [
                    ast.Name(id=arg.arg, ctx=ast.Load())
                    for arg in self.function_node.args.args[1:]
                ]
            else:
                call_func = ast.Name(id=new_func_name, ctx=ast.Load())
                call_args = [
                    ast.Name(id=arg.arg, ctx=ast.Load())
                    for arg in self.function_node.args.args
                ]

            new_body_calls.append(
                ast.Expr(value=ast.Call(func=call_func, args=call_args, keywords=[]))
            )

        original_func_rewritten = ast.FunctionDef(
            name=self.function_node.name,
            args=self.function_node.args,
            body=new_body_calls,
            decorator_list=self.function_node.decorator_list,
            returns=self.function_node.returns,
        )

        # Create a new module to hold all the functions
        new_module = ast.Module(
            body=new_functions + [original_func_rewritten],
            type_ignores=[],
        )

        # Fix missing location info and unparse the entire module
        ast.fix_missing_locations(new_module)
        unformatted_code = ast.unparse(new_module)

        # Format the generated code using black
        try:
            final_code = black.format_str(
                unformatted_code, mode=black.FileMode()
            ).strip()
        except black.NothingChanged:
            final_code = unformatted_code.strip()

        return "# --- Suggested Refactoring: Dimensional Split ---\n\n" + final_code

    def _group_nodes_by_dimension(self) -> Dict[str, List[ast.AST]]:
        """
        Groups the function's body nodes by their semantic dimension,
        keeping control flow blocks together.
        """
        groups = defaultdict(list)

        # This is a simplified approach. A more robust solution would
        # build a dependency graph.
        for node, dimension in self.execution_map.items():
            groups[dimension].append(node)
        return groups

    def _create_new_function(
        self, name: str, body_nodes: List[ast.AST]
    ) -> ast.FunctionDef:
        """Creates a new function definition from a list of body nodes."""
        return ast.FunctionDef(
            name=name,
            args=self.function_node.args,
            body=body_nodes,
            decorator_list=[],
            returns=None,
        )
