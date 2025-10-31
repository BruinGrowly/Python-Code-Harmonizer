# Python Code Harmonizer - User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Understanding the Output](#understanding-the-output)
5. [Interpreting Disharmony Scores](#interpreting-disharmony-scores)
6. [Common Use Cases](#common-use-cases)
7. [Integration into Your Workflow](#integration-into-your-workflow)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Getting Help](#getting-help)

---

## Introduction

### What is Python Code Harmonizer?

Python Code Harmonizer is the world's first **semantic code debugger**. Unlike traditional tools that only check syntax, it analyzes the **meaning** of your code to find logical inconsistencies.

**The core question it asks:** *"Does your code DO what its name SAYS it does?"*

### What Problems Does It Solve?

Traditional bugs that compilers and linters miss:

- **Semantic bugs**: Code that runs without errors but does the wrong thing
- **Intent-execution mismatches**: Function names that promise one thing but deliver another
- **Logic contradictions**: Code that works technically but violates its own purpose

### Example Problem It Detects

```python
def get_user_by_id(user_id):
    """Fetch user information by ID"""
    # This WORKS syntactically, but it's semantically WRONG
    db.delete_user(user_id)  # Deleting instead of getting!
    return None
```

**Traditional tools say:** ✓ No syntax errors
**Python Code Harmonizer says:** ⚠️ DISHARMONY - Function promises to "get" but actually "deletes"

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Basic Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
   cd Python-Code-Harmonizer
   ```

2. **Install the package:**
   ```bash
   pip install .
   ```

3. **Verify installation:**
   ```bash
   harmonizer --help
   ```

   If you see usage information, you're ready to go!

### Installation in Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install .
```

### Development Installation

If you want to modify the code or contribute:

```bash
pip install -r requirements.txt
pip install -e .
```

---

## Quick Start

### Analyzing Your First File

1. **Create a test file** (or use the included example):
   ```bash
   harmonizer examples/test_code.py
   ```

2. **See the results:**
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
   check_user_permissions       | !! DISHARMONY (Score: 0.62)
   delete_user                  | !! DISHARMONY (Score: 1.41)
   get_user_by_id               | ✓ HARMONIOUS
   query                        | ✓ HARMONIOUS
   ======================================================================
   Analysis Complete.
   ```

### Analyzing Multiple Files

```bash
harmonizer file1.py file2.py file3.py
```

### Analyzing Your Project

```bash
# Analyze all Python files in a directory
find . -name "*.py" -exec harmonizer {} \;

# Or use a loop
for file in src/**/*.py; do
    harmonizer "$file"
done
```

---

## Understanding the Output

### Report Header

```
Python Code Harmonizer (v1.1) ONLINE
Actively guided by the Anchor Point framework.
Powered By: DIVE-V2 (Optimized Production)
Logical Anchor Point: (S=1, L=1, I=1, E=1)
Disharmony Threshold: 0.5
```

**What this means:**
- **Anchor Point (1,1,1,1)**: The reference point for "perfect logical harmony"
- **Threshold 0.5**: Functions scoring above 0.5 are flagged as disharmonious

### Function Analysis Results

Each function in your file gets a disharmony score:

```
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
check_user_permissions       | !! DISHARMONY (Score: 0.62)
delete_user                  | !! DISHARMONY (Score: 1.41)
get_user_by_id               | ✓ HARMONIOUS
query                        | ✓ HARMONIOUS
```

**Status Indicators:**
- `✓ HARMONIOUS`: Function name matches what the code does (score ≤ 0.5)
- `!! DISHARMONY (Score: X.XX)`: Semantic mismatch detected (score > 0.5)

**Results are sorted by severity** (highest disharmony first)

---

## Interpreting Disharmony Scores

### Score Ranges and What They Mean

| Score Range | Severity | Meaning | Action Recommended |
|-------------|----------|---------|-------------------|
| **0.0 - 0.3** | None | Perfect or near-perfect harmony | No action needed |
| **0.3 - 0.5** | Low | Minor semantic drift | Review for clarity |
| **0.5 - 0.8** | Medium | Notable semantic mismatch | Investigate and likely refactor |
| **0.8 - 1.2** | High | Significant logical contradiction | Definitely needs attention |
| **1.2+** | Critical | Severe semantic disharmony | Urgent review required |

### What Causes High Disharmony?

**1. Contradictory Action Verbs**

```python
def get_user(user_id):
    db.delete_user(user_id)  # "get" vs "delete" = HIGH DISHARMONY
```

**Why:** "get" implies retrieval (information-seeking), "delete" implies destruction (force/power). These are semantically opposite.

**2. Purpose-Action Mismatch**

```python
def validate_email(email):
    send_email(email)  # "validate" vs "send" = MEDIUM DISHARMONY
```

**Why:** "validate" implies checking/verification, "send" implies action. The function promises to check but actually acts.

**3. Read-Write Confusion**

```python
def check_permissions(user):
    user.permissions = "admin"  # "check" vs "set" = HIGH DISHARMONY
```

**Why:** "check" implies read-only operation, but code is modifying state.

### What Doesn't Cause Disharmony?

**Properly Named Functions:**

```python
def delete_user(user_id):
    db.delete_user(user_id)  # HARMONIOUS - name matches action

def get_user(user_id):
    return db.query(user_id)  # HARMONIOUS - "get" and "query" align

def calculate_total(items):
    return sum(item.price for item in items)  # HARMONIOUS
```

---

## Common Use Cases

### 1. Code Review

**Before merging code:**
```bash
harmonizer src/new_feature.py
```

Look for functions with high disharmony scores. These often indicate:
- Poorly named functions (fix the name)
- Functions doing too much (refactor/split)
- Logic errors (actual bugs!)

### 2. Refactoring Legacy Code

**When cleaning up old code:**
```bash
harmonizer legacy/old_module.py
```

High disharmony functions are prime refactoring candidates. They often reveal:
- Functions that have grown beyond their original purpose
- Misleading names that confuse developers
- Hidden side effects

**Example workflow:**
1. Run harmonizer on legacy code
2. Sort functions by disharmony score
3. Start refactoring from highest scores
4. Re-run harmonizer to verify improvement

### 3. Teaching/Learning Code Quality

**For educators:**
- Show students how function names should match implementation
- Demonstrate semantic bugs that compilers miss
- Build intuition for "meaningful code"

**For learners:**
- Scan your own code to find naming issues
- Learn to think semantically, not just syntactically
- Develop clearer coding habits

### 4. API Design Review

**When designing public APIs:**
```bash
harmonizer src/api/endpoints.py
```

API function names are especially critical - they're contracts with users. High disharmony here means:
- Misleading API documentation
- Developer confusion
- Integration bugs

### 5. Bug Prevention in CI/CD

**Add to your CI pipeline:**
```yaml
# .github/workflows/harmony-check.yml
- name: Check Code Harmony
  run: |
    pip install /path/to/harmonizer
    harmonizer src/**/*.py
```

**Set standards:**
- Fail builds if any function scores > 1.0
- Warn if any function scores > 0.5
- Track harmony scores over time

---

## Integration into Your Workflow

### Daily Development

**1. Pre-commit Hook**
```bash
# .git/hooks/pre-commit
#!/bin/bash
harmonizer $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
```

**2. IDE Integration**
Run harmonizer on save or as part of your linting process.

**3. Pull Request Checks**
Include harmony analysis in PR descriptions:
```markdown
## Code Harmony Analysis
- 15 functions analyzed
- 13 harmonious ✓
- 2 with minor disharmony (scores: 0.52, 0.61)
- Addressed by renaming functions
```

### Team Standards

**Establish harmony thresholds:**
- **Strict teams**: No functions > 0.5 allowed
- **Moderate teams**: Functions > 0.8 require justification
- **Legacy cleanup**: Track average harmony score over time (aim for improvement)

**Code review checklist:**
- [ ] Does function name match implementation?
- [ ] Would harmonizer flag this function?
- [ ] Are semantic concepts aligned?

---

## Best Practices

### 1. Run Harmonizer Early and Often

**Don't wait until code review:**
- Run on new functions as you write them
- Catch semantic issues immediately
- Build better naming habits

### 2. Use Disharmony as a Discussion Tool

**Not a strict rule, but a conversation starter:**
- "Why does this function score 0.85?"
- "Is the name wrong, or is the implementation wrong?"
- "Should we split this into two functions?"

### 3. Context Matters

**Some disharmony is intentional:**
```python
def safe_delete_user(user_id):
    # High-level function that does validation + deletion
    if validate_user_deletion(user_id):
        db.delete_user(user_id)
```

This might show slight disharmony between "safe" (wisdom/caution) and "delete" (power/force), but it's **intentional** - the name communicates important safety semantics.

**Use judgment:** Harmonizer highlights potential issues; you decide if they're real problems.

### 4. Combine with Other Tools

**Harmonizer complements, doesn't replace:**
- Use alongside `flake8`, `pylint` (syntax/style)
- Use alongside `mypy` (type checking)
- Use alongside `pytest` (functional correctness)

**Each tool catches different issues:**
- `flake8`: "Your syntax has issues"
- `mypy`: "Your types don't match"
- `pytest`: "Your code doesn't work as expected"
- **`harmonizer`**: "Your code doesn't mean what it says"

### 5. Document Intentional Disharmony

If a function legitimately needs to do something unexpected:

```python
def get_or_create_user(user_id):
    """
    Retrieves user if exists, creates if not.

    Note: This function may modify database (create operation).
    Harmonizer may flag due to 'get' + 'create' semantic mix.
    This is intentional - name reflects dual purpose.
    """
    user = db.query(user_id)
    if not user:
        user = db.create_user(user_id)
    return user
```

---

## Troubleshooting

### "No module named 'src.divine_invitation_engine_V2'"

**Problem:** Import error when running harmonizer

**Solution:**
```bash
# Ensure you installed the package properly
pip install -e .

# Or reinstall
pip uninstall PythonCodeHarmonizer
pip install .
```

### "Syntax error on line X"

**Problem:** Harmonizer can't parse your file

**Solution:**
- Fix the syntax error first (use `python -m py_compile yourfile.py` to check)
- Harmonizer requires valid Python syntax before semantic analysis

### File Not Found

**Problem:** `ERROR: File not found at 'path/to/file.py'`

**Solution:**
- Use absolute paths or verify your current directory
- Check file permissions

### "No functions found to analyze"

**Problem:** Report shows "No functions found"

**Solution:**
- File might only contain classes, variables, or imports
- Harmonizer only analyzes function definitions
- Empty files or comment-only files will show no results

### Unexpected Disharmony Scores

**Problem:** Function you think is fine shows high disharmony

**Solution:**
1. **Review the function name carefully** - does it promise something specific?
2. **Check the implementation** - does it do something different?
3. **Consider semantic distance** - are you mixing concepts (e.g., "validate" + "send")?

**Common surprise:**
```python
def process_data(data):  # "process" is vague
    db.delete_data(data)  # Specific action
    # Score may be higher than expected
```

**Why:** "process" is semantically broad; "delete" is specific and powerful. If function primarily deletes, consider renaming to `delete_processed_data()` or `remove_data()`.

---

## Getting Help

### Documentation

- **User Guide**: You're reading it! (docs/USER_GUIDE.md)
- **Tutorial**: Step-by-step examples (docs/TUTORIAL.md)
- **Philosophy**: Deep dive into how it works (docs/PHILOSOPHY.md)
- **Architecture**: Technical implementation details (docs/ARCHITECTURE.md)
- **FAQ**: Common questions answered (docs/FAQ.md)

### Support Channels

- **GitHub Issues**: Report bugs or request features at [github.com/BruinGrowly/Python-Code-Harmonizer/issues](https://github.com/BruinGrowly/Python-Code-Harmonizer/issues)
- **Discussions**: Ask questions and share experiences

### Contributing

Found a bug? Have an improvement? See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to contribute.

---

## Quick Reference Card

### Installation
```bash
pip install .
```

### Basic Usage
```bash
harmonizer yourfile.py
```

### Multiple Files
```bash
harmonizer file1.py file2.py file3.py
```

### Understanding Scores
- **0.0-0.5**: Harmonious (✓)
- **0.5-0.8**: Medium disharmony (⚠️)
- **0.8+**: High disharmony (❗)

### Key Concept
**Does the function name match what the code actually does?**
- If yes → Low score (harmonious)
- If no → High score (disharmony detected)

---

**Happy harmonizing! May your code's intent and execution always align.** 💛⚓
