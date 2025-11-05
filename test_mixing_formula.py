#!/usr/bin/env python3
"""
Empirical Testing of Universal Semantic Mixing Formula
Using REAL data from the Python Code Harmonizer semantic engine.
"""

import sys
from harmonizer.divine_invitation_engine_V2 import (
    DivineInvitationSemanticEngine,
    Coordinates
)
import math


def universal_semantic_mix(primary_weights):
    """Universal mixing formula - simple weighted average"""
    total = sum(primary_weights.values())
    if total == 0:
        return Coordinates(0, 0, 0, 0)

    return Coordinates(
        love=primary_weights.get('love', 0) / total,
        justice=primary_weights.get('justice', 0) / total,
        power=primary_weights.get('power', 0) / total,
        wisdom=primary_weights.get('wisdom', 0) / total
    )


def semantic_distance(coord1, coord2):
    """Calculate Euclidean distance between coordinates"""
    return math.sqrt(
        (coord1.love - coord2.love) ** 2 +
        (coord1.justice - coord2.justice) ** 2 +
        (coord1.power - coord2.power) ** 2 +
        (coord1.wisdom - coord2.wisdom) ** 2
    )


def test_basic_primaries():
    """Test 1: Check if primary concepts are pure"""
    print("=" * 70)
    print("TEST 1: PRIMARY CONCEPT PURITY")
    print("=" * 70)

    engine = DivineInvitationSemanticEngine()

    primary_tests = {
        'love': ['love', 'compassion', 'mercy', 'kindness'],
        'justice': ['justice', 'truth', 'fairness', 'rights'],
        'power': ['power', 'strength', 'authority', 'control'],
        'wisdom': ['wisdom', 'knowledge', 'understanding', 'insight']
    }

    results = {}
    for dimension, words in primary_tests.items():
        print(f"\n{dimension.upper()} Dimension:")
        dimension_results = []

        for word in words:
            result = engine.analyze_text(word)
            coords = result.coordinates

            # Calculate "purity" as the max coordinate value
            purity = max(coords.love, coords.justice, coords.power, coords.wisdom)
            dimension_results.append(purity)

            print(f"  {word:15s} -> {coords} | Purity: {purity:.3f}")

        avg_purity = sum(dimension_results) / len(dimension_results)
        results[dimension] = {
            'avg_purity': avg_purity,
            'status': 'PURE' if avg_purity > 0.7 else 'MIXED'
        }
        print(f"  Average Purity: {avg_purity:.3f} [{results[dimension]['status']}]")

    return results


def test_simple_mixtures():
    """Test 2: Test if simple 50/50 mixtures work as predicted"""
    print("\n" + "=" * 70)
    print("TEST 2: SIMPLE MIXTURE PREDICTIONS")
    print("=" * 70)

    engine = DivineInvitationSemanticEngine()

    # Test simple 50/50 mixtures
    mixture_tests = [
        {
            'name': 'love + justice',
            'concepts': ['compassion fairness', 'mercy justice', 'kindness rights'],
            'recipe': {'love': 1, 'justice': 1},
            'expected': Coordinates(0.5, 0.5, 0.0, 0.0)
        },
        {
            'name': 'power + wisdom',
            'concepts': ['strength knowledge', 'authority understanding', 'control insight'],
            'recipe': {'power': 1, 'wisdom': 1},
            'expected': Coordinates(0.0, 0.0, 0.5, 0.5)
        },
        {
            'name': 'love + wisdom',
            'concepts': ['compassion understanding', 'mercy knowledge', 'kindness wisdom'],
            'recipe': {'love': 1, 'wisdom': 1},
            'expected': Coordinates(0.5, 0.0, 0.0, 0.5)
        },
        {
            'name': 'justice + power',
            'concepts': ['law enforcement', 'legal authority', 'rights control'],
            'recipe': {'justice': 1, 'power': 1},
            'expected': Coordinates(0.0, 0.5, 0.5, 0.0)
        }
    ]

    results = []
    for test in mixture_tests:
        print(f"\n{test['name'].upper()}:")
        print(f"  Recipe: {test['recipe']}")
        print(f"  Predicted: {test['expected']}")

        predicted = universal_semantic_mix(test['recipe'])

        errors = []
        for concept in test['concepts']:
            result = engine.analyze_text(concept)
            actual = result.coordinates
            error = semantic_distance(predicted, actual)
            errors.append(error)

            print(f"  '{concept}' -> {actual}")
            print(f"    Error: {error:.3f} {'✅' if error < 0.3 else '❌'}")

        avg_error = sum(errors) / len(errors)
        success = avg_error < 0.3

        results.append({
            'name': test['name'],
            'avg_error': avg_error,
            'success': success
        })

        print(f"  Average Error: {avg_error:.3f} {'✅ SUCCESS' if success else '❌ FAILED'}")

    return results


