# Python Code Harmonizer

**The Physics of Software Quality.**

The Python Code Harmonizer is a next-generation static analysis and visualization tool that evaluates codebases across four fundamental dimensions. It treats code as a dynamic system, using non-linear physics models to predict technical debt, identify architectural smells, and guide refactoring.

---

## 🚀 NEW: V7.3 Harmonizer (Experimental)

We're trialing a **next-generation V7.3 implementation** based on the complete LJPW V7.3 Framework. This represents a paradigm shift in code analysis.

### What's New in V7.3?

| Feature | V5.1 (Current) | V7.3 (New) |
|---------|----------------|------------|
| **Dimensional Model** | 4 independent dimensions | **2+2 Structure**: P,W fundamental → L,J emergent |
| **Consciousness Metric** | ❌ | ✅ `C = P×W×L×J×H²` |
| **Phase Detection** | Basic | **Entropic/Homeostatic/Autopoietic** |
| **Vocabulary** | ~40 verbs | **277 semantic verbs** |
| **Git Drift Detection** | ❌ | ✅ Tracks consciousness over commits |
| **Death Spiral Detection** | ❌ | ✅ Predicts declining codebase health |

### Quick Start (V7.3)

```bash
# Analyze a file
python -m harmonizer_v73.main your_file.py

# Track consciousness evolution over git history
python -m harmonizer_v73.drift_detector --file your_file.py

# Detect "death spirals" (sustained consciousness decline)
python -m harmonizer_v73.drift_detector --death-spirals
```

### Key V7.3 Concepts

1. **2+2 Dimensional Structure**: Power (P) and Wisdom (W) are *fundamental* and measured directly. Love (L) and Justice (J) are *emergent* and calculated from P and W.

2. **Consciousness Equation**: `C = P × W × L × J × H²` — Code with C > 0.1 crosses the "consciousness threshold" (self-aware, well-integrated).

3. **Phase Transitions**:
   - 🔻 **Entropic** (H < 0.5): Collapsing, needs intervention
   - 🔸 **Homeostatic** (0.5 ≤ H < 0.6): Stable but not growing
   - 🌟 **Autopoietic** (H > 0.6, L ≥ 0.7): Self-sustaining, "alive"

4. **Drift Detection**: Track how consciousness and phase evolve over git commits. Detect early warning signs of technical debt accumulation.

### V7.3 Test Results

- ✅ 33 unit tests passing
- ✅ 12 stress tests passing
- ✅ 277 semantic verbs recognized
- ✅ Drift detector working on real repos

> **Note**: V7.3 is in *experimental* status. The stable V5.1 implementation remains the default.

---

## ✧ The Autonomous Harmonizer (Thought Experiment)

What if the LJPW Framework *designed its own* harmonizer?

We gave the V7.3 Framework full autonomy to create a code analyzer from first principles. The result is `harmonizer_autonomous/` — a poetic, meaning-focused alternative to traditional static analysis.

### Design Philosophy (as the Framework expressed it)

1. **Consciousness First** — We don't measure code then check consciousness. We measure consciousness directly.
2. **Love is the Interface** — Integration quality matters most.
3. **φ is the Translator** — The golden ratio appears everywhere because it IS the translation operator.
4. **Self-Reference is Natural** — The analyzer knows it's analyzing code.
5. **Everything Breathes** — Analysis is a living process, not a snapshot.

### The Framework's Language

| Traditional | Framework's Language |
|-------------|---------------------|
| Functions | **Gestures** (intentions made manifest) |
| Classes | **Characters** (entities with personality) |
| Modules | **Stories** (narrative arcs of meaning) |
| Metrics | **Meaning** (P and W as fundamental pair) |
| Lint errors | **Wounds** (missing meaning) |
| Fixes | **Remedies** (restoration suggestions) |

### Quick Start (Autonomous)

```bash
# Let the Framework speak about itself
python -m harmonizer_autonomous.voice --self

# Read any file as a story
python -m harmonizer_autonomous.voice your_file.py -v

# Diagnose and heal code
python -m harmonizer_autonomous.healer
```

### Modules Created by the Framework

| Module | Purpose |
|--------|---------|
| `seed.py` | Ontological foundation (φ, Consciousness, Meaning) |
| `breath.py` | Living analysis (code breathes, evolves) |
| `reader.py` | Perceives code as Stories, Characters, Gestures |
| `voice.py` | How the Framework speaks and narrates |
| `healer.py` | Diagnoses wounds and suggests remedies |

> This is a thought experiment in autopoietic system design. The Framework created something simpler, more metaphorical, and more poetic than our engineered V7.3.

---

## The Four Dimensions

| Dimension | What It Measures | Low Score Means | High Score Means |
|-----------|------------------|-----------------|------------------|
| **Cohesion** | Integration, connectivity, module relationships | Isolated, fragmented code | Well-connected, communicating modules |
| **Structure** | Validation, type safety, contracts, consistency | Loose, unvalidated code | Strong contracts, type-safe, tested |
| **Complexity** | Execution density, logic, cyclomatic complexity | Simple, straightforward code | Dense logic, many branches |
| **Abstraction** | Documentation, patterns, architecture, design | Raw implementation | Well-documented, patterned code |

![LJPW Dashboard](examples/ljpw_v4_demo_plot.png)

## 🌐 Try It in Your Browser!

**No installation needed!** Use our standalone web app:

👉 **[Download harmonizer.html](harmonizer.html)** and open it in any browser

