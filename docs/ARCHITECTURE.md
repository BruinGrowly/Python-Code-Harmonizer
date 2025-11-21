# Python Code Harmonizer - Architecture & Implementation

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Core Components](#core-components)
5. [Integration Points](#integration-points)
6. [Performance Considerations](#performance-considerations)
7. [Extension Guide](#extension-guide)
8. [Testing Strategy](#testing-strategy)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│              Python Code Harmonizer                 │
│                    (CLI Entry)                      │
└──────────────────────┬──────────────────────────────┘
                       │
            ┌──────────┴────────────┐
            │                       │
    ┌───────▼────────┐    ┌────────▼───────────┐
    │   Harmonizer   │    │  DIVE-V2 Engine    │
    │   Main (CLI)   │────│  (Semantic Core)   │
    └───────┬────────┘    └────────┬───────────┘
            │                      │
    ┌───────▼────────┐    ┌────────▼───────────┐
    │  AST Parser    │    │  Vocabulary Mgr    │
    │  (Rosetta      │    │  (Concept Maps)    │
    │   Stone)       │    └────────────────────┘
    └────────────────┘
```

### Technology Stack

**Core:**
- **Python 3.8+** (no external runtime dependencies)
- **ast** module (Python Abstract Syntax Tree parsing)
- **dataclasses** (immutable data structures)
- **typing** (type hints throughout)

**Development:**
- **pytest** (testing framework)
- **black** (code formatting)
- **flake8** (linting)
- **isort** (import sorting)

### Design Principles

1. **Zero runtime dependencies** - Uses only Python stdlib
2. **Deterministic analysis** - Same input = same output
3. **Fast performance** - Analyze typical function in < 10ms
4. **Clear separation** - Parser, Engine, CLI are distinct
5. **Type-safe** - Extensive type hints
6. **Immutable data** - Core data structures are frozen
7. **Testable** - High test coverage, clear interfaces

---

## Component Architecture

### Three-Layer Design

```
┌──────────────────────────────────────────────────┐
│  Layer 1: User Interface (CLI)                   │
│  - src/harmonizer/main.py                        │
│  - Command-line argument parsing                 │
│  - Report formatting and output                  │
└─────────────────┬────────────────────────────────┘
                  │
┌─────────────────▼────────────────────────────────┐
│  Layer 2: Analysis Orchestration                 │
│  - PythonCodeHarmonizer class                    │
│  - Coordinates Parser + Engine                   │
│  - ICE framework application                     │
└─────────────────┬────────────────────────────────┘
                  │
┌─────────────────▼────────────────────────────────┐
│  Layer 3: Semantic Core                          │
│  - DIVE-V2 Engine (semantic analysis)            │
│  - AST Parser (code → concepts)                  │
│  - Vocabulary mapping                            │
└──────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Key Classes |
|-----------|---------------|-------------|
| **CLI** | User interaction, file handling, output formatting | `run_cli()` |
| **Harmonizer** | Orchestration, coordination of analysis | `PythonCodeHarmonizer` |
| **DIVE-V2** | Semantic analysis, distance calculations | `DivineInvitationSemanticEngine` |
| **AST Parser** | Python AST → semantic concepts | `AST_Semantic_Parser` |
| **Vocabulary** | Word → coordinate mapping | `VocabularyManager` |

---

## Data Flow

### End-to-End Analysis Flow

```
        Python File
             │
             ▼
┌─────────────────────────────────┐
│  1. File Read                   │
│     Read Python source code     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  2. AST Parse                   │
│     Python ast.parse()          │
│     → AST tree                  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  3. For Each Function:          │
│                                 │
│  a) Extract INTENT              │
│     - Function name             │
│     - Docstring                 │
│     → List[concept_words]       │
│                                 │
│  b) Extract EXECUTION           │
│     - Walk AST body             │
│     - Identify operations       │
│     → List[concept_words]       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  4. Semantic Analysis           │
│     (DIVE-V2 Engine)            │
│                                 │
│  a) Map concepts to coords      │
│     intent_words → coords       │
│     execution_words → coords    │
│                                 │
│  b) Calculate distance          │
│     distance(intent, execution) │
│     → disharmony_score          │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  5. Report Generation           │
│     Format and display results  │
│     - Function name             │
│     - Disharmony score          │
│     - Status (✓ or !!)          │
└─────────────────────────────────┘
```

### Data Structures

**Key types flowing through the system:**

```python
# Core coordinate representation
@dataclass(frozen=True)
class Coordinates:
    love: float
    justice: float
    power: float
    wisdom: float

# Complete analysis result
@dataclass
class SemanticResult:
    coordinates: Coordinates
    distance_from_anchor: float
    semantic_clarity: float
    concept_count: int
    confidence: float
    # ... additional metrics

# Function-level harmony report
harmony_report: Dict[str, float]
# { "function_name": disharmony_score, ... }
```

---

## Core Components

### 1. DIVE-V2 Engine

**File:** `src/divine_invitation_engine_V2.py` (865 lines)

**Purpose:** Semantic analysis core - maps concepts to coordinates and calculates distances

#### Key Classes

**VocabularyManager**
```python
class VocabularyManager:
    """Maps keywords to semantic dimensions"""

    def __init__(self):
        self._keyword_map: Dict[str, Dimension]
        self._word_cache: Dict[str, Tuple[Coordinates, int]]
        self._build_complete_vocabulary()

    def analyze_text(text: str) -> Tuple[Coordinates, int]:
        """Convert text to semantic coordinates"""
        # 1. Check cache
        # 2. Extract words
        # 3. Map to dimensions
        # 4. Calculate centroid
        # 5. Return (coordinates, concept_count)
```

**Features:**
- 113 unique keywords mapped
- LRU caching for performance
- Handles unknown words gracefully
- Case-insensitive analysis

**SemanticAnalyzer**
```python
class SemanticAnalyzer:
    """Analyzes concept clusters and calculates metrics"""

    def analyze_concept_cluster(concepts: List[str]) -> SemanticResult:
        """Analyze list of concepts → unified result"""
        # 1. Get coordinates for each concept
        # 2. Calculate centroid
        # 3. Calculate distances
        # 4. Calculate harmony metrics
        # 5. Return complete result
```

**ICEAnalyzer**
```python
class ICEAnalyzer:
    """Performs Intent-Context-Execution analysis"""

    def analyze_ice(
        intent_words: List[str],
        context_words: List[str],
        execution_words: List[str]
    ) -> Dict:
        """Complete ICE framework analysis"""
        # 1. Analyze each component
        # 2. Calculate inter-component distances
        # 3. Calculate ICE metrics
        # 4. Determine harmony level
        # 5. Return complete ICE result
```

**DivineInvitationSemanticEngine**
```python
class DivineInvitationSemanticEngine:
    """Main facade - integrates all sub-engines"""

    def __init__(self):
        self.vocabulary = VocabularyManager()
        self.semantic_analyzer = SemanticAnalyzer(...)
        self.ice_analyzer = ICEAnalyzer(...)
        # ... other analyzers

    def perform_ice_analysis(...) -> Dict:
        """Primary entry point for harmonizer"""
```

**Key algorithms:**

**Distance calculation:**
```python
def get_distance(c1: Coordinates, c2: Coordinates) -> float:
    """Euclidean distance in 4D space"""
    return math.sqrt(
        (c1.love - c2.love) ** 2 +
        (c1.justice - c2.justice) ** 2 +
        (c1.power - c2.power) ** 2 +
        (c1.wisdom - c2.wisdom) ** 2
    )
```

**Semantic clarity:**
```python
def get_semantic_clarity(coords: Coordinates) -> float:
    """How clearly defined is this concept?"""
    dims = [coords.love, coords.justice, coords.power, coords.wisdom]
    mean = sum(dims) / len(dims)
    variance = sum((d - mean)**2 for d in dims) / len(dims)
    std_dev = math.sqrt(variance)
    return max(0.0, 1.0 - (std_dev / 0.5))
```

---

### 2. AST Semantic Parser

**File:** `src/ast_semantic_parser.py` (214 lines)

**Purpose:** "Rosetta Stone" - translates Python AST to semantic concepts

#### Architecture

**Extends ast.NodeVisitor:**
```python
class AST_Semantic_Parser(ast.NodeVisitor):
    """Walks AST and extracts semantic concepts"""

    def __init__(self, vocabulary: Set[str]):
        self.known_vocabulary = vocabulary
        self.intent_keyword_map = {...}  # Predefined mappings
        self._concepts_found: Set[str] = set()
```

**Two-phase operation:**

**Phase 1: Intent Extraction**
```python
def get_intent_concepts(
    function_name: str,
    docstring: Optional[str]
) -> List[str]:
    """Extract semantic concepts from name + docstring"""
    # 1. Split snake_case name
    # 2. Map words to concepts
    # 3. Parse docstring for additional concepts
    # 4. Return unified concept list
```

**Phase 2: Execution Extraction**
```python
def get_execution_concepts(body: List[ast.AST]) -> List[str]:
    """Extract semantic concepts from function body"""
    # 1. Walk AST using visitor pattern
    # 2. Each visit_* method extracts concepts
    # 3. Return all found concepts
```

#### AST Visitor Methods

**Key visitors:**

```python
def visit_Call(self, node: ast.Call):
    """Function calls → actions"""
    # db.delete() → "delete", "force"
    # api.query() → "query", "information"

def visit_If(self, node: ast.If):
    """Conditionals → logic"""
    # if condition: → "logic"

def visit_Try(self, node: ast.Try):
    """Error handling → logic + mercy"""
    # try/except → "logic", "mercy"

def visit_Return(self, node: ast.Return):
    """Returns → information"""
    # return value → "information", "wisdom"

def visit_For(self, node: ast.For):
    """Loops → process"""
    # for item in items: → "process"

def visit_Raise(self, node: ast.Raise):
    """Exceptions → power + force"""
    # raise Error() → "power", "force"
```

#### Mapping Strategy

**Intent keyword map:**
```python
{
    # WISDOM (Information, Truth)
    "get": "information",
    "read": "information",
    "query": "information",
    "calculate": "wisdom",
    "validate": "truth",

    # POWER (Action, Control)
    "set": "power",
    "create": "create",
    "delete": "force",
    "execute": "power",

    # JUSTICE (Order, Logic)
    "assert": "law",
    "check": "truth",
    "if": "logic",

    # LOVE (Unity, Connection)
    "add": "community",
    "join": "harmony",
    "merge": "togetherness",
}
```

---

### 3. LJPW Baselines

**File:** `harmonizer/ljpw_baselines.py`

**Purpose:** Mathematical foundations and reference points for LJPW framework

#### Key Features

**Numerical Equivalents**:
- L (Love): φ⁻¹ = 0.618034
- J (Justice): √2-1 = 0.414214  
- P (Power): e-2 = 0.718282
- W (Wisdom): ln(2) = 0.693147

**Reference Points**:
- Natural Equilibrium: (0.618, 0.414, 0.718, 0.693)
- Anchor Point: (1.0, 1.0, 1.0, 1.0)

**Coupling Matrix**: Defines how dimensions interact (amplify/constrain)

**New in v4.1**: Relationship validation methods
```python
# Validate coupling structure patterns
LJPWBaselines.validate_coupling_structure()
# → Checks Love amplifies, Power constrains, etc.

# Check scale-invariant proportions
LJPWBaselines.check_proportions(L, J, P, W)
# → Validates L:J:P:W ratios match Natural Equilibrium
```

---

### 4. Relationship Analyzer **[NEW]**

**File:** `harmonizer/relationship_analyzer.py`

**Purpose:** Validates LJPW relationship patterns and structural health

#### Core Insight

Based on the discovery: *"Relationships between constants are more important than constants themselves"*

This tool validates the **grammar of semantic interaction** - the patterns that define healthy LJPW systems.

#### Key Classes

**RelationshipAnalyzer**
```python
class RelationshipAnalyzer:
    """Analyzes whether a system exhibits healthy LJPW relationship patterns"""
    
    def check_proportions(L, J, P, W, tolerance=0.3):
        """Check if L:J:P:W ratios match Natural Equilibrium (scale-invariant)"""
        # Validates proportional relationships
        # Works at any scale
    
    def check_coupling_character(coupling_matrix):
        """Check if coupling exhibits expected patterns"""
        # Love amplifies (κ_L→* > 1)
        # Power constrains (κ_P→* < 1)
        # Justice supports Wisdom (κ_JW > κ_JP)
    
    def check_asymmetry(coupling_matrix):
        """Check if coupling is properly asymmetric"""
        # κ_ij ≠ κ_ji (giving ≠ receiving)
    
    def full_relationship_diagnostic(L, J, P, W, coupling_matrix=None):
        """Complete structural health analysis"""
        # Returns comprehensive diagnostic with recommendations
```

#### Usage Pattern

```python
from harmonizer.relationship_analyzer import analyze_system_relationships

# Analyze any system (at any scale)
result = analyze_system_relationships(
    L=50, J=30, P=70, W=65  # Any magnitude
)

print(f"Overall Health: {result['overall_health']:.0%}")
print(f"Proportions: {'✓' if result['health_scores']['proportions'] else '✗'}")
print(f"Love amplifies: {'✓' if result['health_scores']['love_amplifies'] else '✗'}")

for rec in result['recommendations']:
    print(f"  {rec}")
```

#### Health Checks

1. **Proportions** (scale-invariant)
   - L/J ≈ 1.49
   - P/J ≈ 1.73
   - W/J ≈ 1.67

2. **Coupling Character**
   - Love amplifies (generosity pattern)
   - Power constrains (restraint pattern)
   - Justice supports Wisdom

3. **Asymmetry**
   - Love gives more than receives
   - Power receives more than gives
   - Directional flow preserved

#### Output Example

```
Overall Health: 80%
Interpretation: Good: Most relationship patterns are healthy

Health Breakdown:
  ✗ proportions: 0% (L/P deviates by 74%)
  ✓ love_amplifies: 100%
  ✓ power_constrains: 100%
  ✓ justice_supports_wisdom: 100%
  ✓ asymmetry: 100%

Recommendations:
  ⚠️ Adjust proportions: L/P deviates from Natural Equilibrium
  ✓ Coupling structure is healthy
```

---

### 5. Harmonizer Main

**File:** `src/harmonizer/main.py` (197 lines)

**Purpose:** Orchestrates analysis and provides CLI

#### PythonCodeHarmonizer Class

```python
class PythonCodeHarmonizer:
    """Main application class"""

    def __init__(self, disharmony_threshold: float = 0.5):
        # Initialize DIVE-V2 engine
        self.engine = dive.DivineInvitationSemanticEngine()

        # Initialize AST parser with vocabulary
        self.parser = AST_Semantic_Parser(
            vocabulary=self.engine.vocabulary.all_keywords
        )

        self.disharmony_threshold = disharmony_threshold

    def analyze_file(file_path: str) -> Dict[str, float]:
        """Analyze Python file → harmony report"""
        # 1. Read file
        # 2. Parse to AST
        # 3. For each function:
        #    a) Extract intent
        #    b) Extract execution
        #    c) Perform ICE analysis
        #    d) Store disharmony score
        # 4. Return {function_name: score}

    def print_report(harmony_report: Dict[str, float]):
        """Format and display results"""
        # 1. Sort by severity
        # 2. Format table
        # 3. Print with status indicators
```

#### CLI Entry Point

```python
def run_cli():
    """Command-line interface"""
    # 1. Parse command-line arguments
    # 2. Initialize harmonizer
    # 3. For each file:
    #    a) Analyze
    #    b) Print report
    # 4. Exit

# Entry point in pyproject.toml:
# [project.scripts]
# harmonizer = "src.harmonizer.main:run_cli"
```

---

## Integration Points

### As a Library

**Programmatic usage:**

```python
from src.harmonizer.main import PythonCodeHarmonizer

# Initialize
harmonizer = PythonCodeHarmonizer(disharmony_threshold=0.5)

# Analyze single file
report = harmonizer.analyze_file("mycode.py")

# Process results
for function_name, score in report.items():
    if score > 0.8:
        print(f"High disharmony in {function_name}: {score:.2f}")
```

### With DIVE-V2 Directly

**Lower-level access:**

```python
from src.divine_invitation_engine_V2 import DivineInvitationSemanticEngine

# Initialize engine
engine = DivineInvitationSemanticEngine()

# Analyze concepts
result = engine.perform_semantic_harmony_analysis(
    concepts=["get", "user", "information"]
)

print(f"Coordinates: {result.coordinates}")
print(f"Distance from anchor: {result.distance_from_anchor}")

# ICE analysis
ice_result = engine.perform_ice_analysis(
    intent_words=["get", "information"],
    context_words=["user", "database"],
    execution_words=["query", "return"]
)

print(f"Intent-Execution disharmony: {ice_result['ice_metrics']['intent_execution_disharmony']}")
```

### Extension Points

**Custom vocabulary:**
```python
# Extend VocabularyManager
class CustomVocabularyManager(VocabularyManager):
    def _build_complete_vocabulary(self):
        super()._build_complete_vocabulary()
        # Add domain-specific keywords
        self._keyword_map["authenticate"] = Dimension.JUSTICE
        self._keyword_map["authorize"] = Dimension.POWER
```

**Custom AST visitors:**
```python
# Extend AST_Semantic_Parser
class CustomASTParser(AST_Semantic_Parser):
    def visit_Async(self, node):
        """Handle async operations"""
        self._concepts_found.add("async")
        self._concepts_found.add("concurrent")
        self.generic_visit(node)
```

**Custom thresholds:**
```python
harmonizer = PythonCodeHarmonizer(
    disharmony_threshold=0.3  # Stricter
)
```

---

## Performance Considerations

### Optimizations

**1. Vocabulary Caching**
```python
# VocabularyManager caches text analysis results
self._word_cache: Dict[str, Tuple[Coordinates, int]] = {}

# Repeated analysis of same text → instant
```

**2. Efficient Distance Calculation**
```python
# Single sqrt operation, vectorized
def get_distance(c1, c2):
    return math.sqrt(
        sum((a - b)**2 for a, b in zip(c1, c2))
    )
```

**3. Lazy Evaluation**
```python
# Only analyze functions (not classes, modules, etc.)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        # Only process functions
```

### Performance Characteristics

**Typical performance:**
- Small file (5 functions): < 50ms
- Medium file (50 functions): < 500ms
- Large file (500 functions): < 5s

**Memory usage:**
- Vocabulary: ~50KB
- Cache: Grows with unique concepts analyzed
- AST: Proportional to file size

**Bottlenecks:**
1. File I/O (reading Python files)
2. AST parsing (Python stdlib overhead)
3. Walking AST (linear in function count)

**Scalability:**
- Analyze files in parallel for large codebases
- Cache analysis results across runs (future enhancement)
- Incremental analysis (only changed files)

---

## Extension Guide

### Adding New Semantic Dimensions

**Currently:** 4 dimensions (L, J, P, W)

**To add a 5th dimension:**

1. **Update Coordinates:**
```python
@dataclass(frozen=True)
class Coordinates:
    love: float
    justice: float
    power: float
    wisdom: float
    creativity: float  # NEW
```

2. **Update Dimension enum:**
```python
class Dimension(Enum):
    LOVE = "love"
    JUSTICE = "justice"
    POWER = "power"
    WISDOM = "wisdom"
    CREATIVITY = "creativity"  # NEW
```

3. **Update vocabulary:**
```python
base_vocab = {
    # ... existing
    Dimension.CREATIVITY: {
        "create", "invent", "design", "innovate"
    }
}
```

4. **Update distance calculations:**
```python
def get_distance(c1, c2):
    return math.sqrt(
        (c1.love - c2.love)**2 +
        # ... existing
        (c1.creativity - c2.creativity)**2  # NEW
    )
```

### Adding New AST Patterns

**To detect new code patterns:**

```python
class AST_Semantic_Parser(ast.NodeVisitor):
    # ... existing visitors

    def visit_AsyncFunctionDef(self, node):
        """Detect async functions"""
        self._concepts_found.add("async")
        self._concepts_found.add("concurrent")
        # Continue walking
        self.generic_visit(node)

    def visit_With(self, node):
        """Detect context managers"""
        self._concepts_found.add("context")
        self._concepts_found.add("manage")
        self.generic_visit(node)
```

### Custom Output Formats

**JSON output example:**

```python
import json

def print_report_json(harmony_report: Dict[str, float]):
    """Output as JSON"""
    output = {
        "analysis_version": "1.1",
        "timestamp": datetime.now().isoformat(),
        "results": [
            {
                "function": name,
                "disharmony_score": score,
                "status": "DISHARMONY" if score > 0.5 else "HARMONIOUS"
            }
            for name, score in harmony_report.items()
        ]
    }
    print(json.dumps(output, indent=2))
```

### Plugin Architecture (Future)

**Planned extension mechanism:**

```python
class HarmonizerPlugin:
    """Base class for plugins"""

    def before_analysis(self, file_path: str):
        """Hook: before file analysis"""
        pass

    def after_analysis(self, report: Dict[str, float]):
        """Hook: after file analysis"""
        pass

    def custom_report(self, report: Dict[str, float]) -> str:
        """Hook: custom reporting"""
        return None
```

---

## Testing Strategy

### Test Structure

```
tests/
├── test_engine.py       # DIVE-V2 engine tests
├── test_parser.py       # AST parser tests
└── test_harmonizer.py   # Integration tests
```

### Test Coverage

**DIVE-V2 Engine (test_engine.py):**
- Engine initialization
- Vocabulary mapping
- Text analysis (single concepts, mixed, unknown)
- Distance calculations
- Semantic clarity
- Cluster analysis
- ICE framework analysis

**AST Parser (test_parser.py):**
- Intent extraction from function names
- Intent extraction from docstrings
- Execution extraction from function calls
- Execution extraction from control flow
- Execution extraction from error handling

**Harmonizer (test_harmonizer.py):**
- End-to-end file analysis
- Error handling (syntax errors, empty files)
- Report generation
- Multiple file analysis

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_engine.py

# With coverage
pytest --cov=src --cov-report=html

# Verbose
pytest -v
```

### Test Patterns

**Unit tests:**
```python
def test_vocabulary_mapping():
    """Test specific word → coordinate mapping"""
    vocab = VocabularyManager()
    coords, count = vocab.analyze_text("get user")
    assert count > 0
    assert coords.wisdom > 0.5  # "get" is wisdom-focused
```

**Integration tests:**
```python
def test_end_to_end_analysis():
    """Test complete analysis flow"""
    harmonizer = PythonCodeHarmonizer()

    # Create test file
    code = '''
def get_user(id):
    db.delete(id)  # Disharmony!
'''
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
        f.write(code)
        f.flush()

        report = harmonizer.analyze_file(f.name)

    assert "get_user" in report
    assert report["get_user"] > 0.8  # High disharmony
```

---

## Conclusion

Python Code Harmonizer is architected as:

**Three clear layers** - UI, Orchestration, Core
**Zero runtime dependencies** - Pure Python stdlib
**Deterministic and fast** - Consistent, performant analysis
**Extensible design** - Clear extension points
**Well-tested** - Comprehensive test coverage

**Key technical achievements:**

1. **Semantic analysis without ML** - Deterministic, explainable
2. **AST-based extraction** - Leverages Python's own parser
3. **Mathematical rigor** - Clear geometric interpretation
4. **Production quality** - Error handling, optimization, tests

**For more information:**
- [Philosophy](PHILOSOPHY.md) - Theoretical foundation
- [User Guide](USER_GUIDE.md) - How to use
- [Tutorial](TUTORIAL.md) - Hands-on examples
- [API Reference](API.md) - Programmatic usage

---

*"Good architecture serves meaning. This architecture serves semantic harmony."* 💛⚓
