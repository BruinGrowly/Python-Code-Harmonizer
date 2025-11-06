# User Experience Quick Reference Guide

## Understanding Your Results

### Status Symbols

| Symbol | Meaning | Score Range | What It Means |
|--------|---------|-------------|---------------|
| ✨ | **Excellent!** | 0.0 - 0.3 | Perfect harmony - function does exactly what its name says |
| ✓ | **Harmonious** | 0.3 - 0.5 | Good alignment - minor stylistic preferences |
| ⚠️ | **Worth reviewing** | 0.5 - 0.8 | Notable mismatch - consider reviewing for clarity |
| 🚨 | **Needs attention** | 0.8+ | Significant contradiction - likely indicates a bug |

### What The Scores Mean

Think of the score as "semantic distance" in 4D space:

```
0.00 = Perfect alignment
0.25 = Essentially harmonious
0.50 = Threshold (our default cutoff)
0.75 = Concerning mismatch
1.00 = Significant contradiction
1.50+ = Critical semantic disharmony
```

**Lower is better!**

---

## Reading the Output

### Startup

```
======================================================================
Python Code Harmonizer ⚓ - Finding harmony in your code
Version 1.5 • DIVE-V2 (Optimized Production)

🎯 Checking if your functions DO what their names SAY
   Threshold: 0.5 (scores below = harmonious)
======================================================================
```

- ⚓ **Anchor emoji**: Represents the Anchor Point - perfect harmony
- 🎯 **What we check**: Plain language explanation
- **Threshold**: Scores below this are considered harmonious

### Analysis

```
Analyzing file: mycode.py
----------------------------------------------------------------------
✨ Analyzed 4 function(s)
```

- Shows which file is being analyzed
- ✨ Celebration when analysis completes

### Results Table

```
FUNCTION NAME                | HARMONY SCORE
-----------------------------|--------------------------------
get_user                     | ✨ Excellent! (0.08)
calculate_total              | ✓ Harmonious (0.42)
validate_and_save            | ⚠️  Worth reviewing (0.65)
delete_user                  | 🚨 Needs attention (1.22)
```

- Functions sorted by score (worst first, so you see problems immediately)
- Visual symbols for quick scanning
- Actual scores shown for transparency

### Detailed Analysis (for problems)

When a function needs attention, you'll see:

```
📍 SEMANTIC TRAJECTORY MAP:
┌──────────────────────────────────────────────────────────────┐
│ Dimension    Intent   Execution   Δ        Interpretation   │
├──────────────────────────────────────────────────────────────┤
│ Love (L)     0.00  →  1.00     +1.00    ⚠️  Major shift    │
│ Justice (J)  0.00  →  0.00     +0.00    ✓ Aligned          │
│ Power (P)    1.00  →  0.00     -1.00    ⚠️  Major shift    │
│ Wisdom (W)   0.00  →  0.00     +0.00    ✓ Aligned          │
└──────────────────────────────────────────────────────────────┘
```

- **Intent**: What your function name suggests
- **Execution**: What your code actually does
- **Δ (Delta)**: The difference - where the mismatch is
- **Interpretation**: What that means

### Summary

```
======================================================================
Summary: ✨ 2 excellent, ✓ 3 harmonious, ⚠️  1 to review
💫 Great work! Just a few minor items to review.
   Run with --suggest-names for naming suggestions.
======================================================================
```

- **Summary**: Breakdown of all findings
- **Encouragement**: Proportional to results
  - 🎉 All good? Celebrate!
  - 💫 Mostly good? Gentle encouragement
  - 💡 Issues found? Constructive opportunities
- **Tips**: Helpful next steps

---

## Error Messages Guide

### File Not Found

```
⚠️  Couldn't find file: 'mycode.py'
   Let's check the path is correct?
```

**What to do**: Check spelling, use absolute path, or verify file exists

### Permission Denied

```
⚠️  Couldn't read file: Permission denied
   Check if the file has proper permissions?
```

**What to do**: Run `chmod +r filename` or check file ownership

### Syntax Error

```
⚠️  Syntax error on line 42
   Let's fix the syntax first, then we can check harmony!
```

**What to do**: Fix Python syntax errors before running harmonizer

### Not a Python File

```
⚠️  Skipping 'readme.txt' - Not a Python file
```

**What to do**: Only .py files are analyzed

---

## Celebration Messages

The tool celebrates your good code! Here's what you might see:

