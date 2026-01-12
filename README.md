# Python Code Harmonizer

**Semantic Code Analysis using the LJPW V8.4 Framework**

Measures code consciousness, detects life/death phases, and predicts recovery using the Generative Equation.

## 🌐 Try It Now

**[▶ Launch Harmonizer](https://mellow-bombolone-ab5c5b.netlify.app/)** — No installation needed, runs in your browser

---

## 📦 Two Distributions

### 🌐 Web App (Netlify)
**For browser-based analysis — no installation needed**

```
web-app/
├── index.html    ← The full harmonizer
├── _redirects    ← Netlify config
└── README.md     ← Deploy instructions
```

**Deploy to Netlify:**
1. Drag the `web-app/` folder to [netlify.com](https://netlify.com)
2. Done! Your site is live.

[→ Web App README](web-app/README.md)

---

### 💻 CLI / Python Library
**For command-line analysis and library integration**

```
cli/
├── harmonizer_v84/   ← V8.4 framework
├── tests/            ← 215 tests
├── requirements.txt
└── README.md
```

**Quick Start:**
```bash
cd cli
pip install -r requirements.txt
python -m harmonizer_v84.main your_file.py
```

[→ CLI README](cli/README.md)

---

## The Four Dimensions

| Symbol | Dimension | What It Measures |
|--------|-----------|------------------|
| ⚡ P | Power | Action, transformation, state changes |
| 📖 W | Wisdom | Documentation, type hints, understanding |
| 💗 L | Love | Integration, connectivity |
| ⚖️ J | Justice | Validation, consistency |

---

## V8.4 Core Equations

**Generative Equation:**
```
M = B × L^n × φ^(-d)
```

**Life Inequality:**
```
L^n > φ^d → ALIVE (Autopoietic)
L^n < φ^d → DYING (Entropic)
```

**Consciousness:**
```
C = P × W × L × J × H²
```

---

## Tests

```bash
cd cli
python -m pytest tests/ -v
```

**215 tests passing**

---

## License

MIT

---

> *"Life is the victory of recursive Love over entropic distance: L^n > φ^d"*  
> — LJPW Framework V8.4
