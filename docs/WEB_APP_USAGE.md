# Python Code Harmonizer - Web App Usage Guide

## 🚀 Quick Start

You now have a **single HTML file** (`harmonizer.html`) that provides a complete web-based Python code analyzer!

### How to Use

**Option 1: Open Locally**
1. Download `harmonizer.html` from the repository
2. Double-click the file to open it in your browser
3. Start analyzing code immediately!

**Option 2: Host on GitHub Pages**
1. Enable GitHub Pages in your repository settings
2. Upload `harmonizer.html`
3. Share the URL with anyone: `https://yourusername.github.io/harmonizer.html`

**Option 3: Bookmark It**
- Add the file to your browser bookmarks
- Access it instantly whenever you need to analyze code

---

## 📋 Features

### ✨ What You Can Do

- **Paste Code**: Copy-paste Python functions directly
- **Drag & Drop**: Drop `.py` files onto the text area
- **Instant Analysis**: Results appear in seconds
- **Visual Results**: Beautiful radar charts and tables
- **Example Code**: Click buttons to load pre-made examples
- **100% Private**: All processing happens in your browser
- **Offline Ready**: Works without internet (after first load)

### 📊 What You'll See

1. **Summary Cards**
   - Total functions analyzed
   - Harmonious vs. disharmonious count
   - Average disharmony score

2. **LJPW Radar Chart**
   - Visual representation of code balance
   - Compare with Natural Equilibrium baseline
   - See which dimension dominates

3. **Function Table**
   - All functions sorted by disharmony score
   - Color-coded severity badges
   - Quick status overview

---

## 🎯 Understanding Results

### Disharmony Score Ranges

| Score   | Meaning | What to Do |
|---------|---------|------------|
| **0.0 - 0.3** | ✨ Excellent | Nothing! Code is semantically perfect |
| **0.3 - 0.5** | ✅ Harmonious | Minor issues, mostly good |
| **0.5 - 0.8** | ⚠️ Medium | Review function name or implementation |
| **0.8+** | 🚨 High | Significant mismatch - needs attention |

### Common Issues Detected

**1. Get vs Delete Mismatch**
```python
def get_user(user_id):
    db.delete_user(user_id)  # ❌ Name says "get" but code "deletes"
    return None
```
**Score:** ~1.2 (High disharmony)  
**Fix:** Rename to `delete_user()` or change implementation

**2. Check vs Modify Mismatch**
```python
def check_valid(data):
    data.save()  # ❌ Name says "check" but code "modifies"
    return True
```
**Score:** ~0.8 (Medium-high disharmony)  
**Fix:** Rename to `validate_and_save()` or split into two functions

**3. Good Example (Harmonious)**
```python
def calculate_total(items):
    return sum(item.price for item in items)  # ✅ Perfect match
```
**Score:** ~0.2 (Excellent)

---

## 🎨 The LJPW Framework

### Four Semantic Dimensions

**Love (L) - Pink**
- **Represents:** Care, connection, communication, user-focus
- **Keywords:** help, support, notify, inform, share, welcome
- **Example:** `notify_user()`, `help_with_task()`

**Justice (J) - Yellow**
- **Represents:** Structure, validation, consistency, rules
- **Keywords:** validate, verify, check, ensure, enforce, audit
- **Example:** `validate_email()`, `check_permissions()`

**Power (P) - Red**
- **Represents:** Action, execution, transformation, force
- **Keywords:** create, delete, update, execute, build, save
- **Example:** `delete_user()`, `create_account()`

**Wisdom (W) - Blue**
- **Represents:** Analysis, insight, computation, patterns
- **Keywords:** analyze, calculate, evaluate, predict, optimize
- **Example:** `calculate_tax()`, `analyze_sentiment()`

### Natural Equilibrium

The "ideal" balance for healthy code:
- **Love:** 0.62 (62%)
- **Justice:** 0.41 (41%)
- **Power:** 0.72 (72%)
- **Wisdom:** 0.69 (69%)

Your code doesn't need to match exactly, but extreme imbalances may indicate issues.

---

## 💡 Use Cases

### 1. Code Review
**Before merging a PR:**
```
1. Copy the new/changed functions
2. Paste into harmonizer
3. Check for semantic issues
4. Comment on PR if disharmony found
```

### 2. Learning Tool
**Teaching good naming:**
```
1. Show students a poorly named function
2. Analyze together
3. Discuss why it's disharmonious
4. Refactor and re-analyze
```

### 3. Refactoring Guide
**Cleaning legacy code:**
```
1. Analyze entire file
2. Sort by disharmony score
3. Start with highest scores
4. Rename or split functions
5. Re-analyze to verify improvement
```

### 4. Daily Development
**While writing code:**
```
1. Write a new function
2. Quick check in harmonizer
3. Adjust name if needed
4. Build better habits over time
```

---

## 🔧 Technical Details

### How It Works

1. **Parsing**: Extracts function definitions using regex
2. **Vocabulary Analysis**: Matches words to LJPW dimensions
3. **Semantic Distance**: Calculates coordinate differences
4. **Mismatch Detection**: Identifies contradictory patterns
5. **Scoring**: Combines distance and specific mismatches

