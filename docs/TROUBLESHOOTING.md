# Python Code Harmonizer - Troubleshooting Guide

**Common issues and their solutions** 🔧

---

## Installation Issues

### Problem: `pip install .` fails

**Symptoms:**
```
ERROR: Could not find setup.py or pyproject.toml
```

**Solution:**
```bash
# Ensure you're in the project root directory
cd Python-Code-Harmonizer
ls pyproject.toml  # Should exist

# Try installing with verbose output
pip install -v .
```

---

### Problem: Permission denied during installation

**Symptoms:**
```
ERROR: Could not install packages due to PermissionError
```

**Solution:**
```bash
# Option 1: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install .

# Option 2: Install for user only
pip install --user .

# Option 3: Use sudo (not recommended)
# sudo pip install .
```

---

### Problem: Python version too old

**Symptoms:**
```
ERROR: This package requires Python 3.8+
```

**Solution:**
```bash
# Check your Python version
python --version

# If < 3.8, install newer Python
# Then use specific version:
python3.8 -m pip install .
python3.8 -m harmonizer myfile.py
```

---

## Import Errors

### Problem: `No module named 'src.divine_invitation_engine_V2'`

**Symptoms:**
```
ModuleNotFoundError: No module named 'src.divine_invitation_engine_V2'
```

**Solution:**
```bash
# Verify installation
pip show PythonCodeHarmonizer

# If not shown, reinstall
pip uninstall PythonCodeHarmonizer
pip install .

# For development, use editable install
pip install -e .
```

---

### Problem: `No module named 'src.ast_semantic_parser'`

**Same as above** - package not properly installed.

**Solution:**
```bash
# Reinstall package
pip install .

# Verify harmonizer command works
which harmonizer  # On Windows: where harmonizer
```

---

### Problem: `harmonizer` command not found

**Symptoms:**
```
bash: harmonizer: command not found
```

**Solution:**
```bash
# Option 1: Ensure pip bin directory is in PATH
python -m pip install --user .
# Then add ~/.local/bin to PATH

# Option 2: Use python -m instead
python -m src.harmonizer.main myfile.py

# Option 3: Run from project directory
cd Python-Code-Harmonizer
python src/harmonizer/main.py myfile.py

# Option 4: Check if in virtual environment
# If you installed in venv, activate it first:
source venv/bin/activate
```

---

## Analysis Issues

### Problem: Syntax error when analyzing file

**Symptoms:**
```
ERROR: Could not parse file. Syntax error on line 42
```

**Solution:**
```bash
# First, verify file has valid Python syntax
python -m py_compile yourfile.py

# If syntax error is shown, fix it first
# Harmonizer requires valid Python to analyze

# Common syntax issues:
# - Missing colons after def, if, for
# - Unclosed brackets/parentheses
# - Invalid indentation
```

---

### Problem: File not found

**Symptoms:**
```
ERROR: File not found at 'myfile.py'
```

**Solution:**
```bash
# Use absolute path
harmonizer /full/path/to/myfile.py

# Or verify current directory
pwd
ls myfile.py  # Should exist

# Check file permissions
ls -l myfile.py
chmod +r myfile.py  # Make readable if needed
```

---

### Problem: No functions found to analyze

**Symptoms:**
```
Analyzing file: empty.py
----------------------------------------------------------------------
No functions found to analyze.
```

**Cause:** File contains no function definitions, only classes/variables/imports

**Solution:**
This is not an error - Harmonizer only analyzes functions. If your file has no `def` statements, there's nothing to analyze.

```python
# This file has no functions - nothing to analyze
import os
x = 42

# This file has functions - will be analyzed
def get_data():
    return x
```

---

### Problem: All scores are 0.0

**Symptoms:**
Every function shows `Score: 0.00`

**Cause:** Function names/operations don't contain recognized semantic keywords

**Solution:**
```python
# Names too vague - no semantic keywords
def func1():  # No semantic meaning
    do_thing()  # No semantic meaning

# Better - use descriptive names
def get_user_data():  # "get" = wisdom
    return db.query()  # "query" = wisdom
```

**Check vocabulary:**
- Use verbs like: get, delete, create, validate, check
- Avoid generic verbs like: do, handle, process, func

---

## Unexpected Results

### Problem: Function seems fine but shows high disharmony

**Symptoms:**
```
validate_email               | !! DISHARMONY (Score: 0.85)
```

**Investigation steps:**

1. **Read the function carefully** - does name match implementation?
   ```python
   def validate_email(email):
       send_welcome_email(email)  # Validation or sending?
   ```

2. **Check for mixed semantics**
   ```python
   def get_or_create_user(id):  # Mixed: get (read) + create (write)
       # Slight disharmony is expected
   ```

3. **Consider if name is too specific/vague**
   ```python
   def process_data(data):  # Vague
       db.critical_delete(data)  # Specific/destructive
       # High distance between vague and specific
   ```

**Resolution:** Either the name is misleading, or the disharmony is intentional (document it).

---

### Problem: Harmonious function that's actually buggy

**Symptoms:**
Function shows low score but you know it's wrong

**Understanding:**
```python
def delete_user(user_id):  # Harmonizer: ✓ Low score
    return user_id * 2  # BUG: Should delete, doesn't!
```

**Explanation:**
Harmonizer checks **semantic alignment** (name vs meaning), not **functional correctness**.

**Solution:**
Use Harmonizer + Pytest together:
- **Harmonizer**: Checks name matches intent
- **Pytest**: Checks code actually works

