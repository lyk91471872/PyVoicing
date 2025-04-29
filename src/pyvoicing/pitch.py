from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Union

from .chroma import Chroma
from .constants import ABC_OF, CHROMA_OF, OFFSET_OF

if TYPE_CHECKING:
    from .interval import Interval


class Pitch:
    def __init__(self, value: Union[int, str, Chroma, Pitch], octave: int = 4):
        match value:
            case int():
                self.value = value
            case str():
                if any(_ in value for _ in '_=^'):
                    self.abc = value
                    return
                chroma = ''.join(_ for _ in value if _.isalpha() or _ == '#')
                if len(chroma) < len(value):
                    octave = int(value[len(chroma) :])
                self.value = OFFSET_OF[chroma] + (octave + 1) * 12
            case Chroma():
                self.value = value.offset + (octave + 1) * 12
            case Pitch():
                self.value = value.value
            case _:
                raise TypeError("expected value of type int|str|Chroma|Pitch")

    def __str__(self) -> str:
        return f"{self.name}{self.octave}"

    def __repr__(self) -> str:
        return f"Pitch('{self.name}', {self.octave})"

    def __invert__(self) -> int:
        """Return the MIDI value of the pitch."""
        return self.value

    def __hash__(self) -> int:
        return hash(str(self))

    def __lt__(self, other: Any) -> bool:
        match other:
            case int():
                return self.value < other
            case Pitch():
                return self.value < other.value
            case _:
                return NotImplemented

    def __le__(self, other: Any) -> bool:
        match other:
            case int():
                return self.value <= other
            case Pitch():
                return self.value <= other.value
            case _:
                return NotImplemented

    def __gt__(self, other: Any) -> bool:
        match other:
            case int():
                return self.value > other
            case Pitch():
                return self.value > other.value
            case _:
                return NotImplemented

    def __ge__(self, other: Any) -> bool:
        match other:
            case int():
                return self.value >= other
            case Pitch():
                return self.value >= other.value
            case _:
                return NotImplemented

    def __eq__(self, other: Any) -> bool:
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

    def __mul__(self, n: int) -> list[Pitch]:
        """Return a list of copies."""
        return [Pitch(self) for i in range(n)]

    def __rshift__(
        self, interval: Union[int, str, "Interval", Chroma, "Pitch"]
    ) -> Pitch:
        """Transpose pitch upwards."""
        from .interval import Interval

        match interval:
            case Pitch():
                return Pitch(self.value + interval.value)
            case _:
                return Pitch(self.value + Interval(interval).distance)

    #    def __truediv__(self, interval: Union[int, str, 'Interval', Chroma, 'Pitch']) -> Pitch:
    #        """Transpose pitch downwards."""
    #        from .interval import Interval
    #        match interval:
    #            case Pitch():
    #                return Pitch(self.value - interval.value)
    #            case _:
    #                return Pitch(self.value - Interval(interval).distance)

    def __lshift__(
        self, interval: Union[int, str, "Interval", Chroma, "Pitch"]
    ) -> Pitch:
        """Transpose pitch downwards."""
        from .interval import Interval

        match interval:
            case Pitch():
                return Pitch(self.value - interval.value)
            case _:
                return Pitch(self.value - Interval(interval).distance)

    def __add__(self, other: Union[int, "Pitch", List["Pitch"]]) -> List["Pitch"]:
        """Concat pitch with other pitch(es)."""
        match other:
            case int() | Pitch():
                return sorted([Pitch(self), Pitch(other)])
            case list():
                return sorted([Pitch(self)] + [Pitch(_) for _ in other])
            case _:
                raise TypeError("expected value of type int|Pitch|list[Pitch]")

    def __radd__(self, other: Union[int, "Pitch", List["Pitch"]]) -> List["Pitch"]:
        """Reverse add operation."""
        return self.__add__(other)

    def __sub__(self, other: Union[int, "Pitch"]) -> int:
        """Compute interval between pitches."""
        return self.value - Pitch(other).value

    def __rsub__(self, pitches: List["Pitch"]) -> List["Pitch"]:
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

    @property
    def abc(self) -> str:
        """Get the ABC notation of this pitch."""
        abc = ABC_OF[self.offset]
        if abc == "z":
            return abc
        if (va := self.octave - 4) <= 0:
            return abc + "," * -va
        return abc.lower() + "'" * (va - 1)

    @abc.setter
    def abc(self, abc: str) -> None:
        """Set the ABC notation of this pitch."""
        if abc == 'z':
            self.value = Rest()
            return
        name, suffix = (abc[0], abc[1:]) if abc[0].isalpha() else (abc[:2], abc[2:])
        if va := int(name[-1].islower()):
            name = name.upper()
        va += suffix.count("'") - suffix.count(",")
        self.value = 0
        self.offset = OFFSET_OF[name]
        self.octave = 4 + va

    @classmethod
    def from_abc(cls, abc: str):
        """Create a new pitch from ABC notation"""
        pitch = cls(0)
        pitch.abc = abc
        return pitch


# shorthand
P = Pitch
