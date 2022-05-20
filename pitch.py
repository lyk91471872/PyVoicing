from __future__ import annotations
import sys

class Pitch:

    def __init__(self, value: int|str|Pitch, octave: int|None=4):
        match value:
            case int():     self.value = value
            case str():     self.value = CHROMA_OF[value] + (octave+1)*12
            case Pitch():    self.value = value.value
            case _:         raise TypeError('expected value of type int|str|Pitch')

    def __str__(self):
        octave, chroma = divmod(self.value, 12)
        return f'{NAME_OF[chroma]}({octave-1})'

    def __repr__(self):
        return f'<Pitch: {self.__str__()}>'

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other: Any):
        match other:
            case Pitch():    return self.value < other.value
            case int():     return self.value < other
            case _:         return NotImplemented

    def __le__(self, other: Any):
        match other:
            case Pitch():    return self.value <= other.value
            case int():     return self.value <= other
            case _:         return NotImplemented

    def __gt__(self, other: Any):
        match other:
            case Pitch():    return self.value > other.value
            case int():     return self.value > other
            case _:         return NotImplemented

    def __ge__(self, other: Any):
        match other:
            case Pitch():    return self.value >= other.value
            case int():     return self.value >= other
            case _:         return NotImplemented

    def __eq__(self, other: Any):
        match other:
            case Pitch():    return self.value == other.value
            case int():     return self.value == other
            case _:         return False

    def __ne__(self, other: Any):
        match other:
            case Pitch():    return self.value != other.value
            case int():     return self.value != other
            case _:         return True

    def __add__(self, other: int|Pitch|list[Pitch]) -> Pitch|list[Pitch]:
        match other:
            case int():     return Pitch(self.value+other)   #transpose
            case Pitch():    return sorted([Pitch(self), Pitch(other)])
            case list():    return sorted([Pitch(self)]+[Pitch(_) for _ in other])

    def __radd__(self, other: int|Pitch|list[Pitch]) -> Pitch|list[Pitch]:
        match other:
            case int():     return Pitch(self.value+other)   #transpose
            case Pitch():    return sorted([Pitch(self), Pitch(other)])
            case list():    return sorted([Pitch(self)]+[Pitch(_) for _ in other])

    #int: transpose; Pitch: compute diff
    def __sub__(self, other: int|Pitch) -> int|Pitch:
        if isinstance(other, int): return Pitch(self.value-other)
        return self.value - other.value

    @property
    def chroma(self):
        return self.value % 12

    @chroma.setter
    def chroma(self, value: int):
        self.value = (self.octave+1)*12 + value

    @property
    def octave(self):
        return self.value//12 - 1

    @octave.setter
    def octave(self, value: int):
        self.value = self.chroma + (value+1)*12

    @property
    def name(self):
        return NAME_OF[self.chroma]

    @name.setter
    def name(self, value: str):
        self.chroma = CHROMA_OF[value]


##dicts##

NAME_OF = {
    0:  'C',
    1:  'Db',
    2:  'D',
    3:  'Eb',
    4:  'E',
    5:  'F',
    6:  'Gb',
    7:  'G',
    8:  'Ab',
    9:  'A',
    10: 'Bb',
    11: 'B',
}

CHROMA_OF = {
    'C':   0,
    'C#':  1,
    'Db':  1,
    'D':   2,
    'D#':  3,
    'Eb':  3,
    'E':   4,
    'F':   5,
    'F#':  6,
    'Gb':  6,
    'G':   7,
    'G#':  8,
    'Ab':  8,
    'A':   9,
    'A#': 10,
    'Bb': 10,
    'B':  11,
}

INTERVAL_OF = {
    0:  'U',
    1:  'm2',
    2:  'M2',
    3:  'm3',
    4:  'M3',
    5:  'P4',
    6:  'T',
    7:  'P5',
    8:  'm6',
    9:  'M6',
    10: 'm7',
    11: 'M7',
    12: 'O',
}

OFFSET_OF = {
    'U':   0,   #Unison
    'P1':  0,   #Perfect first
    'm2':  1,   #minor second
    'M2':  2,   #Major second
    'm3':  3,   #minor third
    'M3':  4,   #Major third
    'P4':  5,   #Perfect fourth
    'A4':  6,   #Augmented fourth
    'T':   6,   #Tritone
    'd5':  6,   #diminished fifth
    'P5':  7,   #Perfect fifth
    'm6':  8,   #minor sixth
    'M6':  9,   #Major sixth
    'm7': 10,   #minor seventh
    'D7': 10,   #Dominant seventh
    'M7': 11,   #Major seventh
    'P8': 12,   #Perfect eighth
    'O':  12,   #Octave
}


##shortcuts##

def P(value: int|str|Pitch, octave: int|None=4):
    return Pitch(value, octave)

def A(octave: int=4):
    return Pitch('A', octave)

def Bb(octave: int=4):
    return Pitch('Bb', octave)

def B(octave: int=4):
    return Pitch('B', octave)

def C(octave: int=4):
    return Pitch('C', octave)

def Db(octave: int=4):
    return Pitch('Db', octave)

def D(octave: int=4):
    return Pitch('D', octave)

def Eb(octave: int=4):
    return Pitch('Eb', octave)

def E(octave: int=4):
    return Pitch('E', octave)

def F(octave: int=4):
    return Pitch('F', octave)

def Gb(octave: int=4):
    return Pitch('Gb', octave)

def G(octave: int=4):
    return Pitch('G', octave)

def Ab(octave: int=4):
    return Pitch('Ab', octave)
