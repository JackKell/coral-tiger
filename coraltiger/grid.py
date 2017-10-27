import pygame
from pygame import Surface

from coraltiger.basegameobject import BaseGameObject
from coraltiger.colors import Colors
from coraltiger.types import Point
from coraltiger.utility import frange


class Grid(BaseGameObject):
    def __init__(self, origin: Point, size: Point, tileSize: Point, lineColor: tuple=Colors.GRAY50.value):
        super().__init__(origin)
        self.size: Point = size
        self.tileSize: Point = tileSize
        self.lineColor: tuple = lineColor

    def draw(self, surface: Surface):
        surface.fill(Colors.GRAY500.value)
        for x in frange(0, self.size[0] + self.tileSize[0], self.size[0] / self.tileSize[0]):
            pygame.draw.line(
                surface,
                self.lineColor,
                (x + self.origin[0], self.origin[1]),
                (x + self.origin[0], self.size[1] + self.origin[1])
            )

        for y in frange(0, self.size[1] + self.tileSize[1], self.size[1] / self.tileSize[1]):
            pygame.draw.line(
                surface,
                self.lineColor,
                (self.origin[0], y + self.origin[1]),
                (self.size[0] + self.origin[0], y + self.origin[1])
            )
