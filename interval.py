from __future__ import annotations
from .constants import *


class Interval:
    def __init__(self, value: int|str|Interval|Chroma, octave: int|None=0):
        from .chroma import Chroma
        match value:
            case int():         self.distance = value
            case str():         self.distance = OFFSET_OF[value] + octave*12
            case Interval():    self.distance = value.distance
            case Chroma():      self.distance = value.offset

    @property
    def offset(self):
        return self.distance % 12

    @offset.setter
    def offset(self, value: int):
        self.distance = value + self.octave*12

    @property
    def octave(self):
        return self.distance // 12

    @octave.setter
    def octave(self, value: int):
        self.distance = value*12 + self.offset

    @property
    def interval(self):
        return INTERVAL_OF[self.offset]

    @interval.setter
    def interval(self, value: str):
        self.offset = OFFSET_OF[value]

    def __str__(self):
        return f'{self.interval}({self.octave})' if self.octave else self.interval

    def __repr__(self):
        return f'Interval("{self.interval}", octave={self.octave})'

    def __invert__(self):
        return self.distance

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other: int|str|Interval):
        return self.distance == Interval(other).distance

    def __gt__(self, other: int|str|Interval):
        return self.distance > Interval(other).distance

    def __ge__(self, other: int|str|Interval):
        return self>other or self==other

    def __le__(self, other: int|str|Interval):
        return self<other or self==other

    def __add__(self, other: int|str|Interval):
        return Interval(self.distance+Interval(other).distance)

    def __sub__(self, other: int|str|Interval):
        return Interval(self.distance-Interval(other).distance)


def U(octave: int|None=0):
    return Interval(octave*12)

def m2(octave: int|None=0):
    return Interval(octave*12+1)

def M2(octave: int|None=0):
    return Interval(octave*12+2)

def m3(octave: int|None=0):
    return Interval(octave*12+3)

def M3(octave: int|None=0):
    return Interval(octave*12+4)

def P4(octave: int|None=0):
    return Interval(octave*12+5)

def T(octave: int|None=0):
    return Interval(octave*12+6)

def P5(octave: int|None=0):
    return Interval(octave*12+7)

def m6(octave: int|None=0):
    return Interval(octave*12+8)

def M6(octave: int|None=0):
    return Interval(octave*12+9)

def m7(octave: int|None=0):
    return Interval(octave*12+10)

def M7(octave: int|None=0):
    return Interval(octave*12+11)
