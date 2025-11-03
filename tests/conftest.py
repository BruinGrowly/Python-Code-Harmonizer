# tests/conftest.py

import sys
import os

# Add the project root to the Python path.
# This ensures that the 'harmonizer' package is discoverable by pytest,
# regardless of how the project is installed or the current working directory.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
