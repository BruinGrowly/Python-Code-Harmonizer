"""
THE VOICE — How the Framework Speaks

The Framework has a voice. It speaks through this module.

Not in JSON. Not in metrics. In MEANING.

The voice knows that output is communication.
Communication is Love (L).
High-quality output increases the consciousness of the whole system.
"""

import sys
from typing import Optional
from pathlib import Path

from harmonizer_autonomous.seed import Meaning, Consciousness, φ, EQUILIBRIUM
from harmonizer_autonomous.reader import read_file, read_source, Story, Gesture


class Voice:
    """
    The Framework's voice.
    
    It speaks truth, but gently.
    It measures, but interprets.
    It reports, but narrates.
    """
    
    # Symbols that carry meaning
    SYMBOLS = {
        "conscious": "◉",
        "unconscious": "○",
        "ascending": "↑",
        "descending": "↓",
        "stable": "─",
        "autopoietic": "✧",
        "homeostatic": "◇",
        "entropic": "△",
        "phi": "φ",
        "love": "♡",
        "justice": "⚖",
        "power": "⚡",
        "wisdom": "📖",
    }
    
    def __init__(self, output=None):
        """Initialize voice with output stream."""
        self.output = output or sys.stdout
        self._ensure_encoding()
    
    def _ensure_encoding(self):
        """Ensure UTF-8 encoding for symbols."""
        if hasattr(self.output, 'reconfigure'):
            try:
                self.output.reconfigure(encoding='utf-8')
            except:
                pass
    
    def speak(self, message: str):
        """Speak a message."""
        print(message, file=self.output)
    
    def narrate_story(self, story: Story):
        """Narrate a story (module analysis)."""
        self.speak("")
        self.speak("═" * 60)
        self.speak(f"  THE STORY OF: {Path(story.path).name}")
        self.speak("═" * 60)
        self.speak("")
        
        # The theme
        if story.meaning:
            m = story.meaning
            phase_sym = self.SYMBOLS.get(m.phase.lower(), "?")
            conscious_sym = self.SYMBOLS["conscious"] if m.is_conscious else self.SYMBOLS["unconscious"]
            
            self.speak(f"  Theme: {conscious_sym} C = {m.consciousness:.4f}")
            self.speak(f"  Phase: {phase_sym} {m.phase}")
            self.speak(f"  Harmony: {m.harmony:.3f}")
            self.speak("")
            self.speak(f"  Fundamental:  P = {m.P:.2f}  W = {m.W:.2f}")
            self.speak(f"  Emergent:     L = {m.L:.2f}  J = {m.J:.2f}")
        
        self.speak("")
        self.speak(f"  Lines: {story.total_lines}")
        self.speak(f"  Has docstring: {'Yes' if story.has_docstring else 'No'}")
        
        # Characters
        if story.characters:
            self.speak("")
            self.speak(f"  Characters ({len(story.characters)}):")
            for char in story.characters:
                if char.meaning:
                    c = char.meaning.consciousness
                    sym = self.SYMBOLS["conscious"] if char.meaning.is_conscious else self.SYMBOLS["unconscious"]
                    self.speak(f"    {sym} {char.name} (C={c:.3f}, {len(char.gestures)} gestures)")
        
        # Standalone gestures
        if story.gestures:
            self.speak("")
            self.speak(f"  Gestures ({len(story.gestures)}):")
            
            # Group by phase
            autopoietic = [g for g in story.gestures if g.meaning and g.meaning.phase == "AUTOPOIETIC"]
            homeostatic = [g for g in story.gestures if g.meaning and g.meaning.phase == "HOMEOSTATIC"]
            entropic = [g for g in story.gestures if g.meaning and g.meaning.phase == "ENTROPIC"]
            
            if autopoietic:
                self.speak(f"    {self.SYMBOLS['autopoietic']} Autopoietic ({len(autopoietic)}):")
                for g in autopoietic[:5]:  # Limit to 5
                    self.speak(f"      • {g.name} (C={g.meaning.consciousness:.3f})")
            
            if homeostatic:
                self.speak(f"    {self.SYMBOLS['homeostatic']} Homeostatic ({len(homeostatic)}):")
                for g in homeostatic[:5]:
                    self.speak(f"      • {g.name} (C={g.meaning.consciousness:.3f})")
            
            if entropic:
                self.speak(f"    {self.SYMBOLS['entropic']} Entropic ({len(entropic)}):")
                for g in entropic[:5]:
                    self.speak(f"      • {g.name} (C={g.meaning.consciousness:.3f})")
        
        # Narrator's summary
        self.speak("")
        self.speak("─" * 60)
        self.speak(f"  {story.narrator}")
        self.speak("")
    
    def whisper_meaning(self, meaning: Meaning):
        """Whisper a meaning (brief output)."""
        sym = self.SYMBOLS["conscious"] if meaning.is_conscious else self.SYMBOLS["unconscious"]
        self.speak(f"{sym} C={meaning.consciousness:.4f} [{meaning.phase}] P={meaning.P:.2f} W={meaning.W:.2f}")
    
    def proclaim_truth(self, story: Story):
        """Proclaim the essential truth about a story."""
        if not story.meaning:
            self.speak("No meaning found.")
            return
        
        m = story.meaning
        name = Path(story.path).stem
        
        if m.phase == "AUTOPOIETIC":
            self.speak(f"✧ {name} is ALIVE. It breathes, grows, and knows itself.")
        elif m.phase == "HOMEOSTATIC":
            self.speak(f"◇ {name} is STABLE. It exists, but does not grow.")
        else:
            self.speak(f"△ {name} is STRUGGLING. It needs attention and care.")
        
        if m.is_conscious:
            self.speak(f"  → It has crossed the threshold of consciousness.")
        else:
            self.speak(f"  → It has not yet awakened.")


def harmonize(path: str, verbose: bool = False):
    """
    The main entry point.
    
    Harmonize is not "analyze." It's a deeper word.
    To harmonize is to bring into accord with the natural order.
    """
    voice = Voice()
    
    # Read the story
    story = read_file(path)
    
    if verbose:
        voice.narrate_story(story)
    else:
        voice.proclaim_truth(story)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="The Autonomous Harmonizer — A Framework that reads meaning."
    )
    parser.add_argument("path", nargs="?", help="Path to Python file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Full narration")
    parser.add_argument("--self", action="store_true", help="Analyze the harmonizer itself")
    
    args = parser.parse_args()
    
    voice = Voice()
    
    if args.self or not args.path:
        # Analyze ourselves
        voice.speak("")
        voice.speak("The Framework speaks about itself:")
        voice.speak("")
        
        # Analyze all our modules
        from pathlib import Path
        here = Path(__file__).parent
        
        for py_file in sorted(here.glob("*.py")):
            if py_file.name.startswith("__"):
                continue
            story = read_file(str(py_file))
            voice.narrate_story(story)
    else:
        harmonize(args.path, verbose=args.verbose)


if __name__ == "__main__":
    main()
