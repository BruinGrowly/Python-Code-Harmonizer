#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programming Constructs Vocabulary
Comprehensive mapping of programming operations to LJPW semantic dimensions.

Based on: PROGRAMMING_LANGUAGE_SEMANTICS.md
Version: 2.0 (Enhanced with programming language theory)
"""

from typing import Dict

# Comprehensive programming verb mappings based on semantic analysis
# These are derived from the PROGRAMMING_LANGUAGE_SEMANTICS.md framework

PROGRAMMING_VERBS: Dict[str, str] = {
    # ====================================================================
    # WISDOM-DOMINANT OPERATIONS (Information & Knowledge)
    # Semantic signature: (L=0.1, J=0.1, P=0.1, W=0.7)
    # ====================================================================
    # Information retrieval
    "get": "wisdom",
    "fetch": "wisdom",
    "read": "wisdom",
    "load": "wisdom",
    "retrieve": "wisdom",
    "query": "wisdom",
    "find": "wisdom",
    "search": "wisdom",
    "lookup": "wisdom",
    "access": "wisdom",
    # Computation & analysis
    "calculate": "wisdom",
    "compute": "wisdom",
    "analyze": "wisdom",
    "evaluate": "wisdom",
    "assess": "wisdom",
    "measure": "wisdom",
    "count": "wisdom",
    "sum": "wisdom",
    "average": "wisdom",
    "aggregate": "wisdom",
    # Understanding & interpretation
    "parse": "wisdom",
    "interpret": "wisdom",
    "decode": "wisdom",
    "decipher": "wisdom",
    "understand": "wisdom",
    "comprehend": "wisdom",
    # Knowledge representation
    "represent": "wisdom",
    "model": "wisdom",
    "describe": "wisdom",
    "define": "wisdom",
    "specify": "wisdom",
    # Observation & monitoring
    "observe": "wisdom",
    "monitor": "wisdom",
    "watch": "wisdom",
    "track": "wisdom",
    "log": "wisdom",
    "record": "wisdom",
    # Returns are WISDOM (giving information back)
    "return": "wisdom",
    "yield": "wisdom",
    # Property/state checking (common in @property decorators)
    "status": "wisdom",  # Checking current state
    "state": "wisdom",  # Checking current state
    "value": "wisdom",  # Retrieving value
    "result": "wisdom",  # Getting result
    "valid": "wisdom",  # Checking validity state (note: different from "validate")
    "empty": "wisdom",  # Checking if empty
    "exists": "wisdom",  # Checking existence
    "available": "wisdom",  # Checking availability
    "ready": "wisdom",  # Checking readiness
    "needs": "wisdom",  # Checking if something is needed (e.g., needs_update)
    # ====================================================================
    # JUSTICE-DOMINANT OPERATIONS (Correctness & Validation)
    # Semantic signature: (L=0.1, J=0.7, P=0.1, W=0.1)
    # ====================================================================
    # Validation & verification
    "validate": "justice",
    "verify": "justice",
    "check": "justice",
    "test": "justice",
    "ensure": "justice",
    "confirm": "justice",
    "certify": "justice",
    # Enforcement & rules
    "enforce": "justice",
    "assert": "justice",
    "require": "justice",
    "demand": "justice",
    "mandate": "justice",
    # Comparison & equality
    "compare": "justice",
    "equals": "justice",
    "match": "justice",
    "differs": "justice",
    # Filtering & selection
    "filter": "justice",
    "select": "justice",
    "reject": "justice",
    "accept": "justice",
    # Authorization & permission
    "authorize": "justice",
    "authenticate": "justice",
    "permit": "justice",
    "allow": "justice",
    "deny": "justice",
    "restrict": "justice",
    "approve": "justice",
    # Boolean predicates (is_*, has_*, can_*)
    # Note: These check state/existence (Wisdom) rather than enforce rules (Justice)
    "is": "wisdom",  # is_valid, is_empty - checking state
    "has": "wisdom",  # has_permission - checking existence
    "can": "wisdom",  # can_access - checking capability
    # Modal verbs that imply rules/enforcement stay as Justice
    "should": "justice",
    "must": "justice",
    # Ordering & structuring
    "order": "justice",
    "sort": "justice",
    "arrange": "justice",
    "organize": "justice",
    "structure": "justice",
    # ====================================================================
    # POWER-DOMINANT OPERATIONS (Execution & Transformation)
    # Semantic signature: (L=0.1, J=0.1, P=0.7, W=0.1)
    # ====================================================================
    # Creation & generation
    "create": "power",
    "build": "power",
    "generate": "power",
    "make": "power",
    "construct": "power",
    "produce": "power",
    "spawn": "power",
    "initialize": "power",
    "instantiate": "power",
    # Modification & transformation
    "modify": "power",
    "update": "power",
    "change": "power",
    "alter": "power",
    "transform": "power",
    "convert": "power",
    "mutate": "power",
    "edit": "power",
    "revise": "power",
    # Destruction & removal
    "delete": "power",
    "remove": "power",
    "destroy": "power",
    "erase": "power",
    "clear": "power",
    "purge": "power",
    "drop": "power",
    "truncate": "power",
    # Storage operations
    "save": "power",
    "store": "power",
    "persist": "power",
    "write": "power",
    "insert": "power",
    "append": "power",
    "prepend": "power",
    # Execution & control
    "execute": "power",
    "run": "power",
    "perform": "power",
    "do": "power",
    "invoke": "power",
    "call": "power",
    "trigger": "power",
    "fire": "power",
    "launch": "power",
    "start": "power",
    "stop": "power",
    "pause": "power",
    "resume": "power",
    "restart": "power",
    # State management
    "set": "power",
    "reset": "power",
    "toggle": "power",
    "enable": "power",
    "disable": "power",
    "activate": "power",
    "deactivate": "power",
    # Processing
    "process": "power",
    "apply": "power",
    "compile": "power",
    # Raising errors is POWER (forcing exception)
    "raise": "power",
    "throw": "power",
    # ====================================================================
    # LOVE-DOMINANT OPERATIONS (Connection & Communication)
    # Semantic signature: (L=0.7, J=0.1, P=0.1, W=0.1)
    # ====================================================================
    # Connection & integration
    "connect": "love",
    "link": "love",
    "bind": "love",
    "attach": "love",
    "associate": "love",
    "relate": "love",
    "join": "love",
    "merge": "love",
    "combine": "love",
    "unite": "love",
    "integrate": "love",
    # Communication & notification
    "send": "love",
    "notify": "love",
    "inform": "love",
    "communicate": "love",
    "broadcast": "love",
    "publish": "love",
    "emit": "love",
    "signal": "love",
    "alert": "love",
    "message": "love",
    # Composition & building relationships
    "compose": "love",
    "assemble": "love",
    "collect": "love",
    "gather": "love",
    # Sharing & distribution
    "share": "love",
    "distribute": "love",
    "spread": "love",
    "propagate": "love",
    # Synchronization & coordination
    "sync": "love",
    "synchronize": "love",
    "coordinate": "love",
    "orchestrate": "love",
    # Output & display (communication to user)
    "print": "love",
    "display": "love",
    "show": "love",
    "render": "love",
    "present": "love",
    # API & interface operations
    "expose": "love",
    "provide": "love",
    "serve": "love",
    "offer": "love",
    # Adding to collections is LOVE (community building)
    # UNLESS it's to a specific technical collection like _concepts_found
    # That case is handled specially in the parser
    "add": "love",
    "include": "love",
    "incorporate": "love",
    # Exception handling is LOVE (mercy, graceful degradation)
    # Note: "handle" is in CONTEXT_DEPENDENT_VERBS with default="love"
    "catch": "love",
    "except": "love",
    "recover": "love",
}

# Control flow keywords - these are recognized differently
# They are always JUSTICE (logical structure)
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
    "assert",
    "break",
    "continue",
}

# Special cases that require context
CONTEXT_DEPENDENT_VERBS = {
    "add": {
        "default": "love",  # Adding to community/collection
        "to_concepts_found": "wisdom",  # Recording information
    },
    "handle": {
        "default": "love",  # Handling exceptions gracefully
        "events": "power",  # Event handling/processing
    },
    "render": {
        "default": "love",  # Rendering output/display (communication to user)
        "compile": "power",  # Rendering in compilation context
    },
    "aggregate": {
        "default": "wisdom",  # Aggregating data (computation)
        "compose": "love",  # Aggregating in composition context
    },
}

# Compound operation patterns (verb + noun combinations)
# These override single-word mappings when detected together
COMPOUND_PATTERNS: Dict[str, str] = {
    # WISDOM patterns
    "get_data": "wisdom",
    "fetch_user": "wisdom",
    "read_file": "wisdom",
    "load_config": "wisdom",
    "query_database": "wisdom",
    "calculate_total": "wisdom",
    "compute_hash": "wisdom",
    # JUSTICE patterns
    "validate_input": "justice",
    "check_permission": "justice",
    "verify_token": "justice",
    "test_condition": "justice",
    "ensure_valid": "justice",
    # POWER patterns
    "create_user": "power",
    "delete_record": "power",
    "update_status": "power",
    "save_file": "power",
    "execute_command": "power",
    "process_request": "power",
    # LOVE patterns
    "send_notification": "love",
    "notify_user": "love",
    "connect_service": "love",
    "join_tables": "love",
    "broadcast_event": "love",
}


def get_semantic_dimension(verb: str, context: str = "default") -> str:
    """
    Get the semantic dimension for a programming verb.

    Args:
        verb: The programming operation verb
        context: Additional context for context-dependent verbs

    Returns:
        The semantic dimension: 'wisdom', 'justice', 'power', or 'love'
    """
    verb_lower = verb.lower()

    # Check context-dependent verbs
    if verb_lower in CONTEXT_DEPENDENT_VERBS:
        contexts = CONTEXT_DEPENDENT_VERBS[verb_lower]
        return contexts.get(context, contexts["default"])

    # Check standard programming verbs
    if verb_lower in PROGRAMMING_VERBS:
        return PROGRAMMING_VERBS[verb_lower]

    # Default to wisdom (information operations) if unknown
    return "wisdom"


def get_dimension_description(dimension: str) -> str:
    """Get a human-readable description of what a dimension means in code."""
    descriptions = {
        "wisdom": "Information & Knowledge (data, queries, calculations, analysis)",
        "justice": "Correctness & Validation (types, tests, assertions, logic)",
        "power": "Execution & Transformation (actions, mutations, I/O, control)",
        "love": "Connection & Communication (APIs, composition, notifications, integration)",
    }
    return descriptions.get(dimension.lower(), "Unknown dimension")


def explain_programming_semantics():
    """Print explanation of programming construct semantics."""
    print("=" * 70)
    print("PROGRAMMING LANGUAGE SEMANTICS - LJPW DIMENSIONS")
    print("=" * 70)
    print()
    print("Every programming operation maps to one of four semantic dimensions:")
    print()
    print("📚 WISDOM (W) - Information & Knowledge")
    print("   Operations that retrieve, compute, or represent information")
    print("   Examples: get, read, calculate, query, analyze, return")
    print()
    print("⚖️  JUSTICE (J) - Correctness & Validation")
    print("   Operations that verify, validate, or ensure correctness")
    print("   Examples: validate, check, assert, test, filter, authorize")
    print()
    print("⚡ POWER (P) - Execution & Transformation")
    print("   Operations that modify state, execute actions, or transform data")
    print("   Examples: create, update, delete, execute, save, process")
    print()
    print("💛 LOVE (L) - Connection & Communication")
    print("   Operations that connect systems, communicate, or integrate")
    print("   Examples: send, notify, connect, join, merge, broadcast")
    print()
    print("All four dimensions are NECESSARY for functional code.")
    print("Code quality = semantic harmony (intent matches execution)")
    print("=" * 70)


if __name__ == "__main__":
    explain_programming_semantics()
    print()
    print(f"Total programming verbs mapped: {len(PROGRAMMING_VERBS)}")
    print(f"Total compound patterns: {len(COMPOUND_PATTERNS)}")

    # Show distribution
    from collections import Counter

    distribution = Counter(PROGRAMMING_VERBS.values())
    print()
    print("Distribution across dimensions:")
    for dim, count in distribution.most_common():
        print(f"  {dim.upper()}: {count} verbs")
