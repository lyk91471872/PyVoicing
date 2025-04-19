"""Pitch module for representing musical pitches."""

from __future__ import annotations
from typing import Union, List, TypeVar, Optional, Any, TYPE_CHECKING

from .constants import OFFSET_OF, CHROMA_OF
from .chroma import Chroma

if TYPE_CHECKING:
    from .interval import Interval

# Forward references and type aliases
PitchValue = Union[int, str, Chroma, 'Pitch']
T = TypeVar('T', bound='Pitch')


class Pitch:
    """Represents a musical pitch with specific octave."""

    def __init__(self, value: PitchValue, octave: Optional[int] = 4):
        """Initialize a Pitch.

        Args:
            value: An integer, string, Chroma, or Pitch value
            octave: An optional octave number (default: 4)
        """
        match value:
            case int():
                self.value = value
            case str():
                self.value = OFFSET_OF[value] + (octave + 1) * 12
            case Chroma():
                self.value = value.offset + (octave + 1) * 12
            case Pitch():
                self.value = value.value
            case _:
                raise TypeError('expected value of type int|str|Chroma|Pitch')

    def __str__(self) -> str:
        """Convert pitch to string representation."""
        return f'{self.name}{self.octave}'

    def __repr__(self) -> str:
        """Create string representation for debugging."""
        return f'Pitch("{self.name}", {self.octave})'

    def repr(self) -> str:
        """Alternative string representation."""
        return f'{self.name}({self.octave})'

    def __invert__(self) -> int:
        """Return the MIDI value of the pitch."""
        return self.value

    def __hash__(self) -> int:
        """Generate hash for the pitch."""
        return hash(str(self))

    def __lt__(self, other: Any) -> bool:
        """Compare if this pitch is lower than another."""
        match other:
            case int():
                return self.value < other
            case Pitch():
                return self.value < other.value
            case _:
                return NotImplemented

    def __le__(self, other: Any) -> bool:
        """Compare if this pitch is lower than or equal to another."""
        match other:
            case int():
                return self.value <= other
            case Pitch():
                return self.value <= other.value
            case _:
                return NotImplemented

    def __gt__(self, other: Any) -> bool:
        """Compare if this pitch is higher than another."""
        match other:
            case int():
                return self.value > other
            case Pitch():
                return self.value > other.value
            case _:
                return NotImplemented

    def __ge__(self, other: Any) -> bool:
        """Compare if this pitch is higher than or equal to another."""
        match other:
            case int():
                return self.value >= other
            case Pitch():
                return self.value >= other.value
            case _:
                return NotImplemented

    def __eq__(self, other: Any) -> bool:
        """Compare if two pitches are equal."""
        from .interval import Interval

        match other:
            case int():
                return self.value == other
            case str():
                return self.name == other
            case Interval():
                return self.offset == other.distance
            case Chroma():
                return self.offset == other.offset
            case Pitch():
                return self.value == other.value
            case _:
                return False

    def __mul__(self, interval: Union[int, str, 'Interval', Chroma, 'Pitch']) -> Pitch:
        """Transpose pitch upwards."""
        from .interval import Interval

        match interval:
            case Pitch():
                return Pitch(self.value + interval.value)
            case _:
                return Pitch(self.value + Interval(interval).distance)

    def __rshift__(self, interval: Union[int, str, 'Interval', Chroma, 'Pitch']) -> Pitch:
        """Transpose pitch upwards (alias for __mul__)."""
        from .interval import Interval

        match interval:
            case Pitch():
                return Pitch(self.value + interval.value)
            case _:
                return Pitch(self.value + Interval(interval).distance)

    def __truediv__(self, interval: Union[int, str, 'Interval', Chroma, 'Pitch']) -> Pitch:
        """Transpose pitch downwards."""
        from .interval import Interval

        match interval:
            case Pitch():
                return Pitch(self.value - interval.value)
            case _:
                return Pitch(self.value - Interval(interval).distance)

    def __lshift__(self, interval: Union[int, str, 'Interval', Chroma, 'Pitch']) -> Pitch:
        """Transpose pitch downwards (alias for __truediv__)."""
        from .interval import Interval

        match interval:
            case Pitch():
                return Pitch(self.value - interval.value)
            case _:
                return Pitch(self.value - Interval(interval).distance)

    def __add__(self, other: Union[int, 'Pitch', List['Pitch']]) -> List['Pitch']:
        """Concat pitch with other pitch(es)."""
        match other:
            case int() | Pitch():
                return sorted([Pitch(self), Pitch(other)])
            case list():
                return sorted([Pitch(self)] + [Pitch(_) for _ in other])
            case _:
                raise TypeError('expected value of type int|Pitch|list[Pitch]')

    def __radd__(self, other: Union[int, 'Pitch', List['Pitch']]) -> List['Pitch']:
        """Reverse add operation."""
        return self.__add__(other)

    def __sub__(self, other: Union[int, 'Pitch']) -> int:
        """Compute interval between pitches."""
        return self.value - Pitch(other).value

    def __rsub__(self, pitches: List['Pitch']) -> List['Pitch']:
        """Filter out this pitch from a list."""
        return [Pitch(_) for _ in pitches if _ != self]

    @property
    def offset(self) -> int:
        """Get the offset within an octave."""
        return self.value % 12

    @offset.setter
    def offset(self, value: int) -> None:
        """Set the offset while preserving the octave."""
        self.value = (self.octave + 1) * 12 + value

    @property
    def octave(self) -> int:
        """Get the octave of the pitch."""
        return self.value // 12 - 1

    @octave.setter
    def octave(self, value: int) -> None:
        """Set the octave while preserving the offset."""
        self.value = self.offset + (value + 1) * 12

    @property
    def name(self) -> str:
        """Get the pitch name."""
        return CHROMA_OF[self.offset]

    @name.setter
    def name(self, value: str) -> None:
        """Set the pitch by name."""
        self.offset = OFFSET_OF[value]

    @property
    def chroma(self) -> Chroma:
        """Get the chroma of this pitch."""
        return Chroma(self)

    @chroma.setter
    def chroma(self, value: Chroma) -> None:
        """Set the chroma while preserving the octave."""
        self.offset = value.offset


