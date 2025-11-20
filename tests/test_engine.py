# tests/test_engine.py

import pytest

from harmonizer.divine_invitation_engine_V2 import (
    Coordinates,
    DivineInvitationSemanticEngine,
)


@pytest.fixture(scope="module")
def engine():
    """Provides a single instance of the engine for all tests in this module."""
    return DivineInvitationSemanticEngine()


def test_engine_initialization(engine):
    """Tests that the engine and its components are initialized correctly."""
    assert engine is not None
    assert engine.get_engine_version() == "DIVE-V2 (Optimized Production)"
    assert engine.ANCHOR_POINT == Coordinates(1.0, 1.0, 1.0, 1.0)
    assert engine.vocabulary is not None
    assert engine.semantic_analyzer is not None
    assert len(engine.vocabulary.all_keywords) > 0


def test_vocabulary_manager_all_keywords(engine):
    """Tests that the all_keywords property returns a comprehensive set of strings."""
    keywords = engine.vocabulary.all_keywords
    assert isinstance(keywords, set)
    assert "love" in keywords
    assert "justice" in keywords
    assert "power" in keywords
    assert "wisdom" in keywords
    assert len(keywords) > 50  # Ensure it's not a trivial set


def test_analyze_text_single_concept(engine):
    """Tests the analysis of a single, clear concept."""
    coords, count = engine.vocabulary.analyze_text("love")
    assert count == 1
    assert coords.love == 1.0
    assert coords.justice == 0.0
    assert coords.power == 0.0
    assert coords.wisdom == 0.0


def test_analyze_text_mixed_concepts(engine):
    """Tests the analysis of a text with multiple concepts, expecting a blend."""
    coords, count = engine.vocabulary.analyze_text("love justice power wisdom")
    assert count == 4
    assert coords.love == pytest.approx(0.25)
    assert coords.justice == pytest.approx(0.25)
    assert coords.power == pytest.approx(0.25)
    assert coords.wisdom == pytest.approx(0.25)


def test_analyze_text_no_concepts(engine):
    """Tests that text with no known concepts returns zero coordinates."""
    coords, count = engine.vocabulary.analyze_text("xyz qwerty")
    assert count == 0
    assert coords == Coordinates(0.0, 0.0, 0.0, 0.0)


def test_get_distance_calculation(engine):
    """Tests the static distance calculation method."""
    c1 = Coordinates(0.0, 0.0, 0.0, 0.0)
    c2 = Coordinates(1.0, 0.0, 0.0, 0.0)
    assert engine.get_distance(c1, c2) == pytest.approx(1.0)

    c3 = Coordinates(1.0, 1.0, 1.0, 1.0)  # Anchor Point
    assert engine.get_distance(c1, c3) == pytest.approx(2.0)


def test_semantic_clarity(engine):
    """Tests the semantic clarity calculation."""
    # A "spiky" concept has high std dev, and thus low clarity.  # noqa: E501
    # The engine defines clarity as dimensional balance.
    specialized_concept = Coordinates(1.0, 0.0, 0.0, 0.0)
    assert engine.get_semantic_clarity(specialized_concept) == pytest.approx(0.13397, abs=1e-5)

    # A perfectly balanced concept has zero standard deviation, and thus perfect clarity.
    perfectly_balanced = Coordinates(0.25, 0.25, 0.25, 0.25)
    assert engine.get_semantic_clarity(perfectly_balanced) == pytest.approx(1.0)

    # An unbalanced concept, should have lower clarity than a perfectly balanced one.
    unbalanced = Coordinates(0.8, 0.2, 0.0, 0.0)
    assert engine.get_semantic_clarity(unbalanced) < 1.0


def test_semantic_analyzer_cluster(engine):
    """Tests the semantic analyzer's ability to find the centroid of a concept cluster."""
    concepts = ["love", "justice"]
    result = engine.perform_semantic_harmony_analysis(concepts)

    assert result.concept_count == 2
    # The centroid should be the average of (1,0,0,0) and (0,1,0,0)
    assert result.coordinates.love == pytest.approx(0.5)
    assert result.coordinates.justice == pytest.approx(0.5)
    assert result.coordinates.power == pytest.approx(0.0)
    assert result.coordinates.wisdom == pytest.approx(0.0)

    # Cohesion should be high for closely related concepts
    assert result.harmonic_cohesion > 0.5


def test_ice_analysis_highly_coherent(engine):
    """
    Tests ICE analysis for a coherent case where all concepts are in the same
    dimension.
    """  # noqa: E501
    result = engine.perform_ice_analysis(
        intent_words=["wisdom", "knowledge"],
        context_words=["science", "research"],
        execution_words=["analysis", "logic"],
    )

    assert "ice_metrics" in result
    disharmony = result["ice_metrics"]["intent_execution_disharmony"]
    harmony_level = result["ice_harmony_level"]

    # All concepts are pure Wisdom, so disharmony should be zero.
    assert disharmony == pytest.approx(0.0)

    # Coherence is perfect, but balance is low because pure concepts are
    # far from the (1,1,1,1) anchor. This should result in a "GOOD" score.
    assert harmony_level == "GOOD_ICE_BALANCE"
