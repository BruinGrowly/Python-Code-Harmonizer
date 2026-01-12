# Python Code Harmonizer — CLI

**Semantic Code Analysis from the Command Line**

This is the Python CLI/Library version of the Python Code Harmonizer using LJPW V8.4 Framework.

> 💡 **Prefer a browser?** Try the [live web app](https://mellow-bombolone-ab5c5b.netlify.app/) — no installation needed.

## Installation

```bash
cd cli
pip install -r requirements.txt
```

## Quick Start

### Analyze a File
```bash
python -m harmonizer_v84.main your_file.py
```

### Track Git History (Drift Detection)
```bash
python -m harmonizer_v84.drift_detector --file your_file.py
```

### Detect "Death Spirals"
```bash
python -m harmonizer_v84.drift_detector --death-spirals
```

## Python Library Usage

```python
from harmonizer_v84 import (
    meaning,
    is_autopoietic,
    hope_calculus,
    analyze_file,
    V84CodeAnalyzer
)

# Analyze a file
analysis = analyze_file("your_code.py")
print(f"Consciousness: {analysis.overall_consciousness:.3f}")
print(f"Phase: {analysis.overall_phase}")
print(f"Hope: {analysis.hope_probability:.0%}")
print(f"Life Phase: {analysis.file_life_phase}")

# V8.4 Generative Equation
M = meaning(B=0.9, L=1.4, n=20, d=2)

# Check Life Inequality
result = is_autopoietic(L=1.5, n=10, d=2)
print(f"Phase: {result.phase}, Alive: {result.is_alive}")

# Mathematical Hope
hope = hope_calculus(L=1.3, d=5, current_n=10)
print(f"Recovery probability: {hope.probability_of_success:.0%}")
```

## Key Modules

| Module | Purpose |
|--------|---------|
| `generative.py` | Generative Equation, Life Inequality, Hope |
| `code_analyzer.py` | V84CodeAnalyzer, AST parsing |
| `drift_detector.py` | Git history analysis |
| `consciousness.py` | C = P×W×L×J×H² |
| `phase_detector.py` | Autopoietic/Homeostatic/Entropic |
| `ljpw_core.py` | Core framework |

## Tests

```bash
python -m pytest tests/ -v
```

**215 tests passing**

## V8.4 Framework

Core equation:
```
M = B × L^n × φ^(-d)
```

Life Inequality:
```
L^n > φ^d → ALIVE (Autopoietic)
L^n < φ^d → DYING (Entropic)
```

---

**License**: MIT