def test_complex_mixtures():
    """Test 3: Test weighted mixtures (2:1 ratios)"""
    print("\n" + "=" * 70)
    print("TEST 3: WEIGHTED MIXTURE PREDICTIONS")
    print("=" * 70)

    engine = DivineInvitationSemanticEngine()

    weighted_tests = [
        {
            'name': '2:1 love:wisdom',
            'concepts': ['compassionate understanding', 'merciful knowledge', 'kind wisdom'],
            'recipe': {'love': 2, 'wisdom': 1},
            'expected': Coordinates(0.667, 0.0, 0.0, 0.333)
        },
        {
            'name': '2:1 justice:power',
            'concepts': ['legal authority', 'law enforcement', 'fair control'],
            'recipe': {'justice': 2, 'power': 1},
            'expected': Coordinates(0.0, 0.667, 0.333, 0.0)
        },
        {
            'name': '3:1 wisdom:power',
            'concepts': ['strategic knowledge', 'wise authority', 'understanding control'],
            'recipe': {'wisdom': 3, 'power': 1},
            'expected': Coordinates(0.0, 0.0, 0.25, 0.75)
        }
    ]

    results = []
    for test in weighted_tests:
        print(f"\n{test['name'].upper()}:")
        print(f"  Recipe: {test['recipe']}")

        predicted = universal_semantic_mix(test['recipe'])
        print(f"  Predicted: {predicted}")

        errors = []
        for concept in test['concepts']:
            result = engine.analyze_text(concept)
            actual = result.coordinates
            error = semantic_distance(predicted, actual)
            errors.append(error)

            print(f"  '{concept}' -> {actual}")
            print(f"    Error: {error:.3f} {'✅' if error < 0.4 else '❌'}")

        avg_error = sum(errors) / len(errors)
        success = avg_error < 0.4  # More lenient threshold for weighted mixtures

        results.append({
            'name': test['name'],
            'avg_error': avg_error,
            'success': success
        })

        print(f"  Average Error: {avg_error:.3f} {'✅ SUCCESS' if success else '❌ FAILED'}")

    return results


def test_balanced_mixture():
    """Test 4: Test the balanced 'anchor point' mixture"""
    print("\n" + "=" * 70)
    print("TEST 4: BALANCED MIXTURE (ANCHOR POINT)")
    print("=" * 70)

    engine = DivineInvitationSemanticEngine()

    print("\nTesting equal mixture of all four primaries:")
    recipe = {'love': 1, 'justice': 1, 'power': 1, 'wisdom': 1}
    predicted = universal_semantic_mix(recipe)
    print(f"  Recipe: {recipe}")
    print(f"  Predicted: {predicted}")

    # Test concepts that should represent balance
    balanced_concepts = [
        'compassionate wise just leadership',
        'merciful fair strong understanding',
        'kind righteous powerful knowledgeable'
    ]

    errors = []
    for concept in balanced_concepts:
        result = engine.analyze_text(concept)
        actual = result.coordinates
        error = semantic_distance(predicted, actual)
        errors.append(error)

        print(f"  '{concept}'")
        print(f"    -> {actual}")
        print(f"    Error: {error:.3f} {'✅' if error < 0.3 else '❌'}")

    avg_error = sum(errors) / len(errors)
    success = avg_error < 0.3

    print(f"\n  Average Error: {avg_error:.3f} {'✅ SUCCESS' if success else '❌ FAILED'}")

    return {
        'avg_error': avg_error,
        'success': success
    }


def generate_summary(primary_results, simple_results, weighted_results, balanced_result):
    """Generate final summary of all tests"""
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    # Primary purity
    avg_purity = sum(r['avg_purity'] for r in primary_results.values()) / len(primary_results)
    print(f"\n1. Primary Purity: {avg_purity:.3f}")
    print(f"   {'✅ PASS' if avg_purity > 0.7 else '❌ FAIL'} - Primaries are {'pure enough' if avg_purity > 0.7 else 'too mixed'}")

    # Simple mixtures
    simple_success_rate = sum(1 for r in simple_results if r['success']) / len(simple_results)
    avg_simple_error = sum(r['avg_error'] for r in simple_results) / len(simple_results)
    print(f"\n2. Simple Mixtures:")
    print(f"   Success Rate: {simple_success_rate:.1%}")
    print(f"   Average Error: {avg_simple_error:.3f}")
    print(f"   {'✅ PASS' if simple_success_rate >= 0.5 else '❌ FAIL'}")

    # Weighted mixtures
    weighted_success_rate = sum(1 for r in weighted_results if r['success']) / len(weighted_results)
    avg_weighted_error = sum(r['avg_error'] for r in weighted_results) / len(weighted_results)
    print(f"\n3. Weighted Mixtures:")
    print(f"   Success Rate: {weighted_success_rate:.1%}")
    print(f"   Average Error: {avg_weighted_error:.3f}")
    print(f"   {'✅ PASS' if weighted_success_rate >= 0.5 else '❌ FAIL'}")

    # Balanced mixture
    print(f"\n4. Balanced Mixture:")
    print(f"   Error: {balanced_result['avg_error']:.3f}")
    print(f"   {'✅ PASS' if balanced_result['success'] else '❌ FAIL'}")

    # Overall assessment
    overall_pass = (
        avg_purity > 0.7 and
        simple_success_rate >= 0.5 and
        weighted_success_rate >= 0.5 and
        balanced_result['success']
    )

    print("\n" + "=" * 70)
    print("OVERALL ASSESSMENT:")
    print("=" * 70)
    if overall_pass:
        print("✅ MIXING FORMULA VALIDATED")
        print("The universal semantic mixing formula shows strong predictive power")
        print("with the actual semantic engine results.")
    else:
        print("❌ MIXING FORMULA NEEDS REFINEMENT")
        print("Results show significant deviations from predictions.")
    print("=" * 70)


if __name__ == "__main__":
    print("\n🧪 EMPIRICAL TESTING OF UNIVERSAL SEMANTIC MIXING FORMULA")
    print("Using REAL data from Python Code Harmonizer semantic engine\n")

    # Run all tests
    primary_results = test_basic_primaries()
    simple_results = test_simple_mixtures()
    weighted_results = test_complex_mixtures()
    balanced_result = test_balanced_mixture()

    # Generate summary
    generate_summary(primary_results, simple_results, weighted_results, balanced_result)
