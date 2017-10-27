from typing import List

from coraltiger.types import Point


class MazeNode:
    def __init__(self, position: Point):
        self.parent: MazeNode = None
        self.neighbors: List[MazeNode] = []
        self.position: Point = position
        self.isVisited = False

    def __str__(self):
        return str(self.position)

    def __repr__(self):
        return str(self)