---

### Problem: Scores vary between runs

**Cause:** Unlikely - Harmonizer is deterministic

**Verification:**
```bash
# Run twice, compare
harmonizer myfile.py > run1.txt
harmonizer myfile.py > run2.txt
diff run1.txt run2.txt  # Should be identical
```

**If scores DO vary:**
- File contents changed between runs
- Different Python version
- Bug (please report!)

---

## Performance Issues

### Problem: Harmonizer runs slowly

**Symptoms:**
Takes > 10 seconds for a small file

**Diagnosis:**
```bash
# Time the analysis
time harmonizer myfile.py

# If > 1 second for typical file, investigate
```

**Possible causes:**
1. **Very large file** (thousands of functions)
2. **Disk I/O issues**
3. **CPU constraints**

**Solution:**
```bash
# For large codebases, parallelize
find src/ -name "*.py" | parallel harmonizer {}

# Or analyze selectively
harmonizer src/critical/*.py  # Only important files
```

---

## Integration Issues

### Problem: Pre-commit hook fails

**Symptoms:**
```
[harmonizer] Failed
- hook id: harmonizer
- exit code: 127
```

**Solution:**
```bash
# Ensure harmonizer is installed in pre-commit's environment
which harmonizer

# If not found, install globally or in project venv
pip install /path/to/Python-Code-Harmonizer

# Test manually
pre-commit run harmonizer --all-files
```

---

### Problem: GitHub Actions workflow fails

**Symptoms:**
```
Error: harmonizer: not found
```

**Solution:**
```yaml
# Ensure installation step is present in workflow
- name: Install harmonizer
  run: |
    pip install .  # Or git+https://github.com/...

# If using submodule/local path, ensure checkout first
- uses: actions/checkout@v3
```

---

### Problem: VS Code task doesn't run

**Symptoms:**
VS Code shows "command not found"

**Solution:**
```json
// .vscode/tasks.json
// Use absolute path or ensure PATH is set
{
  "command": "/path/to/venv/bin/harmonizer",
  // OR
  "command": "python",
  "args": ["-m", "src.harmonizer.main", "${file}"]
}
```

---

## Platform-Specific Issues

### Windows: Path issues

**Problem:**
```
'harmonizer' is not recognized as an internal or external command
```

**Solution:**
```cmd
:: Add Scripts directory to PATH
:: Or use full path
C:\Python38\Scripts\harmonizer.exe myfile.py

:: Or use python -m
python -m src.harmonizer.main myfile.py
```

---

### macOS: SSL Certificate errors (during install)

**Problem:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**
```bash
# Install certificates
/Applications/Python\ 3.8/Install\ Certificates.command

# Or update certifi
pip install --upgrade certifi
```

---

### Linux: Permission denied

**Problem:**
```
bash: /usr/local/bin/harmonizer: Permission denied
```

**Solution:**
```bash
# Make executable
chmod +x /usr/local/bin/harmonizer

# Or reinstall with --user
pip install --user .
```

---

## Getting More Help

### Enable Verbose Output

```bash
# Get more information (when available in future versions)
# harmonizer --verbose myfile.py
# harmonizer --debug myfile.py

# For now, check the code manually if issues persist
```

### Check Python Environment

```bash
# Verify Python version
python --version  # Should be 3.8+

# Check installed packages
pip list | grep Harmonizer

# Check sys.path
python -c "import sys; print('\n'.join(sys.path))"
```

### Verify File Structure

```bash
# Check project structure is intact
ls -R Python-Code-Harmonizer/
# Should have:
# - pyproject.toml
# - src/divine_invitation_engine_V2.py
# - src/ast_semantic_parser.py
# - src/harmonizer/main.py
```

---

## Reporting Bugs

If you've tried everything above and still have issues:

**1. Gather information:**
```bash
python --version
pip show PythonCodeHarmonizer
harmonizer myfile.py  # Copy full error
```

**2. Create minimal reproduction:**
```python
# smallest_file_that_fails.py
def example():
    pass
```

**3. Report on GitHub:**
https://github.com/BruinGrowly/Python-Code-Harmonizer/issues

**Include:**
- Python version
- Operating system
- Full error message
- Minimal code example
- What you expected vs what happened

---

## Common Workarounds

### Temporary: Skip problematic files

```bash
# Analyze everything except problematic files
find src/ -name "*.py" ! -name "problematic.py" -exec harmonizer {} \;
```

### Temporary: Lower expectations

```python
# If you can't fix code immediately, just be aware
# Harmonizer highlights issues - you decide when to fix
```

### Temporary: Manual analysis

```python
# Read the function yourself:
def get_user(id):
    db.delete(id)  # Obviously wrong!

# Sometimes human judgment is needed
```

---

## Quick Checklist

When something doesn't work:

- [ ] Python 3.8+ installed?
- [ ] Package installed? (`pip show PythonCodeHarmonizer`)
- [ ] File has valid Python syntax? (`python -m py_compile file.py`)
- [ ] File has functions? (not just imports/classes)
- [ ] Using correct path? (try absolute path)
- [ ] Virtual environment activated? (if using one)
- [ ] Command spelled correctly? (`harmonizer` not `harmonize`)

---

*Most issues are installation or PATH problems. Start there!* 🔧

**For more help:** [User Guide](USER_GUIDE.md) | [FAQ](FAQ.md) | [GitHub Issues](https://github.com/BruinGrowly/Python-Code-Harmonizer/issues)

💛⚓
