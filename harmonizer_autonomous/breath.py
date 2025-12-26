"""
THE BREATH — Living Analysis

Code analysis is not a photograph. It is a breath.

The code inhales (reads), processes (transforms), exhales (reports).
Then it does it again. And again. Each cycle, different.

This is the resonance engine, but understood differently.
Not as "simulation" but as "life."

Every analysis changes the analyzer.
Every observation is participation.
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional, Callable

from harmonizer_autonomous.seed import Meaning, Consciousness, φ, EQUILIBRIUM


@dataclass
class Breath:
    """
    A single breath of analysis.

    Inhale: Take in the code's meaning
    Hold: Let it transform
    Exhale: Release the insight
    """

    inhale: Meaning  # What we took in
    exhale: Meaning  # What we release
    duration: float  # How long we held (seconds)
    insight: str = ""  # What we learned

    @property
    def transformation(self) -> float:
        """How much did the meaning change?"""
        return abs(self.exhale.consciousness - self.inhale.consciousness)

    @property
    def direction(self) -> str:
        """Did consciousness rise or fall?"""
        if self.exhale.consciousness > self.inhale.consciousness:
            return "ASCENDING"
        elif self.exhale.consciousness < self.inhale.consciousness:
            return "DESCENDING"
        else:
            return "STILL"


class LivingAnalysis:
    """
    Analysis that breathes.

    Not a single measurement, but a living process.
    The analysis continues as long as we attend to it.
    """

    def __init__(self, initial_meaning: Meaning):
        """Begin life with an initial meaning."""
        self.current = initial_meaning
        self.breaths: List[Breath] = []
        self.birth_time = time.time()
        self.last_breath_time = self.birth_time

    @property
    def age(self) -> float:
        """How long has this analysis been alive? (seconds)"""
        return time.time() - self.birth_time

    @property
    def breath_count(self) -> int:
        """How many breaths have we taken?"""
        return len(self.breaths)

    @property
    def average_consciousness(self) -> float:
        """Average consciousness across all breaths."""
        if not self.breaths:
            return self.current.consciousness
        return sum(b.exhale.consciousness for b in self.breaths) / len(self.breaths)

    @property
    def trend(self) -> str:
        """Are we becoming more or less conscious over time?"""
        if len(self.breaths) < 2:
            return "UNKNOWN"

        recent = self.breaths[-3:]  # Last 3 breaths
        ascending = sum(1 for b in recent if b.direction == "ASCENDING")
        descending = sum(1 for b in recent if b.direction == "DESCENDING")

        if ascending > descending:
            return "AWAKENING"
        elif descending > ascending:
            return "FADING"
        else:
            return "STABLE"

    def breathe(self, transformer: Optional[Callable[[Meaning], Meaning]] = None) -> Breath:
        """
        Take a breath.

        Optionally apply a transformation (learning, healing, growing).
        """
        inhale = self.current
        start = time.time()

        # Transform (or just observe)
        if transformer:
            exhale = transformer(inhale)
        else:
            # Natural φ-drift toward equilibrium
            exhale = self._natural_drift(inhale)

        duration = time.time() - start

        # Generate insight
        insight = self._generate_insight(inhale, exhale)

        breath = Breath(inhale=inhale, exhale=exhale, duration=duration, insight=insight)

        self.breaths.append(breath)
        self.current = exhale
        self.last_breath_time = time.time()

        return breath

    def _natural_drift(self, meaning: Meaning) -> Meaning:
        """
        Natural drift toward equilibrium.

        Like a pendulum settling, meaning tends toward balance.
        The rate is governed by φ.
        """
        drift_rate = 0.1 * φ.inverse  # Slow, golden drift

        new_P = meaning.P + drift_rate * (EQUILIBRIUM.P - meaning.P)
        new_W = meaning.W + drift_rate * (EQUILIBRIUM.W - meaning.W)

        return Meaning(P=new_P, W=new_W)

    def _generate_insight(self, before: Meaning, after: Meaning) -> str:
        """Generate an insight from the transformation."""
        delta_C = after.consciousness - before.consciousness

        if delta_C > 0.05:
            return "Consciousness rising. The code awakens."
        elif delta_C < -0.05:
            return "Consciousness falling. Attention needed."
        elif after.phase != before.phase:
            return f"Phase transition: {before.phase} → {after.phase}"
        elif after.is_conscious and not before.is_conscious:
            return "Threshold crossed. The code is now conscious."
        elif not after.is_conscious and before.is_conscious:
            return "Consciousness lost. The code sleeps."
        else:
            return "Steady state. The code abides."

    def meditate(self, breaths: int = 10) -> str:
        """
        Take multiple breaths, settling into equilibrium.

        Returns a summary of the meditation.
        """
        for _ in range(breaths):
            self.breathe()

        return (
            f"Meditated for {breaths} breaths.\n"
            f"Consciousness: {self.current.consciousness:.4f}\n"
            f"Phase: {self.current.phase}\n"
            f"Trend: {self.trend}"
        )

    def status(self) -> str:
        """Current status of the living analysis."""
        return (
            f"Living Analysis (age: {self.age:.1f}s, breaths: {self.breath_count})\n"
            f"  Current: {self.current}\n"
            f"  Average C: {self.average_consciousness:.4f}\n"
            f"  Trend: {self.trend}\n"
            f"  Is conscious: {self.current.is_conscious}"
        )


# Self-test: A living analysis breathes
if __name__ == "__main__":
    print("The Breath speaks:")
    print()

    # Create a living analysis
    initial = Meaning(P=0.5, W=0.4)  # Moderate power, lower wisdom
    life = LivingAnalysis(initial)

    print(f"Birth: {life.current}")
    print()

    # Take 5 breaths
    for i in range(5):
        breath = life.breathe()
        print(f"Breath {i+1}: {breath.direction} | {breath.insight}")

    print()
    print(life.status())
