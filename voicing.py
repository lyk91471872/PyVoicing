from __future__ import annotations
from pitch import *

class Voicing:

    def __init__(self, value: int|Pitch|Voicing, pitches: list[Pitch]=[]):
        match value:
            case int():     pass
            case Pitch():    pass
            case Voicing(): value, pitches = (value.root, value.pitches)
            case _:         raise TypeError('expected value of type Pitch|list[Pitch]')
        self.root = Pitch(value)    #root not in pitches if the voicing is rootless
        self.pitches = [Pitch(_) for _ in pitches]

    def quality(self):
        return ''

    def __str__(self):
        return f'{self.root}{self.quality()}[{", ".join([str(_) for _ in self.pitches])}]'

    def __repr__(self):
        return f'<Voicing {self.__str__()}>'

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(self.pitches)

    def __iter__(self):
        return iter(self.pitches)

    #compare two voicings (relationship root<->pitches)
    def __eq__(self, other: Voicing):
        return (self<<self.root-other.root).pitches == other.pitches

    #whether other.pitches is subset of self.pitches
    def __gt__(self, other: Voicing):
        for pitch in other.pitches:
            if pitch not in self.pitches: return False
        return len(self) > len(other)

    def __ge__(self, other: Voicing):
        return self>other or self==other

    #match given interval and return lower pitches
    def __mod__(self, value: int|str):
        if isinstance(value, str): value = OFFSET_OF[value]
        lowers = []
        for i in range(len(self.pitches)-1):
            for j in range(i, len(self.pitches)):
                if self.pitches[j]-self.pitches[i] == value:
                    lowers.append(Pitch(self.pitches[i]))
        return lowers

    def __add__(self, value: Pitch|list[Pitch]|Voicing):  #different voices can share a same pitch
        ret = Voicing(self)
        match value:
            case Pitch():
                if value not in self.pitches: ret.pitches.append(Pitch(value))
            case list():
                for pitch in value:
                    if not isinstance(pitch, Pitch): raise TypeError('elements in list should be instances of Pitch')
                    ret.pitches.append(Pitch(pitch))
            case Voicing():
                for pitch in value.pitches:
                    if not isinstance(pitch, Pitch): raise TypeError('elements in list should be instances of Pitch')
                    ret.pitches.append(Pitch(pitch))
            case _: raise TypeError('expected value of type Pitch|list[Pitch]|Voicing')
        ret.pitches.sort()
        return ret

    def __sub__(self, value: Pitch|list[Pitch]|Voicing):
        ret = Voicing(self)
        match value:
            case Pitch():
                if value in self.pitches: ret.pitches.remove(value)
            case list():
                for pitch in value:
                    if not isinstance(pitch, Pitch): raise TypeError('elements in list should be instances of Pitch')
                    if pitch in self.pitches: ret.pitches.remove(pitch)
            case Voicing():
                for pitch in value.pitches:
                    if not isinstance(pitch, Pitch): raise TypeError('elements in list should be instances of Pitch')
                    if pitch in self.pitches: ret.pitches.remove(pitch)
            case _: raise TypeError('expected value of type Pitch|list[Pitch]|Voicing')
        return ret

    #transpose upwards
    def __rshift__(self, value: int|str):
        ret = Voicing(self)
        match value:
            case int(): pass
            case str(): value = OFFSET_OF[value]
            case _:     raise TypeError('expected value of type int|str')
        ret.root += value
        for i in range(len(ret.pitches)): ret.pitches[i] += value
        return ret

    #transpose downwards
    def __lshift__(self, value: int|str):
        ret = Voicing(self)
        match value:
            case int(): pass
            case str(): value = OFFSET_OF[value]
            case _:     raise TypeError('expected value of type int|str')
        ret.root -= value
        for i in range(len(ret.pitches)): ret.pitches[i] -= value
        return ret

    #compute interval matrix, ascending (positive) intervals only
    #row index: lower pitch index, column index: higher pitch index
    def matrix(self):
        interval_matrix = []
        for i in range(len(self.pitches)-1):
            interval_matrix.append([])
            for j in range(1, len(self.pitches)):
                interval = self.pitches[j]-self.pitches[i] if j>i else 0
                interval_matrix[i].append(interval)
        return interval_matrix

    #chordal components
    def __invert__(self):
        def role_of(p: Pitch):
            return ROLE_OF[p.chroma+(0 if p.octave<0 else 12)]
        return [role_of(_) for _ in (self<<self.root.value).pitches]


##dicts##

ROLE_OF = {
    0:  '1',
    1:  'b9',
    2:  'S2',
    3:  'm3',
    4:  'M3',
    5:  'S4',
    6:  'b5',
    7:  '5',
    8:  '#5',
    9:  '6',
    10: 'm7',
    11: 'M7',
    12: '1',
    13: 'b9',
    14: '9',
    15: 'm3',
    16: 'M3',
    17: '11',
    18: '#11',
    19: '5',
    20: 'b13',
    21: '13',
    22: 'm7',
    23: 'M7',
}


##shortcuts##

def V(value: int|Pitch|Voicing, pitches: list[Pitch]=[]):
    return Voicing(value, pitches)
