from typing import List
from dataclasses import dataclass, field


@dataclass
class Boundary:
    item: str
    type: str = None

    def __str__(self):
        return f'{self.item}'


@dataclass
class Domain:
    item: str
    type: str = None
    children: List[Boundary] = field(default_factory=list)

    def addItem(self, item: Boundary) -> Boundary:
        
        if not isinstance(item, Boundary):
            return -1
        self.children.append(item)
        return item

    def removeItem(self, index: int) -> Boundary:

        if not isinstance(index, int):
            return -1

        try:
            return self.children.pop(index)
        except IndexError:
            return -1

    def insertItem(self, index: int, item: Boundary) -> Boundary:
        
        if not isinstance(index, int) and not isinstance(item, Boundary):
            return -1
        self.children.insert(index, item)

    def child(self, index) -> Boundary:

        if not isinstance(index, int):
            return -1

        try:
            return self.children[index]
        except IndexError:
            return -1

    def getItemByName(self, item: str) -> Boundary:

        if not isinstance(item, str):
            return -1
        
        return [b for b in self.children if item == b.item] | -1

    def childCount(self):
        return len(self.children)
    
    def __str__(self):
        return f'{self.item}'
   
