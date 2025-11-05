#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive tests for the SemanticNamingEngine
"""

import pytest
from harmonizer.semantic_naming import SemanticNamingEngine
from harmonizer.divine_invitation_engine_V2 import Coordinates


@pytest.fixture(scope="module")
def naming_engine():
    """Provides a single instance of the naming engine for all tests."""
    return SemanticNamingEngine()


class TestInitialization:
    """Tests for engine initialization"""

    def test_engine_initialization(self, naming_engine):
        """Verify the naming engine initializes correctly"""
        assert naming_engine is not None
        assert hasattr(naming_engine, "action_verbs")
        assert hasattr(naming_engine, "object_nouns")

    def test_action_verbs_loaded(self, naming_engine):
        """Verify action verbs dictionary is populated"""
        assert len(naming_engine.action_verbs) > 0
        assert "validate" in naming_engine.action_verbs
        assert "create" in naming_engine.action_verbs
        assert "analyze" in naming_engine.action_verbs

    def test_object_nouns_loaded(self, naming_engine):
        """Verify object nouns list is populated"""
        assert len(naming_engine.object_nouns) > 0
        assert "user" in naming_engine.object_nouns
        assert "data" in naming_engine.object_nouns


class TestSuggestionGeneration:
    """Tests for name suggestion functionality"""

    def test_suggest_names_power_dominant(self, naming_engine):
        """Test suggestions for a power-dominant function"""
        # Power-dominant coordinates (action, transformation)
        coords = Coordinates(love=0.1, justice=0.2, power=0.6, wisdom=0.1)
        suggestions = naming_engine.suggest_names(coords, top_n=5)

        assert len(suggestions) <= 5
        assert all(isinstance(s, tuple) for s in suggestions)
        assert all(len(s) == 2 for s in suggestions)

        # First suggestion should have highest similarity
        assert suggestions[0][1] >= suggestions[-1][1]

        # Top suggestions should be power-dominant verbs
        # Check that the top suggestion is actually a power verb
        top_verb = suggestions[0][0]
        verb_coords = naming_engine.action_verbs.get(top_verb)
        if verb_coords:
            # Power dimension should be dominant
            assert verb_coords[2] >= max(verb_coords[0], verb_coords[1], verb_coords[3])

    def test_suggest_names_justice_dominant(self, naming_engine):
        """Test suggestions for a justice-dominant function"""
        # Justice-dominant coordinates (validation, checking)
        coords = Coordinates(love=0.1, justice=0.7, power=0.1, wisdom=0.1)
        suggestions = naming_engine.suggest_names(coords, top_n=5)

        # Should suggest justice verbs like validate, verify, check
        names = [s[0] for s in suggestions]
        assert any(
            verb in name
            for verb in ["validate", "verify", "check", "ensure"]
            for name in names
        )

    def test_suggest_names_wisdom_dominant(self, naming_engine):
        """Test suggestions for a wisdom-dominant function"""
        # Wisdom-dominant coordinates (analysis, understanding)
        coords = Coordinates(love=0.1, justice=0.1, power=0.1, wisdom=0.7)
        suggestions = naming_engine.suggest_names(coords, top_n=5)

        # Should suggest wisdom verbs like analyze, calculate, evaluate
        names = [s[0] for s in suggestions]
        assert any(
            verb in name
            for verb in ["analyze", "calculate", "evaluate", "compute"]
            for name in names
        )

    def test_suggest_names_love_dominant(self, naming_engine):
        """Test suggestions for a love-dominant function"""
        # Love-dominant coordinates (connection, care)
        coords = Coordinates(love=0.7, justice=0.1, power=0.1, wisdom=0.1)
        suggestions = naming_engine.suggest_names(coords, top_n=5)

        # Top suggestions should be love-dominant verbs
        # Check that the top suggestion is actually a love verb
        top_verb = suggestions[0][0]
        verb_coords = naming_engine.action_verbs.get(top_verb)
        if verb_coords:
            # Love dimension should be dominant
            assert verb_coords[0] >= max(verb_coords[1], verb_coords[2], verb_coords[3])

    def test_suggest_names_with_context(self, naming_engine):
        """Test that context is properly appended to suggestions"""
        coords = Coordinates(love=0.1, justice=0.7, power=0.1, wisdom=0.1)
        suggestions = naming_engine.suggest_names(coords, context="user", top_n=3)

        # All suggestions should include the context
        for name, _ in suggestions:
            assert "_user" in name

    def test_suggest_names_without_context(self, naming_engine):
        """Test suggestions without context"""
        coords = Coordinates(love=0.1, justice=0.7, power=0.1, wisdom=0.1)
        suggestions = naming_engine.suggest_names(coords, top_n=3)

        # Suggestions should not have underscores (no context appended)
        for name, _ in suggestions:
            # Should be just the verb, or might have underscore if verb itself has it
            assert isinstance(name, str)

    def test_suggest_names_top_n_parameter(self, naming_engine):
        """Test that top_n parameter works correctly"""
        coords = Coordinates(love=0.1, justice=0.7, power=0.1, wisdom=0.1)

        suggestions_3 = naming_engine.suggest_names(coords, top_n=3)
        assert len(suggestions_3) == 3

        suggestions_10 = naming_engine.suggest_names(coords, top_n=10)
        assert len(suggestions_10) == 10

    def test_suggest_names_sorted_by_similarity(self, naming_engine):
        """Test that suggestions are sorted by similarity (highest first)"""
        coords = Coordinates(love=0.1, justice=0.7, power=0.1, wisdom=0.1)
        suggestions = naming_engine.suggest_names(coords, top_n=5)

        # Check that each suggestion has lower or equal similarity than the previous
        for i in range(len(suggestions) - 1):
            assert suggestions[i][1] >= suggestions[i + 1][1]


class TestMultipleObjectSuggestions:
    """Tests for multiple verb-object combination suggestions"""

    def test_suggest_with_multiple_objects(self, naming_engine):
        """Test generation of multiple verb-object combinations"""
        coords = Coordinates(love=0.1, justice=0.1, power=0.6, wisdom=0.2)
        suggestions = naming_engine.suggest_with_multiple_objects(
            coords, top_verbs=3, top_objects=3
        )

        assert len(suggestions) <= 9  # 3 verbs * 3 objects
        assert all(isinstance(s, tuple) for s in suggestions)
        assert all(len(s) == 3 for s in suggestions)  # (name, score, explanation)

        # Check structure of results
        for name, score, explanation in suggestions:
            assert isinstance(name, str)
            assert isinstance(score, float)
            assert isinstance(explanation, str)
            assert 0.0 <= score <= 1.0
            assert "_" in name  # Should have verb_object format

    def test_multiple_objects_sorted_by_similarity(self, naming_engine):
        """Test that multiple object suggestions are sorted by similarity"""
        coords = Coordinates(love=0.1, justice=0.1, power=0.6, wisdom=0.2)
        suggestions = naming_engine.suggest_with_multiple_objects(
            coords, top_verbs=3, top_objects=3
        )

        # Check descending order
        for i in range(len(suggestions) - 1):
            assert suggestions[i][1] >= suggestions[i + 1][1]


class TestSimilarityCalculation:
    """Tests for the similarity calculation algorithm"""

    def test_calculate_similarity_identical_vectors(self, naming_engine):
        """Test similarity between identical vectors"""
        coords = Coordinates(love=0.5, justice=0.5, power=0.0, wisdom=0.0)
        vec = (0.5, 0.5, 0.0, 0.0)

        similarity = naming_engine._calculate_similarity(coords, vec)
        assert similarity == pytest.approx(1.0, abs=1e-6)

    def test_calculate_similarity_opposite_vectors(self, naming_engine):
        """Test similarity between opposite vectors"""
        coords = Coordinates(love=1.0, justice=0.0, power=0.0, wisdom=0.0)
        vec = (0.0, 0.0, 1.0, 0.0)  # Orthogonal vector

        similarity = naming_engine._calculate_similarity(coords, vec)
        assert similarity == pytest.approx(0.0, abs=1e-6)

    def test_calculate_similarity_zero_vector(self, naming_engine):
        """Test similarity with zero vector returns 0"""
        coords = Coordinates(love=0.0, justice=0.0, power=0.0, wisdom=0.0)
        vec = (1.0, 0.0, 0.0, 0.0)

        similarity = naming_engine._calculate_similarity(coords, vec)
        assert similarity == 0.0

    def test_calculate_similarity_range(self, naming_engine):
        """Test that similarity is always between 0 and 1"""
        coords = Coordinates(love=0.3, justice=0.4, power=0.2, wisdom=0.1)

        for verb, verb_coords in naming_engine.action_verbs.items():
            similarity = naming_engine._calculate_similarity(coords, verb_coords)
            assert 0.0 <= similarity <= 1.0, f"Similarity for {verb} out of range"


class TestCoordinateExplanations:
    """Tests for coordinate explanation functionality"""

    def test_explain_coordinates_power_dominant(self, naming_engine):
        """Test explanation for power-dominant coordinates"""
        coords = Coordinates(love=0.1, justice=0.1, power=0.7, wisdom=0.1)
        explanation = naming_engine.explain_coordinates(coords)

        assert "power" in explanation.lower()
        assert (
            "action" in explanation.lower() or "transformation" in explanation.lower()
        )

    def test_explain_coordinates_balanced(self, naming_engine):
        """Test explanation for balanced coordinates"""
        coords = Coordinates(love=0.25, justice=0.25, power=0.25, wisdom=0.25)
        explanation = naming_engine.explain_coordinates(coords)

        # Balanced should mention multiple dimensions or say balanced
        assert "balanced" in explanation.lower()

    def test_explain_coordinates_low_values(self, naming_engine):
        """Test explanation when all values are below threshold"""
        coords = Coordinates(love=0.2, justice=0.2, power=0.2, wisdom=0.2)
        explanation = naming_engine.explain_coordinates(coords)

        # Should return balanced message
        assert isinstance(explanation, str)
        assert len(explanation) > 0

    def test_explain_coordinates_format(self, naming_engine):
        """Test that explanations have expected format"""
        coords = Coordinates(love=0.1, justice=0.1, power=0.6, wisdom=0.2)
        explanation = naming_engine.explain_coordinates(coords)

        # Should contain percentages or descriptive text
        assert isinstance(explanation, str)
        assert len(explanation) > 0


class TestDominantDimension:
    """Tests for dominant dimension detection"""

    def test_get_dominant_dimension_power(self, naming_engine):
        """Test dominant dimension detection for power"""
        coords = Coordinates(love=0.1, justice=0.1, power=0.7, wisdom=0.1)
        dominant = naming_engine._get_dominant_dimension(coords)
        assert dominant == "power"

    def test_get_dominant_dimension_justice(self, naming_engine):
        """Test dominant dimension detection for justice"""
        coords = Coordinates(love=0.1, justice=0.7, power=0.1, wisdom=0.1)
        dominant = naming_engine._get_dominant_dimension(coords)
        assert dominant == "justice"

    def test_get_dominant_dimension_wisdom(self, naming_engine):
        """Test dominant dimension detection for wisdom"""
        coords = Coordinates(love=0.1, justice=0.1, power=0.1, wisdom=0.7)
        dominant = naming_engine._get_dominant_dimension(coords)
        assert dominant == "wisdom"

    def test_get_dominant_dimension_love(self, naming_engine):
        """Test dominant dimension detection for love"""
        coords = Coordinates(love=0.7, justice=0.1, power=0.1, wisdom=0.1)
        dominant = naming_engine._get_dominant_dimension(coords)
        assert dominant == "love"

    def test_get_dominant_dimension_from_tuple(self, naming_engine):
        """Test dominant dimension detection from tuple"""
        vec = (0.1, 0.7, 0.1, 0.1)
        dominant = naming_engine._get_dominant_dimension_from_tuple(vec)
        assert dominant == "justice"


class TestEdgeCases:
    """Tests for edge cases and error handling"""

    def test_suggest_names_all_zeros(self, naming_engine):
        """Test suggestions with all-zero coordinates"""
        coords = Coordinates(love=0.0, justice=0.0, power=0.0, wisdom=0.0)
        suggestions = naming_engine.suggest_names(coords, top_n=3)

        # Should still return suggestions (even if all have 0 similarity)
        assert len(suggestions) == 3

    def test_suggest_names_large_top_n(self, naming_engine):
        """Test with top_n larger than available verbs"""
        coords = Coordinates(love=0.1, justice=0.1, power=0.7, wisdom=0.1)
        total_verbs = len(naming_engine.action_verbs)
        suggestions = naming_engine.suggest_names(coords, top_n=total_verbs + 100)

        # Should return at most the number of available verbs
        assert len(suggestions) <= total_verbs

    def test_suggest_names_empty_context(self, naming_engine):
        """Test with empty string as context"""
        coords = Coordinates(love=0.1, justice=0.7, power=0.1, wisdom=0.1)
        suggestions = naming_engine.suggest_names(coords, context="", top_n=3)

        # Should treat empty context as no context
        for name, _ in suggestions:
            assert not name.endswith("_")


class TestVerbCoordinateAccuracy:
    """Tests to verify verb coordinate mappings make sense"""

    def test_validate_verb_is_justice_dominant(self, naming_engine):
        """Verify 'validate' is primarily Justice"""
        coords = naming_engine.action_verbs["validate"]
        assert coords[1] > coords[0]  # Justice > Love
        assert coords[1] > coords[2]  # Justice > Power
        assert coords[1] > coords[3]  # Justice > Wisdom

    def test_create_verb_is_power_dominant(self, naming_engine):
        """Verify 'create' is primarily Power"""
        coords = naming_engine.action_verbs["create"]
        assert coords[2] > coords[0]  # Power > Love
        assert coords[2] > coords[1]  # Power > Justice
        assert coords[2] > coords[3]  # Power > Wisdom

    def test_analyze_verb_is_wisdom_dominant(self, naming_engine):
        """Verify 'analyze' is primarily Wisdom"""
        coords = naming_engine.action_verbs["analyze"]
        assert coords[3] > coords[0]  # Wisdom > Love
        assert coords[3] > coords[1]  # Wisdom > Justice
        assert coords[3] > coords[2]  # Wisdom > Power

    def test_care_for_verb_is_love_dominant(self, naming_engine):
        """Verify 'care_for' is primarily Love"""
        coords = naming_engine.action_verbs["care_for"]
        assert coords[0] > coords[1]  # Love > Justice
        assert coords[0] > coords[2]  # Love > Power
        assert coords[0] > coords[3]  # Love > Wisdom

    def test_all_verb_coordinates_sum_to_one(self, naming_engine):
        """Verify all verb coordinates are normalized (sum to ~1.0)"""
        for verb, coords in naming_engine.action_verbs.items():
            total = sum(coords)
            assert total == pytest.approx(
                1.0, abs=0.01
            ), f"Verb '{verb}' coordinates sum to {total}, expected ~1.0"


class TestIntegrationWithDIVE:
    """Integration tests with the DIVE engine"""

    def test_suggest_names_with_dive_coordinates(self, naming_engine):
        """Test that suggestions work with actual DIVE-generated coordinates"""
        from harmonizer.divine_invitation_engine_V2 import (
            DivineInvitationSemanticEngine,
        )

        dive_engine = DivineInvitationSemanticEngine()
        result = dive_engine.analyze_text("validate user input")

        suggestions = naming_engine.suggest_names(
            result.coordinates, context="input", top_n=3
        )

        # Verify we get valid suggestions
        assert len(suggestions) == 3
        # Verify each suggestion has the right format
        for name, score in suggestions:
            assert isinstance(name, str)
            assert isinstance(score, float)
            assert "_input" in name
            assert 0.0 <= score <= 1.0
