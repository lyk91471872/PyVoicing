from __future__ import annotations
from .interval import *

class Chroma:

    def __init__(self, value: int|str|Chroma|Pitch):
        from .pitch import Pitch
        match value:
            case int():     self.offset = value%12
            case str():     self.offset = OFFSET_OF[value]
            case Chroma():  self.offset = value.offset
            case Pitch():   self.offset = value.offset
            case _:         raise TypeError('expected value of type int|str|Chroma')

    def __str__(self):
        return CHROMA_OF[self.offset]

    def __repr__(self):
        return f'Chroma("{self}")'

    def __invert__(self):
        return self.offset

    def __eq__(self, other: Any):
        from .pitch import Pitch
        match other:
            case int():     return self.offset == other%12
            case str():     return self.offset == OFFSET_OF[other]
            case Chroma():  return self.offset == other.offset
            case Pitch():   return self.offset == other.offset
            case _:         return False

    #transpose upwards
    def __mul__(self, value: int|str|Interval) -> Chroma:
        return Chroma((Interval(value)+self.offset).offset)

    #transpose upwards
    def __add__(self, value: int|str|Interval) -> Chroma:
        return Chroma((Interval(value)+self.offset).offset)

    #transpose upwards
    def __rshift__(self, value: int|str|Interval) -> Chroma:
        return Chroma((Interval(value)+self.offset).offset)

    #transpose downwards
    def __truediv__(self, value: int|str|Interval) -> Chroma:
        return Chroma(self.offset-Interval(value).distance)

    #transpose downwards or compute difference
    def __sub__(self, value: int|str|Interval|Chroma) -> int|Chroma:
        if isinstance(value, Chroma): return (self.offset-value.offset) % 12
        return Chroma(self.offset-Interval(value).distance)

    #transpose downwards
    def __lshift__(self, value: int|str|Interval) -> Chroma:
        return Chroma(self.offset-Interval(value).distance)

    #remove
    def __rsub__(self, pitches: list[Pitch]) -> list[Pitch]:
        from .pitch import Pitch
        return [Pitch(_) for _ in pitches if _!=self]


def Ch(value: int|str|Chroma|Pitch):
    return Chroma(value)
