# Python Code Harmonizer - Tool Comparison Guide

**How Python Code Harmonizer fits in your development toolkit** 🔍

---

## TL;DR

**Python Code Harmonizer complements, doesn't replace, other tools.**

Each tool catches different categories of issues:
- **Syntax checkers** → Is it valid Python?
- **Linters** → Does it follow style rules?
- **Type checkers** → Are types consistent?
- **Test frameworks** → Does it work correctly?
- **Harmonizer** → Does it mean what it says?

---

## Detailed Comparisons

### vs. Pylint / Flake8 (Linters)

| Aspect | Pylint/Flake8 | Python Code Harmonizer |
|--------|---------------|------------------------|
| **Purpose** | Style, common errors, code smells | Semantic meaning alignment |
| **What it checks** | Variable naming, unused imports, complexity | Function name vs behavior |
| **Example catch** | Unused variable `x` | Function named `get_user` that deletes |
| **Bug type** | Style violations, simple errors | Logic contradictions, misleading names |
| **When to use** | Always (every commit) | Code review, refactoring |
| **Strictness** | Configurable rules | Semantic distance threshold |
| **False positives** | Many (style is subjective) | Few (contradictions are objective) |

**Example Pylint catches, Harmonizer doesn't:**
```python
def get_user(id):  # Pylint: argument name 'id' shadows builtin
    return db.query(id)
```

**Example Harmonizer catches, Pylint doesn't:**
```python
def get_user(user_id):  # Pylint: ✓ No issues
    db.delete(user_id)  # Harmonizer: ⚠️ "get" vs "delete" contradiction
```

**Use together:** Pylint enforces style, Harmonizer enforces semantic correctness.

---

### vs. MyPy (Type Checker)

| Aspect | MyPy | Python Code Harmonizer |
|--------|------|------------------------|
| **Purpose** | Type safety | Semantic harmony |
| **What it checks** | Type annotations match usage | Function names match behavior |
| **Example catch** | Passing `str` where `int` expected | Function promising read but writing |
| **Bug type** | Type mismatches | Intent-execution mismatches |
| **Requires** | Type hints | Descriptive function names |
| **When to use** | Always (if using type hints) | Code review, semantic analysis |

**Example MyPy catches, Harmonizer doesn't:**
```python
def get_user(user_id: int) -> str:
    return 42  # MyPy: ⚠️ Returns int, not str
```

**Example Harmonizer catches, MyPy doesn't:**
```python
def get_user(user_id: int) -> None:  # MyPy: ✓ Types correct
    db.delete(user_id)  # Harmonizer: ⚠️ "get" but "deletes"
    return None
```

**Use together:** MyPy ensures type safety, Harmonizer ensures semantic honesty.

---

### vs. Pytest / Unittest (Testing Frameworks)

| Aspect | Pytest | Python Code Harmonizer |
|--------|--------|------------------------|
| **Purpose** | Functional correctness | Semantic correctness |
| **What it checks** | Does code produce expected output? | Does code match its name? |
| **Example catch** | Function returns wrong value | Function name promises wrong thing |
| **Bug type** | Logic errors, wrong results | Misleading names, semantic confusion |
| **Requires** | Test cases | Descriptive names |
| **When to use** | Always (TDD/continuous testing) | Code review, naming validation |

**Example Pytest catches, Harmonizer doesn't:**
```python
def calculate_sum(a, b):  # Harmonizer: ✓ Name matches intent
    return a - b  # Pytest: ⚠️ Should be a + b
```

**Example Harmonizer catches, Pytest might not:**
```python
def validate_input(data):
    # Test might verify it "works"
    process_payment(data)  # Harmonizer: ⚠️ "validate" shouldn't "process payment"
    return True  # Test passes, but name is misleading
```

**Use together:** Pytest ensures behavior correctness, Harmonizer ensures naming correctness.

---

### vs. Black / Autopep8 (Formatters)

| Aspect | Black | Python Code Harmonizer |
|--------|-------|------------------------|
| **Purpose** | Code formatting | Semantic analysis |
| **What it checks** | Line length, spacing, quotes | Meaning alignment |
| **Example action** | Reformats code automatically | Reports disharmony (no auto-fix) |
| **Automated** | Yes (auto-fix) | No (analysis only) |
| **Opinionated** | Very (one style) | No (measures meaning) |

**Harmonizer doesn't format code** - it analyzes semantic meaning.

**Use together:** Black makes code look consistent, Harmonizer makes it mean what it says.

---

### vs. Bandit (Security Linter)

| Aspect | Bandit | Python Code Harmonizer |
|--------|--------|------------------------|
| **Purpose** | Security vulnerabilities | Semantic correctness |
| **What it checks** | SQL injection, hardcoded secrets | Name-behavior alignment |
| **Example catch** | Using `eval()` with user input | Function claiming read-only but modifying |
| **Focus** | Security risks | Semantic clarity |

**Example Bandit catches, Harmonizer doesn't:**
```python
def execute_query(sql):
    cursor.execute(sql)  # Bandit: ⚠️ SQL injection risk
```

**Example Harmonizer catches, Bandit doesn't:**
```python
def check_permissions(user):  # Bandit: ✓ No security issue
    user.role = "admin"  # Harmonizer: ⚠️ "check" but "modifies"
```

**Use together:** Bandit finds security holes, Harmonizer finds semantic holes.

---

