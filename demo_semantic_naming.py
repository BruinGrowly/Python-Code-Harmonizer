#!/usr/bin/env python3
"""
Demo: How semantic naming helps the Harmonizer
Shows practical application of the validated mixing formula
"""

from harmonizer.divine_invitation_engine_V2 import DivineInvitationSemanticEngine, Coordinates
from harmonizer.semantic_naming import SemanticNamingEngine


def demo_1_detect_and_suggest():
    """Demo 1: Detect bad name and suggest better ones"""
    print("=" * 70)
    print("DEMO 1: DETECT BAD NAME + SUGGEST IMPROVEMENTS")
    print("=" * 70)

    # Analyze a disharmonious function name
    engine = DivineInvitationSemanticEngine()
    namer = SemanticNamingEngine()

    # Bad example: function name says "get" but does "delete"
    print("\n❌ BAD CODE:")
    print("def get_user(user_id):")
    print("    database.delete(user_id)")
    print("    return True")

    # Analyze intent vs execution
    intent_result = engine.analyze_text("get user")
    execution_result = engine.analyze_text("delete")

    print(f"\nIntent (function name):  {intent_result.coordinates}")
    print(f"Execution (body):        {execution_result.coordinates}")

    distance = engine.get_distance(intent_result.coordinates, execution_result.coordinates)
    print(f"Disharmony distance:     {distance:.3f} ⚠️ HIGH!")

    # Suggest better names based on actual execution
    print("\n✅ SUGGESTED FIXES based on execution semantics:")
    suggestions = namer.suggest_names(execution_result.coordinates, context="user", top_n=5)

    for name, score in suggestions:
        print(f"  • {name:25s} (match: {score:.1%})")


def demo_2_generate_from_intent():
    """Demo 2: Generate function structure from semantic intent"""
    print("\n" + "=" * 70)
    print("DEMO 2: GENERATE FUNCTION FROM SEMANTIC INTENT")
    print("=" * 70)

    engine = DivineInvitationSemanticEngine()
    namer = SemanticNamingEngine()

    # User describes what they want
    intent = "validate user input compassionately"
    print(f"\n📝 User intent: '{intent}'")

    # Analyze semantic profile
    result = engine.analyze_text(intent)
    print(f"Semantic profile: {result.coordinates}")
    print(f"Explanation: {namer.explain_coordinates(result.coordinates)}")

    # Suggest function names
    print("\n💡 Suggested function names:")
    suggestions = namer.suggest_names(result.coordinates, context="input", top_n=3)
    for name, score in suggestions:
        print(f"  • {name} (match: {score:.1%})")

    # Show what the function should do
    print("\n📋 Generated function skeleton:")
    print(f"""
def {suggestions[0][0]}(user_input):
    '''
    {namer.explain_coordinates(result.coordinates)}
    '''
    # Justice component: Validation logic
    if not user_input:
        # Love component: Helpful error message
        raise ValueError("Please provide valid input")

    # Wisdom component: Check against rules
    if not meets_requirements(user_input):
        # Love component: Explain what's wrong
        return ValidationResult(
            valid=False,
            message="Your input needs: [specific guidance]"
        )

    return ValidationResult(valid=True)
""")