def P(value: PitchValue, octave: Optional[int] = 4) -> Pitch:
    """Create a pitch object.

    Args:
        value: An integer, string, Chroma, or Pitch value
        octave: An optional octave number (default: 4)

    Returns:
        A new Pitch object
    """
    return Pitch(value, octave)


def A(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create an A pitch or chroma.

    Args:
        octave: Optional octave number. If None, returns a Chroma.

    Returns:
        A Pitch if octave is specified, otherwise a Chroma
    """
    return Pitch('A', octave) if octave is not None else Chroma('A')


def Bb(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create a Bb pitch or chroma."""
    return Pitch('Bb', octave) if octave is not None else Chroma('Bb')


def B(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create a B pitch or chroma."""
    return Pitch('B', octave) if octave is not None else Chroma('B')


def C(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create a C pitch or chroma."""
    return Pitch('C', octave) if octave is not None else Chroma('C')


def Db(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create a Db pitch or chroma."""
    return Pitch('Db', octave) if octave is not None else Chroma('Db')


def D(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create a D pitch or chroma."""
    return Pitch('D', octave) if octave is not None else Chroma('D')


def Eb(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create an Eb pitch or chroma."""
    return Pitch('Eb', octave) if octave is not None else Chroma('Eb')


def E(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create an E pitch or chroma."""
    return Pitch('E', octave) if octave is not None else Chroma('E')


def F(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create an F pitch or chroma."""
    return Pitch('F', octave) if octave is not None else Chroma('F')


def Gb(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create a Gb pitch or chroma."""
    return Pitch('Gb', octave) if octave is not None else Chroma('Gb')


def G(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create a G pitch or chroma."""
    return Pitch('G', octave) if octave is not None else Chroma('G')


def Ab(octave: Optional[int] = None) -> Union[Chroma, Pitch]:
    """Create an Ab pitch or chroma."""
    return Pitch('Ab', octave) if octave is not None else Chroma('Ab')
