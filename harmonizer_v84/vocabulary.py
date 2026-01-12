"""
V7.3 Programming Vocabulary - Enhanced semantic verb mappings

Ported and enhanced from v5.1's programming_constructs_vocabulary.py
with V7.3's 2+2 dimensional understanding.

Key V7.3 insight: P and W are fundamental, L and J emerge.
So we focus verb mappings on P (transformation) and W (knowledge).

Based on: PROGRAMMING_LANGUAGE_SEMANTICS.md + LJPW V7.3 Framework
"""

from typing import Dict, Optional, Tuple

# =============================================================================
# SEMANTIC DIMENSION COORDINATES
# =============================================================================
# Each dimension's typical signature (dominant = 0.7, others = 0.1)

DIMENSION_SIGNATURES: Dict[str, Tuple[float, float, float, float]] = {
    "power": (0.3, 0.3, 0.9, 0.3),  # High P (fundamental)
    "wisdom": (0.3, 0.3, 0.3, 0.9),  # High W (fundamental)
    "love": (0.9, 0.3, 0.3, 0.5),  # High L (emergent from W)
    "justice": (0.3, 0.9, 0.5, 0.3),  # High J (emergent from P)
}

# =============================================================================
# POWER-DOMINANT VERBS (Transformation, Execution, State Change)
# =============================================================================
# These are FUNDAMENTAL - P is measured directly

POWER_VERBS = {
    # Creation & generation
    "create",
    "build",
    "generate",
    "make",
    "construct",
    "produce",
    "spawn",
    "initialize",
    "instantiate",
    "new",
    "forge",
    "craft",
    # Modification & transformation
    "modify",
    "update",
    "change",
    "alter",
    "transform",
    "convert",
    "mutate",
    "edit",
    "revise",
    "adapt",
    "adjust",
    "tweak",
    # Destruction & removal
    "delete",
    "remove",
    "destroy",
    "erase",
    "clear",
    "purge",
    "clean",
    "wipe",
    "dispose",
    "drop",
    "kill",
    "terminate",
    # State changes
    "set",
    "assign",
    "put",
    "store",
    "save",
    "persist",
    "write",
    "commit",
    "push",
    "post",
    "submit",
    "upload",
    # Execution & control
    "execute",
    "run",
    "perform",
    "do",
    "invoke",
    "call",
    "trigger",
    "fire",
    "emit",
    "dispatch",
    "apply",
    "process",
    # Activation & management
    "start",
    "stop",
    "pause",
    "resume",
    "restart",
    "reset",
    "enable",
    "disable",
    "activate",
    "deactivate",
    "toggle",
    # Raising exceptions (forcing control flow)
    "raise",
    "throw",
    "error",
    "fail",
    "abort",
    "panic",
    # Moving & transferring
    "move",
    "copy",
    "clone",
    "migrate",
    "transfer",
    "shift",
}

# =============================================================================
# WISDOM-DOMINANT VERBS (Knowledge, Pattern Recognition, Information)
# =============================================================================
# These are FUNDAMENTAL - W is measured directly

WISDOM_VERBS = {
    # Retrieval & access
    "get",
    "fetch",
    "retrieve",
    "read",
    "load",
    "obtain",
    "access",
    "acquire",
    "pull",
    "extract",
    "take",
    "receive",
    # Search & discovery
    "find",
    "search",
    "query",
    "lookup",
    "locate",
    "discover",
    "scan",
    "seek",
    "explore",
    "detect",
    "identify",
    "recognize",
    # Analysis & understanding
    "analyze",
    "parse",
    "interpret",
    "understand",
    "comprehend",
    "study",
    "examine",
    "inspect",
    "investigate",
    "diagnose",
    # Calculation & computation
    "calculate",
    "compute",
    "derive",
    "infer",
    "predict",
    "estimate",
    "measure",
    "count",
    "sum",
    "average",
    "aggregate",
    # Observation & monitoring
    "observe",
    "monitor",
    "watch",
    "track",
    "log",
    "record",
    "trace",
    "profile",
    "benchmark",
    "sample",
    # Returns & yielding (providing information back)
    "return",
    "yield",
    "output",
    "result",
    "respond",
    "reply",
    # Status & state checking
    "check",
    "test",
    "verify",
    "status",
    "state",
    "value",
    "is",
    "has",
    "can",
    "should",
    "exists",
    "contains",
    # Formatting & conversion (of information)
    "format",
    "stringify",
    "serialize",
    "encode",
    "decode",
    "to_string",
    "to_json",
    "to_dict",
    "repr",
}

