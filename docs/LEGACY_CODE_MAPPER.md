# Legacy Code Mapper: LJPW-Based Codebase Understanding

**Challenge:** "Legacy code's real complexity still fights back"

**Response:** Use LJPW to create a **semantic map** of the entire codebase that shows:
1. Where semantic drift accumulated
2. Which modules have contradictory purposes
3. Where refactoring will have maximum impact
4. The actual architecture (not the documented one)

---

## The Core Insight

**Legacy code is hard to understand because:**
- Function names stopped matching implementations (semantic drift)
- Modules grew beyond their original purpose (scope creep)
- Architecture dissolved into spaghetti (lost boundaries)
- No one knows what anything actually does anymore

**LJPW reveals:**
- The **true semantic structure** of the code
- Where boundaries **should** be (natural clusters in LJPW space)
- Which files are **semantically incoherent** (high internal disharmony)
- The **semantic distance** between what code says and what it does

---

## Feature 1: Semantic Codebase Map

### The Visualization

Generate a 3D visualization showing every file/module in LJPW space:

```
             WISDOM (W)
                 △
                /|\
               / | \
              /  |  \
         auth.py |   \
            /    |    \
           /  db.py    api.py
          /      |      \
    JUSTICE -----+------ POWER
          \      |      /
           \     |     /
         cache.py|    /
             \   |   /
              \  |  /
               \ | /
                \|/
                 ▽
              LOVE (L)
```

**What this shows:**
- **Clusters** = Modules that work together semantically
- **Outliers** = Files that don't fit the architecture
- **Distance** = How semantically similar/different modules are
- **Drift** = How far modules moved from their original purpose

### Implementation

```python
# harmonizer/legacy_mapper.py

class LegacyCodeMapper:
    def __init__(self, codebase_path):
        self.harmonizer = PythonCodeHarmonizer()
        self.codebase_path = codebase_path
        self.file_coordinates = {}  # file -> avg LJPW coordinates
        self.semantic_clusters = []

    def analyze_codebase(self):
        """Analyze entire codebase and compute semantic map"""
        for file in glob_python_files(self.codebase_path):
            functions = self.harmonizer.analyze_file(file)

            # Average coordinates of all functions in file
            avg_coords = self._compute_file_coordinates(functions)
            self.file_coordinates[file] = avg_coords

        # Find natural semantic clusters
        self.semantic_clusters = self._cluster_by_semantics()

        return self.generate_report()

    def _compute_file_coordinates(self, functions):
        """Compute average semantic coordinates for a file"""
        all_coords = []
        for func in functions:
            exec_coords = func['execution_coordinates']
            all_coords.append(exec_coords)

        # Average across all functions
        return {
            'love': mean([c.love for c in all_coords]),
            'justice': mean([c.justice for c in all_coords]),
            'power': mean([c.power for c in all_coords]),
            'wisdom': mean([c.wisdom for c in all_coords])
        }

    def _cluster_by_semantics(self):
        """Find natural semantic clusters using K-means in LJPW space"""
        from sklearn.cluster import KMeans

        # Convert to matrix
        coords_matrix = [
            [c['love'], c['justice'], c['power'], c['wisdom']]
            for c in self.file_coordinates.values()
        ]

        # Find optimal clusters (elbow method)
        optimal_k = self._find_optimal_clusters(coords_matrix)

        # Cluster
        kmeans = KMeans(n_clusters=optimal_k)
        labels = kmeans.fit_predict(coords_matrix)

        # Group files by cluster
        clusters = {}
        for file, label in zip(self.file_coordinates.keys(), labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(file)

        return clusters

    def generate_report(self):
        """Generate comprehensive legacy code report"""
        return {
            'semantic_map': self.file_coordinates,
            'natural_clusters': self.semantic_clusters,
            'architectural_smells': self._detect_architectural_smells(),
            'refactoring_opportunities': self._find_refactoring_targets(),
            'semantic_complexity_score': self._compute_complexity(),
        }
```

### Output: Semantic Codebase Report

