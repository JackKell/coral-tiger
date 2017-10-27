from collections import deque
import numpy
from numpy import zeros, full, matrix
from random import uniform
import pygame
from pygame import Surface
from pygame.rect import Rect
from typing import Tuple, List

from coraltiger.basegameobject import BaseGameObject
from coraltiger.utility import drawArrow
from coraltiger.colors import Colors
from coraltiger.grid import Grid
from coraltiger.types import Point
from coraltiger.mazenode import MazeNode


class Maze(BaseGameObject):
    def __init__(self, origin: Point, size: Point, tileCount: Point, start: Point, end: Point):
        super().__init__(origin)
        self.start: Point = start
        self.end: Point = end
        self.size: Point = size
        self.tileCount: Point = tileCount
        self.data: matrix = matrix(zeros(self.tileCount))
        self.grid: Grid = Grid(origin, size, self.tileCount, Colors.GRAY50.value)
        self.randomizeMaze(uniform(0, 0.35))

    def randomizeMaze(self, density: float) -> None:
        for x in range(self.tileCount[0]):
            for y in range(self.tileCount[1]):
                if (x, y) != self.start and (x, y) != self.end:
                    if uniform(0, 1) < density:
                        self.data[x, y] = 1

    def getTileSize(self) -> Tuple[float, float]:
        tileSize = (self.size[0] / self.tileCount[0],
                    self.size[1] / self.tileCount[1])
        return tileSize

    def getGraph(self) -> numpy.matrix:
        graph = numpy.matrix(full(self.tileCount, None))
        for x in range(self.tileCount[0]):
            for y in range(self.tileCount[1]):
                nodeValue = self.data[x, y]
                if nodeValue == 0:
                    if graph[x, y]:
                        currentNode = graph[x, y]
                    else:
                        currentNode = MazeNode((x, y))
                    neighborNodes = []
                    neighborPoints = self.getNeighborPoints((x, y))
                    for neighborPoint in neighborPoints:
                        neighborNode = graph[neighborPoint[0], neighborPoint[1]]
                        if neighborNode is None:
                            neighborNode = MazeNode(neighborPoint)
                            graph[neighborPoint[0], neighborPoint[1]] = neighborNode
                        neighborNodes.append(neighborNode)
                    currentNode.neighbors = neighborNodes
                    graph[x, y] = currentNode
        return graph

    def getPath(self, graph, surface: Surface):
        tileSize = self.getTileSize()
        tileCenterOffset = (int(tileSize[0] / 2), int(tileSize[1] / 2))
        startNode: MazeNode = graph[self.start[0], self.start[1]]
        queue: deque = deque()
        queue.append(startNode)
        while len(queue) > 0:
            currentNode: MazeNode = queue.popleft()
            currentNode.isVisited = True
            if currentNode.position == self.end:
                path = []
                while currentNode is not None:
                    path.insert(0, currentNode.position)
                    currentNode = currentNode.parent
                return path
            else:
                currentNodePosition = self._getPositionFromIndex(currentNode.position, tileCenterOffset)
                for neighborNode in currentNode.neighbors:
                    if not neighborNode.isVisited:
                        neighborNode.parent = currentNode
                        queue.append(neighborNode)
                        # Draw Parent Arrow
                        neighborNodePosition = self._getPositionFromIndex(neighborNode.position, tileCenterOffset)
                        drawArrow(surface, Colors.GREEN500.value, neighborNodePosition, currentNodePosition, (5, 10))
        return []

    def getNeighborPoints(self, point: Point, getDiagonals: bool=False) -> List[Point]:
        neighbors = []
        northPoint = (point[0], point[1] - 1)
        southPoint = (point[0], point[1] + 1)
        westPoint = (point[0] - 1, point[1])
        eastPoint = (point[0] + 1, point[1])
        if northPoint[1] >= 0:
            value = self.data[northPoint[0], northPoint[1]]
            if value == 0:
                neighbors.append(northPoint)
        if southPoint[1] < self.tileCount[1]:
            value = self.data[southPoint[0], southPoint[1]]
            if value == 0:
                neighbors.append(southPoint)
        if westPoint[0] >= 0:
            value = self.data[westPoint[0], westPoint[1]]
            if value == 0:
                neighbors.append(westPoint)
        if eastPoint[0] < self.tileCount[0]:
            value = self.data[eastPoint[0], eastPoint[1]]
            if value == 0:
                neighbors.append(eastPoint)

        # TODO: diagonals do not currently work
        if getDiagonals:
            northWestPoint = (point[0] - 1, point[1] - 1)
            northEastPoint = (point[0] + 1, point[1] - 1)
            southWestPoint = (point[0] - 1, point[1] + 1)
            southEastPoint = (point[0] + 1, point[1] + 1)
            if northWestPoint[0] >= 0 and northWestPoint[1] >= 0:
                value = self.data[northWestPoint[0], northWestPoint[1]]
                if value == 0:
                    neighbors.append(northWestPoint)
            if northEastPoint[0] < self.tileCount[0] and northEastPoint[1] >= 0:
                value = self.data[northEastPoint[0], northEastPoint[1]]
                if value == 0:
                    neighbors.append(northEastPoint)
            if southWestPoint[0] >= 0 and southWestPoint[1] < self.tileCount[1]:
                value = self.data[southWestPoint[0], southWestPoint[1]]
                if value == 0:
                    neighbors.append(southWestPoint)
            if southEastPoint[0] < self.tileCount[0] and southEastPoint[1] < self.tileCount[1]:
                value = self.data[southEastPoint[0], southEastPoint[1]]
                if value == 0:
                    neighbors.append(southEastPoint)
        return neighbors

    def _drawTiles(self, surface: Surface) -> None:
        tileSize = self.getTileSize()
        offset = (int(tileSize[0] / 4), int(tileSize[1] / 4))
        wallSize = (tileSize[1] // 2, tileSize[1] // 2)
        for x in range(self.tileCount[0]):
            for y in range(self.tileCount[1]):
                currentValue: int = self.data[x, y]
                position: Point = self._getPositionFromIndex((x, y), offset)
                if currentValue == 1:
                    pygame.draw.rect(surface, Colors.GRAY900.value, Rect(position, wallSize))
                elif (x, y) == self.start:
                    pygame.draw.rect(surface, Colors.GREEN500.value, Rect(position, wallSize))
                elif (x, y) == self.end:
                    pygame.draw.rect(surface, Colors.RED500.value, Rect(position, wallSize))

    def draw(self, surface: Surface) -> None:
        self.grid.draw(surface)
        self._drawTiles(surface)
        graph = self.getGraph()
        path: List[Point] = self.getPath(graph, surface)
        print(path)
        # self._drawGraph(surface, graph)
        self._drawPath(surface, path)

    def _drawGraph(self, surface: Surface, graph) -> None:
        tileSize = self.getTileSize()
        tileCenterOffset = (int(tileSize[0] / 2), int(tileSize[0] / 2))

        for x in range(self.tileCount[0]):
            for y in range(self.tileCount[1]):
                currentNode: MazeNode = graph[x, y]
                if currentNode is not None:
                    if currentNode.position != self.start and currentNode.position != self.end:
                        position = self._getPositionFromIndex(currentNode.position, tileCenterOffset)
                        pygame.draw.circle(surface,
                                           Colors.BLUE500.value,
                                           position,
                                           int(tileSize[0] / 4))
                    for neighborNode in currentNode.neighbors:
                        startPosition = self._getPositionFromIndex(currentNode.position, tileCenterOffset)
                        endPosition = self._getPositionFromIndex(neighborNode.position, tileCenterOffset)
                        pygame.draw.line(
                            surface,
                            Colors.BLACK.value,
                            startPosition,
                            endPosition
                        )

    def _getPositionFromIndex(self, point: Point, offset: Point=(0, 0)) -> Point:
        tileSize = self.getTileSize()
        return (int(point[0] * tileSize[0] + self.origin[0] + offset[0]),
                int(point[1] * tileSize[1] + self.origin[1] + offset[1]))

    def _drawPath(self, surface: Surface, path: List[Point]) -> None:
        tileSize = self.getTileSize()
        tileCenterOffset = (int(tileSize[0] / 2), int(tileSize[0] / 2))
        for pointIndex in range(len(path) - 1):
            startPoint = path[pointIndex]
            endPoint = path[pointIndex + 1]
            startPosition = self._getPositionFromIndex(startPoint, tileCenterOffset)
            endPosition = self._getPositionFromIndex(endPoint, tileCenterOffset)
            pygame.draw.line(surface, Colors.PINK500.value, startPosition, endPosition)