def demo_3_refactoring_suggestion():
    """Demo 3: Suggest refactoring with semantic names"""
    print("=" * 70)
    print("DEMO 3: SEMANTIC-AWARE REFACTORING")
    print("=" * 70)

    engine = DivineInvitationSemanticEngine()
    namer = SemanticNamingEngine()

    # Analyze a multi-purpose function
    print("\n⚠️  PROBLEMATIC CODE (does too much):")
    print("""
def process_user(user_data):
    # Validation (Justice)
    if not user_data.is_valid:
        raise ValueError("Invalid data")

    # Data transformation (Power)
    transformed = transform_data(user_data)

    # Storage (Power)
    save_to_database(transformed)

    # Notification (Love)
    send_welcome_email(user_data.email)

    # Analytics (Wisdom)
    log_user_metrics(user_data)
""")

    # Analyze each operation
    operations = {
        'validation': 'validate user data',
        'transformation': 'transform data',
        'storage': 'save database',
        'notification': 'send email',
        'analytics': 'log metrics'
    }

    print("\n🔍 SEMANTIC ANALYSIS OF OPERATIONS:")
    coords_map = {}
    for op_name, op_text in operations.items():
        result = engine.analyze_text(op_text)
        coords_map[op_name] = result.coordinates
        dominant = namer._get_dominant_dimension(result.coordinates)
        print(f"  {op_name:15s}: {result.coordinates} [{dominant.upper()}]")

    # Suggest splitting
    print("\n✅ SUGGESTED REFACTORING:")
    print("\nSplit into semantically coherent functions:")

    # Group by semantic similarity
    groups = {
        'validation': ['validation'],
        'processing': ['transformation', 'storage'],
        'notification': ['notification', 'analytics']
    }

    for group_name, ops in groups.items():
        print(f"\n{group_name.upper()} GROUP:")
        # Get average coordinates for this group
        group_coords = Coordinates(
            love=sum(coords_map[op].love for op in ops) / len(ops),
            justice=sum(coords_map[op].justice for op in ops) / len(ops),
            power=sum(coords_map[op].power for op in ops) / len(ops),
            wisdom=sum(coords_map[op].wisdom for op in ops) / len(ops)
        )

        suggestions = namer.suggest_names(group_coords, context="user", top_n=3)
        print(f"  Suggested names:")
        for name, score in suggestions:
            print(f"    • {name} (match: {score:.1%})")


def demo_4_code_review():
    """Demo 4: Automated semantic code review"""
    print("\n" + "=" * 70)
    print("DEMO 4: SEMANTIC CODE REVIEW")
    print("=" * 70)

    engine = DivineInvitationSemanticEngine()
    namer = SemanticNamingEngine()

    # Check if function name matches execution
    functions_to_review = [
        ("calculate_total", "sum values"),  # ✅ Good match
        ("process_data", "delete records"),  # ❌ Mismatch
        ("validate_input", "check rules"),  # ✅ Good match
        ("get_user", "create user"),  # ❌ Mismatch
    ]

    print("\n📊 REVIEWING FUNCTION NAMES:\n")

    for func_name, execution in functions_to_review:
        intent = engine.analyze_text(func_name)
        actual = engine.analyze_text(execution)
        distance = engine.get_distance(intent.coordinates, actual.coordinates)

        if distance < 0.3:
            status = "✅ GOOD"
            icon = "✅"
        elif distance < 0.7:
            status = "⚠️  REVIEW"
            icon = "⚠️"
        else:
            status = "❌ BAD"
            icon = "❌"

        print(f"{icon} {func_name:20s} ({execution:20s})")
        print(f"   Disharmony: {distance:.3f} - {status}")

        if distance > 0.3:
            # Suggest better name
            suggestions = namer.suggest_names(actual.coordinates, top_n=1)
            if suggestions:
                print(f"   💡 Suggest: {suggestions[0][0]} (match: {suggestions[0][1]:.1%})")
        print()


if __name__ == "__main__":
    print("\n🎯 SEMANTIC NAMING ENGINE DEMONSTRATIONS")
    print("Showing how the validated mixing formula helps the Harmonizer\n")

    demo_1_detect_and_suggest()
    demo_2_generate_from_intent()
    demo_3_refactoring_suggestion()
    demo_4_code_review()

    print("\n" + "=" * 70)
    print("✅ DEMOS COMPLETE")
    print("=" * 70)
    print("\nThese demos show how the mixing formula enables:")
    print("  1. Better refactoring suggestions")
    print("  2. Function name generation from intent")
    print("  3. Semantic-aware code splitting")
    print("  4. Automated code review with suggestions")
    print("\nAll powered by the validated LJWP mixing formula! 🚀")
