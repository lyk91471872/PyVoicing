# PyVoicing

A Python library for symbolic music analysis, focusing on chord voicings and tensions, providing intuitive Python classes for working with pitches, chromas, intervals, and voicings.
* Pythonic syntax
* Lightweight, no dependency
> PyVoicing is currently in Alpha stage.
> API and type hints are subject to change.

## Installation

```bash
pip install pyvoicing
```

## Usage

```python
from pyvoicing import Pitch, Chroma, Interval, Voicing
# shorthands
from pyvoicing import P, C, I, V
# or simply
from pyvoicing import *

# Pitch
middle_c = Pitch('C', 4)
middle_c.value  # 60
~middle_c       # 60, shorthand
middle_c.octave # 4
middle_c.offset # 0
middle_c.name   # 'C'
middle_c.chroma # Chroma("C")

g = Pitch('G')  # default octave=4
b = P('B')      # shorthand P for Pitch
e = P('E5')     # octave as part of the string

a = e >> 'P4'   # transpose up a perfect 4th
a <<= 12        # transpose down an octave

# Voicing
Cmaj7open = Voicing([middle_c, g, b, e], root='C')
Cmaj7open   # Voicing('C4 G4 B4 E5', 'C')
~Cmaj7open  # ['1', '5', 'maj7', 'maj5']

C69 = Cmaj7open + a - 'B4' + 'D5'
~C69        # ['1', '5', '6', '9', 'maj3']
C69 >> 3    # Voicing('Eb4 Bb4 C5 F5 G5', 'Eb')

Bm7b5 = V('B D5 F5 A5', 'B')  # shorthand
~Bm7b5      # ['1', 'min3', 'b5', 'min7']
Bm7b5.root = 'G'
~Bm7b5      # ['maj3', '5', 'dom7', '9']
G9rootless = V(Bm7b5)

C913rootless = G9rootless // 'C'
C913rootless    # Voicing('E4 G4 Bb4 D5', 'C')
C913rootless[1] >>= 2
C913rootless    # Voicing('E4 A4 Bb4 D5', 'C')
~C913rootless   # ['maj3', '13', 'dom7', '9']
```

## License
PyVoicing is licensed under the MIT License.

## Contributing
Feature suggestions and bug reports are welcome!

## Changelog
See [CHANGELOG.md](https://github.com/lyk91471872/PyVoicing/blob/main/CHANGELOG.md) for version history and release notes.
