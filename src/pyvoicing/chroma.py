"""Chroma module for representing pitch classes."""

from __future__ import annotations
from typing import Union, List, TypeVar, Any, TYPE_CHECKING

from .constants import OFFSET_OF, CHROMA_OF
from .interval import Interval

if TYPE_CHECKING:
    from .pitch import Pitch

# Forward references and type aliases
ChromaValue = Union[int, str, 'Chroma', 'Pitch']
T = TypeVar('T', bound='Chroma')


class Chroma:
    """Represents a pitch class (chroma) independent of octave."""
    
    def __init__(self, value: ChromaValue):
        """Initialize a Chroma.
        
        Args:
            value: An integer, string, Chroma, or Pitch value
        """
        # Import here to avoid circular imports
        from .pitch import Pitch
        
        match value:
            case int():
                self.offset = value % 12
            case str():
                self.offset = OFFSET_OF[value]
            case Chroma():
                self.offset = value.offset
            case Pitch():
                self.offset = value.offset
            case _:
                raise TypeError('expected value of type int|str|Chroma|Pitch')

    def __str__(self) -> str:
        """Convert chroma to string representation."""
        return CHROMA_OF[self.offset]

    def __repr__(self) -> str:
        """Create string representation for debugging."""
        return f'Chroma("{self}")'

    def __invert__(self) -> int:
        """Return the offset value of the chroma."""
        return self.offset

    def __eq__(self, other: Any) -> bool:
        """Compare if two chromas are equal."""
        from .pitch import Pitch
        
        match other:
            case int():
                return self.offset == other % 12
            case str():
                return self.offset == OFFSET_OF[other]
            case Chroma():
                return self.offset == other.offset
            case Pitch():
                return self.offset == other.offset
            case _:
                return False

    def __mul__(self, value: Union[int, str, Interval]) -> Chroma:
        """Transpose chroma upwards."""
        return Chroma((Interval(value) + self.offset).offset)

    def __add__(self, value: Union[int, str, Interval]) -> Chroma:
        """Transpose chroma upwards (alias for __mul__)."""
        return Chroma((Interval(value) + self.offset).offset)

    def __rshift__(self, value: Union[int, str, Interval]) -> Chroma:
        """Transpose chroma upwards (alias for __mul__)."""
        return Chroma((Interval(value) + self.offset).offset)

    def __truediv__(self, value: Union[int, str, Interval]) -> Chroma:
        """Transpose chroma downwards."""
        return Chroma(self.offset - Interval(value).distance)

    def __sub__(self, value: Union[int, str, Interval, Chroma]) -> Union[int, Chroma]:
        """Transpose downwards or compute difference between chromas."""
        if isinstance(value, Chroma):
            return (self.offset - value.offset) % 12
        return Chroma(self.offset - Interval(value).distance)

    def __lshift__(self, value: Union[int, str, Interval]) -> Chroma:
        """Transpose chroma downwards (alias for __truediv__)."""
        return Chroma(self.offset - Interval(value).distance)

    def __rsub__(self, pitches: List[Pitch]) -> List[Pitch]:
        """Filter out pitches that match this chroma."""
        from .pitch import Pitch
        return [Pitch(_) for _ in pitches if _ != self]


def Ch(value: ChromaValue) -> Chroma:
    """Helper function to create a Chroma object.
    
    Args:
        value: An integer, string, Chroma, or Pitch value
        
    Returns:
        A new Chroma object
    """
    return Chroma(value) 