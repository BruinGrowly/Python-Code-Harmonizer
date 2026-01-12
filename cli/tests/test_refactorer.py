# tests/test_refactorer.py

import ast

import pytest

from harmonizer.ast_semantic_parser import AST_Semantic_Parser
from harmonizer.divine_invitation_engine_V2 import DivineInvitationSemanticEngine
from harmonizer.refactorer import Refactorer

# A sample function with a clear dimensional split (Justice, Power, and Love)
DISHARMONIOUS_FUNCTION = """
class UserManager:
    def __init__(self, db):
        self.db = db

    def validate_and_delete_user(self, user_id):
        \"\"\"Validates a user's status and then deletes them.\"\"\"
        assert user_id > 0, "Invalid user ID"
        self.db.delete_user(user_id=user_id)
        print(f"User {user_id} deleted.")
"""


@pytest.fixture
def db_mock():
    """Mocks a database object."""

    class DBMock:
        def delete_user(self, user_id):
            pass

    return DBMock()


@pytest.fixture(scope="module")
def parser():
    """Provides a parser instance."""
    engine = DivineInvitationSemanticEngine()
    return AST_Semantic_Parser(vocabulary=engine.vocabulary.all_keywords)


def test_dimensional_split_refactoring(parser, db_mock):
    """
    Tests the core dimensional split refactoring logic by inspecting the generated AST.
    """
    # 1. Parse the sample class and get the execution map for the method
    class_node = ast.parse(DISHARMONIOUS_FUNCTION).body[0]
    function_node = class_node.body[1]  # The 'validate_and_delete_user' method
    execution_map, _ = parser.get_execution_map(function_node.body)

    # 2. Generate the refactoring suggestion
    refactorer = Refactorer(function_node, execution_map)
    suggestion_code = refactorer.suggest_dimensional_split()

    # 3. Parse the generated code to ensure it's syntactically valid
    try:
        suggestion_ast = ast.parse(suggestion_code)
    except SyntaxError as e:
        pytest.fail(
            f"The generated refactoring suggestion is not valid Python code.\n"
            f"Error: {e}\n"
            f"--- Code ---\n{suggestion_code}"
        )

    # 4. Validate the generated AST
    # Note: The exact number of functions can vary based on grouping.
    # We are checking for at least the rewritten original + 1 new function.
    assert (
        len(suggestion_ast.body) >= 2
    ), "Expected at least one new function and the rewritten original."

    # Find the generated functions in the new module
    generated_funcs = {
        node.name: node for node in suggestion_ast.body if isinstance(node, ast.FunctionDef)
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
    assert original_func.body[0].value.func.attr == "_validate_and_delete_user_justice"
    assert original_func.body[1].value.func.attr == "_validate_and_delete_user_power"
    assert original_func.body[2].value.func.attr == "_validate_and_delete_user_love"
