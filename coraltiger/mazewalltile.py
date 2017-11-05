from coraltiger.mazebasetile import MazeBaseTile
from coraltiger.types import TPoint


class MazeWallTile(MazeBaseTile):
    def __init__(self, origin: TPoint, color, size):
        super().__init__(origin, color, size)
