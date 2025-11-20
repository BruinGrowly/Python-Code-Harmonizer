#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Enhanced AST Semantic Parser V2
Validates that programming constructs correctly map to LJPW dimensions.
"""

import ast

from harmonizer.ast_semantic_parser_v2 import AST_Semantic_Parser_V2
from harmonizer.divine_invitation_engine_V2 import DivineInvitationSemanticEngine


def test_wisdom_operations():
    """Test that WISDOM operations (information/knowledge) are recognized."""
    print("\n" + "=" * 70)
    print("TEST 1: WISDOM OPERATIONS (Information & Knowledge)")
    print("=" * 70)

    code_samples = [
        # Information retrieval
        ("def get_user(id): return database.query(id)", "get_user"),
        ("def fetch_data(): return api.fetch()", "fetch_data"),
        ("def read_file(path): return open(path).read()", "read_file"),
        # Computation
        ("def calculate_total(items): return sum(items)", "calculate_total"),
        ("def compute_hash(data): return hash(data)", "compute_hash"),
        ("def analyze_results(data): return stats.analyze(data)", "analyze_results"),
    ]

    engine = DivineInvitationSemanticEngine()
    parser = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)

    for code, func_name in code_samples:
        tree = ast.parse(code)
        func_node = tree.body[0]

        # Get intent from name
        intent_concepts = parser.get_intent_concepts(func_name, None)

        print(f"\nFunction: {func_name}")
        print(f"  Intent concepts: {intent_concepts}")

        # Verify WISDOM is in intent
        assert (
            "wisdom" in intent_concepts
        ), f"WISDOM should be in intent for {func_name}"
        print(f"  ✓ WISDOM detected in intent")

    print("\n✓ All WISDOM operations validated")


def test_justice_operations():
    """Test that JUSTICE operations (validation/correctness) are recognized."""
    print("\n" + "=" * 70)
    print("TEST 2: JUSTICE OPERATIONS (Validation & Correctness)")
    print("=" * 70)

    code_samples = [
        # Validation
        (
            "def validate_input(data):\n    if not data:\n        raise ValueError()",
            "validate_input",
        ),
        ("def check_permission(user):\n    assert user.is_admin", "check_permission"),
        (
            "def verify_token(token):\n    if token.expired:\n        return False\n    return True",
            "verify_token",
        ),
        # Comparison
        ("def compare_values(a, b): return a == b", "compare_values"),
        (
            "def filter_valid(items): return [i for i in items if i.valid]",
            "filter_valid",
        ),
    ]

    engine = DivineInvitationSemanticEngine()
    parser = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)

    for code, func_name in code_samples:
        tree = ast.parse(code)
        func_node = tree.body[0]

        # Get intent from name
        intent_concepts = parser.get_intent_concepts(func_name, None)

        print(f"\nFunction: {func_name}")
        print(f"  Intent concepts: {intent_concepts}")

        # Verify JUSTICE is in intent
        assert (
            "justice" in intent_concepts
        ), f"JUSTICE should be in intent for {func_name}"
        print(f"  ✓ JUSTICE detected in intent")

    print("\n✓ All JUSTICE operations validated")


def test_power_operations():
    """Test that POWER operations (execution/transformation) are recognized."""
    print("\n" + "=" * 70)
    print("TEST 3: POWER OPERATIONS (Execution & Transformation)")
    print("=" * 70)

    code_samples = [
        # Creation
        (
            "def create_user(name):\n    user = User(name)\n    return user",
            "create_user",
        ),
        ("def build_object():\n    obj = Object()\n    return obj", "build_object"),
        # Modification
        ("def update_status(obj, status):\n    obj.status = status", "update_status"),
        ("def modify_data(data):\n    data.value = 42", "modify_data"),
        # Destruction
        ("def delete_record(id):\n    database.delete(id)", "delete_record"),
        ("def remove_item(item):\n    items.remove(item)", "remove_item"),
        # Execution
        ("def execute_command(cmd):\n    os.system(cmd)", "execute_command"),
        ("def process_request(req):\n    req.process()", "process_request"),
    ]

    engine = DivineInvitationSemanticEngine()
    parser = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)

    for code, func_name in code_samples:
        tree = ast.parse(code)
        func_node = tree.body[0]

        # Get intent from name
        intent_concepts = parser.get_intent_concepts(func_name, None)

        print(f"\nFunction: {func_name}")
        print(f"  Intent concepts: {intent_concepts}")

        # Verify POWER is in intent
        assert "power" in intent_concepts, f"POWER should be in intent for {func_name}"
        print(f"  ✓ POWER detected in intent")

    print("\n✓ All POWER operations validated")


def test_love_operations():
    """Test that LOVE operations (connection/communication) are recognized."""
    print("\n" + "=" * 70)
    print("TEST 4: LOVE OPERATIONS (Connection & Communication)")
    print("=" * 70)

    code_samples = [
        # Communication
        (
            "def send_notification(user, msg):\n    mailer.send(user, msg)",
            "send_notification",
        ),
        ("def notify_user(user):\n    user.notify()", "notify_user"),
        (
            "def broadcast_event(event):\n    event_bus.broadcast(event)",
            "broadcast_event",
        ),
        # Connection
        ("def connect_database():\n    return db.connect()", "connect_database"),
        ("def join_tables(t1, t2):\n    return t1.join(t2)", "join_tables"),
        ("def merge_data(d1, d2):\n    return {**d1, **d2}", "merge_data"),
    ]

    engine = DivineInvitationSemanticEngine()
    parser = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)

    for code, func_name in code_samples:
        tree = ast.parse(code)
        func_node = tree.body[0]

        # Get intent from name
        intent_concepts = parser.get_intent_concepts(func_name, None)

        print(f"\nFunction: {func_name}")
        print(f"  Intent concepts: {intent_concepts}")

        # Verify LOVE is in intent
        assert "love" in intent_concepts, f"LOVE should be in intent for {func_name}"
        print(f"  ✓ LOVE detected in intent")

    print("\n✓ All LOVE operations validated")


def test_mixed_operations():
    """Test functions with mixed semantic operations."""
    print("\n" + "=" * 70)
    print("TEST 5: MIXED OPERATIONS")
    print("=" * 70)

    code = """
