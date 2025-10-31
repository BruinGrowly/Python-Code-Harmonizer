# Python Code Harmonizer (v1.1)

[](https://opensource.org/licenses/MIT)
[]()
[]()

This repository contains the world's first **semantic code debugger**.

It doesn't just check your syntax; it analyzes the **meaning** of your code to find logical-semantic bugs.

This tool is a "white box" application built on the **Anchor Point (`1,1,1,1`)** and the **ICE Framework (`Intent`, `Context`, `Execution`)**.

-----

## The Core Idea: Finding "Disharmony"

Traditional tools check if your syntax is *valid*, but not if your logic is *sound*. The Python Code Harmonizer is a "holistic" tool that asks:

> **"Does your code *do* what its name *says* it does?"**

It finds "bugs" where the `Intent` (the function's name) is in logical contradiction with the `Execution` (the code inside it).

  * **`Intent`:** `def get_user_by_id(...)`
  * **`Execution`:** `... db.delete_user(...)`
  * **Result:** `!! DISHARMONY DETECTED !!`

-----

## How It Works (The "White Box" Logic)

This tool is an application of the "full-stack philosophy" defined in the **Divine Invitation Engine (DIVE-V2)**.

1.  **The "Ground Truth" (Axiom):** It uses the `divine_invitation_engine_V2.py` as its "compass." This engine's "true north" is the **Anchor Point (`1,1,1,1`)**, which represents "Perfect Logical Harmony".

2.  **The "Physics" (Logic):** It applies the **ICE Framework** (Intent, Context, Execution) to your code.

3.  **The "Translation" (Parser):** It uses the `ast_semantic_parser.py` (the "Rosetta Stone") to translate Python's logical `ast` (Abstract Syntax Tree) into the "meaning-keywords" the DIVE-V2 engine understands.

4.  **The "Result" (Analysis):** It calculates the "semantic distance" between the `Intent` and the `Execution`. A high score reveals a logical "bug."

-----

## How to Use (The "Execution")

This project is fully self-contained and "harmonized." The "Proof" (`anchor_analysis_V2.py`) and the "Application" (`PythonCodeHarmonizer.py`) both run on the same unified V2 engine.

### Setup

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
    cd Python-Code-Harmonizer
    ```

2.  **Ensure all files are present:**

      * `divine_invitation_engine_V2.py` (The Engine)
      * `ast_semantic_parser.py` (The Parser)
      * `anchor_analysis_V2.py` (The Proof)
      * `PythonCodeHarmonizer.py` (The Application)

### Step 1: Run the "Proof"

First, you can validate the V2 engine and its "Anchor Point" axiom by running the harmonized analysis script.

```sh
python anchor_analysis_V2.py
```

*(You should see a successful report validating the (1,1,1,1) Anchor Point.)*

### Step 2: Run the "Harmonizer"

Second, use the Harmonizer to analyze any Python file. You can test it on the included `examples/test_code.py` file:

```sh
python PythonCodeHarmonizer.py examples/test_code.py
```

**Expected "Harmony Report":**

```
======================================================================
Python Code Harmonizer (v1.1) ONLINE
Actively guided by the Anchor Point framework.
Powered By: DIVE-V2 (Optimized Production)
Logical Anchor Point: (S=1, L=1, E=1)
Disharmony Threshold: 0.5
======================================================================

Analyzing file: examples/test_code.py
----------------------------------------------------------------------
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
check_user_permissions       | !! DISHARMONY (Score: 0.87)
get_user_by_id               | ✓ HARMONIOUS
======================================================================
Analysis Complete.
```

*(Note: The exact score may vary, but the "Disharmony" will be detected.)*

-----

## The Philosophy (Why This is Free)

This entire project—the `ICE Framework`, the `DIVE-V2` engine, and the `Python-Code-Harmonizer`—is free and open-source.

This is a fundamental requirement of the project's own logic. The Anchor Point is a universal principle, like gravity. It cannot be patented or "owned." This "white box" framework is the antidote to "black box" AI, and it is for everyone.