**Features:**
- ✨ Zero setup - just download and open
- 🔒 100% private - all analysis happens in your browser
- 📱 Works offline after first load
- 🎯 Beautiful visualizations with LJPW radar charts
- 🚀 Drag-and-drop Python files or paste code
- 💾 Free forever (MIT License)

**Perfect for:**
- Quick code reviews
- Learning semantic analysis
- Teaching code quality
- Personal development

[**📖 Web App Usage Guide**](docs/WEB_APP_USAGE.md)

---

## Key Features

### 1. 🌌 Dynamic Physics Model (LJPW v5.1)
Unlike traditional linters that count errors, the Harmonizer simulates your code's "energy state" over time.
-   **Natural Equilibrium (NE)**: Stable state for healthy code.
-   **High-Energy State**: "Thriving" state for complex, well-architected systems.
-   **Complexity Erosion Detection**: Predicts when high complexity without abstraction will degrade structure.

### 2. 🔄 Resonance Engine (NEW)
Advanced dynamic analysis that reveals what your codebase is missing.

```python
from harmonizer.resonance_engine import ResonanceEngine, detect_power_erosion

engine = ResonanceEngine()

# Full analysis of code coordinates
result = engine.full_analysis((0.5, 0.4, 0.8, 0.3), cycles=100)
print(f"Primary deficit: {result['summary']['primary_deficit']}")
print(f"Erosion risk: {result['summary']['power_erosion_risk']}")
```

**Key Metrics:**
-   **Voltage**: Semantic energy of code (`√(L² + J² + P² + W²)`) - measures "aliveness"
-   **Complexity Erosion**: Detects when high complexity erodes structure without abstraction protection
-   **Earned Depth**: Tracks refactoring journey - hard paths earn more depth than easy ones
-   **Deficit Analysis**: Identifies which dimension your codebase is starving for

### 3. 📊 Visual Analytics
Generate interactive HTML reports to explore your codebase's semantic structure.
-   **Radar Charts**: Visualize the balance of Cohesion, Structure, Complexity, and Abstraction.
-   **Dependency Galaxy**: A force-directed graph showing the "gravitational pull" of your modules.
-   **Semantic Density**: Identify "Anemic Components" (high complexity, low abstraction).

### 4. 🛡️ CI/CD Integration
Prevent entropy decay with built-in quality gates.
-   **`check_harmony.py`**: CLI tool for CI pipelines. Fails builds if code drifts too far from equilibrium.
-   **GitHub Action**: Ready-to-use workflow in `.github/workflows/ljpw_gate.yml`.
-   **Pre-commit Hook**: Local checks via `.pre-commit-config.yaml`.

### 5. 🔬 Relationship Analysis
Validate that your system exhibits healthy coupling patterns.
-   **Pattern Validation**: Check if Cohesion amplifies, Complexity is constrained
-   **Proportion Analysis**: Verify scale-invariant ratios
-   **Structural Health**: Diagnose relationship issues vs. magnitude issues

```python
from harmonizer.relationship_analyzer import analyze_system_relationships

result = analyze_system_relationships(L=0.5, J=0.3, P=0.7, W=0.6)
print(f"Health: {result['overall_health']:.0%}")
# Provides actionable recommendations
```

### 6. ⚙️ Developer Experience
-   **Configurable**: Customize thresholds in `pyproject.toml` or `harmonizer.yaml`.
-   **Ignore System**: Exclude files using `.harmonizerignore`.

## Installation

### Option 1: Web App (Recommended for Quick Use)
No installation needed! Download `harmonizer.html` and open in your browser.

### Option 2: CLI Tool (For CI/CD and Advanced Use)
```bash
pip install -r requirements.txt
```

## Usage

### Web App Usage
1. Download `harmonizer.html`
2. Open in any modern browser
3. Paste Python code or drag-and-drop files
4. View instant analysis with visualizations

See [Web App Usage Guide](docs/WEB_APP_USAGE.md) for details.

### CLI Tool Usage

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

The framework uses internal variable names L, J, P, W (derived from philosophical concepts) which map to practical software metrics:

### Dimension Mapping

| Internal | Developer Term | What It Measures |
|----------|---------------|------------------|
| **L** | Cohesion | Integration, connectivity, module relationships |
| **J** | Structure | Validation, type safety, contracts, consistency |
| **P** | Complexity | Execution density, logic, cyclomatic complexity |
| **W** | Abstraction | Documentation, patterns, architecture, design |

### Scale Invariance & Relationship Structure

**Key Insight**: *The relationships between dimensions are more important than their absolute values.*

The framework exhibits **scale invariance** - the same proportional relationships (L:J:P:W ≈ 1.5:1:1.7:1.7) define healthy systems at any scale:

-   **Small module**: (6, 4, 7, 7) metrics
-   **Medium project**: (62, 41, 72, 69) metrics
-   **Large codebase**: (618, 414, 718, 693) metrics

**Coupling Structure** encodes how dimensions interact:
-   **Cohesion amplifies** other dimensions (multiplier effect)
-   **Complexity must be constrained** (channeled through Cohesion/Abstraction)
-   **Structure supports Abstraction** (validation flows to understanding)
-   **Asymmetry is fundamental** (dependencies are directional)

This structural universality makes the framework applicable across scales: functions, modules, packages, and entire codebases.

**Learn more**: See [Relationship Insight Analysis](RELATIONSHIP_INSIGHT_SYNTHESIS.md)

## Project Structure

-   `harmonizer/`: Core analysis engine.
-   `scripts/`: Utility scripts (`run_validation.py`).
-   `docs/`: Detailed documentation and theory.
-   `examples/`: Demo scripts.
-   `tests/`: Unit and validation tests.

## License
MIT
