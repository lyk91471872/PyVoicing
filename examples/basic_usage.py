#!/usr/bin/env python3
"""Basic usage examples for PyVoicing."""

from pyvoicing import Pitch, Chroma, Interval, Voicing
from pyvoicing import C, E, G, Bb

def main():
    """Demonstrate basic PyVoicing usage."""
    
    # Create pitches
    c4 = Pitch('C', 4)  # C in octave 4
    e4 = Pitch('E', 4)  # E in octave 4
    g4 = Pitch('G', 4)  # G in octave 4
    
    # Alternative way to create pitches
    c4_alt = C(4)  # Same as Pitch('C', 4)
    e4_alt = E(4)  # Same as Pitch('E', 4)
    g4_alt = G(4)  # Same as Pitch('G', 4)
    
    # Create a C major chord
    c_major = Voicing(C(), [c4, e4, g4])
    print(f"C major chord: {c_major}")
    
    # Transpose up a perfect fifth
    g_major = c_major * "P5"  # or c_major >> "P5"
    print(f"G major chord (C transposed up P5): {g_major}")
    
    # Create a dominant 7th chord
    c_dom7 = Voicing(C(), [C(4), E(4), G(4), Bb(4)])
    print(f"C dominant 7th chord: {c_dom7}")
    
    # Analyze chord tones
    print(f"C major chord tones: {~c_major}")
    print(f"C dominant 7th chord tones: {~c_dom7}")
    
    # Interval operations
    m3 = Interval('m3')  # minor third
    p5 = Interval('P5')  # perfect fifth
    
    # Create a chord by adding intervals to a root
    c4_pitch = C(4)
    e4_pitch = c4_pitch * m3  # C4 + minor third = Eb4
    g4_pitch = c4_pitch * p5  # C4 + perfect fifth = G4
    
    c_minor = Voicing(C(), [c4_pitch, e4_pitch, g4_pitch])
    print(f"C minor chord: {c_minor}")
    
    # Compare chord qualities
    print(f"C minor chord tones: {~c_minor}")


if __name__ == "__main__":
    main() 