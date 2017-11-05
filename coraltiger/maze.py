import numpy
from random import uniform
from pygame import Surface
from typing import Tuple, List, Mapping

from coraltiger.basegameobject import BaseGameObject
from coraltiger.mazebasetile import MazeBaseTile
from coraltiger.mazewalltile import MazeWallTile
from coraltiger.colors import Colors
from coraltiger.grid import Grid
from coraltiger.types import TPoint
from mazefloortile import MazeFloorTile


class Maze(BaseGameObject):
    def __init__(self, origin: TPoint, size: TPoint, tileCount: TPoint, start: TPoint, end: TPoint, tileData=None):
        super().__init__(origin)
        self._start: TPoint = start
        self._end: TPoint = end
        self._size: TPoint = size
        self._tileCount: TPoint = tileCount
        self._tiles: numpy.matrix = numpy.matrix(numpy.full(self._tileCount, None))
        if tileData is None:
            self.randomizeTiles(uniform(0.3, 0.4))
        self._grid: Grid = Grid(origin, size, self._tileCount, Colors.GRAY50.value)

    def getStart(self) -> TPoint:
        return self._start

    def setStart(self, x: int, y: int) -> None:
        if x < 0 or x >= self._tileCount[0]:
            raise IndexError()
        if y < 0 or y >= self._tileCount[1]:
            raise IndexError()
        self._start = (x, y)

    def getEnd(self) -> TPoint:
        return self._end

    def setEnd(self, x: int, y: int) -> None:
        if x < 0 or x >= self._tileCount[0]:
            raise IndexError()
        if y < 0 or y >= self._tileCount[1]:
            raise IndexError()
        self._end = (x, y)

    def randomizeTiles(self, density: float) -> None:
        tileSize = self.getTileSize()
        offset = (1, 1)
        wallSize = (tileSize[1] - 1, tileSize[1] - 1)
        for x in range(self._tileCount[0]):
            for y in range(self._tileCount[1]):
                if (x, y) == self._start:
                    self._tiles[x, y] = MazeFloorTile(
                        self.getPixelPositionFromIndex((x, y), offset),
                        Colors.GREEN500.value,
                        wallSize
                    )
                elif (x, y) == self._end:
                    self._tiles[x, y] = MazeFloorTile(
                        self.getPixelPositionFromIndex((x, y), offset),
                        Colors.RED500.value,
                        wallSize
                    )
                elif uniform(0, 1) < density:
                    self._tiles[x, y] = MazeWallTile(
                        self.getPixelPositionFromIndex((x, y), offset),
                        Colors.GRAY600.value,
                        wallSize
                    )
                else:
                    self._tiles[x, y] = MazeFloorTile(
                        self.getPixelPositionFromIndex((x, y), offset),
                        Colors.GRAY200.value,
                        wallSize
                    )

    def getTileSize(self) -> Tuple[float, float]:
        tileSize = (self._size[0] / self._tileCount[0],
                    self._size[1] / self._tileCount[1])
        return tileSize

    def getGraph(self) -> Mapping[TPoint, List[TPoint]]:
        graph = {}
        for x in range(self._tileCount[0]):
            for y in range(self._tileCount[1]):
                # Get current maze tile
                mazeTile = self._tiles[x, y]
                # Check if the tile is traversable (i.e a MazeFloorTile)
                if type(mazeTile) is MazeFloorTile:
                    mazeTilePosition: TPoint = (x, y)
                    neighborTilePositions: List[TPoint] = self.getTraversalNeighborPoints(mazeTilePosition)
                    graph[mazeTilePosition] = neighborTilePositions
        return graph

    def getTraversalNeighborPoints(self, point: TPoint, getDiagonals: bool=False) -> List[TPoint]:
        neighbors = []
        northPoint = (point[0], point[1] - 1)
        southPoint = (point[0], point[1] + 1)
        westPoint = (point[0] - 1, point[1])
        eastPoint = (point[0] + 1, point[1])
        if northPoint[1] >= 0:
            tile: MazeBaseTile = self._tiles[northPoint[0], northPoint[1]]
            if type(tile) is MazeFloorTile:
                neighbors.append(northPoint)
        if southPoint[1] < self._tileCount[1]:
            tile: MazeBaseTile = self._tiles[southPoint[0], southPoint[1]]
            if type(tile) is MazeFloorTile:
                neighbors.append(southPoint)
        if westPoint[0] >= 0:
            tile: MazeBaseTile = self._tiles[westPoint[0], westPoint[1]]
            if type(tile) is MazeFloorTile:
                neighbors.append(westPoint)
        if eastPoint[0] < self._tileCount[0]:
            tile: MazeBaseTile = self._tiles[eastPoint[0], eastPoint[1]]
            if type(tile) is MazeFloorTile:
                neighbors.append(eastPoint)

        # TODO: diagonals do not currently work
        if getDiagonals:
            northWestPoint = (point[0] - 1, point[1] - 1)
            northEastPoint = (point[0] + 1, point[1] - 1)
            southWestPoint = (point[0] - 1, point[1] + 1)
            southEastPoint = (point[0] + 1, point[1] + 1)
            if northWestPoint[0] >= 0 and northWestPoint[1] >= 0:
                tile: MazeBaseTile = self._tiles[northWestPoint[0], northWestPoint[1]]
                if type(tile) is MazeFloorTile:
                    neighbors.append(northWestPoint)
            if northEastPoint[0] < self._tileCount[0] and northEastPoint[1] >= 0:
                tile: MazeBaseTile = self._tiles[northEastPoint[0], northEastPoint[1]]
                if type(tile) is MazeFloorTile:
                    neighbors.append(northEastPoint)
            if southWestPoint[0] >= 0 and southWestPoint[1] < self._tileCount[1]:
                tile: MazeBaseTile = self._tiles[southWestPoint[0], southWestPoint[1]]
                if type(tile) is MazeFloorTile:
                    neighbors.append(southWestPoint)
            if southEastPoint[0] < self._tileCount[0] and southEastPoint[1] < self._tileCount[1]:
                tile: MazeBaseTile = self._tiles[southEastPoint[0], southEastPoint[1]]
                if type(tile) is MazeFloorTile:
                    neighbors.append(southEastPoint)
        return neighbors

    def _drawTiles(self, surface: Surface) -> None:
        for x in range(self._tileCount[0]):
            for y in range(self._tileCount[1]):
                currentTile: MazeBaseTile = self._tiles[x, y]
                currentTile.draw(surface)

    def getPixelPositionFromIndex(self, point: TPoint, offset: TPoint=(0, 0)) -> TPoint:
        tileSize = self.getTileSize()
        return (int(point[0] * tileSize[0] + self._origin[0] + offset[0]),
                int(point[1] * tileSize[1] + self._origin[1] + offset[1]))

    def update(self, deltaTime: float) -> None:
        pass

    def draw(self, surface: Surface) -> None:
        self._grid.draw(surface)
        self._drawTiles(surface)
