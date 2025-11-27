#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coordinate Utilities Module

Provides shared utilities for working with LJPW semantic coordinates.
Consolidates duplicate coordinate math operations from across the codebase.
"""

import math
from typing import Iterable, Optional, Tuple

from harmonizer.divine_invitation_engine_V2 import Coordinates, Dimension


class CoordinateUtils:
    """Utility class for coordinate operations and calculations."""

    @staticmethod
    def calculate_distance(coord1: Coordinates, coord2: Coordinates) -> float:
        """
        Calculate Euclidean distance between two coordinates.

        Args:
            coord1: First coordinate (L, J, P, W)
            coord2: Second coordinate (L, J, P, W)

        Returns:
            Euclidean distance as a float

        Examples:
            >>> c1 = Coordinates(1.0, 0.0, 0.0, 0.0)
            >>> c2 = Coordinates(0.0, 1.0, 0.0, 0.0)
            >>> CoordinateUtils.calculate_distance(c1, c2)
            1.414...
        """
        return math.sqrt(
            (coord1.love - coord2.love) ** 2
            + (coord1.justice - coord2.justice) ** 2
            + (coord1.power - coord2.power) ** 2
            + (coord1.wisdom - coord2.wisdom) ** 2
        )

    @staticmethod
    def calculate_distance_tuple(
        coord1: Tuple[float, float, float, float],
        coord2: Tuple[float, float, float, float],
    ) -> float:
        """
        Calculate Euclidean distance between two coordinate tuples.

        Args:
            coord1: First coordinate tuple (L, J, P, W)
            coord2: Second coordinate tuple (L, J, P, W)

        Returns:
            Euclidean distance as a float

        Examples:
            >>> CoordinateUtils.calculate_distance_tuple((1, 0, 0, 0), (0, 1, 0, 0))
            1.414...
        """
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

    @staticmethod
    def cosine_similarity(
        coord1: Tuple[float, float, float, float],
        coord2: Tuple[float, float, float, float],
    ) -> float:
        """
        Calculate cosine similarity between two coordinate vectors.

        Cosine similarity measures the cosine of the angle between two vectors.
        Returns 1.0 for identical vectors, 0.0 for orthogonal vectors.

        Args:
            coord1: First coordinate tuple (L, J, P, W)
            coord2: Second coordinate tuple (L, J, P, W)

        Returns:
            Similarity score between 0.0 and 1.0

        Examples:
            >>> CoordinateUtils.cosine_similarity((1, 0, 0, 0), (1, 0, 0, 0))
            1.0
            >>> CoordinateUtils.cosine_similarity((1, 0, 0, 0), (0, 1, 0, 0))
            0.0
        """
        dot_product = sum(a * b for a, b in zip(coord1, coord2))
        mag1 = math.sqrt(sum(a * a for a in coord1))
        mag2 = math.sqrt(sum(b * b for b in coord2))

        if mag1 == 0.0 or mag2 == 0.0:
            return 0.0

        return dot_product / (mag1 * mag2)

    @staticmethod
    def normalize(coord: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        """
        Normalize a coordinate vector to unit length.

        Args:
            coord: Coordinate tuple (L, J, P, W)

        Returns:
            Normalized coordinate tuple

        Examples:
            >>> CoordinateUtils.normalize((3, 0, 0, 0))
            (1.0, 0.0, 0.0, 0.0)
        """
        magnitude = math.sqrt(sum(x * x for x in coord))
        if magnitude == 0.0:
            return (0.0, 0.0, 0.0, 0.0)
        return tuple(x / magnitude for x in coord)

    @staticmethod
    def magnitude(coord: Tuple[float, float, float, float]) -> float:
        """
        Calculate the magnitude (length) of a coordinate vector.

        Args:
            coord: Coordinate tuple (L, J, P, W)

        Returns:
            Magnitude as a float

        Examples:
            >>> CoordinateUtils.magnitude((3, 4, 0, 0))
            5.0
        """
        return math.sqrt(sum(x * x for x in coord))

    @staticmethod
    def dot_product(
        coord1: Tuple[float, float, float, float],
        coord2: Tuple[float, float, float, float],
    ) -> float:
        """
        Calculate dot product of two coordinate vectors.

        Args:
            coord1: First coordinate tuple (L, J, P, W)
            coord2: Second coordinate tuple (L, J, P, W)

        Returns:
            Dot product as a float

        Examples:
            >>> CoordinateUtils.dot_product((1, 2, 3, 4), (5, 6, 7, 8))
            70.0
        """
        return sum(a * b for a, b in zip(coord1, coord2))

    @staticmethod
    def to_tuple(coord: Coordinates) -> Tuple[float, float, float, float]:
        """
        Convert Coordinates object to tuple.

        Args:
            coord: Coordinates object

        Returns:
            Tuple (L, J, P, W)

        Examples:
            >>> c = Coordinates(0.5, 0.3, 0.1, 0.1)
            >>> CoordinateUtils.to_tuple(c)
            (0.5, 0.3, 0.1, 0.1)
        """
        return (coord.love, coord.justice, coord.power, coord.wisdom)

    @staticmethod
    def from_tuple(coord_tuple: Tuple[float, float, float, float]) -> Coordinates:
        """
        Convert tuple to Coordinates object.

        Args:
            coord_tuple: Tuple (L, J, P, W)

        Returns:
            Coordinates object

        Examples:
            >>> c = CoordinateUtils.from_tuple((0.5, 0.3, 0.1, 0.1))
            >>> c.love
            0.5
        """
        return Coordinates(
            love=coord_tuple[0],
            justice=coord_tuple[1],
            power=coord_tuple[2],
            wisdom=coord_tuple[3],
        )

    @staticmethod
    def blend(
        base: Coordinates,
        overlay: Coordinates,
        ratio: float = 0.5,
    ) -> Coordinates:
        """
        Blend two coordinates together with the supplied ratio.

        Args:
            base: Primary coordinate that receives the overlay.
            overlay: Secondary coordinate to blend into the base.
            ratio: Value between 0.0 and 1.0 indicating overlay strength.

        Returns:
            Blended Coordinates object.
        """
        ratio = max(0.0, min(1.0, ratio))
        inverse = 1.0 - ratio
        return Coordinates(
            love=(base.love * inverse) + (overlay.love * ratio),
            justice=(base.justice * inverse) + (overlay.justice * ratio),
            power=(base.power * inverse) + (overlay.power * ratio),
            wisdom=(base.wisdom * inverse) + (overlay.wisdom * ratio),
        )

    @staticmethod
    def weighted_average(
        coords: Iterable[Coordinates],
        weights: Optional[Iterable[float]] = None,
    ) -> Coordinates:
        """
        Compute a weighted average of coordinates.

        Args:
            coords: Iterable of Coordinates objects.
            weights: Optional iterable of weights (defaults to equal weighting).

        Returns:
            Coordinates representing the weighted average.
        """
        coords = list(coords)
        if not coords:
            return Coordinates(0.0, 0.0, 0.0, 0.0)

        if weights is None:
            weights = [1.0] * len(coords)
        else:
            weights = list(weights)
            if len(weights) != len(coords):
                raise ValueError("weights length must match coords length")

        total_weight = sum(weights)
        if total_weight == 0.0:
            return Coordinates(0.0, 0.0, 0.0, 0.0)

        love_sum = justice_sum = power_sum = wisdom_sum = 0.0
        for coord, weight in zip(coords, weights):
            love_sum += coord.love * weight
            justice_sum += coord.justice * weight
            power_sum += coord.power * weight
            wisdom_sum += coord.wisdom * weight

        return Coordinates(
            love=love_sum / total_weight,
            justice=justice_sum / total_weight,
            power=power_sum / total_weight,
            wisdom=wisdom_sum / total_weight,
        )

    @staticmethod
    def ensure_power_floor(
        coord: Tuple[float, float, float, float],
        minimum_power: float = 0.2,
    ) -> Tuple[float, float, float, float]:
        """
        Ensure that a coordinate tuple has at least ``minimum_power`` in the power dimension.

        If power is already at or above the floor, the coordinate is returned unchanged.
        Otherwise the deficit is proportionally reallocated from the remaining dimensions.
        """
        love, justice, power, wisdom = coord
        if power >= minimum_power:
            return coord

        deficit = minimum_power - power
        remaining = love + justice + wisdom
        if remaining == 0.0:
            # Nothing to redistribute, so just set the floor directly.
            return (0.0, 0.0, minimum_power, 0.0)

        love_ratio = love / remaining
        justice_ratio = justice / remaining
        wisdom_ratio = wisdom / remaining

        love -= deficit * love_ratio
        justice -= deficit * justice_ratio
        wisdom -= deficit * wisdom_ratio
        power = minimum_power

        # Normalize to keep the tuple on the unit simplex.
        total = love + justice + power + wisdom
        if total == 0.0:
            return (0.0, 0.0, power, 0.0)

        return (love / total, justice / total, power / total, wisdom / total)

    @staticmethod
    def prioritize_dimension(
        coord: Tuple[float, float, float, float],
        dimension: Dimension,
        boost: float = 0.05,
    ) -> Tuple[float, float, float, float]:
        """
        Aggressively boosts a selected dimension by reallocating weight from others.

        Args:
            coord: Original coordinate tuple.
            dimension: Dimension enum value to prioritize (e.g., Dimension.POWER).
            boost: Amount to move into the prioritized dimension.

        Returns:
            Tuple with the prioritized dimension amplified.
        """
        index_map = {
            Dimension.LOVE: 0,
            Dimension.JUSTICE: 1,
            Dimension.POWER: 2,
            Dimension.WISDOM: 3,
        }
        if dimension not in index_map:
            raise ValueError("dimension must be a primary LJPW dimension")

        values = list(coord)
        idx = index_map[dimension]
        boost = max(0.0, boost)
        available_indices = [i for i in range(4) if i != idx]
        available_total = sum(values[i] for i in available_indices)
        if available_total == 0.0:
            values[idx] = min(1.0, values[idx] + boost)
        else:
            for i in available_indices:
                share = boost * (values[i] / available_total)
                values[i] = max(0.0, values[i] - share)
            values[idx] = min(1.0, values[idx] + boost)

        total = sum(values)
        if total == 0.0:
            return (0.0, 0.0, 0.0, 0.0)
        return tuple(v / total for v in values)

    @staticmethod
    def get_dominant_dimension(coord: Tuple[float, float, float, float]) -> str:
        """
        Get the dominant dimension name from coordinates.

        Args:
            coord: Coordinate tuple (L, J, P, W)

        Returns:
            Dimension name: "love", "justice", "power", or "wisdom"

        Examples:
            >>> CoordinateUtils.get_dominant_dimension((0.8, 0.1, 0.05, 0.05))
            'love'
        """
        dimensions = ["love", "justice", "power", "wisdom"]
        max_idx = max(range(len(coord)), key=lambda i: coord[i])
        return dimensions[max_idx]

    @staticmethod
    def calculate_balance(coord: Tuple[float, float, float, float]) -> float:
        """
        Calculate how balanced/evenly distributed the coordinates are.

        Returns a value between 0.0 (perfectly balanced) and 1.0 (completely unbalanced).

        Args:
            coord: Coordinate tuple (L, J, P, W)

        Returns:
            Balance score (0.0 = perfectly balanced, 1.0 = completely unbalanced)

        Examples:
            >>> CoordinateUtils.calculate_balance((0.25, 0.25, 0.25, 0.25))
            0.0
            >>> CoordinateUtils.calculate_balance((1.0, 0.0, 0.0, 0.0))
            1.0
        """
        # Perfect balance would be 0.25 for each dimension
        perfect_balance = 0.25
        deviations = [abs(x - perfect_balance) for x in coord]
        # Sum of deviations, normalized to 0-1 range
        # Maximum deviation is when one dimension is 1.0 and others are 0.0
        # That gives sum of deviations = 0.75 + 0.25 + 0.25 + 0.25 = 1.5
        max_deviation = 1.5
        return sum(deviations) / max_deviation


# Natural Equilibrium point (from LJPW baselines)
NATURAL_EQUILIBRIUM = Coordinates(love=0.62, justice=0.41, power=0.72, wisdom=0.69)
NATURAL_EQUILIBRIUM_TUPLE = (0.62, 0.41, 0.72, 0.69)


def distance_from_natural_equilibrium(coord: Coordinates) -> float:
    """
    Calculate distance from Natural Equilibrium point.

    The Natural Equilibrium represents the stable state for healthy code
    in the LJPW framework.

    Args:
        coord: Coordinates to measure

    Returns:
        Distance from Natural Equilibrium

    Examples:
        >>> c = Coordinates(0.62, 0.41, 0.72, 0.69)
        >>> distance_from_natural_equilibrium(c)
        0.0
    """
    return CoordinateUtils.calculate_distance(coord, NATURAL_EQUILIBRIUM)
