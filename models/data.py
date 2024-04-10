from __future__ import annotations

from copy import deepcopy
from typing import List
from dataclasses import dataclass, field


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
class Domain:
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

    def __str__(self):
        return f'{self.name}'


@dataclass
class Template:
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
class Boundaries:
    boundaries: List[Boundary] = field(default_factory=list)

    def items(self):
        return deepcopy(self.boundaries)
    
    def item(self, index: int) -> Boundary:
        return self.boundaries[index]
    
    def rowCount(self):
        return len(self.boundaries)
    
    def columnCount(self):
        return 1
    
    def addItem(self, item: Boundary) -> None:
        self.boundaries.append(item)

    def addItems(self, items: List[Boundary]) -> None:
        self.boundaries.extend(items)

    def delItem(self, index: int) -> Boundary:
        return self.boundaries.pop(index)
    
    def parent(self, index: int):
        return self.boundaries[index].parent()
    

@dataclass
class Domains:
    domains: List[Domain] = field(default_factory=list)

    def items(self):
        return deepcopy(self.domains)

    def item(self, index: int):
        return self.domains[index]

    def children(self, index: int):
        return self.domains[index].items()

    def child(self, row: int, col: int) -> Boundary:
        return self.domains[row].item(col)

    def columnCount(self, index: int) -> int:
        return self.domains[index].rowCount()

    def addItem(self, item: Domain):
        self.domains.append(item)

    def addItems(self, items: List[Domain]):
        self.domains.extend(items)

    def delItem(self, index: int) -> Domain:
        return self.domains.pop(index)
    
    def addChild(self, index: int, child: Boundary):
        self.domains[index].addItem(child)

    def addChildren(self, index: int, children: List[Boundary]):
        self.domains[index].addItems(children)

    def delChild(self, row: int, col: int) -> Boundary:
        return self.domains[row].delItem(col)

    def rowCount(self):
        return len(self.domains)
    
    def boundaries(self):
        return Boundaries([b for d in self.domains for b in d.items()])


@dataclass
class Templates:
    templates: List[Template] = field(default_factory=list)

    def items(self):
        return deepcopy(self.templates)

    def item(self, index: int):
        return self.templates[index]

    def children(self, index: int):
        return self.templates[index].items()

    def child(self, row: int, col: int) -> str:
        return self.templates[row].item(col)

    def addItem(self, item: Template):
        self.templates.append(item)

    def addItems(self, items: List[Template]):
        self.templates.extend(items)

    def delItem(self, index: int) -> Template:
        return self.templates.pop(index)
    
    def addChild(self, index: int, item: Template):
        self.templates[index].addItem(item)

    def addChildren(self, index: int, children: List[Template]):
        self.templates[index].addItems(children)

    def delChild(self, row: int, col: int) -> Template:
        return self.templates[row].delItem(col)

    def rowCount(self):
        return len(self.templates)
    
    def columnCount(self, index: int) -> int:
        return self.templates[index].rowCount()
   
