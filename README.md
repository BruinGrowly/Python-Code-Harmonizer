# Python Code Harmonizer (LJPW v4.0)

**The Physics of Software Quality.**

The Python Code Harmonizer is a next-generation static analysis and visualization tool that evaluates codebases using the **LJPW v4.0 Framework** (Love, Justice, Power, Wisdom). It treats code as a dynamic system, using non-linear physics models to predict technical debt, identify architectural smells, and guide refactoring.

![LJPW Dashboard](examples/ljpw_v4_demo_plot.png)

## Key Features

### 1. 🌌 Dynamic Physics Model (LJPW v4.0)
Unlike traditional linters that count errors, the Harmonizer simulates your code's "energy state" over time.
-   **Natural Equilibrium (NE)**: Stable state for healthy code (`L=0.62, J=0.41, P=0.72, W=0.69`).
-   **High-Energy State**: "Thriving" state for complex, well-architected systems.
-   **Entropy Detection**: Predicts "Justice Collapse" (technical debt avalanches) before they happen.

### 2. 📊 Visual Analytics
Generate interactive HTML reports to explore your codebase's semantic structure.
-   **Radar Charts**: Visualize the balance of Love (Care), Justice (Structure), Power (Action), and Wisdom (Abstraction).
-   **Dependency Galaxy**: A force-directed graph showing the "gravitational pull" of your modules.
-   **Semantic Density**: Identify "Anemic Components" (high complexity, low action).

### 3. 🛡️ CI/CD Integration
Prevent entropy decay with built-in quality gates.
-   **`check_harmony.py`**: CLI tool for CI pipelines. Fails builds if code drifts too far from equilibrium.
-   **GitHub Action**: Ready-to-use workflow in `.github/workflows/ljpw_gate.yml`.
-   **Pre-commit Hook**: Local checks via `.pre-commit-config.yaml`.

### 4. ⚙️ Developer Experience
-   **Configurable**: Customize thresholds in `pyproject.toml` or `harmonizer.yaml`.
-   **Ignore System**: Exclude files using `.harmonizerignore`.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 1. Generate Visual Report
Analyze your codebase and generate an interactive HTML dashboard:

```bash
python scripts/run_validation.py
# Opens harmonizer_report.html
```

### 2. Run Quality Gate (CI/CD)
Check if your code meets LJPW standards (exit code 0 = PASS, 1 = FAIL):

```bash
python check_harmony.py .
```

### 3. Configuration
Create a `pyproject.toml` to customize thresholds:

```toml
[tool.harmonizer.thresholds]
max_disharmony = 1.0
max_imbalance = 0.8
min_density = 0.1

[tool.harmonizer.paths]
exclude = ["venv", "tests"]
```

## The LJPW Framework

-   **Love (L)**: Care, readability, comments, user-focus.
-   **Justice (J)**: Structure, types, tests, consistency.
-   **Power (P)**: Action, logic, complexity, performance.
-   **Wisdom (W)**: Abstraction, architecture, patterns, insight.

## Project Structure

-   `harmonizer/`: Core analysis engine.
-   `scripts/`: Utility scripts (`run_validation.py`).
-   `docs/`: Detailed documentation and theory.
-   `examples/`: Demo scripts.
-   `tests/`: Unit and validation tests.

## License
MIT