```
======================================================================
LEGACY CODE SEMANTIC MAP
Codebase: /path/to/legacy-app
Files analyzed: 247
======================================================================

NATURAL SEMANTIC CLUSTERS (What the code ACTUALLY is):
----------------------------------------------------------------------

📚 CLUSTER 1: Information Layer (WISDOM-dominant)
  Coordinates: L=0.1, J=0.2, P=0.1, W=0.6

  Files (23):
  - data/queries.py
  - data/readers.py
  - cache/retrieval.py
  - api/getters.py
  ...

  PURPOSE: Data retrieval and information access
  COHERENCE: 0.85 (HIGH - cluster makes semantic sense)

⚖️  CLUSTER 2: Validation Layer (JUSTICE-dominant)
  Coordinates: L=0.1, J=0.7, P=0.1, W=0.1

  Files (18):
  - auth/validators.py
  - security/checkers.py
  - data/integrity.py
  ...

  PURPOSE: Validation and correctness enforcement
  COHERENCE: 0.92 (VERY HIGH - well-defined boundary)

⚡ CLUSTER 3: Execution Layer (POWER-dominant)
  Coordinates: L=0.1, J=0.2, P=0.6, W=0.1

  Files (31):
  - core/processors.py
  - data/writers.py
  - jobs/executors.py
  ...

  PURPOSE: State modification and execution
  COHERENCE: 0.78 (GOOD)

💛 CLUSTER 4: Integration Layer (LOVE-dominant)
  Coordinates: L=0.6, J=0.1, P=0.2, W=0.1

  Files (19):
  - api/endpoints.py
  - notifications/senders.py
  - integrations/connectors.py
  ...

  PURPOSE: System integration and communication
  COHERENCE: 0.81 (HIGH)

⚠️  OUTLIERS (Semantically incoherent):
  - utils/helpers.py (L=0.25, J=0.25, P=0.25, W=0.25)
    → Generic utility file, no clear purpose

  - core/manager.py (L=0.3, J=0.2, P=0.4, W=0.1)
    → Mixed concerns, should be split

  - legacy/adapter.py (L=0.4, J=0.1, P=0.3, W=0.2)
    → Bridge between old/new arch, semantic confusion

======================================================================
ARCHITECTURAL SMELLS DETECTED
======================================================================

🚨 SMELL 1: Semantic Boundary Violation
  File: api/endpoints.py (LOVE cluster)
  Contains: 12 POWER-dominant functions

  Problem: API layer directly modifies database (architectural violation)
  Functions:
  - create_user_and_send_email() - Should be split
  - validate_and_save() - Mixing concerns

  Impact: HIGH
  Recommendation: Extract business logic to separate POWER layer

🚨 SMELL 2: God Object
  File: core/manager.py
  Semantic spread: All four dimensions present equally

  Problem: File has no coherent purpose, does everything
  Functions span:
  - WISDOM: get_config(), load_settings()
  - JUSTICE: validate_state(), check_permissions()
  - POWER: execute_job(), update_cache()
  - LOVE: send_notification(), connect_service()

  Impact: CRITICAL
  Recommendation: Split into 4 focused modules

🚨 SMELL 3: Semantic Drift Accumulation
  File: data/repository.py
  Original purpose: WISDOM (data access)
  Current state: Mixed (W=0.4, P=0.4, J=0.2)

  Problem: Repository grew to include business logic
  Drift over time:
  - Started: Pure data access (W=0.9)
  - v2.0: Added validation (W=0.7, J=0.3)
  - v3.5: Added state modification (W=0.5, P=0.4, J=0.1)
  - Current: Lost original purpose

  Impact: HIGH
  Recommendation: Refactor back to pure data access

======================================================================
REFACTORING OPPORTUNITIES (Sorted by Impact)
======================================================================

1. Split core/manager.py into semantic layers
   Complexity reduction: 68%
   Estimated LOC change: 450 lines
   Risk: MEDIUM

   Suggested split:
   - manager_config.py (WISDOM)
   - manager_validation.py (JUSTICE)
   - manager_executor.py (POWER)
   - manager_notifications.py (LOVE)

2. Extract business logic from API layer
   Architecture improvement: 45%
   Estimated LOC change: 320 lines
   Risk: LOW

   Create new service layer with proper POWER functions

3. Restore data/repository.py to original purpose
   Semantic clarity: 72%
   Estimated LOC change: 180 lines
   Risk: MEDIUM

   Move business logic to separate service modules

======================================================================
SEMANTIC COMPLEXITY METRICS
======================================================================

Overall Codebase Health: 67/100 (MODERATE)

Breakdown:
- Semantic Coherence: 72/100 (GOOD)
  → Most files have clear purpose within clusters

- Architectural Clarity: 58/100 (MODERATE)
  → Some boundary violations, needs cleanup

- Semantic Drift: 45/100 (CONCERNING)
  → Significant drift in 23% of files

- Disharmony Score: 0.62 (MEDIUM)
  → Average across all functions

Trend Analysis:
- Drift accelerated after v2.0 (2019)
- Worst areas: core/ and api/ directories
- Best maintained: security/ and data/readers.py

======================================================================
RECOMMENDATIONS
======================================================================

Priority 1 (Next Sprint):
✓ Refactor core/manager.py (god object)
✓ Extract business logic from API layer

Priority 2 (Next Quarter):
✓ Create proper service layer (POWER cluster)
✓ Restore semantic boundaries in data access

Priority 3 (Long-term):
✓ Reorganize directory structure to match semantic clusters
✓ Establish semantic guidelines for new code
✓ Add semantic harmony checks to CI/CD

======================================================================
```

