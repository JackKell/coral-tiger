from typing import List

from coraltiger.types import TPoint


class MazeNode:
    def __init__(self, position: TPoint):
        self.parent: MazeNode = None
        self.neighbors: List[MazeNode] = []
        self.position: TPoint = position
        self.isVisited = False

    def __str__(self):
        return str(self.position)

    def __repr__(self):
        return str(self)