### Browser Compatibility

- ✅ **Chrome/Edge:** Fully supported
- ✅ **Firefox:** Fully supported
- ✅ **Safari:** Fully supported
- ✅ **Mobile:** Responsive, works on phones/tablets

### File Size

- **HTML file:** ~30 KB (tiny!)
- **Chart.js (CDN):** ~200 KB (cached after first load)
- **Total first load:** ~230 KB
- **Subsequent loads:** Instant (everything cached)

### Privacy & Security

- ✅ **No server required** - Runs entirely in browser
- ✅ **No data uploaded** - Code never leaves your computer
- ✅ **No tracking** - No analytics, no cookies
- ✅ **No account needed** - Just open and use
- ✅ **Works offline** - After first load, internet not required

---

## 🎓 Tips & Best Practices

### Getting Accurate Results

**DO:**
- ✅ Analyze individual functions or small files
- ✅ Use descriptive function names
- ✅ Include docstrings for better context
- ✅ Compare multiple versions to track improvement

**DON'T:**
- ❌ Analyze entire large codebases (use CLI tool instead)
- ❌ Worry about false positives (use judgment)
- ❌ Expect 100% accuracy (it's a guide, not a rule)

### Interpreting Edge Cases

**Case 1: High score but code is fine**
- Maybe the function does multiple things (consider splitting)
- Or the name is vague (consider being more specific)

**Case 2: Low score but code has issues**
- The name might match what it does, but what it does might be wrong!
- Harmonizer checks semantic alignment, not correctness

**Case 3: Utilities and helpers**
- Generic names like `process()` or `handle()` may score poorly
- This is intentional - vague names are semantically unclear

---

## 🚀 Keyboard Shortcuts

- **Ctrl/Cmd + Enter**: Analyze code (when textarea focused)
- **Ctrl/Cmd + K**: Clear code
- **Ctrl/Cmd + L**: Load simple example

*(Note: These need to be implemented in a future version)*

---

## 📦 Customization

### Hosting Your Own Version

**On GitHub Pages:**
1. Fork the repository
2. Enable GitHub Pages
3. Access at `https://yourusername.github.io/python-code-harmonizer/harmonizer.html`

**On Your Own Server:**
1. Download `harmonizer.html`
2. Upload to any web server
3. No backend needed - it's just a static file!

**Embed in Your Site:**
```html
<iframe 
    src="path/to/harmonizer.html" 
    width="100%" 
    height="800px"
    frameborder="0">
</iframe>
```

### Customizing Colors/Theme

Edit the CSS variables in the HTML file:
```css
:root {
    --bg-dark: #0f172a;      /* Background color */
    --accent: #38bdf8;       /* Primary accent */
    --love: #f472b6;         /* Love dimension color */
    /* ... etc ... */
}
```

### Adding Your Own Examples

Find the `examples` object in the JavaScript section:
```javascript
const examples = {
    simple: `def my_function():
        pass`,
    // Add your own here
    myexample: `def custom_example():
        print("Hello!")`
};
```

Then add a button:
```html
<button class="example-btn" onclick="loadExample('myexample')">
    My Example
</button>
```

---

## 🐛 Troubleshooting

### "No functions found"
**Problem:** Analysis returns no results

**Solutions:**
- Make sure you have `def function_name():` declarations
- Check that your Python syntax is valid
- Try one of the example buttons first

### Chart doesn't show
**Problem:** Radar chart is blank

**Solutions:**
- Make sure you're connected to internet (first load)
- Check browser console for errors
- Try refreshing the page

### Unexpected scores
**Problem:** Function scores don't make sense

**Solutions:**
- Remember this is a simplified implementation
- For full accuracy, use the CLI tool
- Consider the function's context
- It's a guide, not absolute truth

### File won't drop
**Problem:** Drag-and-drop not working

**Solutions:**
- Make sure it's a `.py` file
- Try dragging onto the textarea specifically
- Alternatively, copy-paste the code instead

---

## 📚 Further Reading

- **Philosophy:** See `docs/PHILOSOPHY.md` for the theory behind LJPW
- **Tutorial:** See `docs/TUTORIAL.md` for step-by-step examples
- **CLI Tool:** Use `python harmonizer/main.py` for full-featured analysis
- **API:** See `docs/API.md` for programmatic usage

---

## 🤝 Contributing

Want to improve the web app?

**Easy improvements:**
- Better Python parsing
- More example code
- Additional visualizations
- Keyboard shortcuts
- Export functionality (PDF/JSON)
- Dark/light theme toggle

**Advanced improvements:**
- Integrate actual Pyodide for 100% accuracy
- Multi-file analysis
- Historical tracking (localStorage)
- Share results via URL

See `CONTRIBUTING.md` for guidelines.

---

## 📄 License

MIT License - Free for everyone to use, modify, and distribute!

```
Copyright (c) 2024 Python Code Harmonizer Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## ❤️ Support

**Found a bug?** Open an issue on GitHub  
**Have a question?** Check the FAQ or start a discussion  
**Love the tool?** Give us a star ⭐ on GitHub!

---

**Happy Harmonizing! May your code's intent and execution always align.** 🎯✨
