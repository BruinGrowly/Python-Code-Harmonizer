# Python Code Harmonizer - API Reference

## Table of Contents

1. [Overview](#overview)
2. [Installation for Programmatic Use](#installation-for-programmatic-use)
3. [Quick Start](#quick-start)
4. [Main Harmonizer API](#main-harmonizer-api)
5. [DIVE-V2 Engine API](#dive-v2-engine-api)
6. [AST Parser API](#ast-parser-api)
7. [Data Structures](#data-structures)
8. [Integration Examples](#integration-examples)
9. [Error Handling](#error-handling)

---

## Overview

Python Code Harmonizer can be used as a library for programmatic analysis of Python code.

**Use cases:**
- Automated code review tools
- IDE integrations
- CI/CD pipeline checks
- Custom analysis workflows
- Batch processing of codebases

---

## Installation for Programmatic Use

**Standard installation:**
```bash
pip install .
```

**Editable installation (for development):**
```bash
pip install -e .
```

**Import in your code:**
```python
# High-level API
from src.harmonizer.main import PythonCodeHarmonizer

# Low-level API
from src.divine_invitation_engine_V2 import (
    DivineInvitationSemanticEngine,
    Coordinates,
    SemanticResult
)
from src.ast_semantic_parser import AST_Semantic_Parser
```

---

## Quick Start

**Analyze a single file:**
```python
from src.harmonizer.main import PythonCodeHarmonizer

# Initialize
harmonizer = PythonCodeHarmonizer()

# Analyze
report = harmonizer.analyze_file("mycode.py")

# Process results
for function_name, disharmony_score in report.items():
    if disharmony_score > 0.5:
        print(f"{function_name}: DISHARMONY (Score: {disharmony_score:.2f})")
```

**Analyze multiple files:**
```python
import glob

harmonizer = PythonCodeHarmonizer()

for filepath in glob.glob("src/**/*.py", recursive=True):
    report = harmonizer.analyze_file(filepath)
    if any(score > 0.8 for score in report.values()):
        print(f"High disharmony in: {filepath}")
```

---

## Main Harmonizer API

### PythonCodeHarmonizer

**Location:** `src.harmonizer.main`

**Purpose:** High-level interface for code harmony analysis

#### Constructor

```python
PythonCodeHarmonizer(disharmony_threshold: float = 0.5)
```

**Parameters:**
- `disharmony_threshold` (float, optional): Threshold above which functions are flagged as disharmonious. Default: 0.5

**Example:**
```python
# Strict threshold
harmonizer = PythonCodeHarmonizer(disharmony_threshold=0.3)

# Lenient threshold
harmonizer = PythonCodeHarmonizer(disharmony_threshold=0.8)
```

#### Methods

##### analyze_file()

```python
def analyze_file(self, file_path: str) -> Dict[str, float]
```

**Purpose:** Analyze a Python file for semantic harmony

**Parameters:**
- `file_path` (str): Absolute or relative path to Python file

**Returns:**
- `Dict[str, float]`: Dictionary mapping function names to disharmony scores

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `SyntaxError`: If file contains invalid Python syntax

**Example:**
```python
harmonizer = PythonCodeHarmonizer()

try:
    report = harmonizer.analyze_file("src/mymodule.py")

    for func_name, score in report.items():
        print(f"{func_name}: {score:.2f}")

except FileNotFoundError:
    print("File not found")
except SyntaxError as e:
    print(f"Syntax error on line {e.lineno}")
```

##### print_report()

```python
def print_report(self, harmony_report: Dict[str, float]) -> None
```

**Purpose:** Format and print harmony report to stdout

**Parameters:**
- `harmony_report` (Dict[str, float]): Output from `analyze_file()`

**Returns:**
- None (prints to stdout)

**Example:**
```python
harmonizer = PythonCodeHarmonizer()
report = harmonizer.analyze_file("mycode.py")
harmonizer.print_report(report)
```

**Output format:**
```
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
check_permissions            | !! DISHARMONY (Score: 0.78)
get_user                     | ✓ HARMONIOUS
```

#### Attributes

```python
harmonizer.engine               # DivineInvitationSemanticEngine instance
harmonizer.parser              # AST_Semantic_Parser instance
harmonizer.disharmony_threshold  # float
```

---

## DIVE-V2 Engine API

### DivineInvitationSemanticEngine

**Location:** `src.divine_invitation_engine_V2`

**Purpose:** Core semantic analysis engine

#### Constructor

```python
DivineInvitationSemanticEngine()
```

**Example:**
```python
from src.divine_invitation_engine_V2 import DivineInvitationSemanticEngine

engine = DivineInvitationSemanticEngine()
```

#### Methods

##### perform_ice_analysis()

```python
def perform_ice_analysis(
    self,
    intent_words: List[str],
    context_words: List[str],
    execution_words: List[str]
) -> Dict
```

**Purpose:** Perform Intent-Context-Execution framework analysis

**Parameters:**
- `intent_words` (List[str]): Concepts representing intent
- `context_words` (List[str]): Concepts representing context
- `execution_words` (List[str]): Concepts representing execution

**Returns:**
- `Dict` containing:
  - `ice_components`: Intent, Context, Execution results
  - `ice_metrics`: ICE coherence, balance, disharmony scores
  - `ice_harmony_level`: String classification

**Example:**
```python
engine = DivineInvitationSemanticEngine()

result = engine.perform_ice_analysis(
    intent_words=["get", "information"],
    context_words=["user", "database"],
    execution_words=["delete", "remove"]
)

print(f"Intent-Execution disharmony: {result['ice_metrics']['intent_execution_disharmony']:.2f}")
print(f"Harmony level: {result['ice_harmony_level']}")
```

##### analyze_text()

```python
def analyze_text(self, text: str) -> SemanticResult
```

**Purpose:** Analyze text and return semantic coordinates

**Parameters:**
- `text` (str): Text to analyze

**Returns:**
- `SemanticResult` object with coordinates and metrics

**Example:**
```python
result = engine.analyze_text("get user information")

print(f"Coordinates: {result.coordinates}")
print(f"Distance from anchor: {result.distance_from_anchor:.2f}")
print(f"Concept count: {result.concept_count}")
```

##### perform_semantic_harmony_analysis()

```python
def perform_semantic_harmony_analysis(self, concepts: List[str]) -> SemanticResult
```

**Purpose:** Analyze list of concepts for semantic harmony

**Parameters:**
- `concepts` (List[str]): List of concept words

**Returns:**
- `SemanticResult` with cluster analysis

**Example:**
```python
result = engine.perform_semantic_harmony_analysis([
    "validate",
    "check",
    "verify"
])

print(f"Semantic clarity: {result.semantic_clarity:.2f}")
print(f"Harmonic cohesion: {result.harmonic_cohesion:.2f}")
```

##### get_distance()

```python
def get_distance(self, c1: Coordinates, c2: Coordinates) -> float
```

**Purpose:** Calculate Euclidean distance between two coordinate points

**Parameters:**
- `c1` (Coordinates): First coordinate
- `c2` (Coordinates): Second coordinate

**Returns:**
- `float`: Distance value

**Example:**
```python
from src.divine_invitation_engine_V2 import Coordinates

coord1 = Coordinates(love=0.2, justice=0.3, power=0.1, wisdom=0.4)
coord2 = Coordinates(love=0.3, justice=0.3, power=0.3, wisdom=0.1)

distance = engine.get_distance(coord1, coord2)
print(f"Distance: {distance:.2f}")
```

#### Attributes

```python
engine.ENGINE_VERSION        # str: "DIVE-V2 (Optimized Production)"
engine.ANCHOR_POINT          # Coordinates(1.0, 1.0, 1.0, 1.0)
engine.vocabulary           # VocabularyManager instance
engine.semantic_analyzer    # SemanticAnalyzer instance
engine.ice_analyzer         # ICEAnalyzer instance
```

---

### VocabularyManager

**Location:** `src.divine_invitation_engine_V2.VocabularyManager`

**Purpose:** Manages semantic vocabulary and keyword mappings

#### Methods

##### analyze_text()

```python
def analyze_text(self, text: str) -> Tuple[Coordinates, int]
```

**Purpose:** Convert text to semantic coordinates

**Parameters:**
- `text` (str): Text to analyze

**Returns:**
- `Tuple[Coordinates, int]`: (coordinates, concept_count)

**Example:**
```python
vocab = engine.vocabulary

coords, count = vocab.analyze_text("delete user from database")
print(f"Found {count} concepts")
print(f"Power dimension: {coords.power:.2f}")
```

##### get_distance()

```python
@staticmethod
def get_distance(c1: Coordinates, c2: Coordinates) -> float
```

**Purpose:** Static method for distance calculation

**Parameters:**
- `c1`, `c2` (Coordinates): Coordinate points

**Returns:**
- `float`: Euclidean distance

##### get_semantic_clarity()

```python
@staticmethod
def get_semantic_clarity(coords: Coordinates) -> float
```

**Purpose:** Calculate how clearly defined a concept is

**Parameters:**
- `coords` (Coordinates): Semantic coordinates

**Returns:**
- `float`: Clarity score (0.0 to 1.0)

**Example:**
```python
coords = Coordinates(0.9, 0.1, 0.0, 0.0)  # Very focused on Love
clarity = vocab.get_semantic_clarity(coords)
print(f"Clarity: {clarity:.2f}")  # High clarity (focused)

coords2 = Coordinates(0.25, 0.25, 0.25, 0.25)  # Balanced
clarity2 = vocab.get_semantic_clarity(coords2)
print(f"Clarity: {clarity2:.2f}")  # Lower clarity (diffuse)
```

#### Properties

```python
vocab.all_keywords  # Set[str]: All mapped keywords
```

---

## AST Parser API

### AST_Semantic_Parser

**Location:** `src.ast_semantic_parser`

**Purpose:** Parse Python AST to extract semantic concepts

#### Constructor

```python
AST_Semantic_Parser(vocabulary: Set[str])
```

**Parameters:**
- `vocabulary` (Set[str]): Set of known semantic keywords

**Example:**
```python
from src.ast_semantic_parser import AST_Semantic_Parser

vocab = engine.vocabulary.all_keywords
parser = AST_Semantic_Parser(vocabulary=vocab)
```

#### Methods

##### get_intent_concepts()

```python
def get_intent_concepts(
    self,
    function_name: str,
    docstring: Optional[str]
) -> List[str]
```

**Purpose:** Extract intent concepts from function name and docstring

**Parameters:**
- `function_name` (str): Name of the function
- `docstring` (Optional[str]): Function's docstring

**Returns:**
- `List[str]`: Semantic concepts representing intent

**Example:**
```python
intent = parser.get_intent_concepts(
    function_name="get_user_by_id",
    docstring="Retrieve user information from database"
)
print(intent)  # ['information', 'information', 'information']
```

##### get_execution_concepts()

```python
def get_execution_concepts(self, body: List[ast.AST]) -> List[str]
```

**Purpose:** Extract execution concepts from function body AST

**Parameters:**
- `body` (List[ast.AST]): List of AST nodes from function body

**Returns:**
- `List[str]`: Semantic concepts representing execution

**Example:**
```python
import ast

code = """
def example():
    db.delete(user_id)
    return None
"""

tree = ast.parse(code)
func_node = tree.body[0]  # FunctionDef

execution = parser.get_execution_concepts(func_node.body)
print(execution)  # ['force', 'information', 'wisdom', ...]
```

---

## Data Structures

### Coordinates

**Immutable 4D semantic coordinates**

```python
@dataclass(frozen=True)
class Coordinates:
    love: float
    justice: float
    power: float
    wisdom: float
```

**Usage:**
```python
from src.divine_invitation_engine_V2 import Coordinates

coords = Coordinates(
    love=0.2,
    justice=0.3,
    power=0.1,
    wisdom=0.4
)

print(coords.love)     # 0.2
print(coords)          # Coordinates(L=0.200, J=0.300, P=0.100, W=0.400)

# Immutable - this will raise error:
# coords.love = 0.5  # FrozenInstanceError
```

### SemanticResult

**Complete semantic analysis result**

```python
@dataclass
class SemanticResult:
    coordinates: Coordinates
    distance_from_anchor: float
    semantic_clarity: float
    concept_count: int
    confidence: float
    distances: Optional[List[float]] = None
    centroid: Optional[Coordinates] = None
    harmonic_cohesion: Optional[float] = None
```

**Usage:**
```python
result = engine.analyze_text("get user data")

print(f"Coordinates: {result.coordinates}")
print(f"Distance from (1,1,1,1): {result.distance_from_anchor:.2f}")
print(f"How clear: {result.semantic_clarity:.2f}")
print(f"Concepts found: {result.concept_count}")
print(f"Confidence: {result.confidence:.2f}")
```

### Dimension

**Semantic dimension enumeration**

```python
class Dimension(Enum):
    LOVE = "love"
    JUSTICE = "justice"
    POWER = "power"
    WISDOM = "wisdom"
    INTENT = "intent"
    CONTEXT = "context"
    EXECUTION = "execution"
    BENEVOLENCE = "benevolence"
```

**Usage:**
```python
from src.divine_invitation_engine_V2 import Dimension

dim = Dimension.LOVE
print(dim.value)  # "love"
```

---

## Integration Examples

### Example 1: Custom Threshold Analysis

```python
from src.harmonizer.main import PythonCodeHarmonizer
import sys

def analyze_with_custom_threshold(filepath, threshold):
    """Analyze file with custom threshold"""
    harmonizer = PythonCodeHarmonizer(disharmony_threshold=threshold)
    report = harmonizer.analyze_file(filepath)

    critical = {k: v for k, v in report.items() if v > threshold}

    if critical:
        print(f"Found {len(critical)} functions above threshold {threshold}")
        for func, score in critical.items():
            print(f"  - {func}: {score:.2f}")
        return False  # Failure
    return True  # Success

if __name__ == "__main__":
    success = analyze_with_custom_threshold(sys.argv[1], threshold=0.5)
    sys.exit(0 if success else 1)
```

### Example 2: Batch Analysis

```python
from src.harmonizer.main import PythonCodeHarmonizer
import glob
import json

def analyze_project(root_dir, output_file):
    """Analyze entire project and save results"""
    harmonizer = PythonCodeHarmonizer()
    results = {}

    for filepath in glob.glob(f"{root_dir}/**/*.py", recursive=True):
        try:
            report = harmonizer.analyze_file(filepath)
            results[filepath] = {
                "functions": len(report),
                "average_score": sum(report.values()) / len(report) if report else 0,
                "high_disharmony": [
                    {"name": k, "score": v}
                    for k, v in report.items()
                    if v > 0.8
                ]
            }
        except Exception as e:
            results[filepath] = {"error": str(e)}

    # Save to JSON
    with open(output_file, 'w') as f:
        json.dumps(results, f, indent=2)

    return results

# Usage
results = analyze_project("src/", "harmony_report.json")
```

### Example 3: Direct DIVE-V2 Usage

```python
from src.divine_invitation_engine_V2 import DivineInvitationSemanticEngine

def compare_function_names(name1, name2):
    """Compare semantic similarity of two function names"""
    engine = DivineInvitationSemanticEngine()

    result1 = engine.analyze_text(name1)
    result2 = engine.analyze_text(name2)

    distance = engine.get_distance(result1.coordinates, result2.coordinates)

    print(f"{name1} vs {name2}")
    print(f"  {name1}: {result1.coordinates}")
    print(f"  {name2}: {result2.coordinates}")
    print(f"  Distance: {distance:.2f}")
    print(f"  Similar: {distance < 0.5}")

# Usage
compare_function_names("get_user", "fetch_user")    # Should be similar
compare_function_names("get_user", "delete_user")   # Should be different
```

### Example 4: CI/CD Integration

```python
#!/usr/bin/env python
"""
CI/CD script to check code harmony
Exit code 0 = pass, 1 = fail
"""
from src.harmonizer.main import PythonCodeHarmonizer
import sys
import glob

def main():
    harmonizer = PythonCodeHarmonizer(disharmony_threshold=0.7)

    failures = []
    for filepath in glob.glob("src/**/*.py", recursive=True):
        report = harmonizer.analyze_file(filepath)
        for func_name, score in report.items():
            if score > 0.7:
                failures.append({
                    "file": filepath,
                    "function": func_name,
                    "score": score
                })

    if failures:
        print(f"❌ Harmony check failed: {len(failures)} functions")
        for failure in failures:
            print(f"  {failure['file']}::{failure['function']} ({failure['score']:.2f})")
        return 1

    print(f"✅ Harmony check passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Example 5: Custom Reporting

```python
from src.harmonizer.main import PythonCodeHarmonizer
import csv

def generate_csv_report(filepath, output_csv):
    """Generate CSV report of harmony analysis"""
    harmonizer = PythonCodeHarmonizer()
    report = harmonizer.analyze_file(filepath)

    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Function", "Score", "Status", "Severity"])

        for func_name, score in sorted(report.items(), key=lambda x: x[1], reverse=True):
            status = "DISHARMONY" if score > 0.5 else "HARMONIOUS"
            if score > 1.0:
                severity = "CRITICAL"
            elif score > 0.7:
                severity = "HIGH"
            elif score > 0.5:
                severity = "MEDIUM"
            else:
                severity = "LOW"

            writer.writerow([func_name, f"{score:.2f}", status, severity])

# Usage
generate_csv_report("src/mymodule.py", "harmony_report.csv")
```

---

## Error Handling

### Common Exceptions

**FileNotFoundError**
```python
try:
    report = harmonizer.analyze_file("nonexistent.py")
except FileNotFoundError:
    print("File not found")
```

**SyntaxError**
```python
try:
    report = harmonizer.analyze_file("invalid_syntax.py")
except SyntaxError as e:
    print(f"Syntax error on line {e.lineno}: {e.msg}")
```

**Empty Results**
```python
report = harmonizer.analyze_file("empty.py")
if not report:
    print("No functions found to analyze")
```

### Graceful Handling

```python
from src.harmonizer.main import PythonCodeHarmonizer

def safe_analyze(filepath):
    """Analyze file with comprehensive error handling"""
    harmonizer = PythonCodeHarmonizer()

    try:
        report = harmonizer.analyze_file(filepath)

        if not report:
            return {"status": "no_functions", "filepath": filepath}

        return {
            "status": "success",
            "filepath": filepath,
            "report": report
        }

    except FileNotFoundError:
        return {"status": "not_found", "filepath": filepath}

    except SyntaxError as e:
        return {
            "status": "syntax_error",
            "filepath": filepath,
            "line": e.lineno,
            "message": e.msg
        }

    except Exception as e:
        return {
            "status": "error",
            "filepath": filepath,
            "error": str(e)
        }

# Usage
result = safe_analyze("mycode.py")
if result["status"] == "success":
    print(f"Analyzed: {result['filepath']}")
else:
    print(f"Failed: {result['status']}")
```

---

## Best Practices

### 1. Reuse Harmonizer Instance

**Don't:**
```python
for file in files:
    harmonizer = PythonCodeHarmonizer()  # Creates new engine each time
    report = harmonizer.analyze_file(file)
```

**Do:**
```python
harmonizer = PythonCodeHarmonizer()  # Create once
for file in files:
    report = harmonizer.analyze_file(file)  # Reuse
```

### 2. Handle Errors Appropriately

**Always wrap file analysis in try/except**

### 3. Use Type Hints

```python
from typing import Dict, List
from src.harmonizer.main import PythonCodeHarmonizer

def analyze_files(filepaths: List[str]) -> Dict[str, Dict[str, float]]:
    """Type-hinted function"""
    harmonizer: PythonCodeHarmonizer = PythonCodeHarmonizer()
    results: Dict[str, Dict[str, float]] = {}

    for filepath in filepaths:
        results[filepath] = harmonizer.analyze_file(filepath)

    return results
```

### 4. Cache Results When Possible

```python
import pickle

def analyze_with_cache(filepath, cache_file):
    """Analyze with caching"""
    try:
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        harmonizer = PythonCodeHarmonizer()
        report = harmonizer.analyze_file(filepath)

        with open(cache_file, 'wb') as f:
            pickle.dump(report, f)

        return report
```

---

## Conclusion

The Python Code Harmonizer API provides:

**High-level interface** - `PythonCodeHarmonizer` for file analysis
**Low-level access** - `DIVE-V2` engine for custom semantic analysis
**Clear data structures** - Type-safe, immutable coordinates
**Extensible design** - Easy to integrate and customize

**For more information:**
- [User Guide](USER_GUIDE.md) - Usage patterns and workflows
- [Architecture](ARCHITECTURE.md) - Technical implementation details
- [Philosophy](PHILOSOPHY.md) - Theoretical foundations
- [Tutorial](TUTORIAL.md) - Hands-on examples

---

*"Clear APIs enable clear integration. Semantic harmony extends to code that uses the tool."* 💛⚓
