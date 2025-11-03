#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Map Generator for Python Code Harmonizer

Visualizes the semantic trajectory from Intent to Execution in 4D space,
showing WHERE in the Meaning Scaffold the disharmony occurs.
"""

from typing import Dict, Tuple
from .divine_invitation_engine_V2 import Coordinates


class SemanticMapGenerator:
    """
    Generates semantic trajectory maps showing how execution drifts
    from intent across the 4D semantic space (Love, Justice, Power, Wisdom).
    """

    # Dimension interpretations for human-readable explanations
    DIMENSION_MEANINGS = {
        "love": "connection, communication, relationship-building, empathy",
        "justice": "ordering, enforcement, judgment, deletion, structure",
        "power": "transformation, control, execution, force, action",
        "wisdom": "analysis, understanding, reflection, knowledge, insight",
    }

    # Behavior keywords associated with each dimension
    DIMENSION_BEHAVIORS = {
        "love": ["send", "notify", "connect", "relate", "share", "communicate"],
        "justice": ["delete", "remove", "enforce", "judge", "order", "validate"],
        "power": ["execute", "transform", "control", "modify", "change", "process"],
        "wisdom": ["analyze", "understand", "calculate", "evaluate", "learn", "assess"],
    }

    def __init__(self):
        """Initialize the semantic map generator."""
        pass

    def generate_map(self, ice_result: Dict, function_name: str) -> Dict:
        """
        Generate a complete semantic map from ICE analysis results.

        Args:
            ice_result: The ICE analysis result from DIVE-V2
            function_name: Name of the function being analyzed

        Returns:
            Dictionary containing semantic map data
        """
        intent = ice_result["ice_components"]["intent"]
        execution = ice_result["ice_components"]["execution"]

        intent_coords = intent.coordinates
        exec_coords = execution.coordinates

        # Calculate dimensional deltas
        deltas = self._calculate_deltas(intent_coords, exec_coords)

        # Identify dominant dimensions
        intent_dominant = self._get_dominant_dimension(intent_coords)
        exec_dominant = self._get_dominant_dimension(exec_coords)

        # Find primary misalignment
        primary_misalignment = self._find_primary_misalignment(deltas)

        # Generate trajectory description
        trajectory = self._generate_trajectory(intent_dominant, exec_dominant)

        # Generate interpretation
        interpretation = self._generate_interpretation(
            intent_dominant, exec_dominant, deltas, function_name
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            intent_dominant, exec_dominant, function_name
        )

        return {
            "function_name": function_name,
            "intent": {
                "coordinates": {
                    "love": intent_coords.love,
                    "justice": intent_coords.justice,
                    "power": intent_coords.power,
                    "wisdom": intent_coords.wisdom,
                },
                "dominant_dimension": intent_dominant,
                "interpretation": self.DIMENSION_MEANINGS[intent_dominant.lower()],
            },
            "execution": {
                "coordinates": {
                    "love": exec_coords.love,
                    "justice": exec_coords.justice,
                    "power": exec_coords.power,
                    "wisdom": exec_coords.wisdom,
                },
                "dominant_dimension": exec_dominant,
                "interpretation": self.DIMENSION_MEANINGS[exec_dominant.lower()],
            },
            "trajectory": {
                "vector": trajectory,
                "deltas": deltas,
                "primary_misalignment": primary_misalignment,
            },
            "interpretation": interpretation,
            "recommendations": recommendations,
        }

    def _calculate_deltas(
        self, intent_coords: Coordinates, exec_coords: Coordinates
    ) -> Dict[str, float]:
        """Calculate per-dimension deltas from intent to execution."""
        return {
            "love": exec_coords.love - intent_coords.love,
            "justice": exec_coords.justice - intent_coords.justice,
            "power": exec_coords.power - intent_coords.power,
            "wisdom": exec_coords.wisdom - intent_coords.wisdom,
        }

    def _get_dominant_dimension(self, coords: Coordinates) -> str:
        """Identify which dimension has the highest value."""
        dims = {
            "Love": coords.love,
            "Justice": coords.justice,
            "Power": coords.power,
            "Wisdom": coords.wisdom,
        }
        return max(dims.items(), key=lambda x: x[1])[0]

    def _find_primary_misalignment(self, deltas: Dict[str, float]) -> Dict:
        """Find the dimension with the largest absolute change."""
        largest = max(deltas.items(), key=lambda x: abs(x[1]))
        return {
            "dimension": largest[0],
            "magnitude": abs(largest[1]),
            "direction": "increase" if largest[1] > 0 else "decrease",
            "delta": largest[1],
        }

    def _generate_trajectory(self, intent_dim: str, exec_dim: str) -> str:
        """Generate a trajectory description."""
        if intent_dim == exec_dim:
            return f"{intent_dim} (aligned)"
        return f"{intent_dim} → {exec_dim}"

    def _generate_interpretation(
        self,
        intent_dim: str,
        exec_dim: str,
        deltas: Dict[str, float],
        function_name: str,
    ) -> str:
        """Generate human-readable interpretation of the semantic drift."""
        if intent_dim == exec_dim:
            # Check for significant deltas even if dominant dimension is the same
            significant_deltas = [
                (dim, delta) for dim, delta in deltas.items() if abs(delta) > 0.3
            ]
            if significant_deltas:
                changes = ", ".join(
                    [
                        f"{dim.capitalize()} {'increased' if delta > 0 else 'decreased'}"
                        for dim, delta in significant_deltas
                    ]
                )
                return f"Function '{function_name}' operates primarily in {intent_dim} domain, but shows significant drift: {changes}."
            return f"Function '{function_name}' is semantically aligned in {intent_dim} domain."

        # Different dominant dimensions
        intent_meaning = self.DIMENSION_MEANINGS[intent_dim.lower()]
        exec_meaning = self.DIMENSION_MEANINGS[exec_dim.lower()]

        return (
            f"Function name '{function_name}' suggests {intent_dim} domain "
            f"({intent_meaning}), but execution operates in {exec_dim} domain "
            f"({exec_meaning})."
        )

    def _generate_recommendations(
        self, intent_dim: str, exec_dim: str, function_name: str
    ) -> list:
        """Generate actionable recommendations based on semantic drift."""
        recommendations = []

        if intent_dim == exec_dim:
            recommendations.append(
                f"✓ Function is semantically aligned in {intent_dim} domain"
            )
            return recommendations

        # Get expected vs actual behaviors
        intent_behaviors = self.DIMENSION_BEHAVIORS.get(intent_dim.lower(), [])
        exec_behaviors = self.DIMENSION_BEHAVIORS.get(exec_dim.lower(), [])

        recommendations.append(
            f"Consider renaming to reflect {exec_dim} domain operations"
        )

        recommendations.append(f"Expected behaviors: {', '.join(intent_behaviors[:3])}")

        recommendations.append(f"Actual behaviors: {', '.join(exec_behaviors[:3])}")

        # Suggest split if mixing concerns
        if intent_dim != exec_dim:
            recommendations.append(
                f"Or split into separate functions: one for {intent_dim}, one for {exec_dim}"
            )

        return recommendations

    def format_text_map(self, semantic_map: Dict, disharmony_score: float) -> str:
        """
        Format the semantic map as human-readable text.

        Args:
            semantic_map: The semantic map data
            disharmony_score: The disharmony score

        Returns:
            Formatted text visualization
        """
        lines = []
        lines.append("")
        lines.append("📍 SEMANTIC TRAJECTORY MAP:")
        lines.append("┌" + "─" * 70 + "┐")
        lines.append(
            "│ Dimension    Intent   Execution   Δ        Interpretation       │"
        )
        lines.append("├" + "─" * 70 + "┤")

        deltas = semantic_map["trajectory"]["deltas"]
        intent_coords = semantic_map["intent"]["coordinates"]
        exec_coords = semantic_map["execution"]["coordinates"]

        for dim in ["love", "justice", "power", "wisdom"]:
            delta = deltas[dim]
            intent_val = intent_coords[dim]
            exec_val = exec_coords[dim]

            # Format delta with sign
            delta_str = f"{delta:+.2f}"

            # Determine interpretation
            if abs(delta) > 0.5:
                interp = "⚠️  Major shift"
            elif abs(delta) > 0.3:
                interp = "⚡ Notable drift"
            elif abs(delta) > 0.1:
                interp = "~ Minor variance"
            else:
                interp = "✓ Aligned"

            # Format dimension name
            dim_name = f"{dim.capitalize()} ({dim[0].upper()})"

            line = f"│ {dim_name:12} {intent_val:.2f}  →  {exec_val:.2f}     {delta_str:6}   {interp:20} │"
            lines.append(line)

        lines.append("└" + "─" * 70 + "┘")
        lines.append("")
        lines.append("🧭 DISHARMONY VECTOR:")
        lines.append(f"   {semantic_map['trajectory']['vector']}")
        lines.append("")
        lines.append("💡 INTERPRETATION:")
        lines.append(f"   {semantic_map['interpretation']}")
        lines.append("")
        lines.append("🔧 RECOMMENDATIONS:")
        for rec in semantic_map["recommendations"]:
            lines.append(f"   • {rec}")

        return "\n".join(lines)

    def format_compact_map(self, semantic_map: Dict) -> str:
        """
        Format a compact version of the semantic map for brief output.

        Args:
            semantic_map: The semantic map data

        Returns:
            Compact formatted text
        """
        trajectory = semantic_map["trajectory"]["vector"]
        primary = semantic_map["trajectory"]["primary_misalignment"]

        return (
            f"   Trajectory: {trajectory} | "
            f"Primary drift: {primary['dimension'].capitalize()} "
            f"({primary['delta']:+.2f})"
        )
