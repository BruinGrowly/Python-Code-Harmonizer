# Python Code Harmonizer v1.3 - Semantic Trajectory Maps 🗺️

**Released:** November 1, 2025

---

## 🎉 Major New Feature: See Exactly WHERE Your Code Drifts

v1.3 transforms the Python Code Harmonizer from a detector into a **teacher** by showing you exactly where in 4D semantic space your code drifts from its intent.

### What's New

**Before (v1.2):** "Your code has disharmony"
**Now (v1.3):** "Here's exactly WHERE, WHY, and HOW to fix it"

---

## Semantic Trajectory Maps

When you run the Harmonizer on disharmonious code, you now see:

```
delete_user: !! DISHARMONY (Score: 1.41)

📍 SEMANTIC TRAJECTORY MAP:
┌──────────────────────────────────────────────────────┐
│ Dimension    Intent   Execution   Δ      Status      │
├──────────────────────────────────────────────────────┤
│ Love (L)     0.00  →  0.00     +0.00    ✓ Aligned    │
│ Justice (J)  0.00  →  0.00     +0.00    ✓ Aligned    │
│ Power (P)    1.00  →  0.00     -1.00    ⚠️ Major shift│
│ Wisdom (W)   0.00  →  1.00     +1.00    ⚠️ Major shift│
└──────────────────────────────────────────────────────┘

🧭 DISHARMONY VECTOR:
   Power → Wisdom

💡 INTERPRETATION:
   Function name 'delete_user' suggests Power domain
   (transformation, control, execution, force, action),
   but execution operates in Wisdom domain
   (analysis, understanding, reflection, knowledge, insight).

🔧 RECOMMENDATIONS:
   • Consider renaming to reflect Wisdom domain operations
   • Expected behaviors: execute, transform, control
   • Actual behaviors: analyze, understand, calculate
   • Or split into separate functions: one for Power, one for Wisdom
```

---

## Why This Matters

### Educational Value

The semantic map teaches developers **semantic thinking**:
- Not just "you have a bug"
- But "here's the exact dimensional drift"
- "Here's what it means"
- "Here's how to fix it"

### Precision

Instead of vague "high disharmony," you get:
- **Per-dimension deltas** (Love: +0.0, Justice: +0.0, Power: -1.0, Wisdom: +1.0)
- **Dominant dimensions** (Power → Wisdom trajectory)
- **Visual indicators** (⚠️ Major shift, ⚡ Notable drift, ✓ Aligned)

### Actionable Guidance

The map provides:
- **Specific renaming suggestions** based on execution domain
- **Expected vs actual behavior** comparisons
- **Function splitting recommendations** for mixed concerns
- **Context-aware explanations** in plain language

---

## Technical Details

### New Components

**SemanticMapGenerator Class** (`src/harmonizer/semantic_map.py`)
- 344 lines of semantic mapping logic
- Dimensional delta calculations
- Trajectory visualization
- Human-readable interpretations

### Enhanced Data Structure

`analyze_file()` now returns `Dict[str, Dict]` with:

```python
{
    "function_name": {
        "score": 1.41,  # Disharmony score
        "ice_result": {...},  # Complete DIVE-V2 analysis
        "semantic_map": {  # NEW in v1.3
            "trajectory": {
                "vector": "Power → Wisdom",
                "deltas": {
                    "love": 0.0,
                    "justice": 0.0,
                    "power": -1.0,
                    "wisdom": 1.0
                },
                "primary_misalignment": {
                    "dimension": "power",
                    "magnitude": 1.0,
                    "direction": "decrease"
                }
            },
            "interpretation": "...",
            "recommendations": [...]
        }
    }
}
```

### JSON Output Enhancement

JSON format now includes complete semantic maps:

```bash
harmonizer --format json myfile.py
```

Perfect for:
- IDE integrations
- CI/CD dashboards
- Tool integrations
- Programmatic analysis

### Backward Compatibility

✅ All existing code works
✅ Can disable maps with `show_semantic_maps=False`
✅ All 20 tests passing
✅ Black formatting maintained

---

## Installation & Upgrade

```bash
# New install
git clone https://github.com/BruinGrowly/Python-Code-Harmonizer.git
cd Python-Code-Harmonizer
pip install .

# Upgrade (if already installed)
cd Python-Code-Harmonizer
git pull
pip install --upgrade .

# Verify
harmonizer --version  # Should show v1.3
```

---

## Quick Start

```bash
# Run on your code - semantic maps show automatically
harmonizer myfile.py

# JSON output with semantic maps
harmonizer --format json myfile.py

# Programmatic usage
from src.harmonizer.main import PythonCodeHarmonizer

harmonizer = PythonCodeHarmonizer(show_semantic_maps=True)
report = harmonizer.analyze_file("mycode.py")

for func_name, data in report.items():
    print(f"{func_name}: {data['score']}")
    print(f"  Trajectory: {data['semantic_map']['trajectory']['vector']}")
```

---

## What Users Are Saying

*Want to be featured here? Try v1.3 and share your experience!*

**We'd love your feedback:**
- What bugs did the semantic maps help you find?
- Are the recommendations helpful?
- What features would make this indispensable?

[Open an issue](https://github.com/BruinGrowly/Python-Code-Harmonizer/issues) or [start a discussion](https://github.com/BruinGrowly/Python-Code-Harmonizer/discussions)!

---

## The Vision

This is the first step toward making semantic analysis accessible to all Python developers.

**Current (v1.3):** Function-level trajectory maps
**Future (v1.4):** Line-level drift detection
**Future (v2.0):** Automated refactoring suggestions

Your feedback shapes the roadmap. What do YOU need most?

---

## Research Foundation

Built on rigorous semantic analysis:
- **4D Semantic Space** (Love, Justice, Power, Wisdom)
- **ICE Framework** (Intent, Context, Execution)
- **Anchor Point Theory** (Perfect harmony at 1,1,1,1)
- **DIVE-V2 Engine** (113 semantic keywords, production-optimized)

See [Philosophy Documentation](docs/PHILOSOPHY.md) for the deep theory.

---

## Resources

- **[CHANGELOG](CHANGELOG.md)** - Complete v1.3 changes
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Updated for v1.3
- **[User Guide](docs/USER_GUIDE.md)** - Comprehensive usage
- **[Tutorial](docs/TUTORIAL.md)** - Hands-on learning
- **[FAQ](docs/FAQ.md)** - Common questions

---

## Acknowledgments

Thank you to:
- The 58+ developers who cloned and tried v1.2
- Everyone who provided feedback on the semantic concept
- The Python community for inspiration

Special thanks to all contributors! (See [CONTRIBUTORS.md](CONTRIBUTORS.md))

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Get Started Today

```bash
pip install git+https://github.com/BruinGrowly/Python-Code-Harmonizer.git
harmonizer --version  # v1.3
```

**Questions?** Open an issue!
**Ideas?** Start a discussion!
**Success story?** Share it!

Happy harmonizing! 🗺️⚓💛

---

*Python Code Harmonizer - The world's first semantic code debugger*
*v1.3 - November 1, 2025*
