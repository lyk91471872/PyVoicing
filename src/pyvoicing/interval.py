"""Interval module for musical interval representation."""

from __future__ import annotations
from typing import Union, TypeVar, Optional, Any, TYPE_CHECKING

from .constants import OFFSET_OF, INTERVAL_OF

if TYPE_CHECKING:
    from .chroma import Chroma

# Forward references and type aliases
IntervalValue = Union[int, str, 'Interval', 'Chroma']
T = TypeVar('T', bound='Interval')


class Interval:
    """Represents a musical interval."""
    
    def __init__(self, value: IntervalValue, octave: Optional[int] = 0):
        """Initialize an Interval.
        
        Args:
            value: An integer, string, Interval, or Chroma value
            octave: An optional octave number (default: 0)
        """
        # Import here to avoid circular imports
        from .chroma import Chroma
        
        match value:
            case int():
                self.distance = value
            case str():
                self.distance = OFFSET_OF[value] + octave * 12
            case Interval():
                self.distance = value.distance
            case Chroma():
                self.distance = value.offset
            case _:
                raise TypeError('expected value of type int|str|Interval|Chroma')

    @property
    def offset(self) -> int:
        """Get the interval offset within an octave."""
        return self.distance % 12

    @offset.setter
    def offset(self, value: int) -> None:
        """Set the interval offset while preserving the octave."""
        self.distance = value + self.octave * 12

    @property
    def octave(self) -> int:
        """Get the octave component of the interval."""
        return self.distance // 12

    @octave.setter
    def octave(self, value: int) -> None:
        """Set the octave while preserving the offset."""
        self.distance = value * 12 + self.offset

    @property
    def interval(self) -> str:
        """Get the interval name."""
        return INTERVAL_OF[self.offset]

    @interval.setter
    def interval(self, value: str) -> None:
        """Set the interval by name."""
        self.offset = OFFSET_OF[value]

    def __str__(self) -> str:
        """Convert interval to string representation."""
        return f'{self.interval}({self.octave})' if self.octave else self.interval

    def __repr__(self) -> str:
        """Create string representation for debugging."""
        return f'Interval("{self.interval}", octave={self.octave})'

    def __invert__(self) -> int:
        """Return the distance value of the interval."""
        return self.distance

    def __hash__(self) -> int:
        """Generate hash for the interval."""
        return hash(str(self))

    def __eq__(self, other: Union[int, str, Interval]) -> bool:
        """Compare if two intervals are equal."""
        return self.distance == Interval(other).distance

    def __gt__(self, other: Union[int, str, Interval]) -> bool:
        """Check if this interval is greater than another."""
        return self.distance > Interval(other).distance

    def __ge__(self, other: Union[int, str, Interval]) -> bool:
        """Check if this interval is greater than or equal to another."""
        return self > other or self == other

    def __lt__(self, other: Union[int, str, Interval]) -> bool:
        """Check if this interval is less than another."""
        return not (self >= other)

    def __le__(self, other: Union[int, str, Interval]) -> bool:
        """Check if this interval is less than or equal to another."""
        return not (self > other)

    def __add__(self, other: Union[int, str, Interval]) -> Interval:
        """Add two intervals together."""
        return Interval(self.distance + Interval(other).distance)

    def __sub__(self, other: Union[int, str, Interval]) -> Interval:
        """Subtract another interval from this one."""
        return Interval(self.distance - Interval(other).distance)


def U(octave: Optional[int] = 0) -> Interval:
    """Create a unison interval."""
    return Interval(octave * 12)


def m2(octave: Optional[int] = 0) -> Interval:
    """Create a minor second interval."""
    return Interval(octave * 12 + 1)


def M2(octave: Optional[int] = 0) -> Interval:
    """Create a major second interval."""
    return Interval(octave * 12 + 2)


def m3(octave: Optional[int] = 0) -> Interval:
    """Create a minor third interval."""
    return Interval(octave * 12 + 3)


def M3(octave: Optional[int] = 0) -> Interval:
    """Create a major third interval."""
    return Interval(octave * 12 + 4)


def P4(octave: Optional[int] = 0) -> Interval:
    """Create a perfect fourth interval."""
    return Interval(octave * 12 + 5)


def T(octave: Optional[int] = 0) -> Interval:
    """Create a tritone interval."""
    return Interval(octave * 12 + 6)


def P5(octave: Optional[int] = 0) -> Interval:
    """Create a perfect fifth interval."""
    return Interval(octave * 12 + 7)


def m6(octave: Optional[int] = 0) -> Interval:
    """Create a minor sixth interval."""
    return Interval(octave * 12 + 8)


def M6(octave: Optional[int] = 0) -> Interval:
    """Create a major sixth interval."""
    return Interval(octave * 12 + 9)


def m7(octave: Optional[int] = 0) -> Interval:
    """Create a minor seventh interval."""
    return Interval(octave * 12 + 10)


def M7(octave: Optional[int] = 0) -> Interval:
    """Create a major seventh interval."""
    return Interval(octave * 12 + 11) 