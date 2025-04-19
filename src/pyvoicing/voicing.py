"""Voicing module for representing and manipulating musical voicings."""

from __future__ import annotations
from typing import Union, List, TypeVar, Callable, Optional, Any, cast, TYPE_CHECKING
import copy

from .constants import OFFSET_OF
from .pitch import Pitch
from .chroma import Chroma

if TYPE_CHECKING:
    from .interval import Interval

class Voicing:
    """Represents a musical voicing (collection of pitches with a root)."""

    def __init__(self, pitches: List[Pitch]=[], root: Union[int, str, Chroma, Pitch, Voicing, None]=None):
        """Initialize a Voicing.

        Args:
            root: The root of the voicing
            pitches: List of pitches (optional)
        """
        self.pitches = [Pitch(_) for _ in pitches]
        self.root = root

    @property
    def root(self) -> Chroma:
        """Get the root chroma of the voicing."""
        return self._root

    @root.setter
    def root(self, value: Union[int, str, Chroma, Pitch, None]) -> None:
        """Set the root chroma of the voicing."""
        self._root = None if value is None else Chroma(value)

    @property
    def csv(self) -> str:
        """Get CSV representation of the voicing."""
        if len(self) == 0:
            return str(self.root.offset)
        return f'{self.root.offset},{",".join((str(_.value) for _ in self))}'

    @csv.setter
    def csv(self, csv: str) -> None:
        """Set the voicing from a CSV representation."""
        values = [int(_) for _ in csv.split(',')]
        self.root = values[0]
        self.pitches = [Pitch(_) for _ in values[1:]] if len(values) > 1 else []

    @classmethod
    def from_csv(cls, csv: str):
        v = cls()
        v.csv = csv
        return v

    def quality(self) -> str:
        """Get the chord quality as a string."""
        return ''

    def __str__(self) -> str:
        """Convert voicing to a readable string."""
        return f'{self.root}{self.quality()}[{" ".join([str(_) for _ in self])}]'

    def __repr__(self) -> str:
        """Create string representation for debugging."""
        return f'Voicing({self.root}, [{", ".join([_.repr() for _ in self])}])'

    def __hash__(self) -> int:
        """Generate hash for the voicing."""
        return hash(str(self))

    def __len__(self) -> int:
        """Get the number of pitches in the voicing."""
        return len(self.pitches)

    def __iter__(self):
        """Iterate through the pitches in the voicing."""
        return iter(self.pitches)

    def __eq__(self, other: Any) -> bool:
        """Compare if two voicings are equivalent (taking into account transposition)."""
        if not isinstance(other, Voicing) or len(self) != len(other):
            return False
        # Transpose to the same root and compare pitches
        return (self << (self[0] - other[0])).pitches == other.pitches if len(self) > 0 else self.root == other.root

    def __gt__(self, other: Voicing) -> bool:
        """Check if this voicing is a superset of the other."""
        for pitch in other:
            if pitch not in self:
                return False
        return len(self) > len(other)

    def __ge__(self, other: Voicing) -> bool:
        """Check if this voicing is a superset of or equal to the other."""
        return self > other or self == other

    def __mod__(self, value: Union[int, str]) -> List[Pitch]:
        """Find pitches that form the given interval with higher pitches."""
        if isinstance(value, str):
            value = OFFSET_OF[value]

        lowers = []
        for i in range(len(self) - 1):
            for j in range(i + 1, len(self)):
                if self[j] - self[i] == value:
                    lowers.append(Pitch(self[i]))
        return lowers

    def __add__(self, value: Union[Pitch, List[Pitch], Voicing]) -> Voicing:
        """Add pitch(es) to the voicing."""
        ret = copy.deepcopy(self)

        match value:
            case Pitch():
                if value not in self:
                    ret.pitches.append(Pitch(value))
            case list():
                for pitch in value:
                    if not isinstance(pitch, Pitch):
                        raise TypeError('elements in list should be instances of Pitch')
                    ret.pitches.append(Pitch(pitch))
            case Voicing():
                for pitch in value:
                    if not isinstance(pitch, Pitch):
                        raise TypeError('elements in list should be instances of Pitch')
                    ret.pitches.append(Pitch(pitch))
            case _:
                raise TypeError('expected value of type Pitch|list[Pitch]|Voicing')

        ret.pitches.sort()
        return ret

    def __sub__(self, value: Union[Pitch, List[Pitch], Voicing]) -> Voicing:
        """Remove pitch(es) from the voicing."""
        ret = copy.deepcopy(self)

        match value:
            case Pitch():
                if value in self:
                    ret.pitches.remove(value)
            case list():
                for pitch in value:
                    if not isinstance(pitch, Pitch):
                        raise TypeError('elements in list should be instances of Pitch')
                    if pitch in self:
                        ret.pitches.remove(pitch)
            case Voicing():
                for pitch in value:
                    if not isinstance(pitch, Pitch):
                        raise TypeError('elements in list should be instances of Pitch')
                    if pitch in self:
                        ret.pitches.remove(pitch)
            case _:
                raise TypeError('expected value of type Pitch|list[Pitch]|Voicing')

        return ret

    def __mul__(self, value: Union[int, str, 'Interval']) -> Voicing:
        """Transpose the voicing upwards."""
        from .interval import Interval

        ret = copy.deepcopy(self)
        ret.root += value
        for i in range(len(ret)):
            ret[i] *= value
        return ret

    def __rshift__(self, value: Union[int, str, 'Interval']) -> Voicing:
        """Transpose the voicing upwards (alias for __mul__)."""
        from .interval import Interval

        ret = copy.deepcopy(self)
        ret.root += value
        for i in range(len(ret)):
            ret[i] *= value
        return ret

    def __truediv__(self, value: Union[int, str, 'Interval', Chroma]) -> Voicing:
        """Transpose the voicing downwards."""
        from .interval import Interval

        ret = copy.deepcopy(self)
        ret.root -= value
        for i in range(len(ret)):
            ret[i] /= value
        return ret

    def __lshift__(self, value: Union[int, str, 'Interval', Chroma]) -> Voicing:
        """Transpose the voicing downwards (alias for __truediv__)."""
        from .interval import Interval

        ret = copy.deepcopy(self)
        ret.root -= value
        for i in range(len(ret)):
            ret[i] /= value
        return ret

    def __floordiv__(self, target: Union[int, Pitch]) -> Voicing:
        """Transpose the voicing to a specific target pitch/value."""
        if len(self) == 0:
            return copy.deepcopy(self)

        root = self[0] << (self[0].chroma - self.root)
        return self << (root - target)

    def matrix(self) -> List[List[int]]:
        """Compute the interval matrix between all pitches in the voicing.

        Returns:
            A 2D array where each cell represents the interval between two pitches
        """
        if len(self) <= 1:
            return []

        interval_matrix = []
        for i in range(len(self) - 1):
            interval_matrix.append([])
            for j in range(len(self)):
                interval = self[j] - self[i] if j > i else 0
                interval_matrix[i].append(interval)
        return interval_matrix

    def index(self, key: Union[int, str, Pitch, Chroma]) -> int:
        """Find the index of a pitch in the voicing.

        Args:
            key: The pitch to find

        Returns:
            The index of the pitch or -1 if not found
        """
        if callable(key):
            key = key()
        elif isinstance(key, str):
            if any(_.isdigit() for _ in key):
                # Look for a pitch name with octave like "C4"
                return (~self).index(key) if key in ~self else -1
            # Look for a chroma name
            key = Chroma(key)

        try:
            return self.pitches.index(key)
        except ValueError:
            return -1

    def __getitem__(self, key: Union[int, str, Pitch, Chroma]) -> Optional[Pitch]:
        """Get a pitch by index, name, or object.

        Args:
            key: The index or pitch to retrieve

        Returns:
            The pitch at the given index or None if not found
        """
        if isinstance(key, int):
            return self.pitches[key]

        if callable(key):
            key = key()

        idx = self.index(key)
        return self.pitches[idx] if idx >= 0 else None

    def __delitem__(self, key: Union[int, str, Pitch, Chroma]) -> None:
        """Remove a pitch from the voicing.

        Args:
            key: The index or pitch to remove
        """
        if isinstance(key, int):
            del self.pitches[key]
        else:
            idx = self.index(key)
            if idx >= 0:
                del self.pitches[idx]

    def __setitem__(self, key: Union[int, str, Pitch, Chroma], value: Union[int, Pitch]) -> None:
        """Set a pitch at the given index or replace a pitch.

        Args:
            key: The index or pitch to replace
            value: The new pitch
        """
        if isinstance(key, int):
            self.pitches[key] = Pitch(value)
        else:
            idx = self.index(key)
            if idx >= 0:
                self.pitches[idx] = Pitch(value)

    def __invert__(self) -> List[str]:
        """Analyze the chord tones relative to the root.

        Returns:
            A list of chord tone names
        """
        if not self.pitches:
            return []

        offsets = [_.offset for _ in (self << self.root)]

        def has(*values):
            return any(_ in offsets for _ in values)

        if len(self) == 0:
            return []

        root = self[0] / offsets[0]
        tones = []

        for i, p in enumerate(self):
            match offsets[i]:
                case 0:
                    tones.append('1')
                case 1:
                    tones.append('b9')
                case 2:
                    if p - root > 12:
                        tones.append('9' if has(10, 11) else 'add9')
                    else:
                        tones.append('add2' if has(3, 4) else 'sus2')
                case 3:
                    tones.append('#9' if has(4) else 'min3')
                case 4:
                    tones.append('maj3')
                case 5:
                    if p - root > 12:
                        tones.append('11' if has(10, 11) else 'add11')
                    else:
                        tones.append('add4' if has(3, 4) else 'sus4')
                case 6:
                    if has(4, 7, 9):
                        tones.append('#11')
                    elif has(3, 5):
                        tones.append('b5')
                    else:
                        tones.append('#11' if p - root > 12 else 'b5')
                case 7:
                    tones.append('5')
                case 8:
                    tones.append('b13' if has(1, 3, 5, 6, 7, 9, 10) else '#5')
                case 9:
                    if p - root > 12:
                        tones.append('13')
                    elif all(_ in offsets for _ in (0, 3, 6)) and not has(10, 11):
                        tones.append('dim7')
                    else:
                        tones.append('6')
                case 10:
                    tones.append('dom7' if has(4) else 'min7')
                case 11:
                    tones.append('maj7')

        return tones

# shorthand
V = Voicing
