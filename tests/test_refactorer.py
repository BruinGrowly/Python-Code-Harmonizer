# tests/test_refactorer.py

import ast
import pytest

from harmonizer.refactorer import Refactorer
from harmonizer.ast_semantic_parser import AST_Semantic_Parser
from harmonizer.divine_invitation_engine_V2 import DivineInvitationSemanticEngine

# A sample function with a clear dimensional split (Justice, Power, and Love)
DISHARMONIOUS_FUNCTION = """
def validate_and_delete_user(user_id):
    \"\"\"Validates a user's status and then deletes them.\"\"\"
    assert user_id > 0, "Invalid user ID"
    db.delete_user(user_id=user_id)
    print(f"User {user_id} deleted.")
"""


@pytest.fixture(scope="module")
def parser():
    """Provides a parser instance."""
    engine = DivineInvitationSemanticEngine()
    return AST_Semantic_Parser(vocabulary=engine.vocabulary.all_keywords)


def test_dimensional_split_refactoring(parser):
    """
    Tests the core dimensional split refactoring logic by inspecting the generated AST.
    """
    # 1. Parse the sample function and get the execution map
    function_node = ast.parse(DISHARMONIOUS_FUNCTION).body[0]
    execution_map, _ = parser.get_execution_map(function_node.body)

    # 2. Generate the refactoring suggestion
    refactorer = Refactorer(function_node, execution_map)
    suggestion_code = refactorer.suggest_dimensional_split()

    # 3. Parse the generated code into an AST for validation
    suggestion_ast = ast.parse(suggestion_code)

    # 4. Validate the generated AST
    assert len(suggestion_ast.body) == 4  # 3 new functions + 1 rewritten original

    # Find the generated functions in the new module
    generated_funcs = {
        node.name: node
        for node in suggestion_ast.body
        if isinstance(node, ast.FunctionDef)
    }

    # Check for the presence of all expected functions
    assert "_validate_and_delete_user_justice" in generated_funcs
    assert "_validate_and_delete_user_power" in generated_funcs
    assert "_validate_and_delete_user_love" in generated_funcs
    assert "validate_and_delete_user" in generated_funcs

    # Check the bodies of the new, dimensionally-pure functions
    justice_func = generated_funcs["_validate_and_delete_user_justice"]
    assert isinstance(justice_func.body[0], ast.Assert)

    power_func = generated_funcs["_validate_and_delete_user_power"]
    assert isinstance(power_func.body[0].value, ast.Call)
    assert power_func.body[0].value.func.attr == "delete_user"

    love_func = generated_funcs["_validate_and_delete_user_love"]
    assert isinstance(love_func.body[0].value, ast.Call)
    assert love_func.body[0].value.func.id == "print"

    # Check the body of the rewritten original function
    original_func = generated_funcs["validate_and_delete_user"]
    assert len(original_func.body) == 3
    assert original_func.body[0].value.func.id == "_validate_and_delete_user_justice"
    assert original_func.body[1].value.func.id == "_validate_and_delete_user_power"
    assert original_func.body[2].value.func.id == "_validate_and_delete_user_love"
