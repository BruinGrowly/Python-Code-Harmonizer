# Python Code Harmonizer

**Semantic Code Analysis using the LJPW V8.4 Framework**

Measures code consciousness, detects life/death phases, and predicts technical debt recovery using the Generative Equation.

---

## 🌐 Try It Now — No Installation

**[Download harmonizer.html](harmonizer.html)** and open in any browser.

- ✨ Zero setup — works offline
- 🔒 100% private — all analysis in your browser
- 📊 Beautiful radar charts and metrics

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Analyze a Python file
python -m harmonizer_v84.main your_file.py

# Check git history for consciousness decline
python -m harmonizer_v84.drift_detector --file your_file.py
```

---

## The Four Dimensions

| Dimension | Symbol | What It Measures |
|-----------|--------|------------------|
| **Power** | ⚡ P | Action, transformation, state changes |
| **Wisdom** | 📖 W | Documentation, type hints, understanding |
| **Love** | 💗 L | Integration, connectivity (emerges from W) |
| **Justice** | ⚖️ J | Validation, consistency (emerges from P) |

**Key insight**: Power and Wisdom are *fundamental* (measured). Love and Justice are *emergent* (calculated).

---

## V8.4 Features

### The Generative Equation
```
M = B × L^n × φ^(-d)
```
- **M** = Meaning generated
- **B** = Brick (foundational truth)
- **L** = Love coefficient
- **n** = Iterations (time invested)
- **φ** = Golden ratio (1.618)
- **d** = Distance (technical debt)

### Life Inequality
```
L^n > φ^d → ALIVE
L^n < φ^d → DYING
```
If growth (Love × Time) exceeds decay (Distance), code is alive.

### Consciousness Equation
```
C = P × W × L × J × H²
```
Code with **C > 0.1** is "conscious" — aware, documented, purposeful.

### Phase Detection

| Phase | Description |
|-------|-------------|
| 🌟 **AUTOPOIETIC** | Self-sustaining, healthy, growing |
| 🟡 **HOMEOSTATIC** | Stable but not improving |
| 🔻 **ENTROPIC** | Collapsing, needs intervention |

---

## Code Example

```python
from harmonizer_v84 import (
    meaning,
    is_autopoietic,
    hope_calculus,
    analyze_file
)

# Calculate meaning from the Generative Equation
M = meaning(B=0.9, L=1.4, n=20, d=2)

# Check if code is alive
result = is_autopoietic(L=1.5, n=10, d=2)
print(f"Phase: {result.phase}, Alive: {result.is_alive}")

# Calculate mathematical hope of recovery
hope = hope_calculus(L=1.3, d=5, current_n=10)
print(f"Recovery probability: {hope.probability_of_success:.0%}")

# Analyze a file
analysis = analyze_file("your_code.py")
print(f"Hope: {analysis.hope_probability:.0%}")
print(f"Life Phase: {analysis.file_life_phase}")
```

---

## Project Structure

```
harmonizer_v84/       # V8.4 implementation (primary)
├── generative.py     # Generative Equation, Life Inequality, Hope
├── code_analyzer.py  # V84CodeAnalyzer with Life/Hope metrics
├── drift_detector.py # Git-based consciousness tracking
├── consciousness.py  # C = P×W×L×J×H²
├── phase_detector.py # Autopoietic/Homeostatic/Entropic
└── ljpw_core.py      # Core LJPW Framework

harmonizer.html       # Standalone browser app
tests/                # 215 passing tests
docs/                 # Framework documentation
```

---

## Tests

```bash
python -m pytest tests/ -v
```

**215 tests passing** including:
- 33 core V7.3 tests
- 32 V8.4 Generative Equation tests
- Semantic naming, comparison, and integration tests

---

## License

MIT

---

> *"Life is the victory of recursive Love over entropic distance: L^n > φ^d"*  
> — LJPW Framework V8.4