# =============================================================================
# LOVE-DOMINANT VERBS (Connection, Integration, Communication)
# =============================================================================
# These EMERGE from high W (Love = correlation of wisdom)

LOVE_VERBS = {
    # Communication & messaging
    "send",
    "notify",
    "broadcast",
    "publish",
    "signal",
    "message",
    "email",
    "alert",
    "announce",
    "communicate",
    # Connection & integration
    "connect",
    "link",
    "bind",
    "attach",
    "couple",
    "wire",
    "join",
    "merge",
    "combine",
    "union",
    "integrate",
    "unify",
    # Synchronization & coordination
    "sync",
    "synchronize",
    "coordinate",
    "orchestrate",
    "schedule",
    "queue",
    "pipeline",
    "chain",
    "sequence",
    # Sharing & providing
    "share",
    "provide",
    "serve",
    "offer",
    "expose",
    "export",
    "import",
    "include",
    "incorporate",
    "inject",
    "embed",
    # Display & presentation (to user)
    "print",
    "display",
    "show",
    "render",
    "present",
    "visualize",
    "draw",
    "paint",
    "plot",
    "graph",
    # Exception handling (graceful recovery = mercy)
    "catch",
    "except",
    "recover",
    "handle",
    "rescue",
    "fallback",
    "retry",
    "heal",
    "fix",
    "repair",
}

# =============================================================================
# JUSTICE-DOMINANT VERBS (Validation, Structure, Correctness)
# =============================================================================
# These EMERGE from high P (Justice = symmetry of power)

JUSTICE_VERBS = {
    # Validation & verification
    "validate",
    "verify",
    "ensure",
    "assert",
    "confirm",
    "check",
    "test",
    "evaluate",
    "assess",
    "audit",
    # Constraints & requirements
    "require",
    "demand",
    "mandate",
    "enforce",
    "constrain",
    "restrict",
    "limit",
    "bound",
    "cap",
    "clamp",
    # Comparison & equality
    "compare",
    "equals",
    "match",
    "differs",
    "same",
    "different",
    "greater",
    "less",
    "between",
    "within",
    "outside",
    # Filtering & selection
    "filter",
    "select",
    "reject",
    "accept",
    "include",
    "exclude",
    "pick",
    "choose",
    "sort",
    "order",
    "group",
    "partition",
    # Authorization & permission
    "authorize",
    "authenticate",
    "permit",
    "allow",
    "deny",
    "grant",
    "revoke",
    "forbid",
    "protect",
    "secure",
    "sanitize",
}

# =============================================================================
# COMBINED VOCABULARY
# =============================================================================

PROGRAMMING_VERBS: Dict[str, str] = {}

# Add all verbs with their dimensions
for verb in POWER_VERBS:
    PROGRAMMING_VERBS[verb] = "power"
for verb in WISDOM_VERBS:
    PROGRAMMING_VERBS[verb] = "wisdom"
for verb in LOVE_VERBS:
    PROGRAMMING_VERBS[verb] = "love"
for verb in JUSTICE_VERBS:
    PROGRAMMING_VERBS[verb] = "justice"

# =============================================================================
# COMPOUND PATTERNS (multi-word operations)
# =============================================================================

