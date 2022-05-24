from __future__ import annotations
from .pitch import *

class Voicing:

    def __init__(self, root: int|str|Chroma|Pitch|Voicing, pitches: list[Pitch]=[]):
        if isinstance(root, str) and ',' in root:
            self.csv = root
            return
        if callable(root):
            root = root()
        elif isinstance(root, Voicing):
            root, pitches = (root.root, root.pitches)
        self.root = root
        self.pitches = [Pitch(_) for _ in pitches]

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value: int|str|Chroma|Pitch):
        self._root = Chroma(value)

    @property
    def csv(self):
        if len(self) == 0: return str(self.root.offset)
        return f'{self.root.offset},{",".join((str(_.value) for _ in self))}'

    @csv.setter
    def csv(self, data: str):
        self.root, *pitches = (int(_) for _ in data.split(','))
        self.pitches = [Pitch(_) for _ in pitches]

    def quality(self):
        return ''

    def __str__(self):
        return f'{self.root}{self.quality()}[{", ".join([str(_) for _ in self])}]'

    def __repr__(self):
        return f'Voicing({self.root}, {self.pitches})'

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(self.pitches)

    def __iter__(self):
        return iter(self.pitches)

    #compare two voicings (relationship root<->pitches)
    def __eq__(self, other: Voicing):
        if (not isinstance(other, Voicing)) or len(self)!=len(other):
            return False
        return (self<<self[0]-other[0]).pitches == other.pitches

    #whether other.pitches is subset of self.pitches
    def __gt__(self, other: Voicing):
        for pitch in other:
            if pitch not in self: return False
        return len(self) > len(other)

    def __ge__(self, other: Voicing):
        return self>other or self==other

    #match given interval and return lower pitches
    def __mod__(self, value: int|str):
        if isinstance(value, str): value = OFFSET_OF[value]
        lowers = []
        for i in range(len(self)-1):
            for j in range(i, len(self)):
                if self[j]-self[i] == value:
                    lowers.append(Pitch(self[i]))
        return lowers

    def __add__(self, value: Pitch|list[Pitch]|Voicing):  #different voices can share a same pitch
        ret = Voicing(self)
        match value:
            case Pitch():
                if value not in self: ret.pitches.append(Pitch(value))
            case list():
                for pitch in value:
                    if not isinstance(pitch, Pitch): raise TypeError('elements in list should be instances of Pitch')
                    ret.pitches.append(Pitch(pitch))
            case Voicing():
                for pitch in value:
                    if not isinstance(pitch, Pitch): raise TypeError('elements in list should be instances of Pitch')
                    ret.pitches.append(Pitch(pitch))
            case _: raise TypeError('expected value of type Pitch|list[Pitch]|Voicing')
        ret.pitches.sort()
        return ret

    def __sub__(self, value: Pitch|list[Pitch]|Voicing):
        ret = Voicing(self)
        match value:
            case Pitch():
                if value in self: ret.pitches.remove(value)
            case list():
                for pitch in value:
                    if not isinstance(pitch, Pitch): raise TypeError('elements in list should be instances of Pitch')
                    if pitch in self: ret.pitches.remove(pitch)
            case Voicing():
                for pitch in value:
                    if not isinstance(pitch, Pitch): raise TypeError('elements in list should be instances of Pitch')
                    if pitch in self: ret.pitches.remove(pitch)
            case _: raise TypeError('expected value of type Pitch|list[Pitch]|Voicing')
        return ret

    #transpose upwards
    def __rshift__(self, value: int|str|Interval) -> Voicing:
        ret = Voicing(self)
        ret.root += value
        for i in range(len(ret)): ret[i] *= value
        return ret

    #transpose downwards
    def __lshift__(self, value: int|str|Interval|Chroma) -> Voicing:
        ret = Voicing(self)
        ret.root -= value
        for i in range(len(ret)): ret[i] /= value
        return ret

    #compute interval matrix, ascending (positive) intervals only
    #row index: lower pitch index, column index: higher pitch index
    def matrix(self):
        interval_matrix = []
        for i in range(len(self)-1):
            interval_matrix.append([])
            for j in range(1, len(self)):
                interval = self[j]-self[i] if j>i else 0
                interval_matrix[i].append(interval)
        return interval_matrix

    def index(self, key: int|str|Pitch|Chroma) -> int:
        if callable(key):
            key = key()
        elif isinstance(key, str):
            if any(_.isdigit() for _ in key):
                return (~self).index(key) if key in ~self else -1
            key = Chroma(key)
        return self.pitches.index(key)

    def __getitem__(self, key: int|str|Pitch|Chroma) -> Pitch:
        if isinstance(key, int): return self.pitches[key]
        if callable(key): key = key()
        return self[self.index(key)] if key in self or key in ~self else None

    def __delitem__(self, key: int|str|Pitch|Chroma):
        if isinstance(key, int):
            del self.pitches[key]
        else:
            del self.pitches[self.index(key)]

    def __setitem__(self, key: int|str|Pitch|Chroma, value: int|Pitch):
        if isinstance(key, int):
            self.pitches[key] = Pitch(value)
        else:
            self.pitches[self.index(key)] = Pitch(value)

    #chordal tones
    def __invert__(self):
        offsets = [_.offset for _ in (self<<self.root)]
        def has(*values): return any(_ in offsets for _ in values)
        root = 128
        tones = []
        for i, p in enumerate(self):
            match offsets[i]:
                case 0:
                    root = min(root, p)
                    tones.append('1')
                case 1:
                    tones.append('b9')
                case 2:
                    if p-root > 12:
                        tones.append('9' if has(10, 11) else 'add9')
                    else:
                        tones.append('add2' if has(3, 4) else 'sus2')
                case 3:
                    root = min(root, p-3)
                    tones.append('#9' if has(4) else 'min3')
                case 4:
                    root = min(root, p-4)
                    tones.append('maj3')
                case 5:
                    if p-root > 12:
                        tones.append('11' if has(10, 11) else 'add11')
                    else:
                        tones.append('add4' if has(3, 4) else 'sus4')
                case 6:
                    if has(4, 7, 9):    tones.append('#11')
                    elif has(3, 5):     tones.append('b5')
                    else:               tones.append('#11' if p-root>12 else 'b5')
                case 7:
                    tones.append('5')
                case 8:
                    tones.append('b13' if has(1, 3, 5, 6, 7, 9, 10) else '#5')
                case 9:
                    if p-root>12:
                        tones.append('13')
                    elif all(_ in offsets for _ in (0, 3, 6)) and not has(10, 11):
                        tones.append('dim7')
                    else:
                        tones.append('6')
                case 10:
                    tones.append('min7' if has(3) else 'dom7')
                case 11:
                    tones.append('maj7')
        return tones


def V(root: int|str|Chroma|Pitch|Voicing, pitches: list[Pitch]=[]):
    return Voicing(root, pitches)
