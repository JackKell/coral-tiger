import pygame
from pygame import Surface
import time


from coraltiger.maze import Maze
from coraltiger.types import Point
from coraltiger.utility import getRandomPoint


def main():
    pygame.init()

    screenWidth: int = 800
    screenHeight: int = 800
    screenSize: Point = (screenWidth, screenHeight)
    screen: Surface = pygame.display.set_mode(screenSize)

    isRunning: bool = True

    mazeTileCountX: int = 10
    mazeTileCountY: int = 10
    mazeTileCount: Point = (mazeTileCountX, mazeTileCountY)
    mazeOrigin: Point = (0, 0)
    mazeSize: Point = screenSize

    while isRunning:
        time.sleep(2)
        randomStart: Point = getRandomPoint(0, mazeTileCountX - 1, 0, mazeTileCountY - 1)
        randomEnd: Point = randomStart
        while randomEnd == randomStart:
            randomEnd = getRandomPoint(0, mazeTileCountX - 1, 0, mazeTileCountY - 1)

        maze: Maze = Maze(
            mazeOrigin,
            mazeSize,
            mazeTileCount,
            randomStart,
            randomEnd
        )

        maze.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
        
        pygame.display.flip()


if __name__ == "__main__":
    main()