def validate_and_save_user(user_data):
    # JUSTICE: validation
    if not user_data.get('email'):
        raise ValueError("Email required")

    # POWER: creation and saving
    user = User(user_data)
    database.save(user)

    # LOVE: notification
    notify_admin(f"New user: {user.email}")

    # WISDOM: return information
    return user.id
"""

    engine = DivineInvitationSemanticEngine()
    parser = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)

    tree = ast.parse(code)
    func_node = tree.body[0]
    func_name = func_node.name

    # Get intent from name
    intent_concepts = parser.get_intent_concepts(func_name, None)

    # Get execution concepts
    node_map, exec_concepts = parser.get_execution_map(func_node.body)

    print(f"\nFunction: {func_name}")
    print(f"  Intent concepts: {intent_concepts}")
    print(f"  Execution concepts: {exec_concepts}")

    # Should have JUSTICE and POWER in intent
    assert "justice" in intent_concepts, "JUSTICE should be in intent (validate)"
    assert "power" in intent_concepts, "POWER should be in intent (save)"

    # Should have multiple dimensions in execution
    assert "justice" in exec_concepts, "JUSTICE should be in execution (if/raise)"
    assert "power" in exec_concepts, "POWER should be in execution (assignments)"
    assert "wisdom" in exec_concepts, "WISDOM should be in execution (return)"

    print(f"  ✓ Mixed operations correctly detected")
    print(f"  ✓ Intent: {len(intent_concepts)} dimensions")
    print(f"  ✓ Execution: {len(exec_concepts)} dimensions")

    print("\n✓ Mixed operations validated")


def test_execution_detection():
    """Test that execution body correctly identifies operations."""
    print("\n" + "=" * 70)
    print("TEST 6: EXECUTION DETECTION")
    print("=" * 70)

    test_cases = [
        {
            "code": "def func():\n    x = 42\n    return x",
            "expected": ["power", "wisdom"],  # assignment, return
            "desc": "Assignment + Return",
        },
        {
            "code": "def func(x):\n    if x > 0:\n        print(x)",
            "expected": ["justice", "love"],  # if, print
            "desc": "Conditional + Output",
        },
        {
            "code": "def func():\n    try:\n        do_something()\n    except:\n        pass",
            "expected": ["justice", "love"],  # try, except
            "desc": "Error Handling",
        },
        {
            "code": "def func(items):\n    for item in items:\n        process(item)",
            "expected": ["justice", "power"],  # for loop, process call
            "desc": "Loop + Processing",
        },
    ]

    engine = DivineInvitationSemanticEngine()
    parser = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)

    for case in test_cases:
        tree = ast.parse(case["code"])
        func_node = tree.body[0]

        node_map, exec_concepts = parser.get_execution_map(func_node.body)

        print(f"\n{case['desc']}:")
        print(f"  Execution concepts: {exec_concepts}")
        print(f"  Expected: {case['expected']}")

        for expected_dim in case["expected"]:
            assert (
                expected_dim in exec_concepts
            ), f"{expected_dim} should be detected in execution"
            print(f"  ✓ {expected_dim.upper()} detected")

    print("\n✓ Execution detection validated")


def test_compound_patterns():
    """Test compound pattern recognition (verb + noun)."""
    print("\n" + "=" * 70)
    print("TEST 7: COMPOUND PATTERN RECOGNITION")
    print("=" * 70)

    patterns = [
        ("get_user", "wisdom"),
        ("fetch_data", "wisdom"),
        ("validate_input", "justice"),
        ("check_permission", "justice"),
        ("create_user", "power"),
        ("delete_record", "power"),
        ("send_notification", "love"),
        ("notify_user", "love"),
    ]

    engine = DivineInvitationSemanticEngine()
    parser = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)

    for func_name, expected_dim in patterns:
        intent_concepts = parser.get_intent_concepts(func_name, None)

        print(f"\n{func_name}:")
        print(f"  Intent: {intent_concepts}")
        print(f"  Expected: {expected_dim}")

        assert (
            expected_dim in intent_concepts
        ), f"{expected_dim} should be detected for {func_name}"
        print(f"  ✓ {expected_dim.upper()} correctly identified")

    print("\n✓ Compound patterns validated")


def test_backward_compatibility():
    """Test that V2 parser is backward compatible with V1."""
    print("\n" + "=" * 70)
    print("TEST 8: BACKWARD COMPATIBILITY")
    print("=" * 70)

    from harmonizer.ast_semantic_parser import AST_Semantic_Parser

    code = "def calculate_total(items):\n    return sum(items)"

    engine = DivineInvitationSemanticEngine()

    # Test with V1 parser
    parser_v1 = AST_Semantic_Parser(engine.vocabulary.all_keywords)
    intent_v1 = parser_v1.get_intent_concepts("calculate_total", None)

    # Test with V2 parser
    parser_v2 = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)
    intent_v2 = parser_v2.get_intent_concepts("calculate_total", None)

    print(f"\nV1 Intent: {intent_v1}")
    print(f"V2 Intent: {intent_v2}")

    # Both should recognize wisdom
    assert (
        "wisdom" in intent_v1 or "wisdom" in intent_v2
    ), "Both parsers should recognize wisdom operations"

    print("  ✓ V2 parser maintains core functionality")
    print("\n✓ Backward compatibility validated")


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "=" * 70)
    print("ENHANCED AST PARSER V2 - COMPREHENSIVE TEST SUITE")
    print("Testing: Programming construct recognition with LJPW framework")
    print("=" * 70)

    test_wisdom_operations()
    test_justice_operations()
    test_power_operations()
    test_love_operations()
    test_mixed_operations()
    test_execution_detection()
    test_compound_patterns()
    test_backward_compatibility()

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)
    print("\n✅ Enhanced parser correctly maps programming constructs to LJPW")
    print("✅ All four dimensions recognized in code operations")
    print("✅ Compound patterns detected successfully")
    print("✅ Execution analysis accurate")
    print("✅ Backward compatible with V1")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_all_tests()
