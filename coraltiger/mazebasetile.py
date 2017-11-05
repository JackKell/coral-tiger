import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from coraltiger.basegameobject import BaseGameObject
from coraltiger.types import TPoint


class MazeBaseTile(BaseGameObject):
    def __init__(self, origin: TPoint, color, size):
        super().__init__(origin)
        self.color = color
        self.size = size

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, self.color, Rect(self._origin, self.size))

    def update(self, deltaTime: float) -> None:
        pass

