# Python Code Harmonizer (v1.1)

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository contains the world's first **semantic code debugger**.

It doesn't just check your syntax; it analyzes the **meaning** of your code to find logical-semantic bugs.

This tool is a "white box" application built on the **Anchor Point (`1,1,1,1`)** and the **ICE Framework (`Intent`, `Context`, `Execution`)**.

---

## The Core Idea: Finding "Disharmony"

Traditional tools check if your syntax is *valid*, but not if your logic is *sound*. The Python Code Harmonizer is a "holistic" tool that asks:

> **"Does your code *do* what its name *says* it does?"**

It finds "bugs" where the `Intent` (the function's name) is in logical contradiction with the `Execution` (the code inside it).

*   **`Intent`:** `def get_user_by_id(...)`
*   **`Execution`:** `... db.delete_user(...)`
*   **Result:** `!! DISHARMONY DETECTED !!`

---

## How It Works (The "White Box" Logic)

This tool is an application of the "full-stack philosophy" defined in the **Divine Invitation Engine (DIVE-V2)**.

1.  **The "Ground Truth" (Axiom):** It uses the `divine_invitation_engine_V2.py` as its "compass." This engine's "true north" is the **Anchor Point (`1,1,1,1`)**, which represents "Perfect Logical Harmony".

2.  **The "Physics" (Logic):** It applies the **ICE Framework** (Intent, Context, Execution) to your code.

3.  **The "Translation" (Parser):** It uses the `ast_semantic_parser.py` (the "Rosetta Stone") to translate Python's logical `ast` (Abstract Syntax Tree) into the "meaning-keywords" the DIVE-V2 engine understands.

4.  **The "Result" (Analysis):** It calculates the "semantic distance" between the `Intent` and the `Execution`. A high score reveals a logical "bug."

---

## How to Use

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
    cd Python-Code-Harmonizer
    ```

2.  **Install the project:**
    *   This project is packaged and can be installed using `pip`. It is recommended to do this in a virtual environment.
    ```sh
    pip install .
    ```

### Running the Harmonizer

Once installed, the Harmonizer can be run from the command line using the `harmonizer` script. You can test it on the included example file:

```sh
harmonizer examples/test_code.py
```

**Expected "Harmony Report":**

```
======================================================================
Python Code Harmonizer (v1.1) ONLINE
Actively guided by the Anchor Point framework.
Powered By: DIVE-V2 (Optimized Production)
Logical Anchor Point: (S=1, L=1, I=1, E=1)
Disharmony Threshold: 0.5
======================================================================

Analyzing file: examples/test_code.py
----------------------------------------------------------------------
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
delete_user                  | !! DISHARMONY (Score: 1.41)
check_user_permissions       | !! DISHARMONY (Score: 0.62)
get_user_by_id               | ✓ HARMONIOUS
query                        | ✓ HARMONIOUS
======================================================================
Analysis Complete.
```

*(Note: The exact score may vary, but the "Disharmony" will be detected.)*

---

## Development & Contribution

This project is now equipped with a full suite of professional development tools to ensure code quality and stability.

### Setup for Development

If you wish to contribute, please install the project in "editable" mode along with the development dependencies:

```sh
# It is recommended to use a virtual environment
pip install -r requirements.txt
pip install -e .
```

### Running Tests and Quality Checks

*   **Run the full test suite:**
    ```sh
    pytest
    ```
*   **Run code quality checks:**
    *   This project uses `pre-commit` to automatically run `black`, `flake8`, and `isort`. To run the checks manually:
    ```sh
    pre-commit run --all-files
    ```

For more detailed information, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.
