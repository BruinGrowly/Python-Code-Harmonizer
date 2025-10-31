# tests/test_harmonizer.py

import os
import tempfile

import pytest

from src.harmonizer.main import PythonCodeHarmonizer

# A self-contained Python script to be used for testing.
# It contains one harmonious function and one disharmonious one.
TEST_CODE_CONTENT = """
def get_user_data():
    \"\"\"Fetches user information from the database.\"\"\"
    db.query("SELECT * FROM users")
    return True

def check_permissions():
    \"\"\"This function is supposed to check user rights.\"\"\"
    # This is the logical bug: the name implies a check (Wisdom/Justice),
    # but the action is a deletion (Power).
    db.delete_user(user_id=42)
    return False
"""


@pytest.fixture
def harmonizer():
    """Provides a standard instance of the Harmonizer."""
    return PythonCodeHarmonizer()


@pytest.fixture
def temp_python_file():
    """
    Creates a temporary Python file with the test code content.
    This ensures the test is self-contained and doesn't rely on external files.
    """
    # tempfile.NamedTemporaryFile creates a file and returns a file-like object.
    # We use 'delete=False' to be able to close it and still use its name.
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as fp:
        fp.write(TEST_CODE_CONTENT)
        filepath = fp.name

    # Yield the path to the test. The code inside the 'with' block runs before the test,
    # and the code after the 'yield' runs after the test.
    yield filepath

    # Teardown: Clean up the temporary file after the test is done.
    os.unlink(filepath)


def test_harmonizer_end_to_end_analysis(harmonizer, temp_python_file):
    """
    Performs an end-to-end integration test of the Harmonizer.
    It runs the analysis on the temporary file and checks the report.
    """
    # 1. Analyze the temporary file.
    report = harmonizer.analyze_file(temp_python_file)

    # 2. Verify the report contents.
    assert "get_user_data" in report
    assert "check_permissions" in report

    # 3. Check the harmony scores.
    # The 'get_user_data' function should be harmonious (low score).
    # Intent: get, information. Execution: query, information.
    assert report["get_user_data"] < harmonizer.disharmony_threshold

    # The 'check_permissions' function should be disharmonious (high score).
    # Intent: check, truth. Execution: delete, force.
    assert report["check_permissions"] > harmonizer.disharmony_threshold


def test_harmonizer_on_empty_file(harmonizer, temp_python_file):
    """Tests that the harmonizer handles an empty file gracefully."""
    # Overwrite the temp file to be empty
    with open(temp_python_file, "w") as f:
        f.write("")

    report = harmonizer.analyze_file(temp_python_file)
    assert report == {}


def test_harmonizer_on_file_with_only_comments(harmonizer, temp_python_file):
    """Tests that the harmonizer handles a file with only comments."""
    with open(temp_python_file, "w") as f:
        f.write("# This is a comment\\n# And another one")

    report = harmonizer.analyze_file(temp_python_file)
    assert report == {}


def test_harmonizer_on_syntax_error(harmonizer, temp_python_file):
    """Tests that the harmonizer catches SyntaxError and returns an empty report."""
    with open(temp_python_file, "w") as f:
        f.write("def invalid_syntax:")

    report = harmonizer.analyze_file(temp_python_file)
    assert report == {}
