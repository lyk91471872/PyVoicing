# PyVoicing

A Python library for musical pitch, interval, and voicing analysis.

## Installation

```bash
pip install pyvoicing
```

## Usage

```python
from pyvoicing import Pitch, Chroma, Interval, Voicing
from pyvoicing import P, C, E, G  # Note helper functions

# Create a C major chord
c_major = Voicing(C(), [C(4), E(4), G(4)])
print(c_major)  # C[C4 E4 G4]

# Transpose the chord
c_major_up_fifth = c_major * "P5"  # or c_major >> "P5"
print(c_major_up_fifth)  # G[G4 B4 D5]

# Analyze chord tones
print(~c_major)  # ['1', 'maj3', '5']
```

## License

See the LICENSE file for details. 