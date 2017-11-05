from collections import deque
from typing import List

from pygame.surface import Surface

from coraltiger.basegameobject import BaseGameObject
from coraltiger.colors import Colors
from coraltiger.maze import Maze
from coraltiger.types import TGraph, TPoint
from coraltiger.utility import drawArrow


class MazeSolver(BaseGameObject):
    def __init__(self, maze: Maze):
        super().__init__(maze._origin)
        self._maze: Maze = maze
        self._startPoint: TPoint = maze.getStart()
        self._endPoint: TPoint = maze.getEnd()
        self._mazeGraph: TGraph = maze.getGraph()
        self._frontierPoints: deque = deque()
        self._frontierPoints.append(self._startPoint)
        self._points = list(self._mazeGraph.keys())
        self._visitedPoints: dict = dict.fromkeys(self._points, False)
        self._visitedPoints[self._startPoint] = True
        self._parentPoints: dict = dict.fromkeys(self._points, None)
        self._pointPositions: dict = {}
        for point in self._points:
            position = maze.getPixelPositionFromIndex(point)
            self._pointPositions[point] = position
        self._path: List[TPoint] = []
        self._foundEndPoint: bool = False
        self._currentPoint: TPoint = self._startPoint
        self._noPossiblePath: bool = False
        self._pathFound: bool = False

    def solve(self):
        while not self._noPossiblePath and not self._pathFound:
            self.step()
        return self._path

    def step(self):
        if self._noPossiblePath:
            return []
        elif not self._foundEndPoint and len(self._frontierPoints) > 0:
            self._currentPoint = self._frontierPoints.popleft()
            if self._currentPoint == self._endPoint:
                self._foundEndPoint = True
            else:
                for neighborPoint in self._mazeGraph[self._currentPoint]:
                    if not self._visitedPoints[neighborPoint]:
                        self._parentPoints[neighborPoint] = self._currentPoint
                        self._frontierPoints.append(neighborPoint)
                        self._visitedPoints[neighborPoint] = True
        elif not self._foundEndPoint and len(self._frontierPoints) == 0:
            self._noPossiblePath = True
        elif self._foundEndPoint:
            if self._currentPoint:
                self._path.insert(0, self._currentPoint)
                self._currentPoint = self._parentPoints[self._currentPoint]
            else:
                self._pathFound = True

    def mazeSolved(self):
        return self._noPossiblePath or self._pathFound

    def update(self, deltaTime: float) -> None:
        pass

    def draw(self, surface: Surface) -> None:
        tileSize = self._maze.getTileSize()
        gridFittedTileSize = tileSize[0] - 1, tileSize[1] - 1
        # draw tile colors
        for point in self._points:
            position = self._pointPositions[point]
            position = position[0] + 1, position[1] + 1
            highlightTile = Surface(gridFittedTileSize)
            if point in self._path:
                highlightTile.set_alpha(128)
                highlightTile.fill(Colors.RED500.value)
                surface.blit(highlightTile, position)
            elif point in self._frontierPoints:
                highlightTile.set_alpha(128)
                highlightTile.fill(Colors.BLUE500.value)
                surface.blit(highlightTile, position)
            elif self._visitedPoints[point]:
                highlightTile.set_alpha(70)
                highlightTile.fill(Colors.BLUE500.value)
                surface.blit(highlightTile, position)
        for point in self._points:
            # draw arrows
            position = self._pointPositions[point]
            position = position[0] + tileSize[0] // 2, position[1] + tileSize[1] // 2
            parentPoint = self._parentPoints[point]
            if parentPoint:
                parentPosition = self._pointPositions[parentPoint]
                parentPosition = parentPosition[0] + tileSize[0] // 2, parentPosition[1] + tileSize[1] // 2
                drawArrow(surface, Colors.BLUE500.value, position, parentPosition, (3, 5))

