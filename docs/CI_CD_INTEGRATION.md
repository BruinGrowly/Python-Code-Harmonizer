# CI/CD Integration Guide

**Python Code Harmonizer v1.2+ includes built-in CI/CD support with exit codes and JSON output.**

This guide shows you how to integrate Harmonizer into your continuous integration pipelines to enforce code harmony standards automatically.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Exit Codes Reference](#exit-codes-reference)
3. [GitHub Actions Integration](#github-actions-integration)
4. [GitLab CI Integration](#gitlab-ci-integration)
5. [Jenkins Integration](#jenkins-integration)
6. [CircleCI Integration](#circleci-integration)
7. [JSON Output for Dashboards](#json-output-for-dashboards)
8. [Custom Thresholds](#custom-thresholds)
9. [Best Practices](#best-practices)

---

## Quick Start

### Basic CI/CD Integration

```yaml
# Minimum viable integration
- name: Check Code Harmony
  run: harmonizer src/**/*.py
```

**That's it!** Harmonizer v1.2+ automatically:
- Returns exit code 0 if harmonious
- Returns exit codes 1-3 based on severity
- Fails your build on high/critical disharmony

---

## Exit Codes Reference

Harmonizer returns meaningful exit codes based on the **highest severity** found:

| Exit Code | Severity | Score Range | CI/CD Behavior | Recommended Action |
|-----------|----------|-------------|----------------|-------------------|
| `0` | Excellent/Low | < 0.5 | ✅ Build passes | None - code is harmonious |
| `1` | Medium | 0.5 - 0.8 | ⚠️ Warning | Review flagged functions |
| `2` | High | 0.8 - 1.2 | ❌ Build fails | Refactor before merge |
| `3` | Critical | ≥ 1.2 | 🚨 Build fails | Immediate attention required |

### Exit Code Examples

```bash
# Harmonious code
$ harmonizer good_code.py
# Exit code: 0

# Medium disharmony
$ harmonizer medium_code.py
# Exit code: 1

# Critical disharmony
$ harmonizer bad_code.py
# Exit code: 3
```

---

## GitHub Actions Integration

### Option 1: Add to Existing CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install .

      - name: Run tests
        run: pytest

      - name: Check Code Harmony  # ← Add this step
        run: harmonizer src/**/*.py
```

### Option 2: Dedicated Harmony Workflow

```yaml
# .github/workflows/harmony-check.yml
name: Code Harmony Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  harmony:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Harmonizer
        run: pip install .

      - name: Check Code Harmony
        run: |
          echo "🔍 Checking Code Harmony..."
          harmonizer src/**/*.py
          echo "✅ Harmony check passed!"
```

### Option 3: With JSON Report Artifact

```yaml
jobs:
  harmony-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Harmonizer
        run: pip install .

      - name: Generate Harmony Report
        run: |
          harmonizer --format json src/**/*.py > harmony-report.json || true

      - name: Upload Report Artifact
        uses: actions/upload-artifact@v3
        with:
          name: harmony-report
          path: harmony-report.json
          retention-days: 30

      - name: Display Summary
        run: |
          cat harmony-report.json | python -c "
          import json, sys
          data = json.load(sys.stdin)
          summary = data['summary']
          print(f\"📊 Harmony Summary:\")
          print(f\"  Total functions: {summary['total_functions']}\")
          print(f\"  Highest severity: {summary['highest_severity']}\")
          for sev, count in summary['severity_counts'].items():
              if count > 0:
                  print(f\"    {sev.capitalize()}: {count}\")
          "
```

---

## GitLab CI Integration

```yaml
# .gitlab-ci.yml
harmony-check:
  stage: test
  image: python:3.11
  script:
    - pip install .
    - harmonizer src/**/*.py
  allow_failure: false  # Fail build on disharmony
```

### With JSON Artifact

```yaml
harmony-report:
  stage: test
  image: python:3.11
  script:
    - pip install .
    - harmonizer --format json src/**/*.py > harmony-report.json || true
  artifacts:
    name: "harmony-report"
    paths:
      - harmony-report.json
    expire_in: 30 days
```

---

## Jenkins Integration

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Code Harmony Check') {
            steps {
                sh '''
                    pip install .
                    harmonizer src/**/*.py
                '''
            }
        }
    }
}
```

### With Exit Code Handling

```groovy
stage('Code Harmony Check') {
    steps {
        script {
            def exitCode = sh(
                script: 'harmonizer src/**/*.py',
                returnStatus: true
            )

            if (exitCode == 3) {
                error('Critical disharmony detected - build failed')
            } else if (exitCode == 2) {
                unstable('High disharmony detected - review required')
            } else if (exitCode == 1) {
                echo 'Medium disharmony detected - consider refactoring'
            } else {
                echo 'Code harmony check passed ✅'
            }
        }
    }
}
```

---

## CircleCI Integration

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  harmony-check:
    docker:
      - image: python:3.11
    steps:
      - checkout
      - run:
          name: Install Harmonizer
          command: pip install .
      - run:
          name: Check Code Harmony
          command: harmonizer src/**/*.py

workflows:
  test:
    jobs:
      - harmony-check
```

---

## JSON Output for Dashboards

### Generate JSON Report

```bash
harmonizer --format json src/**/*.py > harmony-report.json
```

### JSON Structure

```json
{
  "version": "1.2",
  "threshold": 0.5,
  "severity_thresholds": {
    "excellent": 0.3,
    "low": 0.5,
    "medium": 0.8,
    "high": 1.2
  },
  "files": [{
    "file": "src/mymodule.py",
    "functions": [{
      "name": "get_user",
      "score": 0.95,
      "severity": "high",
      "disharmonious": true
    }]
  }],
  "summary": {
    "total_files": 10,
    "total_functions": 50,
    "severity_counts": {
      "excellent": 30,
      "low": 10,
      "medium": 7,
      "high": 2,
      "critical": 1
    },
    "highest_severity": "critical"
  }
}
```

### Parse JSON in CI

```python
# parse_harmony.py
import json, sys

with open('harmony-report.json') as f:
    data = json.load(f)

summary = data['summary']
print(f"Total functions analyzed: {summary['total_functions']}")
print(f"Highest severity: {summary['highest_severity']}")

# Fail if critical issues found
if summary['severity_counts']['critical'] > 0:
    print(f"❌ {summary['severity_counts']['critical']} critical issues found!")
    sys.exit(1)
```

---

## Custom Thresholds

### Strict Mode (Excellent Standard)

```yaml
# Enforce excellent harmony (0.3 threshold)
- name: Strict Harmony Check
  run: harmonizer --threshold 0.3 src/**/*.py
```

### Permissive Mode (Only Critical)

```yaml
# Only fail on critical issues
- name: Critical-Only Check
  run: |
    harmonizer src/**/*.py || EXIT_CODE=$?
    if [ $EXIT_CODE -eq 3 ]; then
      echo "Critical disharmony found - failing build"
      exit 1
    else
      echo "No critical issues - build continues"
      exit 0
    fi
```

### Different Thresholds for Different Paths

```yaml
- name: Check Critical Modules (Strict)
  run: harmonizer --threshold 0.3 src/core/**/*.py

- name: Check Other Modules (Standard)
  run: harmonizer --threshold 0.5 src/**/*.py
```

---

## Best Practices

### 1. Start Permissive, Then Tighten

```yaml
# Week 1-2: Don't fail builds, just report
- run: harmonizer src/**/*.py || true

# Week 3-4: Fail only on critical
- run: |
    harmonizer src/**/*.py || EXIT_CODE=$?
    [ $EXIT_CODE -lt 3 ] && exit 0 || exit 1

# Week 5+: Fail on high or critical (default)
- run: harmonizer src/**/*.py
```

### 2. Separate Source and Test Standards

```yaml
# Strict for source code
- name: Check Source Code
  run: harmonizer --threshold 0.5 src/**/*.py

# Permissive for tests (allow some disharmony)
- name: Check Tests (Informational)
  run: harmonizer tests/**/*.py || echo "Test disharmony noted"
  continue-on-error: true
```

### 3. Track Trends with JSON

```yaml
- name: Generate Harmony Report
  run: harmonizer --format json src/**/*.py > harmony-${{ github.sha }}.json

- name: Upload to Metrics System
  run: |
    # Send to your metrics/monitoring system
    curl -X POST \
      -H "Content-Type: application/json" \
      -d @harmony-${{ github.sha }}.json \
      https://your-metrics-system/api/harmony
```

### 4. Comment on Pull Requests

```yaml
- name: Comment Harmony Results
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const report = JSON.parse(fs.readFileSync('harmony-report.json'));
      const summary = report.summary;

      const comment = `
      ## 🎯 Code Harmony Report

      - **Total Functions**: ${summary.total_functions}
      - **Excellent**: ${summary.severity_counts.excellent} 🟢
      - **Medium**: ${summary.severity_counts.medium} 🟡
      - **High**: ${summary.severity_counts.high} 🟠
      - **Critical**: ${summary.severity_counts.critical} 🔴

      ${summary.highest_severity === 'critical' ? '❌ Build will fail due to critical disharmony' : '✅ No critical issues found'}
      `;

      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: comment
      });
```

### 5. Pre-merge Hooks

```yaml
# Only run on PRs, not on main
on:
  pull_request:
    branches: [ main ]

jobs:
  harmony-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install .
      - run: harmonizer src/**/*.py
```

---

## Example: Full Production Setup

```yaml
# .github/workflows/harmony-check.yml
name: Code Harmony Quality Gate

on:
  pull_request:
    branches: [ main, develop ]

jobs:
  # Job 1: Standard harmony check
  harmony-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Harmonizer
        run: pip install .

      - name: Run Harmony Check
        run: |
          echo "🔍 Checking code harmony..."
          harmonizer src/**/*.py
          echo "✅ Harmony check passed!"

  # Job 2: Detailed JSON report
  harmony-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Harmonizer
        run: pip install .

      - name: Generate JSON Report
        run: |
          harmonizer --format json src/**/*.py > harmony-report.json || true

      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: harmony-report-${{ github.sha }}
          path: harmony-report.json

      - name: Display Top Issues
        run: |
          python -c "
          import json
          with open('harmony-report.json') as f:
              data = json.load(f)
          funcs = []
          for file in data['files']:
              for func in file['functions']:
                  if func['disharmonious']:
                      funcs.append((func['score'], func['name'], file['file']))
          funcs.sort(reverse=True)
          print('🎯 Top 5 Functions to Refactor:')
          for i, (score, name, file) in enumerate(funcs[:5], 1):
              print(f'  {i}. {name} ({score:.2f}) in {file}')
          "
```

---

## Troubleshooting

### "harmonizer: command not found"

Make sure you install the package:
```yaml
- run: pip install .
```

### Build passes when it should fail

Check you're using v1.2+:
```bash
harmonizer --version
# Should show: Python Code Harmonizer v1.2
```

### JSON output is broken

Make sure to redirect stderr:
```bash
harmonizer --format json myfile.py 2>/dev/null > report.json
```

Or capture both:
```bash
harmonizer --format json myfile.py > report.json 2>&1
```

### Want to see which files have issues in CI logs

Add verbose output before the check:
```yaml
- run: |
    echo "Files to analyze:"
    find src/ -name "*.py"
    harmonizer src/**/*.py
```

---

## Summary

**Python Code Harmonizer v1.2+ makes CI/CD integration effortless:**

✅ **Exit codes** automatically fail builds on critical disharmony
✅ **JSON output** enables dashboards and trend tracking
✅ **Custom thresholds** let teams set their own standards
✅ **Works everywhere** - GitHub Actions, GitLab CI, Jenkins, CircleCI, etc.

**Minimum integration:**
```yaml
- run: harmonizer src/**/*.py
```

**That's it!** Your builds now enforce semantic code harmony. 💛⚓

---

## Resources

- [Quick Reference](QUICK_REFERENCE.md) - Command-line options
- [User Guide](USER_GUIDE.md) - Comprehensive usage
- [FAQ](FAQ.md) - Common questions
- [Examples](../examples/) - Real-world examples

**Questions?** Open an issue on GitHub!
