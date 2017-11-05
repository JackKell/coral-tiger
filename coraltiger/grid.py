import pygame
from pygame import Surface

from coraltiger.basegameobject import BaseGameObject
from coraltiger.colors import Colors
from coraltiger.types import TPoint
from coraltiger.utility import frange


class Grid(BaseGameObject):
    def __init__(self, origin: TPoint, size: TPoint, tileSize: TPoint, lineColor: tuple=Colors.GRAY50.value):
        super().__init__(origin)
        self.size: TPoint = size
        self.tileSize: TPoint = tileSize
        self.lineColor: tuple = lineColor

    def draw(self, surface: Surface):
        for x in frange(0, self.size[0] + self.tileSize[0], self.size[0] / self.tileSize[0]):
            pygame.draw.line(
                surface,
                self.lineColor,
                (x + self._origin[0], self._origin[1]),
                (x + self._origin[0], self.size[1] + self._origin[1])
            )

        for y in frange(0, self.size[1] + self.tileSize[1], self.size[1] / self.tileSize[1]):
            pygame.draw.line(
                surface,
                self.lineColor,
                (self._origin[0], y + self._origin[1]),
                (self.size[0] + self._origin[0], y + self._origin[1])
            )

    def update(self, deltaTime: float) -> None:
        pass