COMPOUND_PATTERNS: Dict[str, str] = {
    # Wisdom patterns
    "get_data": "wisdom",
    "fetch_user": "wisdom",
    "read_file": "wisdom",
    "load_config": "wisdom",
    "query_database": "wisdom",
    "calculate_total": "wisdom",
    "parse_json": "wisdom",
    "find_by_id": "wisdom",
    # Power patterns
    "save_to": "power",
    "write_file": "power",
    "update_record": "power",
    "delete_item": "power",
    "execute_command": "power",
    "process_request": "power",
    "create_instance": "power",
    "set_value": "power",
    # Love patterns
    "send_notification": "love",
    "notify_user": "love",
    "connect_service": "love",
    "join_tables": "love",
    "broadcast_event": "love",
    "sync_data": "love",
    "merge_results": "love",
    # Justice patterns
    "validate_input": "justice",
    "check_permissions": "justice",
    "verify_signature": "justice",
    "filter_results": "justice",
    "enforce_policy": "justice",
    "assert_valid": "justice",
}

# =============================================================================
# CONTROL FLOW KEYWORDS (always Justice - logical structure)
# =============================================================================

CONTROL_FLOW_KEYWORDS = {
    "if",
    "else",
    "elif",
    "for",
    "while",
    "with",
    "try",
    "except",
    "finally",
    "match",
    "case",
    "break",
    "continue",
    "pass",
    "return",
    "yield",
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_semantic_dimension(verb: str, context: str = "default") -> str:
    """
    Get the semantic dimension for a programming verb.

    Args:
        verb: The programming operation verb
        context: Additional context for disambiguation

    Returns:
        The semantic dimension: 'wisdom', 'justice', 'power', or 'love'
    """
    verb_lower = verb.lower()

    # Check direct mapping
    if verb_lower in PROGRAMMING_VERBS:
        return PROGRAMMING_VERBS[verb_lower]

    # Check for prefix matches
    for known_verb, dimension in PROGRAMMING_VERBS.items():
        if verb_lower.startswith(known_verb):
            return dimension

    # Default to wisdom (information operation)
    return "wisdom"


def get_verb_coordinates(verb: str) -> Tuple[float, float, float, float]:
    """
    Get the LJPW coordinates for a verb.

    Returns:
        Tuple of (L, J, P, W)
    """
    dimension = get_semantic_dimension(verb)
    return DIMENSION_SIGNATURES.get(dimension, (0.5, 0.5, 0.5, 0.5))


def classify_function_name(name: str) -> Dict[str, any]:
    """
    Classify a function name by its semantic content.

    Args:
        name: Function name (e.g., "get_user_by_id")

    Returns:
        Dict with dimension, confidence, and reasoning
    """
    import re

    # Split into parts
    if "_" in name:
        parts = name.split("_")
    else:
        parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+", name)

    # Check compound patterns first
    for length in [3, 2]:
        if len(parts) >= length:
            compound = "_".join(parts[:length]).lower()
            if compound in COMPOUND_PATTERNS:
                return {
                    "dimension": COMPOUND_PATTERNS[compound],
                    "confidence": 0.9,
                    "matched": compound,
                    "type": "compound",
                }

    # Check individual words
    dimensions_found = []
    for part in parts:
        dim = get_semantic_dimension(part.lower())
        if dim:
            dimensions_found.append(dim)

    if dimensions_found:
        # Return the first (usually the verb)
        return {
            "dimension": dimensions_found[0],
            "confidence": 0.7,
            "matched": parts[0] if parts else name,
            "type": "verb",
        }

    return {"dimension": "wisdom", "confidence": 0.3, "matched": None, "type": "default"}  # Default


def get_vocabulary_stats() -> Dict[str, int]:
    """Get statistics about the vocabulary."""
    from collections import Counter

    distribution = Counter(PROGRAMMING_VERBS.values())
    return {
        "total_verbs": len(PROGRAMMING_VERBS),
        "power_verbs": len(POWER_VERBS),
        "wisdom_verbs": len(WISDOM_VERBS),
        "love_verbs": len(LOVE_VERBS),
        "justice_verbs": len(JUSTICE_VERBS),
        "compound_patterns": len(COMPOUND_PATTERNS),
        "distribution": dict(distribution),
    }
