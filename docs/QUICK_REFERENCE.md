# Python Code Harmonizer - Quick Reference

**One-page cheat sheet for fast reference** 📋

---

## Installation

```bash
# Clone and install
git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
cd Python-Code-Harmonizer
pip install .

# Verify
harmonizer --help
```

---

## Basic Usage

```bash
# Analyze single file
harmonizer myfile.py

# Analyze multiple files
harmonizer file1.py file2.py file3.py

# Analyze directory (with find)
find src/ -name "*.py" -exec harmonizer {} \;
```

---

## Score Interpretation

| Score | Status | Meaning | Action |
|-------|--------|---------|--------|
| **0.0-0.3** | ✅ Excellent | Perfect/near-perfect harmony | None needed |
| **0.3-0.5** | ✅ Good | Minor semantic drift | Review for clarity |
| **0.5-0.8** | ⚠️ Medium | Notable mismatch | Investigate |
| **0.8-1.2** | ❗ High | Significant contradiction | Definitely fix |
| **1.2+** | 🚨 Critical | Severe disharmony | Urgent attention |

---

## Common Semantic Patterns

### Wisdom (Information/Knowledge)
```python
get_*, fetch_*, retrieve_*, read_*, query_*
find_*, search_*, calculate_*, analyze_*
```
**Semantic dimension**: High Wisdom, Low Power

### Justice (Truth/Validation)
```python
validate_*, verify_*, check_*, is_*, has_*
assert_*, test_*, ensure_*
```
**Semantic dimension**: High Justice, Low Power

### Power (Action/Modification)
```python
create_*, delete_*, update_*, remove_*
execute_*, run_*, perform_*, build_*
set_*, modify_*, change_*
```
**Semantic dimension**: High Power, Variable Justice

### Love (Unity/Connection)
```python
merge_*, join_*, connect_*, combine_*
add_to_*, attach_*, link_*
```
**Semantic dimension**: High Love, Moderate Power

---

## Disharmony Examples

### ❌ Bad: Action Contradiction
```python
def get_user(id):
    db.delete(id)  # Says "get", does "delete"
    # Score: ~1.4 (CRITICAL)
```

### ✅ Good: Aligned Action
```python
def delete_user(id):
    db.delete(id)  # Name matches action
    # Score: ~0.1 (EXCELLENT)
```

### ❌ Bad: Purpose Mismatch
```python
def validate_email(email):
    send_email(email)  # Says "validate", does "send"
    # Score: ~0.9 (HIGH)
```

### ✅ Good: Clear Purpose
```python
def validate_email(email):
    return "@" in email  # Name matches action
    # Score: ~0.1 (EXCELLENT)
```

---

## Integration Quick Start

### GitHub Actions (CI/CD)
```yaml
# .github/workflows/harmony-check.yml
- name: Check Code Harmony
  run: |
    pip install .
    harmonizer src/**/*.py
```

### Pre-commit Hook
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: harmonizer
      name: Code Harmony Check
      entry: harmonizer
      language: system
      types: [python]
```

### VS Code Task
```json
// .vscode/tasks.json
{
  "label": "Check Harmony",
  "type": "shell",
  "command": "harmonizer ${file}"
}
```

---

## Programmatic Usage

```python
from src.harmonizer.main import PythonCodeHarmonizer

# Initialize
harmonizer = PythonCodeHarmonizer(disharmony_threshold=0.5)

# Analyze
report = harmonizer.analyze_file("mycode.py")

# Process results
for func_name, score in report.items():
    if score > 0.8:
        print(f"⚠️ {func_name}: {score:.2f}")
```

---

## The Four Dimensions

| Dimension | Symbol | Represents | Example Keywords |
|-----------|--------|------------|------------------|
| **Love** | L | Unity, compassion | merge, connect, care, help |
| **Justice** | J | Truth, order | validate, check, verify, assert |
| **Power** | P | Action, force | create, delete, execute, force |
| **Wisdom** | W | Knowledge, understanding | get, analyze, calculate, learn |

**Anchor Point (1,1,1,1)** = Perfect balance of all four

---

## ICE Framework

**Intent** → **Context** → **Execution**

- **Intent**: What function name promises (L+W)
- **Context**: Actual situation (J)
- **Execution**: What code does (P)

**Harmony** = Intent aligns with Execution

---

## Common Issues & Fixes

### Issue: Function not detected
**Cause**: Not a function definition, or syntax error
**Fix**: Ensure valid Python with `def` statements

### Issue: All scores are 0
**Cause**: No semantic keywords recognized
**Fix**: Use clearer, more descriptive function names

### Issue: Import error
**Cause**: Package not installed
**Fix**: `pip install .` in project directory

---

## Quick Tips

✅ **DO:**
- Use specific verbs (get, delete, create)
- Match names to actual behavior
- Run before committing code
- Review high scores in code review

❌ **DON'T:**
- Use vague verbs (process, handle, do)
- Ignore high scores without investigation
- Expect perfect 0.0 on everything
- Use as sole quality metric

---

## Resources

- **[User Guide](USER_GUIDE.md)** - Comprehensive usage
- **[Tutorial](TUTORIAL.md)** - Hands-on learning
- **[FAQ](FAQ.md)** - Common questions
- **[Philosophy](PHILOSOPHY.md)** - Deep theory
- **[Architecture](ARCHITECTURE.md)** - Implementation
- **[API](API.md)** - Programmatic use

---

## One-Liner Summary

> **"Does your code DO what its name SAYS?"**
> If yes → Harmonious. If no → Bug.

---

*Keep this reference handy for quick lookups!* 💛⚓
