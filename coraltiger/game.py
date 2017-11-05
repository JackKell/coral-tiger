import pygame
from pygame.time import Clock
from pygame.surface import Surface

from coraltiger.colors import Colors


class Game:
    def __init__(self):
        self.screenSize = (0, 0)
        self.frameRate = 60
        self.clock = Clock()

    def loop(self, screen: Surface):
        while True:
            deltaTime = self.clock.tick(self.frameRate)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill(Colors.BLACK.value)

            pygame.display.update()

    def quit(self):
        pass
