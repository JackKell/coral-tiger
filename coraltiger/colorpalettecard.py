import pygame
from pygame import Surface

from coraltiger.colors import Colors
from coraltiger.types import Point


class ColorPaletteCard:
    def __init__(self, origin: Point, size: Point):
        self.origin: Point = origin
        self.size: Point = size
        self.colorFont = pygame.font.SysFont(None, 12)

    def draw(self, surface: Surface) -> None:
        colorCount = len(Colors.__members__)
        colorIndex = 0
        rowHeight = self.size[0] // colorCount
        startY = rowHeight // 2
        for color in Colors:
            textSurface = self.colorFont.render(color.name, True, Colors.WHITE.value, Colors.BLACK.value)
            pygame.draw.line(surface,
                             color.value,
                             (self.origin[0], startY + self.origin[1]),
                             (self.origin[0] + self.size[0], startY + self.origin[1]),
                             rowHeight)
            surface.blit(textSurface,
                         [self.origin[0],
                          startY - (textSurface.get_rect().size[1] // 2) + self.origin[1]])
            startY += rowHeight
            colorIndex += 1
        return

