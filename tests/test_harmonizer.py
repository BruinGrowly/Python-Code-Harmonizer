# tests/test_harmonizer.py

import pytest
from src.harmonizer.main import PythonCodeHarmonizer
import tempfile
import os

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
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as fp:
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
