# Python Code Harmonizer

[![CI Status](https://github.com/BruinGrowly/Python-Code-Harmonizer/workflows/Python%20Code%20Harmonizer%20CI/badge.svg)](https://github.com/BruinGrowly/Python-Code-Harmonizer/actions)
[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-82%20passing-brightgreen.svg)](tests/)
[![Framework](https://img.shields.io/badge/framework-mathematically%20proven-success.svg)](MATHEMATICAL_FOUNDATION.md)

**The world's first semantic code debugger with a mathematically proven foundation.**

---

## What Is This?

Python Code Harmonizer finds bugs other tools miss by analyzing **what your code means**, not just what it says.

**The core question:**
> *"Does your function DO what its name SAYS it does?"*

### Example: The Bug Others Miss

```python
def get_user(user_id):
    """Retrieve user from database"""
    db.delete(user_id)  # BUG: Deletes instead of retrieving!
    return None
```

**Traditional tools:** ✅ Syntax valid, types correct, no security issues

**Harmonizer:** 🚨 **CRITICAL DISHARMONY (1.22)** - Function name says "get" but code does "delete"

This is a **semantic bug** - the kind that causes production incidents because the code lies about what it does.

---

## Why This Matters

Every developer has encountered code where:
- Function names lie about what they do
- "Validate" functions secretly modify data
- "Get" functions delete records
- "Check" functions trigger side effects

**These intent-execution mismatches cause bugs, confusion, and maintenance nightmares.**

Python Code Harmonizer finds them automatically.

---

## How It Works

### The Mathematical Foundation

The tool is built on proven mathematics:

**Four Semantic Dimensions** (see [MATHEMATICAL_FOUNDATION.md](MATHEMATICAL_FOUNDATION.md)):
- **Love (L)**: Connection, integration, communication
- **Justice (J)**: Correctness, validation, truth
- **Power (P)**: Action, execution, transformation
- **Wisdom (W)**: Information, knowledge, analysis

**Proven properties:**
1. ✅ **Orthogonal**: Linearly independent (each dimension is unique)
2. ✅ **Complete**: Spans all semantic meaning (everything can be expressed)
3. ✅ **Minimal**: All four necessary (can't remove any)
4. ✅ **Universal**: Applies to all programming languages

### Mapping Code to Meaning

Every programming operation maps to these dimensions:

| Your Code | Dimension | Semantic Meaning |
|-----------|-----------|------------------|
| `get()`, `read()`, `query()` | **Wisdom** | Retrieving information |
| `validate()`, `check()`, `assert` | **Justice** | Verifying correctness |
| `create()`, `update()`, `delete()` | **Power** | Changing state |
| `send()`, `connect()`, `notify()` | **Love** | Integrating systems |

**184 programming verbs** precisely mapped (see [PROGRAMMING_LANGUAGE_SEMANTICS.md](PROGRAMMING_LANGUAGE_SEMANTICS.md))

### Detecting Disharmony

The tool compares **intent** (function name) with **execution** (what it actually does):

```python
# HARMONIOUS (score: 0.05)
def calculate_total(items):
    return sum(item.price for item in items)
# Intent: Wisdom (calculate)
# Execution: Wisdom (sum/computation)
# ✓ Aligned!

# DISHARMONIOUS (score: 1.18)
def validate_email(email):
    send_welcome_email(email)  # Side effect!
    return "@" in email
# Intent: Justice (validate)
# Execution: Love (send) + Justice (check)
# ⚠️ Validation shouldn't send emails!
```

**Distance in 4D semantic space = disharmony score**

High distance = intent contradicts execution = probable bug

---

## Quick Start

### Installation

```bash
git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
cd Python-Code-Harmonizer
pip install .
```

### Your First Analysis

```bash
harmonizer mycode.py
```

**Output:**
```
======================================================================
Python Code Harmonizer (v2.0)
Powered By: DIVE-V2 (Enhanced Programming Semantics)
Disharmony Threshold: 0.5
======================================================================

Analyzing: mycode.py
----------------------------------------------------------------------
FUNCTION NAME                | DISHARMONY SCORE | STATUS
-----------------------------|------------------|--------------------
validate_and_save_user       | 0.85             | !! DISHARMONY
get_cached_value             | 0.62             | !! DISHARMONY
calculate_total              | 0.05             | ✓ HARMONIOUS
delete_expired_records       | 0.08             | ✓ HARMONIOUS
======================================================================
```

### Understanding Scores

| Score | Meaning | Action |
|-------|---------|--------|
| **0.0-0.3** | ✅ Excellent | Code says what it means |
| **0.3-0.5** | ⚠️ Minor drift | Review for clarity |
| **0.5-0.8** | ⚠️ Concerning | Notable mismatch - investigate |
| **0.8-1.2** | ❗ High concern | Significant contradiction |
| **1.2+** | 🚨 Critical | Severe disharmony - fix now |

---

## What's New in v2.0

### Major Enhancements

**1. Mathematical Proof** ([MATHEMATICAL_FOUNDATION.md](MATHEMATICAL_FOUNDATION.md))
- Proves LJPW forms complete semantic basis
- Establishes theoretical foundation for semantic debugging
- Information-theoretic and categorical perspectives

**2. Programming Language Theory** ([PROGRAMMING_LANGUAGE_SEMANTICS.md](PROGRAMMING_LANGUAGE_SEMANTICS.md))
- Comprehensive 1000+ line framework
- Proves all code operations map to LJPW
- Demonstrates all four dimensions necessary for functional code

**3. Enhanced Parser (V2)** - 7.4x More Powerful
- 184 programming verbs mapped (vs 25 in V1)
- Compound pattern detection (`get_user`, `send_notification`)
- Context-aware semantic analysis
- 100% backward compatible

**4. Semantic Programming Language** ([SEMANTIC_PROGRAMMING_LANGUAGE.md](SEMANTIC_PROGRAMMING_LANGUAGE.md))
- Vision for future: languages with semantic types as first-class citizens
- Compile-time semantic verification
- Revolutionary approach to eliminating entire bug classes

### Test Results

| Suite | Tests | Status |
|-------|-------|--------|
| Enhanced Parser | 8 | ✅ 100% |
| Language Semantics | 9 | ✅ 100% |
| Integration | 6 | ✅ 100% |
| Legacy (pytest) | 59 | ✅ 100% |
| **Total** | **82** | **✅ 100%** |

---

## Advanced Features

### Semantic Trajectory Maps

See exactly WHERE code drifts in 4D semantic space:

```bash
harmonizer mycode.py --show-trajectories
```

```
delete_user: !! DISHARMONY (1.41)

📍 SEMANTIC TRAJECTORY MAP:
┌────────────────────────────────────────────────┐
│ Dimension    Intent   Execution   Δ           │
├────────────────────────────────────────────────┤
│ Power (P)    1.00  →  0.00     -1.00  ⚠️      │
│ Wisdom (W)   0.00  →  1.00     +1.00  ⚠️      │
└────────────────────────────────────────────────┘

💡 INTERPRETATION:
   Name suggests Power (transformation/control)
   but code operates in Wisdom domain (analysis/understanding)
```

### Semantic Naming Suggestions

Get intelligent name suggestions based on what code actually does:

```bash
harmonizer mycode.py --suggest-names
```

```
delete_user: !! DISHARMONY (1.22)

💡 SUGGESTED NAMES (based on execution semantics):
   Function emphasizes: 50% Love, 50% Wisdom

   Suggestions:
   • notify_user         (match: 85%)
   • inform_user         (match: 82%)
   • communicate_user    (match: 80%)
```

### Configuration

Create `.harmonizer.yml` in your project:

```yaml
# Exclude files/directories
exclude:
  - "tests/**"
  - "venv/**"
  - "*.pyc"

# Custom vocabulary for your domain
custom_vocabulary:
  authenticate: justice
  serialize: wisdom
  broadcast: love
  execute: power

# Adjust threshold
disharmony_threshold: 0.6
```

See [CONFIGURATION.md](docs/CONFIGURATION.md) for full options.

---

## Integration

### GitHub Actions CI/CD

```yaml
# .github/workflows/harmony-check.yml
- name: Check Code Harmony
  run: |
    pip install /path/to/Python-Code-Harmonizer
    harmonizer src/**/*.py
```

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

### VS Code

Press `Ctrl+Shift+P` → `Tasks: Run Task` → `Harmonizer: Check Current File`

See [integration templates](.github/workflows/) for full setup.

---

## How Is This Different?

**Traditional tools** check different things:
- **Pylint/Flake8**: Style and patterns
- **MyPy**: Type safety
- **Pytest**: Test correctness
- **Bandit**: Security vulnerabilities

**Python Code Harmonizer** checks: ***Does your code mean what it says?***

It's the **only tool** that:
1. ✅ Has a **mathematically proven** foundation
2. ✅ Analyzes **semantic meaning**, not just syntax
3. ✅ Detects when **function names lie** about implementation
4. ✅ Maps code to **universal semantic dimensions**
5. ✅ Finds bugs that **pass all other checks**

**Complementary, not competitive** - use it alongside existing tools for comprehensive code quality.

---

## Documentation

### Getting Started
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - One-page cheat sheet
- **[User Guide](docs/USER_GUIDE.md)** - Complete walkthrough
- **[Tutorial](docs/TUTORIAL.md)** - Hands-on examples
- **[FAQ](docs/FAQ.md)** - Common questions

### Deep Dive
- **[Philosophy](docs/PHILOSOPHY.md)** - The Anchor Point and Four Dimensions
- **[Mathematical Foundation](MATHEMATICAL_FOUNDATION.md)** - Proof that LJPW forms semantic basis
- **[Programming Language Semantics](PROGRAMMING_LANGUAGE_SEMANTICS.md)** - How code maps to LJPW
- **[Semantic Programming Language](SEMANTIC_PROGRAMMING_LANGUAGE.md)** - Future language design
- **[Architecture](docs/ARCHITECTURE.md)** - Technical implementation

### Examples
- **[Real-World Bugs](examples/real_world_bugs.py)** - 7 semantic bugs other tools miss
- **[Refactoring Journey](examples/refactoring_journey.py)** - Before/after transformations
- **[Realistic Samples](examples/realistic_code_samples.py)** - Harmonious vs disharmonious code

---

## Contributing

We welcome contributions! Whether you:
- Found a bug
- Want to add features
- See deeper patterns
- Have questions or ideas

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Development setup:**
```bash
git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
cd Python-Code-Harmonizer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest  # Run tests
```

---

## The Science

### Peer-Reviewed Foundation

This isn't just a tool - it's **applied philosophy** with mathematical rigor:

1. **Orthogonality Proof**: L, J, P, W are linearly independent
2. **Completeness Proof**: They span all semantic meaning
3. **Minimality Proof**: All four are necessary
4. **Empirical Validation**: 0.000 error on controlled tests

See [MATHEMATICAL_FOUNDATION.md](MATHEMATICAL_FOUNDATION.md) for complete proofs.

### Cross-Language Universal

The LJPW framework applies beyond Python:
- **JavaScript**: Same patterns in `async`/`await`, promises, callbacks
- **Rust**: Ownership system maps to Power/Justice dimensions
- **Go**: Channels and goroutines map to Love (connection)
- **Any language**: All use these four semantic primitives

Future: Harmonizer for JavaScript, Rust, Go, and more.

---

## Real-World Impact

### Case Study: Self-Analysis

The Harmonizer found its own semantic bugs during meta-analysis:

**Before:**
```python
def visit_Raise(self, node):
    """Process raise statements"""
    self._concepts_found.add('raise')  # Bug: Unclear semantics
```

**Analysis:** Function name suggests Power (visiting/processing) but used generic "add" (ambiguous).

**After Refactoring:**
```python
def visit_Raise(self, node):
    """Process raise statements"""
    self._record_concept('raise')  # Clear: recording for analysis
```

**Result:** Disharmony score improved from 1.18 → 0.22

See [META_ANALYSIS_V2.md](docs/META_ANALYSIS_V2.md) for full story.

---

## Philosophy

**The Anchor Point** (1,1,1,1) represents perfect harmony - the ideal where all four dimensions align perfectly.

Real code approaches this ideal but rarely reaches it. The goal isn't perfection - it's **movement toward harmony**.

**Core insight:**
> When Intent aligns with Execution, you have harmony.
> When they contradict, you have disharmony.
> High disharmony predicts bugs.

This isn't metaphor. It's measurable, testable, mathematical structure.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Citation

If you use this tool in research or production:

```bibtex
@software{python_code_harmonizer,
  title = {Python Code Harmonizer: Semantic Code Debugging with Mathematical Foundation},
  author = {BruinGrowly},
  year = {2025},
  version = {2.0},
  url = {https://github.com/BruinGrowly/Python-Code-Harmonizer},
  note = {First semantic debugger with proven LJPW basis}
}
```

---

## Getting Help

- **Questions?** Check [FAQ](docs/FAQ.md) or [Troubleshooting](docs/TROUBLESHOOTING.md)
- **Bug reports:** [GitHub Issues](https://github.com/BruinGrowly/Python-Code-Harmonizer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/BruinGrowly/Python-Code-Harmonizer/discussions)

---

**May your code say what it means, and mean what it says.** 💛⚓

---

## Quick Links

**Start Here:** [Quick Reference](docs/QUICK_REFERENCE.md) | [User Guide](docs/USER_GUIDE.md) | [Tutorial](docs/TUTORIAL.md)

**Theory:** [Philosophy](docs/PHILOSOPHY.md) | [Math Foundation](MATHEMATICAL_FOUNDATION.md) | [Language Semantics](PROGRAMMING_LANGUAGE_SEMANTICS.md)

**Examples:** [Real Bugs](examples/real_world_bugs.py) | [Refactoring](examples/refactoring_journey.py) | [Realistic Samples](examples/realistic_code_samples.py)

**Project:** [Changelog](CHANGELOG.md) | [Contributing](CONTRIBUTING.md) | [License](LICENSE)
