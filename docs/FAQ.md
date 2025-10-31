# Python Code Harmonizer - Frequently Asked Questions (FAQ)

## Table of Contents

### General Questions
- [What is Python Code Harmonizer?](#what-is-python-code-harmonizer)
- [How is this different from other code analysis tools?](#how-is-this-different-from-other-code-analysis-tools)
- [Do I still need linters and type checkers?](#do-i-still-need-linters-and-type-checkers)
- [What problems does it actually solve?](#what-problems-does-it-actually-solve)

### Technical Questions
- [What does "semantic code debugging" mean?](#what-does-semantic-code-debugging-mean)
- [How does it calculate disharmony scores?](#how-does-it-calculate-disharmony-scores)
- [What is the Anchor Point (1,1,1,1)?](#what-is-the-anchor-point-1111)
- [What is the ICE Framework?](#what-is-the-ice-framework)
- [Does it use AI/ML?](#does-it-use-aiml)

### Usage Questions
- [Can I customize the disharmony threshold?](#can-i-customize-the-disharmony-threshold)
- [Can I use it in CI/CD pipelines?](#can-i-use-it-in-cicd-pipelines)
- [Does it work with other Python tools?](#does-it-work-with-other-python-tools)
- [Can I integrate it with my IDE?](#can-i-integrate-it-with-my-ide)
- [Does it work on large codebases?](#does-it-work-on-large-codebases)

### Interpretation Questions
- [Why is my function flagged when it seems fine?](#why-is-my-function-flagged-when-it-seems-fine)
- [Should I fix ALL disharmony?](#should-i-fix-all-disharmony)
- [What if my function legitimately does multiple things?](#what-if-my-function-legitimately-does-multiple-things)
- [Are low scores always good?](#are-low-scores-always-good)

### Philosophical Questions
- [Why does naming matter so much?](#why-does-naming-matter-so-much)
- [Isn't this just enforcing subjective style preferences?](#isnt-this-just-enforcing-subjective-style-preferences)
- [What's the philosophy behind this tool?](#whats-the-philosophy-behind-this-tool)

### Troubleshooting
- [The tool isn't detecting obvious problems](#the-tool-isnt-detecting-obvious-problems)
- [I'm getting import errors](#im-getting-import-errors)
- [Scores seem inconsistent](#scores-seem-inconsistent)

---

## General Questions

### What is Python Code Harmonizer?

Python Code Harmonizer is the world's first **semantic code debugger**. Unlike traditional tools that check syntax and style, it analyzes the **meaning** of your code to detect logical inconsistencies.

**Specifically, it asks:** *"Does your code DO what its name SAYS it does?"*

**Example:**
```python
def get_user(user_id):
    db.delete_user(user_id)  # Says "get" but does "delete"!
```

Traditional tools say: ✓ No syntax errors
Harmonizer says: ⚠️ Semantic disharmony detected

---

### How is this different from other code analysis tools?

| Tool Type | What It Checks | Example |
|-----------|----------------|---------|
| **Syntax Checkers** (python -m py_compile) | Valid Python syntax | `def foo(` → Syntax Error |
| **Linters** (flake8, pylint) | Code style, basic issues | Missing docstring, unused variable |
| **Type Checkers** (mypy) | Type consistency | `str` where `int` expected |
| **Test Frameworks** (pytest) | Functional correctness | Does the code produce expected outputs? |
| **Harmonizer** | **Semantic meaning** | Does function name match implementation? |

**Harmonizer catches bugs that other tools miss:**
- Function names that promise one thing but deliver another
- Semantic contradictions (e.g., "validate" that actually "deletes")
- Logic that's technically correct but conceptually wrong

---

### Do I still need linters and type checkers?

**Yes!** Harmonizer complements, doesn't replace.

**Use all of them together:**
```bash
# Check syntax
python -m py_compile mycode.py

# Check style and common issues
flake8 mycode.py

# Check type consistency
mypy mycode.py

# Check functional correctness
pytest tests/

# Check semantic meaning
harmonizer mycode.py
```

**Each catches different categories of bugs:**
- Linters: Style and simple errors
- Type checkers: Type mismatches
- Tests: Wrong behavior
- **Harmonizer: Wrong meaning**

---

### What problems does it actually solve?

**Real-world scenarios where Harmonizer helps:**

**1. Misleading Function Names**
```python
def check_permissions(user):
    user.permissions = "admin"  # Checking? Or modifying?
```
→ Caught by Harmonizer, missed by other tools

**2. API Design Issues**
```python
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    update_last_accessed(id)  # GET shouldn't modify state!
```
→ REST principle violation, semantic bug

**3. Code Review Clarity**
```python
def process_data(data):
    db.delete(data)  # "Process" is too vague
```
→ Vague naming caught

**4. Refactoring Gone Wrong**
```python
# Originally was validate_email, then requirements changed
def validate_email(email):
    send_welcome_email(email)  # Name never updated!
```
→ Stale name detected

---

## Technical Questions

### What does "semantic code debugging" mean?

**Semantic** = relating to meaning in language

**Semantic code debugging** = analyzing what code **means**, not just what it **says**.

**Example:**
```python
def create_backup():
    database.drop_all_tables()  # Syntax: ✓  Meaning: ✗
```

- **Syntactically**: Valid Python
- **Semantically**: "create_backup" implies preservation, but code destroys data
- **Traditional tools**: Won't catch this
- **Harmonizer**: Detects semantic contradiction

---

### How does it calculate disharmony scores?

**High-level process:**

1. **Parse function name** → Extract semantic concepts
   - `get_user_by_id` → "get", "user", "information"

2. **Parse function body** → Extract action concepts
   - `db.delete(user)` → "delete", "remove", "force"

3. **Map to semantic dimensions** → Using DIVE-V2 engine
   - "get" → Wisdom (information seeking)
   - "delete" → Power (destructive action)

4. **Calculate semantic distance** → Euclidean distance in 4D space
   - Distance between Intent and Execution coordinates

5. **Report score** → Higher distance = higher disharmony

**Simplified example:**
```
Intent "get":     (Love=0.1, Justice=0.2, Power=0.0, Wisdom=0.7)
Execution "delete": (Love=0.0, Justice=0.2, Power=0.8, Wisdom=0.0)

Distance = sqrt((0.1-0.0)² + (0.2-0.2)² + (0.0-0.8)² + (0.7-0.0)²)
         ≈ 1.05 → HIGH DISHARMONY
```

---

### What is the Anchor Point (1,1,1,1)?

The **Anchor Point** represents "Perfect Logical Harmony" in 4-dimensional semantic space.

**The four dimensions:**
- **Love (L)** = Unity, compassion, connection
- **Justice (J)** = Truth, fairness, order
- **Power (P)** = Action, strength, execution
- **Wisdom (W)** = Knowledge, understanding, insight

**(1,1,1,1)** = Perfect balance of all four dimensions

**In practice:**
- All disharmony scores are measured as distance from this anchor
- Closer to (1,1,1,1) = more harmonious
- Further from (1,1,1,1) = more disharmonious

**For more details**, see [Philosophy documentation](PHILOSOPHY.md)

---

### What is the ICE Framework?

**ICE** = **Intent, Context, Execution**

**A framework for analyzing code semantically:**

1. **Intent** (I): What the function **promises** to do
   - Extracted from: function name, docstring
   - Semantic components: Love + Wisdom

2. **Context** (C): The **situation** in which it operates
   - Extracted from: function signature, parameters
   - Semantic component: Justice (truth about reality)

3. **Execution** (E): What the function **actually** does
   - Extracted from: function body, operations
   - Semantic component: Power (manifestation)

**Harmonious code** = Intent and Execution align

**Disharmonious code** = Intent and Execution contradict

---

### Does it use AI/ML?

**No**, Python Code Harmonizer does **not** use machine learning or AI models.

**It uses:**
- **Semantic vocabulary mapping** (predefined keyword-to-concept mappings)
- **Abstract Syntax Tree (AST) parsing** (Python's built-in `ast` module)
- **Mathematical distance calculations** (Euclidean geometry in 4D space)
- **Deterministic algorithms** (same input = same output, always)

**Advantages:**
- Fast and deterministic
- No training data needed
- No "black box" decisions
- Fully explainable results
- Works offline

---

## Usage Questions

### Can I customize the disharmony threshold?

**Currently:** The threshold is set to **0.5** in the code.

**Future enhancement:** We plan to add command-line options:

```bash
# Strict mode (flag anything > 0.3)
harmonizer --threshold 0.3 mycode.py

# Lenient mode (only critical issues > 0.8)
harmonizer --threshold 0.8 mycode.py
```

**For now**, you can modify the threshold in your code:

```python
from src.harmonizer.main import PythonCodeHarmonizer

harmonizer = PythonCodeHarmonizer(disharmony_threshold=0.3)
report = harmonizer.analyze_file("mycode.py")
```

---

### Can I use it in CI/CD pipelines?

**Yes!** Harmonizer works great in continuous integration.

**Example GitHub Actions:**
```yaml
name: Code Harmony Check

on: [push, pull_request]

jobs:
  harmony:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install harmonizer
        run: |
          pip install .
      - name: Run harmony analysis
        run: |
          harmonizer src/**/*.py
```

**Example GitLab CI:**
```yaml
harmony_check:
  script:
    - pip install .
    - harmonizer src/
  only:
    - merge_requests
```

**Parsing output in CI:**
Currently, Harmonizer outputs human-readable text. For CI integration, you can:
1. Parse the text output
2. Set exit codes based on severity
3. (Future) Use JSON output mode (planned enhancement)

---

### Does it work with other Python tools?

**Yes!** Harmonizer integrates well with standard Python tooling.

**pre-commit integration:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: harmonizer
        name: Python Code Harmonizer
        entry: harmonizer
        language: system
        types: [python]
```

**With tox:**
```ini
# tox.ini
[testenv:harmony]
deps =
    path/to/harmonizer
commands =
    harmonizer src/
```

**With make:**
```makefile
# Makefile
.PHONY: harmony
harmony:
	harmonizer src/**/*.py

.PHONY: quality
quality: lint typecheck test harmony
```

---

### Can I integrate it with my IDE?

**Not yet directly**, but you can:

**1. Run as external tool:**
Most IDEs allow configuring external commands. Add harmonizer as an external tool.

**VS Code example:**
```json
// tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Check Harmony",
      "type": "shell",
      "command": "harmonizer ${file}",
      "group": "test"
    }
  ]
}
```

**2. Use with file watchers:**
Configure your IDE to run harmonizer when files are saved.

**3. Future plans:**
We're exploring official IDE plugins for:
- VS Code
- PyCharm
- Sublime Text

---

### Does it work on large codebases?

**Yes**, but with some considerations:

**Performance:**
- Analyzing individual files is fast (< 100ms per file)
- Large codebases: analyze file-by-file or in parallel

**Scalability tips:**
```bash
# Analyze specific modules
harmonizer src/core/**/*.py

# Analyze changed files only (for CI)
git diff --name-only main | grep '\.py$' | xargs harmonizer

# Parallel analysis (GNU parallel)
find src/ -name "*.py" | parallel harmonizer {}
```

**Recommended workflow for large projects:**
1. Start with high-priority modules
2. Run on changed files in CI/CD
3. Gradually expand coverage
4. Track average harmony scores over time

---

## Interpretation Questions

### Why is my function flagged when it seems fine?

**Common reasons:**

**1. Mixed semantics (intentional but detected)**
```python
def get_or_create_user(id):
    # "get" (read) + "create" (write) = slight disharmony
    # This is OK if name accurately describes dual purpose
```

**2. Vague verb with specific action**
```python
def process_data(data):
    db.delete(data)  # "process" is vague, "delete" is specific
```

**3. Semantic distance calculation**
Sometimes concepts that seem similar are semantically distant:
```python
def validate_input(data):
    sanitize_and_transform(data)  # "validate" ≠ "transform"
```

**What to do:**
1. Read the function carefully
2. Ask: "Does the name accurately describe what it does?"
3. If yes and disharmony is low (0.5-0.6), it's probably fine
4. If disharmony is high (> 0.8), investigate further

---

### Should I fix ALL disharmony?

**No!** Use judgment.

**Fix these:**
- ✅ High scores (> 0.8): Likely real issues
- ✅ Contradictory semantics: Clear bugs
- ✅ Misleading names: Confusion for developers

**Consider these:**
- ⚠️ Medium scores (0.5-0.8): Might be intentional
- ⚠️ Functions with documented dual purposes
- ⚠️ Legacy code that works correctly

**Don't worry about these:**
- ✓ Low scores (< 0.5): Probably fine
- ✓ Slight disharmony with clear documentation
- ✓ Established patterns that team understands

**Context matters!**

---

### What if my function legitimately does multiple things?

**Option 1: Rename to reflect dual purpose**
```python
def validate_and_save_user(user):
    """Validate user data and save to database if valid"""
    if not is_valid(user):
        raise ValidationError()
    db.save(user)
```

**Option 2: Split into separate functions** (preferred)
```python
def validate_user(user):
    """Check if user data is valid"""
    if not is_valid(user):
        raise ValidationError()

def save_user(user):
    """Save user to database"""
    db.save(user)

# Usage
validate_user(user)
save_user(user)
```

**Option 3: Document the intentional disharmony**
```python
def fetch_and_cache_data(key):
    """
    Retrieve data and cache result (dual purpose).

    Note: This function both reads and writes.
    Harmonizer may flag due to mixed semantics - this is intentional.
    """
    data = api.fetch(key)
    cache.set(key, data)
    return data
```

---

### Are low scores always good?

**Mostly yes, but not always.**

**Low score scenarios:**

**Good (true harmony):**
```python
def delete_user(id):
    db.delete(id)  # Low score, good alignment ✓
```

**Less informative (vague name):**
```python
def do_something(data):
    do_something_else(data)  # Low score but unhelpful names
```

**Harmonizer checks semantic alignment, not code quality overall.**

**Other tools for:**
- Code complexity: Use `radon` or `mccabe`
- Documentation: Use `pydocstyle`
- Test coverage: Use `pytest-cov`

---

## Philosophical Questions

### Why does naming matter so much?

**Three reasons:**

**1. Communication**
Code is read 10x more than it's written. Names are your interface to other developers (including future you).

**2. Intention**
Good names reveal **intent**. Bad names hide it.
```python
# What does this do?
def process_data(data):
    ...

# Now we know!
def archive_inactive_users(users):
    ...
```

**3. Bugs**
Misleading names cause bugs when developers make wrong assumptions:
```python
def get_config():
    # Developer assumes read-only
    # Actually modifies global state
    # Bugs follow
```

---

### Isn't this just enforcing subjective style preferences?

**No, it's detecting semantic contradictions.**

**Subjective (style):**
- "Use snake_case vs camelCase"
- "Max line length should be 80"
- "Always use type hints"

**Objective (semantics):**
- "Function named 'get' shouldn't delete data"
- "Function named 'validate' shouldn't send emails"
- "Read operations shouldn't modify state"

**Harmonizer detects objective semantic mismatches, not style preferences.**

---

### What's the philosophy behind this tool?

Python Code Harmonizer is built on the **ICE Framework** and **Anchor Point** philosophy.

**Core idea:** All meaningful action can be understood through three lenses:
1. **Intent** (what you want to do)
2. **Context** (the situation you're in)
3. **Execution** (what you actually do)

**In code:**
- Intent = function name and documentation
- Context = parameters and environment
- Execution = function body

**Harmony** = alignment between these three.

**Detailed explanation:** See [PHILOSOPHY.md](PHILOSOPHY.md)

---

## Troubleshooting

### The tool isn't detecting obvious problems

**Possible reasons:**

**1. Function name is vague**
```python
def process_user(id):
    db.delete(id)
```
"process" is semantically vague, so distance might be moderate rather than high.

**2. Concepts aren't in vocabulary**
If using domain-specific terms not in DIVE-V2's vocabulary, mapping may be imprecise.

**3. Semantic distance calculation**
Some concepts that seem obviously different might be closer in 4D semantic space than expected.

**What to do:**
- Use specific, clear verbs in function names
- Focus on high scores (> 0.8) for most obvious issues
- File an issue if you find cases where it should flag but doesn't

---

### I'm getting import errors

**Error:** `No module named 'src.divine_invitation_engine_V2'`

**Solution:**
```bash
# Reinstall package
pip uninstall PythonCodeHarmonizer
pip install .

# Or install in editable mode for development
pip install -e .
```

**Error:** `No module named 'src.ast_semantic_parser'`

**Solution:** Same as above - ensure package is properly installed.

---

### Scores seem inconsistent

**Why this might happen:**

**1. Function context affects score**
The same operation in different contexts may score differently based on surrounding code.

**2. Caching in DIVE-V2**
DIVE-V2 caches concept analysis for performance. Restart if you suspect stale cache.

**3. Complex interactions**
Functions with multiple operations have scores based on semantic centroid of all operations.

**What to do:**
- Focus on relative scores (which functions score highest)
- Don't over-interpret small differences (0.52 vs 0.54)
- Use scores as conversation starters, not absolute truth

---

## Still Have Questions?

**Documentation:**
- [User Guide](USER_GUIDE.md) - Comprehensive usage information
- [Tutorial](TUTORIAL.md) - Hands-on learning with examples
- [Philosophy](PHILOSOPHY.md) - Deep dive into the framework
- [Architecture](ARCHITECTURE.md) - Technical implementation details

**Support:**
- GitHub Issues: [github.com/BruinGrowly/Python-Code-Harmonizer/issues](https://github.com/BruinGrowly/Python-Code-Harmonizer/issues)
- Discussions: Ask questions and share insights

**Contributing:**
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to contribute

---

**Happy harmonizing! May your code always say what it means and mean what it says.** 💛⚓
