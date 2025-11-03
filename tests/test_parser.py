# tests/test_parser.py

import pytest
import ast

from harmonizer.ast_semantic_parser import AST_Semantic_Parser
from harmonizer.divine_invitation_engine_V2 import DivineInvitationSemanticEngine


@pytest.fixture(scope="module")
def parser():
    """Provides a parser instance initialized with the engine's vocabulary."""
    engine = DivineInvitationSemanticEngine()
    return AST_Semantic_Parser(vocabulary=engine.vocabulary.all_keywords)


# --- Test Intent Parsing ---


def test_intent_from_function_name(parser):
    """
    Tests that concepts are correctly extracted from a function name.
    """
    name = "get_user_by_id_and_update_status"
    # 'get' -> wisdom, 'update' -> power
    expected_concepts = {"wisdom", "power", "status"}
    concepts = parser.get_intent_concepts(name, None)
    assert set(concepts) == expected_concepts


def test_intent_from_docstring(parser):
    """Tests that concepts from the docstring are merged with the name's concepts."""
    name = "process_data"
    docstring = "This function will calculate and analyze the results."
    expected_concepts = {"wisdom"}
    concepts = parser.get_intent_concepts(name, docstring)
    assert set(concepts) == expected_concepts


def test_intent_name_and_docstring_combined(parser):
    """Ensures concepts from both the name and docstring are found."""
    name = "get_data"
    docstring = "This function will create a new user."
    expected_concepts = {"wisdom", "power"}
    concepts = parser.get_intent_concepts(name, docstring)
    assert set(concepts) == expected_concepts


# --- Test Execution Parsing ---


def test_execution_simple_function_call(parser):
    """Tests that a simple function call is mapped to a concept."""
    code = "delete_user(user_id)"
    expected_concepts = {"power"}
    body = ast.parse(code).body
    _, concepts = parser.get_execution_map(body)
    assert set(concepts) == expected_concepts


def test_execution_contextual_override(parser):
    """
    Tests the contextual override for `_concepts_found.add`.
    This should be mapped to 'wisdom', not 'love'.
    """
    code = "self._concepts_found.add('new_concept')"
    expected_concepts = {"wisdom"}
    body = ast.parse(code).body
    _, concepts = parser.get_execution_map(body)
    assert set(concepts) == expected_concepts


def test_execution_contextual_override(parser):
    """
    Tests the contextual override for `_concepts_found.add`.
    This should be mapped to 'wisdom', not 'community'.
    """
    code = "self._concepts_found.add('new_concept')"
    expected_concepts = {"wisdom"}

    import ast

    body = ast.parse(code).body
    concepts = parser.get_execution_concepts(body)

    assert set(concepts) == expected_concepts


def test_execution_method_call(parser):
    """Tests that a method call (e.g., db.query) is mapped correctly."""
    code = "db.query('SELECT * FROM users')"
    expected_concepts = {"wisdom"}
    body = ast.parse(code).body
    _, concepts = parser.get_execution_map(body)
    assert set(concepts) == expected_concepts


def test_execution_control_flow(parser):
    """Tests that control flow statements like 'if' and 'for' are mapped."""
    code = """
if user.is_admin:
    for item in items:
        process_item(item)
    """
    expected_concepts = {"justice"}
    body = ast.parse(code).body
    _, concepts = parser.get_execution_map(body)
    assert set(concepts) == expected_concepts


def test_execution_error_handling(parser):
    """Tests that 'try/except/raise' are mapped to their respective concepts."""
    code = """
try:
    result = 1 / 0
except ZeroDivisionError:
    log_error("Division by zero")
    raise ValueError("Invalid operation")
    """
    expected_concepts = {"justice", "love", "power"}
    body = ast.parse(code).body
    _, concepts = parser.get_execution_map(body)
    assert set(concepts) == expected_concepts