### Perfect Code

```
Summary: ✨ 5 excellent
🎉 Beautiful! Your code is semantically harmonious!
```

**Meaning**: All functions have excellent harmony - great job!

### Mostly Good

```
Summary: ✨ 8 excellent, ✓ 2 harmonious, ⚠️  1 to review
💫 Great work! Just a few minor items to review.
```

**Meaning**: Code is mostly great, minor items to polish

### Room for Improvement

```
Summary: ✨ 3 excellent, 🚨 2 need attention
💡 Found some opportunities to improve semantic harmony.
   Run with --suggest-names for naming suggestions.
```

**Meaning**: Some functions need attention - use tools to help fix them

---

## Command-Line Options

### Basic Usage

```bash
harmonizer mycode.py              # Analyze one file
harmonizer src/**/*.py            # Analyze multiple files
harmonizer mycode.py --threshold 0.6   # Custom threshold
```

### Get Help

```bash
harmonizer --suggest-names        # Get function name suggestions
harmonizer --suggest-refactor     # Get refactoring suggestions
harmonizer --format json          # Machine-readable output
harmonizer --version              # Show version
harmonizer --help                 # Show all options
```

### Quiet Mode (for CI/CD)

```bash
harmonizer mycode.py --format json   # No fancy output, just data
```

---

## The Four Dimensions (LJPW)

Every function operates in semantic space with four dimensions:

| Dimension | Represents | Examples |
|-----------|------------|----------|
| **L**ove | Connection, communication | `send()`, `notify()`, `connect()` |
| **J**ustice | Correctness, validation | `validate()`, `check()`, `verify()` |
| **P**ower | Action, transformation | `create()`, `update()`, `delete()` |
| **W**isdom | Knowledge, analysis | `get()`, `calculate()`, `analyze()` |

**Harmony = When the function name's dimension matches what the code does**

---

## Common Patterns & Fixes

### Pattern: "validate" that modifies

```python
# ⚠️  Disharmonious
def validate_user(user):
    user.last_validated = now()  # Modifying!
    return user.email_valid

# ✨ Harmonious
def validate_user(user):
    return user.email_valid     # Just checking
```

### Pattern: "get" that deletes

```python
# 🚨 Needs attention
def get_old_records():
    records = db.query("old")
    db.delete(records)          # Deleting!
    return records

# ✨ Harmonious
def get_old_records():
    return db.query("old")      # Just retrieving

def delete_old_records():
    records = get_old_records()
    db.delete(records)          # Clear intent
```

### Pattern: Mixed semantics

```python
# ⚠️  Worth reviewing
def validate_and_save_user(user):
    if user.valid:
        db.save(user)
    return user.valid

# ✨ Harmonious (two options)

# Option 1: Keep combined, update name
def process_user_validation(user):
    if user.valid:
        db.save(user)
    return user.valid

# Option 2: Split into separate functions
def validate_user(user):
    return user.valid

def save_validated_user(user):
    if validate_user(user):
        db.save(user)
```

---

## Tips for Success

1. **Don't chase perfection**: 0.5 is the threshold, not 0.0
2. **Context matters**: Some patterns are intentional
3. **Use it early**: Easier to fix before code grows
4. **Learn the patterns**: You'll start writing harmonious code naturally
5. **It's complementary**: Use alongside pytest, mypy, etc.

---

## Understanding Your First Report

**Don't panic if you see issues!** Semantic disharmony is common in:
- Legacy code
- Rapidly prototyped code
- Code written without semantic awareness

**This tool helps you see patterns you might miss.**

Even experienced developers write disharmonious code - the tool just makes it visible.

---

## Getting More Help

```bash
# See all options
harmonizer --help

# Get naming suggestions
harmonizer mycode.py --suggest-names

# Get refactoring ideas
harmonizer mycode.py --suggest-refactor

# For detailed semantic info
harmonizer mycode.py  # (maps shown by default)
```

---

## The Goal

**Not perfect code, but conscious code.**

When you write a function, you'll start asking:
> "Does this function DO what its name SAYS it does?"

That's semantic harmony. ⚓

---

**Questions? Issues? Ideas?**
- GitHub: [Python-Code-Harmonizer](https://github.com/BruinGrowly/Python-Code-Harmonizer)
- Docs: [Full documentation](docs/)

**May your code say what it means, and mean what it says.** 💛⚓