### vs. Radon / McCabe (Complexity Analysis)

| Aspect | Radon/McCabe | Python Code Harmonizer |
|--------|--------------|------------------------|
| **Purpose** | Measure code complexity | Measure semantic alignment |
| **What it measures** | Cyclomatic complexity, LOC | Semantic distance |
| **Metric** | Number (complexity score) | Number (disharmony score) |
| **Good score** | Low complexity (< 10) | Low disharmony (< 0.5) |

**Example Radon catches, Harmonizer doesn't:**
```python
def complex_function():  # Radon: ⚠️ Complexity 15 (high)
    if a:
        if b:
            if c:
                # Many nested conditions
```

**Example Harmonizer catches, Radon doesn't:**
```python
def get_data():  # Radon: ✓ Complexity 1 (simple)
    delete_everything()  # Harmonizer: ⚠️ Semantic contradiction
```

**Use together:** Radon measures cognitive complexity, Harmonizer measures semantic clarity.

---

### vs. Sourcery / Rope (Refactoring Tools)

| Aspect | Sourcery | Python Code Harmonizer |
|--------|----------|------------------------|
| **Purpose** | Code improvement suggestions | Semantic analysis |
| **What it does** | Suggests refactorings | Identifies disharmony |
| **Automation** | Auto-refactoring | Analysis only |
| **Focus** | Code structure | Code meaning |

**Use together:** Sourcery suggests how to improve, Harmonizer identifies what needs improving.

---

## Comprehensive Comparison Matrix

| Tool | Syntax | Style | Types | Security | Complexity | **Semantics** |
|------|--------|-------|-------|----------|------------|---------------|
| Python compiler | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Pylint/Flake8 | ✅ | ✅ | ❌ | ⚠️ | ✅ | ❌ |
| MyPy | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Pytest | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Bandit | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Black | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Radon | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Harmonizer** | ✅ | ❌ | ❌ | ❌ | ❌ | **✅** |

**Python Code Harmonizer is the ONLY tool that checks semantic meaning.**

---

## Real-World Example: All Tools Together

```python
def validate_user(user: str) -> bool:  # Line 42
    """Validate user credentials"""
    db.delete_user(user)
    return True
```

**What each tool says:**

- **Python compiler**: ✅ Valid syntax
- **Pylint**: ✅ No style issues
- **MyPy**: ✅ Types are correct
- **Black**: ✅ Formatting is fine
- **Pytest**: ✅ Function returns bool as expected
- **Bandit**: ⚠️ Possible security issue (no input validation)
- **Harmonizer**: ⚠️ **High disharmony (0.95)** - "validate" but actually "deletes"!

**Only Harmonizer caught the semantic bug:**
- Name promises validation (checking)
- Code performs deletion (destructive action)
- This is a logic error that would confuse developers

---

## When to Use Python Code Harmonizer

### ✅ Use Harmonizer For:

1. **Code Review** - Catch misleading function names
2. **Refactoring** - Identify functions that grew beyond their name
3. **API Design** - Ensure public APIs are honest about behavior
4. **Legacy Code** - Find semantic drift in old codebases
5. **Team Standards** - Enforce semantic clarity
6. **Documentation** - Find functions whose names don't match docs

### ⚠️ Don't Use Harmonizer For:

1. **Replacing tests** - Harmonizer doesn't verify functionality
2. **Style enforcement** - Use linters for that
3. **Type checking** - Use MyPy for that
4. **Security** - Use Bandit for that
5. **Replacing human judgment** - Harmonizer highlights issues; you decide

---

## Recommended Tool Stack

### Minimal (Essential)
```bash
python -m py_compile  # Syntax
pytest                # Correctness
harmonizer           # Semantics
```

### Standard (Recommended)
```bash
black                # Formatting
flake8              # Linting
mypy                # Types
pytest              # Testing
harmonizer          # Semantics
```

### Complete (Professional)
```bash
black               # Formatting
isort               # Import sorting
flake8              # Linting
mypy                # Type checking
bandit              # Security
pytest              # Testing
pytest-cov          # Coverage
radon               # Complexity
harmonizer          # Semantics
```

---

## Integration Order

**Recommended workflow:**

1. **Write code**
2. **Black** - Format
3. **Flake8** - Lint
4. **MyPy** - Type check
5. **Harmonizer** - Semantic check ← *New step!*
6. **Pytest** - Test
7. **Commit**

---

## Unique Value Proposition

**What makes Harmonizer different:**

- ✅ **Only tool analyzing semantic meaning**
- ✅ **Finds bugs other tools miss** (misleading names)
- ✅ **Based on philosophical framework** (Anchor Point, ICE)
- ✅ **No machine learning** (deterministic, explainable)
- ✅ **Zero runtime dependencies** (pure Python)
- ✅ **Language-agnostic concepts** (ICE applies beyond Python)

---

## Summary

**Python Code Harmonizer is not a replacement - it's a complement.**

| Question | Tool |
|----------|------|
| Is it valid Python? | **Compiler** |
| Does it follow style? | **Pylint/Flake8** |
| Are types correct? | **MyPy** |
| Does it work? | **Pytest** |
| Is it secure? | **Bandit** |
| Is it complex? | **Radon** |
| **Does it mean what it says?** | **Harmonizer** |

**Use them all. Each catches different bugs.** 🛠️

---

*Python Code Harmonizer: Because code should say what it means and mean what it says.* 💛⚓
