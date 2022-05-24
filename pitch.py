from __future__ import annotations
from .chroma import *

class Pitch:

    def __init__(self, value: int|str|Chroma|Pitch, octave: int|None=4):
        match value:
            case int():     self.value = value
            case str():     self.value = OFFSET_OF[value] + (octave+1)*12
            case Chroma():  self.value = value.offset + (octave+1)*12
            case Pitch():   self.value = value.value
            case _:         raise TypeError('expected value of type int|str|Chroma|Pitch')

    def __str__(self):
        return f'{self.chroma}{self.octave}'

    def __repr__(self):
        return f'Pitch("{self.chroma}", {self.octave})'

    def __invert__(self):
        return self.value

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other: Any):
        match other:
            case int():     return self.value < other
            case Pitch():   return self.value < other.value
            case _:         return NotImplemented

    def __le__(self, other: Any):
        match other:
            case int():     return self.value <= other
            case Pitch():   return self.value <= other.value
            case _:         return NotImplemented

    def __gt__(self, other: Any):
        match other:
            case int():     return self.value > other
            case Pitch():   return self.value > other.value
            case _:         return NotImplemented

    def __ge__(self, other: Any):
        match other:
            case int():     return self.value >= other
            case Pitch():   return self.value >= other.value
            case _:         return NotImplemented

    def __eq__(self, other: Any):
        match other:
            case int():         return self.value == other
            case str():         return self.chroma == other
            case Interval():    return self.offset == other.distance
            case Chroma():      return self.offset == other.offset
            case Pitch():       return self.value == other.value
            case _:             return False

    #transpose upwards
    def __mul__(self, interval: int|str|Interval|Chroma|Pitch) -> Pitch:
        match interval:
            case Pitch():   return Pitch(self.value+interval.value)
            case _:         return Pitch(self.value+Interval(interval).distance)

    #transpose downwards
    def __truediv__(self, interval: int|str|Interval|Chroma|Pitch) -> Pitch:
        match interval:
            case Pitch():   return Pitch(self.value-interval.value)
            case _:         return Pitch(self.value-Interval(interval).distance)

    #concat list
    def __add__(self, other: int|Pitch|list[Pitch]) -> list[Pitch]:
        match other:
            case int()|Pitch(): return sorted([Pitch(self), Pitch(other)])
            case list():        return sorted([Pitch(self)]+[Pitch(_) for _ in other])

    #append
    def __radd__(self, other: int|Pitch|list[Pitch]) -> list[Pitch]:
        match other:
            case int()|Pitch(): return sorted([Pitch(self), Pitch(other)])
            case list():        return sorted([Pitch(self)]+[Pitch(_) for _ in other])

    def __sub__(self, other: int|Pitch) -> int:
        return self.value - Pitch(other).value

    #remove
    def __rsub__(self, pitches: list[Pitch]) -> list[Pitch]:
        return [Pitch(_) for _ in pitches if _!=self]

    @property
    def offset(self):
        return self.value % 12

    @offset.setter
    def offset(self, value: int):
        self.value = (self.octave+1)*12 + value

    @property
    def octave(self):
        return self.value//12 - 1

    @octave.setter
    def octave(self, value: int):
        self.value = self.offset + (value+1)*12

    @property
    def chroma(self):
        return CHROMA_OF[self.offset]

    @chroma.setter
    def chroma(self, value: str):
        self.offset = OFFSET_OF[value]


def P(value: int|str|Pitch, octave: int|None=4) -> Pitch:
    return Pitch(value, octave)

def A(octave: int=None) -> Chroma|Pitch:
    return Pitch('A', octave) if octave is not None else Chroma('A')

def Bb(octave: int=None) -> Chroma|Pitch:
    return Pitch('Bb', octave) if octave is not None else Chroma('Bb')

def B(octave: int=None) -> Chroma|Pitch:
    return Pitch('B', octave) if octave is not None else Chroma('B')

def C(octave: int=None) -> Chroma|Pitch:
    return Pitch('C', octave) if octave is not None else Chroma('C')

def Db(octave: int=None) -> Chroma|Pitch:
    return Pitch('Db', octave) if octave is not None else Chroma('Db')

def D(octave: int=None) -> Chroma|Pitch:
    return Pitch('D', octave) if octave is not None else Chroma('D')

def Eb(octave: int=None) -> Chroma|Pitch:
    return Pitch('Eb', octave) if octave is not None else Chroma('Eb')

def E(octave: int=None) -> Chroma|Pitch:
    return Pitch('E', octave) if octave is not None else Chroma('E')

def F(octave: int=None) -> Chroma|Pitch:
    return Pitch('F', octave) if octave is not None else Chroma('F')

def Gb(octave: int=None) -> Chroma|Pitch:
    return Pitch('Gb', octave) if octave is not None else Chroma('Gb')

def G(octave: int=None) -> Chroma|Pitch:
    return Pitch('G', octave) if octave is not None else Chroma('G')

def Ab(octave: int=None) -> Chroma|Pitch:
    return Pitch('Ab', octave) if octave is not None else Chroma('Ab')
