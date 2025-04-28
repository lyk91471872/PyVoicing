from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Union

from .constants import CHROMA_OF, OFFSET_OF
from .interval import Interval

if TYPE_CHECKING:
    from .pitch import Pitch


class Chroma:
    """Represents a pitch class (chroma) without a specific octave."""

    def __init__(self, value: Union[int, str, "Chroma", "Pitch"]):
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
                raise TypeError("expected value of type int|str|Chroma|Pitch")

    def __str__(self) -> str:
        return CHROMA_OF[self.offset]

    def __repr__(self) -> str:
        return f"Chroma('{self}')"

    def __invert__(self) -> int:
        """Return the offset value of the chroma."""
        return self.offset

    def __eq__(self, other: Any) -> bool:
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

    def __neg__(self) -> int:
        return -self.offset

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


# shorthand
C = Chroma
