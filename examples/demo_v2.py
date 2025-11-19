#!/usr/bin/env python3
"""Demo script showing Enhanced Parser V2 in action."""

import ast
from harmonizer.divine_invitation_engine_V2 import DivineInvitationSemanticEngine
from harmonizer.ast_semantic_parser_v2 import AST_Semantic_Parser_V2


def analyze_with_v2(code, function_name):
    """Analyze code using Enhanced Parser V2."""
    # Initialize engine and parser
    engine = DivineInvitationSemanticEngine()
    parser = AST_Semantic_Parser_V2(engine.vocabulary.all_keywords)

    # Parse code
    tree = ast.parse(code)
    func_node = tree.body[0]

    # Get semantic analysis
    intent_concepts = parser.get_intent_concepts(function_name, None)
    _, execution_concepts = parser.get_execution_map(func_node.body)

    # Calculate coordinates
    intent_text = " ".join(intent_concepts)
    execution_text = " ".join(execution_concepts)

    intent_result = engine.analyze_text(intent_text)
    execution_result = engine.analyze_text(execution_text)

    intent_coords = intent_result.coordinates
    execution_coords = execution_result.coordinates

    # Calculate disharmony
    disharmony = engine.get_distance(intent_coords, execution_coords)

    return {
        "function": function_name,
        "intent_concepts": intent_concepts,
        "execution_concepts": execution_concepts,
        "intent_coords": intent_coords,
        "execution_coords": execution_coords,
        "disharmony": disharmony,
    }


def print_analysis(result):
    """Pretty print analysis results."""
    print(f"\n{'='*70}")
    print(f"FUNCTION: {result['function']}")
    print(f"{'='*70}")

    print(f"\nINTENT (what function claims to do):")
    print(f"  Concepts: {result['intent_concepts']}")
    print(
        f"  Coordinates: L={result['intent_coords'].love:.3f}, J={result['intent_coords'].justice:.3f}, "
        f"P={result['intent_coords'].power:.3f}, W={result['intent_coords'].wisdom:.3f}"
    )

    print(f"\nEXECUTION (what function actually does):")
    print(f"  Concepts: {result['execution_concepts']}")
    print(
        f"  Coordinates: L={result['execution_coords'].love:.3f}, J={result['execution_coords'].justice:.3f}, "
        f"P={result['execution_coords'].power:.3f}, W={result['execution_coords'].wisdom:.3f}"
    )

    print(f"\nDISHARMONY SCORE: {result['disharmony']:.3f}")

    if result["disharmony"] < 0.5:
        print("STATUS: ✅ EXCELLENT HARMONY")
    elif result["disharmony"] < 1.0:
        print("STATUS: ⚠️  MEDIUM DISHARMONY")
    else:
        print("STATUS: 🚨 CRITICAL DISHARMONY - Likely Bug!")


# Test examples
print("=" * 70)
print("ENHANCED PARSER V2 - REAL-WORLD DEMONSTRATION")
print("=" * 70)

# Example 1: Harmonious function
code1 = '''
def get_user_data(user_id):
    """Retrieve user data from database."""
    user = database.query(user_id)
    return user
'''
result1 = analyze_with_v2(code1, "get_user_data")
print_analysis(result1)

# Example 2: Harmonious validation
code2 = '''
def validate_email(email):
    """Validate email address format."""
    if "@" in email and "." in email:
        return True
    return False
'''
result2 = analyze_with_v2(code2, "validate_email")
print_analysis(result2)

# Example 3: Harmonious communication
code3 = '''
def send_notification(user, message):
    """Send notification to user."""
    notification_service.send(user.email, message)
    return True
'''
result3 = analyze_with_v2(code3, "send_notification")
print_analysis(result3)

# Example 4: BUG - Function name says "check" but deletes!
code4 = '''
def check_user_permissions(user_token):
    """Check user permissions."""
    database.delete_user(user_token)  # BUG!
    return "Deleted"
'''
result4 = analyze_with_v2(code4, "check_user_permissions")
print_analysis(result4)
print("\n⚠️  WARNING: This function's name suggests checking (JUSTICE) but it")
print("    actually deletes (POWER). This is a semantic bug!")

# Example 5: Harmonious mixed operation
code5 = '''
def fetch_validate_and_save(data_id):
    """Fetch data, validate it, and save changes."""
    data = database.fetch(data_id)
    if validate(data):
        database.save(data)
    return data
'''
result5 = analyze_with_v2(code5, "fetch_validate_and_save")
print_analysis(result5)

print(f"\n{'='*70}")
print("DEMONSTRATION COMPLETE")
print("=" * 70)
print("\n✅ Enhanced Parser V2 Features:")
print("   • 184 programming verbs (7.4x more than V1)")
print("   • Compound pattern detection (get_user, send_notification, etc.)")
print("   • Context-aware analysis")
print("   • Accurate bug detection through semantic disharmony")
print("   • 100% backward compatible with V1")