---

## Feature 2: Function Genealogy Tracker

Track how functions evolved over time and where semantic drift occurred.

### The Analysis

```python
class FunctionGenealogy:
    def trace_semantic_drift(self, function_name, git_history):
        """Trace how function semantics changed over time"""
        commits = git.log(function_name)

        history = []
        for commit in commits:
            # Analyze function at this commit
            code = git.show(commit, function_name)
            coords = self.harmonizer.analyze_function(code)

            history.append({
                'commit': commit,
                'date': commit.date,
                'coordinates': coords,
                'author': commit.author,
                'message': commit.message
            })

        return self._generate_drift_report(history)
```

### Output: Drift Timeline

```
======================================================================
SEMANTIC DRIFT ANALYSIS: process_user()
======================================================================

📅 2018-03-15 (Initial implementation)
   Author: Alice
   Coordinates: L=0.1, J=0.2, P=0.6, W=0.1
   Purpose: POWER-dominant (processing/execution)
   Disharmony: 0.08 (EXCELLENT)

📅 2019-06-22 (Added validation)
   Author: Bob
   Coordinates: L=0.1, J=0.4, P=0.5, W=0.0
   Purpose: POWER + JUSTICE (processing + validation)
   Disharmony: 0.35 (ACCEPTABLE)
   Drift: +0.27 from original

📅 2020-11-08 (Added caching)
   Author: Charlie
   Coordinates: L=0.1, J=0.3, P=0.4, W=0.2
   Purpose: Mixed concerns
   Disharmony: 0.58 (CONCERNING)
   Drift: +0.50 from original
   ⚠️  Function purpose becoming unclear

📅 2022-02-14 (Added notifications)
   Author: Dana
   Coordinates: L=0.3, J=0.2, P=0.3, W=0.2
   Purpose: LOST - no dominant dimension
   Disharmony: 0.89 (HIGH)
   Drift: +0.81 from original
   🚨 SEMANTIC DRIFT CRITICAL

📅 2024-08-19 (Current state)
   Author: Eve
   Coordinates: L=0.25, J=0.25, P=0.25, W=0.25
   Purpose: GOD FUNCTION - does everything
   Disharmony: 1.15 (CRITICAL)
   Drift: +1.07 from original
   🚨 URGENT REFACTORING NEEDED

======================================================================
DRIFT ANALYSIS
======================================================================

Original intent: "Process user data" (POWER)
Current reality: Validates, caches, processes, and notifies (ALL)

Semantic drift rate: 0.22 per year (HIGH)
Contributors: 5 developers, 23 commits

Root cause: Incremental feature additions without refactoring

Recommendation:
  Split into 4 functions matching original POWER focus:
  - validate_user_data() → JUSTICE module
  - get_cached_user() → WISDOM module
  - process_user_core() → Keep POWER focus
  - notify_user_processed() → LOVE module
```

---

## Feature 3: Semantic Complexity Heatmap

Visual heatmap showing where complexity is concentrated.

```
Codebase Semantic Complexity Heatmap
(Darker = Higher complexity/disharmony)

Directory Structure:
├── api/              ████████░░ (0.82 - HIGH)
├── auth/             ███░░░░░░░ (0.35 - LOW)
├── cache/            ████░░░░░░ (0.41 - MODERATE)
├── core/             █████████░ (0.94 - CRITICAL)
│   ├── manager.py    ██████████ (1.15 - CRITICAL)
│   ├── executor.py   ████████░░ (0.78 - HIGH)
│   └── utils.py      ██████░░░░ (0.62 - MODERATE)
├── data/             █████░░░░░ (0.52 - MODERATE)
├── integrations/     ████░░░░░░ (0.39 - LOW)
└── security/         ██░░░░░░░░ (0.18 - EXCELLENT)

Hotspots (Refactoring Priority):
1. core/manager.py (1.15)
2. api/endpoints.py (0.98)
3. core/executor.py (0.78)
```

---

## Feature 4: Architectural Reconstruction

