# Python Code Harmonizer

[![CI Status](https://github.com/BruinGrowly/Python-Code-Harmonizer/workflows/Python%20Code%20Harmonizer%20CI/badge.svg)](https://github.com/BruinGrowly/Python-Code-Harmonizer/actions)
[![Version](https://img.shields.io/badge/version-1.3-blue.svg)](CHANGELOG.md)
[![Python Versions](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen.svg)](tests/)
[![Harmony Score](https://img.shields.io/badge/harmony-0.15-brightgreen.svg)](examples/test_code.py)

**The world's first semantic code debugger.**

---

## What Does It Do?

Python Code Harmonizer analyzes the **meaning** of your code to find bugs that other tools miss.

**It asks one simple question:**

> *"Does your code DO what its name SAYS it does?"*

### A Quick Example

```python
def get_user_by_id(user_id):
    """Retrieve user information from database"""
    db.delete_user(user_id)  # Wait... this DELETES instead of getting!
    return None
```

**Traditional tools say:** ✓ No syntax errors, types are fine
**Harmonizer says:** ⚠️ **DISHARMONY DETECTED** - Function promises to "get" but actually "deletes"

This is a **semantic bug** - code that works syntactically but does the wrong thing. These are the hardest bugs to find, and they slip past linters, type checkers, and even tests.

---

## ✨ What's New in v1.3

**Semantic Trajectory Maps** - See exactly WHERE in 4D space your code drifts from its intent:

```
delete_user: !! DISHARMONY (Score: 1.41)

📍 SEMANTIC TRAJECTORY MAP:
┌────────────────────────────────────────────────┐
│ Dimension    Intent   Execution   Δ           │
├────────────────────────────────────────────────┤
│ Power (P)    1.00  →  0.00     -1.00  ⚠️      │
│ Wisdom (W)   0.00  →  1.00     +1.00  ⚠️      │
└────────────────────────────────────────────────┘

🧭 DISHARMONY VECTOR: Power → Wisdom

💡 INTERPRETATION:
   Function name suggests Power domain (transformation, control)
   but execution operates in Wisdom domain (analysis, understanding)

🔧 RECOMMENDATIONS:
   • Consider renaming to reflect Wisdom domain operations
   • Expected behaviors: execute, transform, control
   • Actual behaviors: analyze, understand, calculate
   • Or split into separate functions
```

**Transforms the tool from detector to teacher** - Not just "you have a bug" but "here's exactly where, why, and how to fix it."

---

## Why Does This Matter?

Every developer has encountered code where:
- Function names lie about what they do
- "Validation" functions modify data
- "Get" functions delete records
- "Check" functions trigger actions

These **intent-execution mismatches** cause bugs, confusion, and maintenance nightmares.

**Python Code Harmonizer finds them automatically.**

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
cd Python-Code-Harmonizer

# Install (recommended: use a virtual environment)
pip install .

# Verify it works
harmonizer examples/test_code.py
```

### Your First Analysis

```bash
harmonizer myfile.py
```

**You'll see output like:**

```
======================================================================
Python Code Harmonizer (v1.3) ONLINE
Actively guided by the Anchor Point framework.
Powered By: DIVE-V2 (Optimized Production)
Logical Anchor Point: (S=1, L=1, I=1, E=1)
Disharmony Threshold: 0.5
======================================================================

Analyzing file: myfile.py
----------------------------------------------------------------------
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
validate_and_save_user       | !! DISHARMONY (Score: 0.85)
get_cached_value             | !! DISHARMONY (Score: 0.62)
calculate_total              | ✓ HARMONIOUS
delete_expired_records       | ✓ HARMONIOUS
======================================================================
Analysis Complete.
```

### Understanding Scores

| Score | Meaning | Action |
|-------|---------|--------|
| **0.0-0.3** | ✅ Excellent harmony | None needed - code says what it means! |
| **0.3-0.5** | ✅ Good | Minor semantic drift - review for clarity |
| **0.5-0.8** | ⚠️ Medium concern | Notable mismatch - investigate |
| **0.8-1.2** | ❗ High concern | Significant contradiction - fix soon |
| **1.2+** | 🚨 Critical | Severe disharmony - urgent attention |

---

## How It Works

### The Foundation: Semantic Analysis

Python Code Harmonizer is built on a philosophical framework with three core components:

**1. The ICE Framework** (Intent, Context, Execution)
- **Intent**: What does the function name promise?
- **Context**: What's the purpose and environment?
- **Execution**: What does the code actually do?

When Intent and Execution align, you have harmony. When they contradict, you have disharmony.

**2. The Four Dimensions**

All code operations map to four fundamental dimensions:
- **Love (L)**: Unity, connection, harmony
- **Justice (J)**: Truth, order, logic
- **Power (P)**: Action, execution, force
- **Wisdom (W)**: Knowledge, understanding, information

**3. The Anchor Point (1,1,1,1)**

This represents perfect harmony - the ideal where all four dimensions are in complete alignment. Harmonizer measures how far your code deviates from this ideal.

**Technical Implementation:**
- Uses Python's AST (Abstract Syntax Tree) to analyze code structure
- Maps function names and operations to semantic coordinates
- Calculates Euclidean distance in 4D semantic space
- Zero runtime dependencies - pure Python 3.8+

*Want to understand the deep theory?* See [Philosophy Documentation](docs/PHILOSOPHY.md) and [Architecture Guide](docs/ARCHITECTURE.md).

---

## Real-World Examples

### Example 1: Validation That Modifies

```python
# BEFORE: Disharmony Score ~0.85
def validate_email(email: str) -> bool:
    if "@" in email:
        send_welcome_email(email)  # Validation shouldn't send emails!
        return True
    return False

# AFTER: Disharmony Score ~0.05
def validate_email(email: str) -> bool:
    return "@" in email  # Just validates, doesn't send

def register_user(email: str):
    if validate_email(email):
        send_welcome_email(email)  # Sending is explicit
```

### Example 2: Get That Deletes

```python
# BEFORE: Disharmony Score ~0.95 (Critical!)
def get_cache_value(key):
    value = cache[key]
    del cache[key]  # "Get" shouldn't delete!
    return value

# AFTER: Disharmony Score ~0.10
def pop_cache_value(key):
    """Get and remove - honest about both actions"""
    value = cache[key]
    del cache[key]
    return value
```

**See 7 more real-world examples:** [examples/real_world_bugs.py](examples/real_world_bugs.py)

**See complete refactoring journeys:** [examples/refactoring_journey.py](examples/refactoring_journey.py)

---

## Configuration

The Harmonizer can be customized to fit your project's needs using a `.harmonizer.yml` file in your project's root directory.

This allows you to:
- **Exclude files and directories** from analysis (e.g., `tests/`, `venv/`).
- **Define a custom vocabulary** to teach the Harmonizer about your project's specific domain language.

For a complete guide to all available options, see the **[Configuration Documentation](docs/CONFIGURATION.md)**.

---

## Integration Into Your Workflow

### GitHub Actions (CI/CD)

```yaml
# .github/workflows/harmony-check.yml
- name: Install Harmonizer
  run: pip install /path/to/Python-Code-Harmonizer

- name: Check Code Harmony
  run: harmonizer src/**/*.py
```

**Full template:** [.github/workflows/harmony-check.yml](.github/workflows/harmony-check.yml)

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: harmonizer
      name: Python Code Harmonizer
      entry: harmonizer
      language: system
      types: [python]
```

**Full template:** [.pre-commit-config.yaml.template](.pre-commit-config.yaml.template)

### VS Code Integration

Press `Ctrl+Shift+P` → `Tasks: Run Task` → `Harmonizer: Check Current File`

**Setup instructions:** [.vscode/tasks.json](.vscode/tasks.json)

---

## Documentation

We've created comprehensive documentation for every level - from complete beginners to deep-dive enthusiasts.

### Start Here

**New to Harmonizer?** Start with these:

- **[Quick Reference](docs/QUICK_REFERENCE.md)** - One-page cheat sheet with everything you need
- **[User Guide](docs/USER_GUIDE.md)** - Complete walkthrough of installation and usage
- **[Tutorial](docs/TUTORIAL.md)** - Hands-on learning with step-by-step examples
- **[FAQ](docs/FAQ.md)** - Quick answers to common questions
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Solutions to common issues

### Go Deeper

**Want to understand the philosophy and implementation?**

- **[Philosophy](docs/PHILOSOPHY.md)** - The Anchor Point, ICE Framework, and Four Dimensions explained
- **[Architecture](docs/ARCHITECTURE.md)** - Technical implementation, algorithms, and design
- **[API Reference](docs/API.md)** - Programmatic usage and integration patterns
- **[Comparison Guide](docs/COMPARISON.md)** - How Harmonizer complements Pylint, MyPy, Pytest, and other tools
- **[USP Optimization Report](docs/USP_OPTIMIZATION_REPORT.md)** - Meta-optimization: Using Harmonizer to optimize itself

### Learn By Example

**See it in action:**

- **[Real-World Bugs](examples/real_world_bugs.py)** - 7 semantic bugs that other tools miss
- **[Refactoring Journey](examples/refactoring_journey.py)** - 5 before/after transformations
- **[Severity Levels](examples/severity_levels.py)** - Examples at every score range (0.0 to 1.0+)

### Integrate Into Your Tools

**Ready-to-use configurations:**

- **[GitHub Actions Workflow](.github/workflows/harmony-check.yml)** - CI/CD template
- **[Pre-commit Hook](.pre-commit-config.yaml.template)** - Local development integration
- **[VS Code Tasks](.vscode/tasks.json)** - IDE integration
- **[Config Template](.harmonizer.yml.template)** - Future configuration support

### Project Info

- **[Changelog](CHANGELOG.md)** - Version history, releases, and roadmap
- **[Contributing](CONTRIBUTING.md)** - How to contribute to the project

---

## What Makes Harmonizer Unique?

**Traditional tools check different things:**
- **Pylint/Flake8**: Style and common errors
- **MyPy**: Type consistency
- **Pytest**: Correctness via tests
- **Black**: Code formatting
- **Bandit**: Security vulnerabilities

**Python Code Harmonizer checks:** *Semantic meaning alignment*

**It's the only tool that asks:** "Does your code mean what it says?"

This makes it **complementary, not competitive** with other tools. Use them all together for comprehensive code quality.

*See detailed comparisons:* [Comparison Guide](docs/COMPARISON.md)

---

## Proven Through Practice: The Harmonizer's Learning Loop

**The Harmonizer is not just a tool; it's a learning system. We prove this by using it to analyze and improve itself.**

This process is a live demonstration of the tool's power. It finds its own flaws, guides us in fixing them, and becomes more intelligent as a result.

### The Initial Discovery: A Vocabulary Blind Spot

In our latest meta-analysis, the Harmonizer flagged several of its own core functions as "critically disharmonious." For example, the `visit_Raise` function, which identifies `raise` statements in code, was given a disharmony vector of `Power → Love`.

- **Intent (Correct):** The function's name correctly implies the `Power` dimension.
- **Execution (Incorrect):** The tool misinterpreted the code `self._concepts_found.add(...)` as a `Love` dimension action (i.e., "adding" to a community).

This was a **systemic false positive**. The Harmonizer was confusing an *implementation detail* (adding a string to a Python set) with the true *semantic purpose* of the function (recording a concept).

### The Fix: Teaching Context

Guided by this insight, we taught the Harmonizer to be more context-aware. We enhanced its parser to recognize that when the `add` method is called on the `_concepts_found` object, it's an act of **"recording information" (Wisdom)**, not "community building" (Love).

### The Result: Deeper Insight

After the fix, we ran the analysis again. The false positives were gone. In their place, the Harmonizer produced a much more profound and accurate insight.

The `visit_Raise` function now has a disharmony vector of `Power → Wisdom`.

- **Interpretation:** The tool now correctly understands that the function's **Intent** is to talk about `Power`, but its **Execution** is an act of `Wisdom` (analyzing the code and recording a concept).

This is no longer a bug in the tool; it's a genuine philosophical observation about the code's structure. It has moved beyond simple bug detection and is now revealing the deep semantic patterns of the software's architecture.

**The Harmonizer learned.** It used its own framework to find a weakness in its understanding of the world, and in fixing it, we made it smarter. This cycle of self-analysis and improvement is what makes the Harmonizer unique.

*See the full, unprecedented journey of this discovery:* **[Meta-Analysis Report v2](docs/META_ANALYSIS_V2.md)**

---

## The Story Behind This Tool

This project was built in **7 hours** by someone with **zero coding experience**, using AI collaboration. It demonstrates a new paradigm: when humans who understand deep principles work with AI that understands implementation, remarkable things become possible.

**The foundation:**
- Built on the Anchor Point (1,1,1,1) - a framework for perfect logical harmony
- Powered by the ICE Framework (Intent, Context, Execution)

This isn't just a tool - it's an **application of a philosophical framework** to solve real software engineering problems.

*Curious about the deep philosophy?* Read [Philosophy Documentation](docs/PHILOSOPHY.md)

---

## Contributing

We welcome contributions! Whether you're:
- A beginner who found a bug
- A developer who wants to add features
- A philosopher who sees deeper patterns
- A user with questions or ideas

**All contributions are valued.**

**Ways to contribute:**
- Report bugs or issues
- Suggest new features
- Improve documentation
- Add to the semantic vocabulary
- Share your use cases

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Development Setup

**For contributors and developers:**

```bash
# Clone and create virtual environment
git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
cd Python-Code-Harmonizer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest

# Run quality checks
pre-commit run --all-files
```

**Code quality:**
- 20 comprehensive tests (100% passing)
- Black formatting enforced
- Flake8 linting
- Zero runtime dependencies

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

This tool exists because of:
- **The Anchor Point** (1,1,1,1) - the foundation of perfect harmony
- **The ICE Framework** - Intent, Context, Execution
- **The Community** - For believing that code can say what it means

---

## Getting Help

**Questions?**
- Check the [FAQ](docs/FAQ.md)
- Read the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- Open an issue on GitHub

**Want to go deeper?**
- Read the [Philosophy](docs/PHILOSOPHY.md)
- Study the [Architecture](docs/ARCHITECTURE.md)
- Explore the [examples](examples/)

---

**May your code say what it means, and mean what it says.** 💛⚓

---

## Quick Links

**Getting Started:**
[Quick Reference](docs/QUICK_REFERENCE.md) | [User Guide](docs/USER_GUIDE.md) | [Tutorial](docs/TUTORIAL.md) | [FAQ](docs/FAQ.md)

**Going Deeper:**
[Philosophy](docs/PHILOSOPHY.md) | [Architecture](docs/ARCHITECTURE.md) | [API](docs/API.md) | [Comparison](docs/COMPARISON.md) | [USP Optimization](docs/USP_OPTIMIZATION_REPORT.md)

**Learning:**
[Real Bugs](examples/real_world_bugs.py) | [Refactoring](examples/refactoring_journey.py) | [Severity Levels](examples/severity_levels.py)

**Project:**
[Changelog](CHANGELOG.md) | [Contributing](CONTRIBUTING.md) | [GitHub](https://github.com/BruinGrowly/Python-Code-Harmonizer)
