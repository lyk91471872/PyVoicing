#!/usr/bin/env python3
"""Basic tests for PyVoicing."""

import unittest
from pyvoicing import Pitch, Chroma, Interval, Voicing
from pyvoicing import C, E, G, Bb


class TestPitch(unittest.TestCase):
    """Test the Pitch class."""

    def test_creation(self):
        """Test pitch creation."""
        c4 = Pitch('C', 4)
        self.assertEqual(c4.name, 'C')
        self.assertEqual(c4.octave, 4)
        self.assertEqual(c4.offset, 0)
        self.assertEqual(c4.value, 60)

    def test_transposition(self):
        """Test pitch transposition."""
        c4 = Pitch('C', 4)
        g4 = c4 * 'P5'
        self.assertEqual(g4.name, 'G')
        self.assertEqual(g4.octave, 4)

        c5 = c4 * 12
        self.assertEqual(c5.name, 'C')
        self.assertEqual(c5.octave, 5)


class TestChroma(unittest.TestCase):
    """Test the Chroma class."""

    def test_creation(self):
        """Test chroma creation."""
        c = Chroma('C')
        self.assertEqual(c.offset, 0)
        self.assertEqual(str(c), 'C')

        c_from_pitch = Chroma(Pitch('C', 4))
        self.assertEqual(c_from_pitch.offset, 0)


class TestInterval(unittest.TestCase):
    """Test the Interval class."""

    def test_creation(self):
        """Test interval creation."""
        unison = Interval('U')
        self.assertEqual(unison.distance, 0)

        fifth = Interval('P5')
        self.assertEqual(fifth.distance, 7)

    def test_addition(self):
        """Test interval addition."""
        fifth = Interval('P5')
        fourth = Interval('P4')
        octave = fifth + fourth
        self.assertEqual(octave.distance, 12)


class TestVoicing(unittest.TestCase):
    """Test the Voicing class."""

    def test_creation(self):
        """Test voicing creation."""
        c_major = Voicing(C(), [C(4), E(4), G(4)])
        self.assertEqual(len(c_major), 3)
        self.assertEqual(c_major.root.offset, 0)

    def test_chord_tones(self):
        """Test chord tone analysis."""
        c_major = Voicing(C(), [C(4), E(4), G(4)])
        tones = ~c_major
        self.assertIn('1', tones)
        self.assertIn('maj3', tones)
        self.assertIn('5', tones)

        c_dom7 = Voicing(C(), [C(4), E(4), G(4), Bb(4)])
        tones = ~c_dom7
        self.assertIn('dom7', tones)


if __name__ == '__main__':
    unittest.main() 