**The killer feature:** Use LJPW clustering to show what the architecture **actually is**, not what the docs say.

```python
class ArchitecturalReconstructor:
    def reconstruct_true_architecture(self, codebase):
        """Discover actual architecture from semantic analysis"""

        # 1. Cluster files by semantic similarity
        clusters = self.cluster_by_semantics(codebase)

        # 2. Identify natural boundaries
        boundaries = self.find_semantic_boundaries(clusters)

        # 3. Detect coupling/cohesion
        coupling = self.measure_cross_cluster_dependencies(clusters)

        # 4. Compare to documented architecture
        documented_arch = self.load_documented_architecture()
        reality_gap = self.compare_architectures(clusters, documented_arch)

        return {
            'true_architecture': clusters,
            'documented_architecture': documented_arch,
            'reality_gap': reality_gap,
            'recommendations': self.generate_alignment_plan()
        }
```

### Output: Architecture Reality Check

```
======================================================================
ARCHITECTURAL REALITY CHECK
======================================================================

DOCUMENTED ARCHITECTURE (What we think we have):
------------------------------------------------
┌─────────────────┐
│  Presentation   │  (api/, views/)
└────────┬────────┘
         │
┌────────▼────────┐
│   Business      │  (services/, logic/)
└────────┬────────┘
         │
┌────────▼────────┐
│  Data Access    │  (data/, db/)
└─────────────────┘

ACTUAL ARCHITECTURE (What LJPW reveals):
------------------------------------------------
     api/               services/
  (LOVE+POWER)         (POWER+JUSTICE)
       │   ╲            ╱    │
       │    ╲          ╱     │
       │     ╲        ╱      │
   data/      core/     auth/
 (WISDOM)  (ALL DIMS) (JUSTICE)
       │     ╱  ╲       │
       │    ╱    ╲      │
       │   ╱      ╲     │
    cache/         security/
  (WISDOM)         (JUSTICE)

REALITY GAP ANALYSIS:
------------------------------------------------
🚨 Gap #1: Business Logic Scattered
   Documented: services/ directory
   Reality: 47% in api/, 31% in core/, 22% in services/

🚨 Gap #2: API Layer Violation
   Documented: Presentation only
   Reality: Contains 23 POWER functions (business logic)

🚨 Gap #3: Core Module Chaos
   Documented: Utilities
   Reality: God module doing everything

✅ Gap #4: Security Well-Isolated
   Documented: Security layer
   Reality: Clean JUSTICE cluster (matches!)

ARCHITECTURAL DEBT: $127,000
(Estimated cost to align reality with documented architecture)

RECOMMENDED REALIGNMENT:
1. Extract business logic from api/ → Create proper service layer
2. Dissolve core/ → Distribute functions to semantic-appropriate modules
3. Update documentation to reflect true boundaries
4. Enforce boundaries with semantic CI checks
```

---

## CLI Commands

```bash
# Generate full legacy code map
harmonizer legacy-map /path/to/codebase --output report.html

# Track semantic drift for specific function
harmonizer drift-track process_user --git-history

# Find refactoring opportunities
harmonizer refactor-suggest /path/to/codebase --top 10

# Visualize semantic clusters
harmonizer visualize /path/to/codebase --3d

# Compare documented vs actual architecture
harmonizer arch-check /path/to/codebase --docs architecture.md

# Generate complexity heatmap
harmonizer heatmap /path/to/codebase --output heatmap.svg
```

---

## The Value Proposition

**For the LinkedIn commenter:**

"Legacy code's real complexity" comes from:
1. **Lost intent** - Functions don't match their names anymore
2. **Architectural decay** - Boundaries dissolved over time
3. **Semantic drift** - Code wandered from original purpose
4. **Hidden structure** - No one knows what the actual architecture is

**LJPW solves this by:**
1. **Revealing true structure** - Semantic clusters show actual architecture
2. **Tracking drift** - Git analysis shows where/when code lost its way
3. **Prioritizing refactoring** - Metrics show highest-impact targets
4. **Providing roadmap** - Clear path from chaos to clarity

**The framework doesn't just analyze legacy code - it creates a MAP to escape from it.**

---

## Next Steps

1. **Build the mapper** (`harmonizer/legacy_mapper.py`)
2. **Add visualization** (3D semantic space plotting)
3. **Integrate git analysis** (track drift over time)
4. **Add CLI commands** (make it usable)
5. **Test on real legacy codebases** (validate approach)

This turns LJPW from "interesting framework" into **essential legacy code survival tool**.

Want me to start implementing?
