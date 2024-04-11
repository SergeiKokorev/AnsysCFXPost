from __future__ import annotations

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from typing import List
from dataclasses import dataclass, field


@dataclass
class Data(metaclass=ABCMeta):

    name: str
    
    def item(self):
        return self.name

    @abstractmethod
    def items(self) -> list:
        pass

    @abstractmethod
    def rowCount(self) -> int:
        pass

    @abstractmethod
    def columnCount(self) -> int:
        pass

    @abstractmethod
    def addItem(self) -> None:
        pass
    
    @abstractmethod
    def addItems(self) -> None:
        pass

    @abstractmethod
    def delItem(self, index: int) -> None:
        pass


@dataclass
class DataCache(metaclass=ABCMeta):
    cache: list = field(default_factory=list)

    def rowCount(self):
        return len(self.cache)

    def items(self):
        return deepcopy(self.cache)
    
    def item(self, index: int):
        if not (0 <= index <= self.rowCount()):
            return None
        
        return self.cache[index]

    def child(self, row: int, col: int):
        if not (0 <= row <= self.rowCount()):
            return None
        
        if not(0 <= col <= self.cache[row].rowCount()):
            return None
        
        return self.cache[row].item(col)
    
    def children(self, row):
        if (0 <= row <= self.rowCount()):
            return None
        
        return self.cache[row].items()

    def addChild(self, index: int, item):
        if not (0 <= index <= self.rowCount()):
            return None
        self.cache[index].addItem(item)

    def addChildren(self, index: int, items):
        if not (0 <= index <= self.rowCount()):
            return None
        
        self.cache[index].addItems(items)

    def columnCount(self, index: int):
        if not (0 <= index <= self.rowCount()):
            return None
        return self.cache[index].rowCount()

    def delItem(self, index: int):
        if not (0 <= index <= self.rowCount()):
            return None
        
    def delChild(self, row: int, col: int):
        if not (0 <= row <= self.rowCount()):
            return None

        self.cache[row].delItem(col)

    @abstractmethod
    def addItem(self, item):
        pass

    @abstractmethod
    def addItems(self, items):
        pass


@dataclass
class Boundary:
    name: str
    parentIndex: int = 0
    type: str = None

    def item(self):
        return self.name

    def parent(self):
        return self.parentIndex

    def __str__(self):
        return f'{self.name}'
    
    def __repr__(self):
        return f'{self.__class__.__name__}[name={self.name}, type={self.type}, parent={self.parentIndex}]'


@dataclass
class Domain(Data):
    index: int
    name: str
    type: str = None
    boundaries: List[Boundary] = field(default_factory=list)

    def items(self):
        return deepcopy(self.boundaries)

    def addItem(self, item: Boundary) -> Boundary:
        
        if not isinstance(item, Boundary):
            return -1
        self.boundaries.append(item)
        return item

    def addItems(self, items: List[Boundary]):
        self.boundaries.extend(items)

    def delItem(self, index: int) -> Boundary:

        if not isinstance(index, int):
            return -1

        try:
            return self.boundaries.pop(index)
        except IndexError:
            return -1

    def item(self, index) -> Boundary:

        if not isinstance(index, int):
            return -1
        try:
            return self.boundaries[index]
        except IndexError:
            return -1

    def rowCount(self):
        return len(self.boundaries)

    def columnCount(self) -> int:
        return 1

    def __str__(self):
        return f'{self.name}'


@dataclass
class Template(Data):
    name: str
    data: dict = field(default_factory=dict)
    model: Domains = None
    files: List[str] = field(default_factory=list)

    def item(self):
        return self.name

    def info(self):
        out = f'{self.name}\n'
        for v in self.data.values():
            out += f'\t{v[0]}\t{v[1]}\n'
        return out

    def rowCount(self):
        return len(self.files)
    
    def columnCount(self):
        return 1

    def addItem(self, item: str):
        self.files.append(item)

    def addItems(self, items: List[str]):
        self.files.extend(items)

    def delItem(self, index: int):
        self.files.pop(index)

    def items(self):
        return deepcopy(self.files)

    def __str__(self):
        return self.name


@dataclass
class Boundaries(DataCache):

    def items(self):
        return deepcopy(self.cache)
    
    def item(self, index: int) -> Boundary:
        return self.cache[index]
    
    def rowCount(self):
        return len(self.cache)
    
    def columnCount(self):
        return 1
    
    def addItem(self, item: Boundary) -> None:
        self.cache.append(item)

    def addItems(self, items: List[Boundary]) -> None:
        self.cache.extend(items)

    def delItem(self, index: int) -> Boundary:
        return self.cache.pop(index)
    
    def parent(self, index: int):
        return self.cache[index].parent()
    

@dataclass
class Domains(DataCache):

    def addItem(self, item: Domain):
        if not isinstance(item, Domain):
            return None

        self.cache.append(item)

    def addItems(self, items: List[Domain]):
        if not hasattr(items, '__iter__'):
            return None
        
        if not all([isinstance(i, Domain) for i in items]):
            return None
        self.cache.extend(items)

    def listModel(self):
        return Boundaries([b for d in self.cache for b in d.items()])


@dataclass
class Templates(DataCache):

    def addItem(self, item: Template):
        if not isinstance(item, Template):
            return None
        
        self.cache.append(item)

    def addItems(self, items: List[Template]):
        if not hasattr(items, '__iter__'):
            return None
        
        if not all([isinstance(i, Template) for i in items]):
            return None
        
        self.cache.extend(items)

