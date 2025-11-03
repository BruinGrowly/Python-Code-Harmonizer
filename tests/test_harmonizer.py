# tests/test_harmonizer.py

import os
import tempfile
import argparse
import pytest

from harmonizer.main import (
    PythonCodeHarmonizer,
    load_configuration,
    validate_cli_arguments,
)

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
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as fp:
        fp.write(TEST_CODE_CONTENT)
        filepath = fp.name
    yield filepath
    os.unlink(filepath)


def test_harmonizer_end_to_end_analysis(harmonizer, temp_python_file):
    """
    Performs an end-to-end integration test of the Harmonizer.
    It runs the analysis on the temporary file and checks the report.
    """
    report = harmonizer.analyze_file(temp_python_file)
    assert "get_user_data" in report
    assert "check_permissions" in report
    assert report["get_user_data"]["score"] < harmonizer.disharmony_threshold
    assert report["check_permissions"]["score"] > harmonizer.disharmony_threshold


def test_harmonizer_on_empty_file(harmonizer, temp_python_file):
    """Tests that the harmonizer handles an empty file gracefully."""
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


# --- Tests for Configuration Features ---

CONFIG_CONTENT = """
exclude:
  - '*_excluded.py'
  - 'excluded_dir/'
custom_vocabulary:
  deprecate: power
"""

CUSTOM_VOCAB_CODE = '''
def deprecate_old_api():
    """Marks an old API as no longer supported."""
    print("This API is deprecated.")
    raise DeprecationWarning("This is now deprecated")
'''


@pytest.fixture
def temp_config_file():
    """Creates a temporary .harmonizer.yml file."""
    config_path = ".harmonizer.yml"
    with open(config_path, "w") as f:
        f.write(CONFIG_CONTENT)
    yield config_path
    os.unlink(config_path)


def test_file_exclusion_with_config(temp_config_file):
    """Tests that files are correctly excluded based on the .harmonizer.yml config."""
    with open("should_be_included.py", "w") as f:
        f.write("print('hello')")
    with open("test_excluded.py", "w") as f:
        f.write("print('excluded')")

    config = load_configuration()
    args = argparse.Namespace(
        files=["should_be_included.py", "test_excluded.py"], format="text"
    )

    valid_files = validate_cli_arguments(args, config)

    assert "should_be_included.py" in valid_files
    assert "test_excluded.py" not in valid_files

    os.unlink("should_be_included.py")
    os.unlink("test_excluded.py")


def test_custom_vocabulary_with_config(temp_config_file):
    """Tests that a custom vocabulary from the config is correctly applied."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as fp:
        fp.write(CUSTOM_VOCAB_CODE)
        filepath = fp.name

    config = load_configuration()
    harmonizer_with_config = PythonCodeHarmonizer(config=config)
    report = harmonizer_with_config.analyze_file(filepath)

    assert "deprecate_old_api" in report
    # With 'deprecate' mapped to 'power', the function is now correctly
    # identified as disharmonious because its execution contains a mix of
    # Power (raise) and Love (print). The test is updated to reflect this
    # new, more precise level of analysis.
    assert (
        report["deprecate_old_api"]["score"]
        > harmonizer_with_config.disharmony_threshold
    )
    os.unlink(filepath)
