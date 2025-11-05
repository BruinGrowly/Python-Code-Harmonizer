#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Semantic Naming Engine
Uses the validated mixing formula to suggest optimal function names.
"""

from typing import List, Tuple
from harmonizer.divine_invitation_engine_V2 import Coordinates
import math


class SemanticNamingEngine:
    """Suggests function names based on semantic coordinates"""

    def __init__(self):
        # Vocabulary of action verbs mapped to LJWP coordinates
        self.action_verbs = {
            # LOVE-dominant verbs (connection, care)
            'care_for': (0.9, 0.05, 0.05, 0.0),
            'support': (0.8, 0.1, 0.1, 0.0),
            'help': (0.8, 0.1, 0.1, 0.0),
            'nurture': (0.85, 0.1, 0.05, 0.0),
            'connect': (0.7, 0.2, 0.1, 0.0),
            'communicate': (0.7, 0.2, 0.05, 0.05),
            'share': (0.75, 0.15, 0.05, 0.05),
            'greet': (0.85, 0.05, 0.05, 0.05),
            'welcome': (0.8, 0.1, 0.05, 0.05),
            'notify': (0.6, 0.1, 0.2, 0.1),
            'inform': (0.65, 0.1, 0.15, 0.1),
            'collaborate': (0.7, 0.15, 0.1, 0.05),
            'synchronize': (0.5, 0.2, 0.2, 0.1),
            'merge': (0.4, 0.2, 0.3, 0.1),

            # JUSTICE-dominant verbs (validation, checking)
            'validate': (0.1, 0.8, 0.1, 0.0),
            'verify': (0.05, 0.75, 0.1, 0.1),
            'check': (0.05, 0.7, 0.15, 0.1),
            'enforce': (0.05, 0.7, 0.2, 0.05),
            'ensure': (0.1, 0.7, 0.15, 0.05),
            'audit': (0.05, 0.75, 0.05, 0.15),
            'inspect': (0.05, 0.65, 0.1, 0.2),
            'filter': (0.05, 0.7, 0.15, 0.1),
            'authorize': (0.05, 0.75, 0.15, 0.05),
            'authenticate': (0.05, 0.75, 0.15, 0.05),
            'certify': (0.05, 0.8, 0.1, 0.05),
            'confirm': (0.1, 0.75, 0.1, 0.05),
            'approve': (0.15, 0.7, 0.1, 0.05),
            'reject': (0.05, 0.75, 0.15, 0.05),
            'restrict': (0.05, 0.75, 0.15, 0.05),
            'allow': (0.15, 0.7, 0.1, 0.05),
            'deny': (0.05, 0.75, 0.15, 0.05),
            'compare': (0.05, 0.6, 0.1, 0.25),
            'match': (0.1, 0.65, 0.1, 0.15),

            # POWER-dominant verbs (action, transformation)
            'create': (0.05, 0.1, 0.8, 0.05),
            'build': (0.05, 0.1, 0.8, 0.05),
            'generate': (0.05, 0.1, 0.75, 0.1),
            'transform': (0.05, 0.1, 0.75, 0.1),
            'process': (0.05, 0.15, 0.7, 0.1),
            'execute': (0.05, 0.1, 0.8, 0.05),
            'perform': (0.05, 0.1, 0.75, 0.1),
            'modify': (0.05, 0.15, 0.7, 0.1),
            'update': (0.05, 0.15, 0.7, 0.1),
            'delete': (0.05, 0.15, 0.75, 0.05),
            'remove': (0.05, 0.15, 0.75, 0.05),
            'save': (0.05, 0.2, 0.65, 0.1),
            'store': (0.05, 0.2, 0.65, 0.1),
            'send': (0.15, 0.1, 0.65, 0.1),
            'insert': (0.05, 0.15, 0.75, 0.05),
            'append': (0.05, 0.15, 0.75, 0.05),
            'prepend': (0.05, 0.15, 0.75, 0.05),
            'replace': (0.05, 0.15, 0.75, 0.05),
            'overwrite': (0.05, 0.1, 0.8, 0.05),
            'clear': (0.05, 0.1, 0.8, 0.05),
            'reset': (0.05, 0.15, 0.75, 0.05),
            'initialize': (0.05, 0.15, 0.75, 0.05),
            'setup': (0.05, 0.15, 0.75, 0.05),
            'configure': (0.05, 0.2, 0.7, 0.05),
            'install': (0.05, 0.15, 0.75, 0.05),
            'uninstall': (0.05, 0.15, 0.75, 0.05),
            'deploy': (0.05, 0.2, 0.7, 0.05),
            'publish': (0.1, 0.15, 0.7, 0.05),
            'upload': (0.05, 0.1, 0.8, 0.05),
            'download': (0.05, 0.1, 0.8, 0.05),
            'import': (0.05, 0.1, 0.8, 0.05),
            'export': (0.05, 0.1, 0.8, 0.05),
            'render': (0.05, 0.1, 0.75, 0.1),
            'format': (0.05, 0.2, 0.7, 0.05),
            'sanitize': (0.05, 0.25, 0.65, 0.05),
            'normalize': (0.05, 0.25, 0.6, 0.1),
            'convert': (0.05, 0.15, 0.75, 0.05),
            'migrate': (0.05, 0.15, 0.75, 0.05),
            'sync': (0.1, 0.2, 0.65, 0.05),
            'refresh': (0.05, 0.1, 0.8, 0.05),
            'reload': (0.05, 0.1, 0.8, 0.05),
            'restart': (0.05, 0.1, 0.8, 0.05),
            'start': (0.05, 0.1, 0.8, 0.05),
            'stop': (0.05, 0.1, 0.8, 0.05),
            'pause': (0.05, 0.1, 0.8, 0.05),
            'resume': (0.05, 0.1, 0.8, 0.05),
            'cancel': (0.05, 0.15, 0.75, 0.05),
            'abort': (0.05, 0.15, 0.75, 0.05),
            'commit': (0.05, 0.2, 0.7, 0.05),
            'rollback': (0.05, 0.2, 0.7, 0.05),
            'backup': (0.05, 0.2, 0.7, 0.05),
            'restore': (0.05, 0.2, 0.7, 0.05),
            'archive': (0.05, 0.2, 0.7, 0.05),
            'compress': (0.05, 0.1, 0.8, 0.05),
            'decompress': (0.05, 0.1, 0.8, 0.05),
            'encrypt': (0.05, 0.2, 0.7, 0.05),
            'decrypt': (0.05, 0.2, 0.7, 0.05),
            'encode': (0.05, 0.15, 0.75, 0.05),
            'decode': (0.05, 0.15, 0.75, 0.05),
            'serialize': (0.05, 0.15, 0.75, 0.05),
            'deserialize': (0.05, 0.15, 0.75, 0.05),
            'parse': (0.05, 0.15, 0.6, 0.2),
            'compile': (0.05, 0.15, 0.7, 0.1),
            'optimize': (0.05, 0.2, 0.65, 0.1),

            # WISDOM-dominant verbs (analysis, understanding)
            'analyze': (0.05, 0.1, 0.1, 0.75),
            'calculate': (0.05, 0.15, 0.1, 0.7),
            'compute': (0.05, 0.15, 0.1, 0.7),
            'evaluate': (0.05, 0.2, 0.1, 0.65),
            'assess': (0.05, 0.2, 0.1, 0.65),
            'determine': (0.05, 0.2, 0.1, 0.65),
            'classify': (0.05, 0.25, 0.1, 0.6),
            'categorize': (0.05, 0.25, 0.1, 0.6),
            'predict': (0.05, 0.1, 0.15, 0.7),
            'infer': (0.05, 0.1, 0.1, 0.75),
            'learn': (0.1, 0.1, 0.1, 0.7),
            'understand': (0.15, 0.1, 0.05, 0.7),
            'recognize': (0.05, 0.15, 0.1, 0.7),
            'discover': (0.1, 0.1, 0.1, 0.7),
            'detect': (0.05, 0.2, 0.1, 0.65),
            'identify': (0.05, 0.2, 0.1, 0.65),
            'measure': (0.05, 0.2, 0.1, 0.65),
            'monitor': (0.05, 0.2, 0.1, 0.65),
            'track': (0.05, 0.2, 0.15, 0.6),
            'observe': (0.1, 0.15, 0.1, 0.65),
            'scan': (0.05, 0.15, 0.1, 0.7),
            'search': (0.05, 0.1, 0.15, 0.7),
            'find': (0.05, 0.1, 0.15, 0.7),
            'locate': (0.05, 0.1, 0.15, 0.7),
            'lookup': (0.05, 0.1, 0.15, 0.7),
            'query': (0.05, 0.15, 0.1, 0.7),
            'retrieve': (0.05, 0.1, 0.2, 0.65),
            'fetch': (0.05, 0.1, 0.2, 0.65),
            'get': (0.05, 0.1, 0.2, 0.65),
            'read': (0.05, 0.1, 0.15, 0.7),
            'extract': (0.05, 0.15, 0.2, 0.6),
            'aggregate': (0.05, 0.15, 0.15, 0.65),
            'summarize': (0.05, 0.1, 0.15, 0.7),
            'count': (0.05, 0.15, 0.1, 0.7),
            'rank': (0.05, 0.2, 0.1, 0.65),
            'sort': (0.05, 0.25, 0.15, 0.55),
            'order': (0.05, 0.25, 0.15, 0.55),
            'group': (0.05, 0.2, 0.15, 0.6),
            'partition': (0.05, 0.2, 0.15, 0.6),
            'split': (0.05, 0.15, 0.2, 0.6),
            'join': (0.05, 0.15, 0.2, 0.6),
            'correlate': (0.05, 0.15, 0.1, 0.7),
            'interpolate': (0.05, 0.15, 0.1, 0.7),
            'extrapolate': (0.05, 0.1, 0.15, 0.7),
            'estimate': (0.05, 0.15, 0.1, 0.7),
            'approximate': (0.05, 0.15, 0.1, 0.7),
            'model': (0.05, 0.15, 0.15, 0.65),
            'simulate': (0.05, 0.1, 0.15, 0.7),
            'test': (0.05, 0.3, 0.15, 0.5),
            'debug': (0.05, 0.25, 0.15, 0.55),
            'trace': (0.05, 0.2, 0.1, 0.65),
            'profile': (0.05, 0.2, 0.1, 0.65),
            'benchmark': (0.05, 0.25, 0.15, 0.55),

            # Mixed verbs
            'handle': (0.2, 0.3, 0.4, 0.1),  # Mixed: care + rules + action
            'manage': (0.15, 0.35, 0.4, 0.1),  # Justice + Power
            'coordinate': (0.3, 0.3, 0.3, 0.1),  # Balanced Love/Justice/Power
            'orchestrate': (0.2, 0.3, 0.4, 0.1),  # Similar to handle
            'dispatch': (0.1, 0.25, 0.6, 0.05),  # Power with Justice
            'route': (0.1, 0.3, 0.55, 0.05),  # Power with Justice
            'schedule': (0.05, 0.35, 0.55, 0.05),  # Justice + Power
            'queue': (0.05, 0.3, 0.6, 0.05),  # Justice + Power
            'enqueue': (0.05, 0.25, 0.65, 0.05),  # More Power
            'dequeue': (0.05, 0.25, 0.65, 0.05),  # More Power
            'push': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'pop': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'peek': (0.05, 0.1, 0.15, 0.7),  # Wisdom dominant
            'invoke': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'call': (0.1, 0.15, 0.7, 0.05),  # Power with Love
            'request': (0.15, 0.2, 0.6, 0.05),  # Power with Love
            'respond': (0.2, 0.15, 0.6, 0.05),  # Power with Love
            'reply': (0.25, 0.15, 0.55, 0.05),  # More Love
            'acknowledge': (0.3, 0.2, 0.45, 0.05),  # Love + Justice
            'log': (0.05, 0.2, 0.5, 0.25),  # Power + Wisdom
            'record': (0.05, 0.2, 0.5, 0.25),  # Power + Wisdom
            'register': (0.05, 0.25, 0.6, 0.1),  # Power + Justice
            'unregister': (0.05, 0.25, 0.6, 0.1),  # Power + Justice
            'subscribe': (0.15, 0.2, 0.6, 0.05),  # Power with Love
            'unsubscribe': (0.1, 0.2, 0.65, 0.05),  # Power dominant
            'listen': (0.2, 0.15, 0.5, 0.15),  # Love + Power + Wisdom
            'watch': (0.15, 0.2, 0.5, 0.15),  # Justice + Power + Wisdom
            'poll': (0.05, 0.2, 0.6, 0.15),  # Power + Wisdom
            'wait': (0.1, 0.15, 0.6, 0.15),  # Power + Wisdom
            'sleep': (0.05, 0.1, 0.8, 0.05),  # Power dominant
            'yield': (0.15, 0.2, 0.6, 0.05),  # Power with Love/Justice
            'return': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'raise': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'throw': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'catch': (0.1, 0.25, 0.6, 0.05),  # Power + Justice
            'resolve': (0.15, 0.3, 0.45, 0.1),  # Justice + Love + Power
            'fix': (0.1, 0.25, 0.6, 0.05),  # Power + Justice
            'repair': (0.15, 0.2, 0.6, 0.05),  # Power + Love
            'heal': (0.6, 0.15, 0.2, 0.05),  # Love dominant
            'clean': (0.05, 0.3, 0.6, 0.05),  # Power + Justice
            'purge': (0.05, 0.25, 0.65, 0.05),  # Power + Justice
            'flush': (0.05, 0.2, 0.7, 0.05),  # Power dominant
            'drain': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'fill': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'load': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'unload': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'open': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'close': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'lock': (0.05, 0.3, 0.6, 0.05),  # Justice + Power
            'unlock': (0.05, 0.3, 0.6, 0.05),  # Justice + Power
            'acquire': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'release': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'allocate': (0.05, 0.25, 0.65, 0.05),  # Power + Justice
            'deallocate': (0.05, 0.25, 0.65, 0.05),  # Power + Justice
            'reserve': (0.05, 0.3, 0.6, 0.05),  # Justice + Power
            'claim': (0.05, 0.3, 0.6, 0.05),  # Justice + Power
            'own': (0.1, 0.3, 0.55, 0.05),  # Justice + Power
            'grant': (0.2, 0.4, 0.35, 0.05),  # Justice + Love
            'revoke': (0.05, 0.4, 0.5, 0.05),  # Justice + Power
            'delegate': (0.2, 0.3, 0.45, 0.05),  # Love + Justice + Power
            'forward': (0.15, 0.2, 0.6, 0.05),  # Power with Love
            'redirect': (0.1, 0.25, 0.6, 0.05),  # Power + Justice
            'proxy': (0.1, 0.25, 0.6, 0.05),  # Power + Justice
            'wrap': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'unwrap': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'decorate': (0.1, 0.15, 0.7, 0.05),  # Power with Love
            'extend': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'implement': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'override': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'inherit': (0.1, 0.25, 0.6, 0.05),  # Power + Justice
            'compose': (0.05, 0.2, 0.65, 0.1),  # Power + Justice + Wisdom
            'combine': (0.1, 0.2, 0.65, 0.05),  # Power with Love
            'aggregate_data': (0.05, 0.2, 0.5, 0.25),  # Power + Wisdom
            'reduce': (0.05, 0.15, 0.6, 0.2),  # Power + Wisdom
            'map': (0.05, 0.15, 0.6, 0.2),  # Power + Wisdom
            'apply': (0.05, 0.15, 0.75, 0.05),  # Power dominant
            'bind': (0.1, 0.25, 0.6, 0.05),  # Power + Justice
            'unbind': (0.05, 0.25, 0.65, 0.05),  # Power + Justice
            'attach': (0.1, 0.2, 0.65, 0.05),  # Power with Love
            'detach': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'link': (0.15, 0.2, 0.6, 0.05),  # Love + Power
            'unlink': (0.05, 0.2, 0.7, 0.05),  # Power + Justice
            'associate': (0.2, 0.2, 0.55, 0.05),  # Love + Justice + Power
            'dissociate': (0.05, 0.25, 0.65, 0.05),  # Justice + Power
            'relate': (0.25, 0.2, 0.5, 0.05),  # Love + Justice + Power
            'correlate_data': (0.05, 0.2, 0.5, 0.25),  # Power + Wisdom
        }

        # Common object nouns for function names
        self.object_nouns = [
            'user', 'data', 'record', 'item', 'entity', 'resource',
            'file', 'document', 'message', 'request', 'response',
            'transaction', 'event', 'task', 'job', 'process',
            'config', 'settings', 'preferences', 'state', 'status'
        ]

    def suggest_names(
        self,
        coordinates: Coordinates,
        context: str = "",
        top_n: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Suggest function names based on semantic coordinates.

        Args:
            coordinates: The LJWP coordinates of the function's execution
            context: Optional context (e.g., "user", "data") for object nouns
            top_n: Number of suggestions to return

        Returns:
            List of (function_name, similarity_score) tuples
        """
        suggestions = []

        for verb, verb_coords in self.action_verbs.items():
            similarity = self._calculate_similarity(coordinates, verb_coords)

            # Generate function name
            if context:
                func_name = f"{verb}_{context}"
            else:
                func_name = verb

            suggestions.append((func_name, similarity))

        # Sort by similarity (higher is better)
        suggestions.sort(key=lambda x: x[1], reverse=True)

        return suggestions[:top_n]

    def suggest_with_multiple_objects(
        self,
        coordinates: Coordinates,
        top_verbs: int = 3,
        top_objects: int = 3
    ) -> List[Tuple[str, float, str]]:
        """
        Suggest function names by trying multiple verb-object combinations.

        Returns:
            List of (function_name, similarity_score, explanation) tuples
        """
        # Get top verbs
        verb_suggestions = []
        for verb, verb_coords in self.action_verbs.items():
            similarity = self._calculate_similarity(coordinates, verb_coords)
            verb_suggestions.append((verb, similarity, verb_coords))

        verb_suggestions.sort(key=lambda x: x[1], reverse=True)
        top_verbs_list = verb_suggestions[:top_verbs]

        # Generate combinations
        results = []
        for verb, similarity, verb_coords in top_verbs_list:
            for obj in self.object_nouns[:top_objects]:
                func_name = f"{verb}_{obj}"
                explanation = self._generate_explanation(coordinates, verb_coords)
                results.append((func_name, similarity, explanation))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _calculate_similarity(
        self,
        coords1: Coordinates,
        coords2: Tuple[float, float, float, float]
    ) -> float:
        """
        Calculate cosine similarity between two coordinate vectors.
        Returns value between 0 (opposite) and 1 (identical).
        """
        # Convert Coordinates to tuple if needed
        if isinstance(coords1, Coordinates):
            vec1 = (coords1.love, coords1.justice, coords1.power, coords1.wisdom)
        else:
            vec1 = coords1

        vec2 = coords2

        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        # Calculate magnitudes
        mag1 = math.sqrt(sum(a * a for a in vec1))
        mag2 = math.sqrt(sum(b * b for b in vec2))

        # Avoid division by zero
        if mag1 == 0 or mag2 == 0:
            return 0.0

        # Cosine similarity
        return dot_product / (mag1 * mag2)

    def _generate_explanation(
        self,
        execution_coords: Coordinates,
        verb_coords: Tuple[float, float, float, float]
    ) -> str:
        """Generate human-readable explanation of why this verb fits"""
        dominant = self._get_dominant_dimension(execution_coords)
        verb_dominant = self._get_dominant_dimension_from_tuple(verb_coords)

        if dominant == verb_dominant:
            return f"Strong {dominant} emphasis matches execution pattern"
        else:
            return f"Balances {dominant} execution with {verb_dominant} intent"

    def _get_dominant_dimension(self, coords: Coordinates) -> str:
        """Get the dominant dimension from coordinates"""
        values = {
            'love': coords.love,
            'justice': coords.justice,
            'power': coords.power,
            'wisdom': coords.wisdom
        }
        return max(values, key=values.get)

    def _get_dominant_dimension_from_tuple(
        self,
        coords: Tuple[float, float, float, float]
    ) -> str:
        """Get dominant dimension from tuple"""
        dimensions = ['love', 'justice', 'power', 'wisdom']
        max_idx = coords.index(max(coords))
        return dimensions[max_idx]

    def explain_coordinates(self, coordinates: Coordinates) -> str:
        """Generate human-readable explanation of semantic coordinates"""
        dims = {
            'love': (coordinates.love, 'connection/care'),
            'justice': (coordinates.justice, 'validation/order'),
            'power': (coordinates.power, 'action/transformation'),
            'wisdom': (coordinates.wisdom, 'analysis/understanding')
        }

        # Sort by value
        sorted_dims = sorted(dims.items(), key=lambda x: x[1][0], reverse=True)

        explanation_parts = []
        for dim_name, (value, meaning) in sorted_dims:
            if value > 0.3:
                percentage = int(value * 100)
                explanation_parts.append(f"{percentage}% {dim_name} ({meaning})")

        if not explanation_parts:
            return "Balanced across all dimensions"

        return "Function emphasizes: " + ", ".join(explanation_parts)


# Example usage
if __name__ == "__main__":
    engine = SemanticNamingEngine()

    # Test with a power-heavy function (e.g., data transformation)
    coords = Coordinates(love=0.1, justice=0.2, power=0.6, wisdom=0.1)

    print("Semantic coordinates:", coords)
    print("\nExplanation:", engine.explain_coordinates(coords))
    print("\nTop name suggestions:")

    suggestions = engine.suggest_names(coords, context="data", top_n=5)
    for name, score in suggestions:
        print(f"  {name:30s} (similarity: {score:.3f})")

    print("\n" + "="*60)
    print("Suggestions with multiple objects:")
    multi_suggestions = engine.suggest_with_multiple_objects(coords, top_verbs=3, top_objects=3)
    for name, score, explanation in multi_suggestions[:10]:
        print(f"  {name:30s} {score:.3f} - {explanation}")
