import pygame
from pygame import Surface


from coraltiger.maze import Maze
from coraltiger.mazesolver import MazeSolver
from coraltiger.types import TPoint
from coraltiger.utility import getRandomPoint


def getRandomMaze(mazeSize):
    mazeTileCountX: int = 35
    mazeTileCountY: int = 35
    mazeTileCount: TPoint = (mazeTileCountX, mazeTileCountY)
    mazeOrigin: TPoint = (0, 0)
    mazeSize: TPoint = mazeSize

    randomStart: TPoint = getRandomPoint(0, mazeTileCountX - 1, 0, mazeTileCountY - 1)
    randomEnd: TPoint = randomStart
    while randomEnd == randomStart:
        randomEnd = getRandomPoint(0, mazeTileCountX - 1, 0, mazeTileCountY - 1)

    maze: Maze = Maze(
        mazeOrigin,
        mazeSize,
        mazeTileCount,
        randomStart,
        randomEnd
    )
    return maze


def main():
    pygame.init()

    framePerSecond = 60

    screenWidth: int = 800
    screenHeight: int = 800
    screenSize: TPoint = (screenWidth, screenHeight)
    screen: Surface = pygame.display.set_mode(screenSize)

    isRunning: bool = True

    # mazeTileCountX: int = 10
    # mazeTileCountY: int = 10
    # mazeTileCount: TPoint = (mazeTileCountX, mazeTileCountY)
    # mazeOrigin: TPoint = (0, 0)
    # mazeSize: TPoint = (screenWidth, screenHeight)

    dirtyRects = []
    clock = pygame.time.Clock()

    maze = getRandomMaze(screenSize)
    mazeSolver = MazeSolver(maze)
    maze.draw(screen)
    pygame.display.update()

    while isRunning:
        maze.draw(screen)

        if not mazeSolver.mazeSolved():
            mazeSolver.step()
            mazeSolver.draw(screen)
        else:
            maze = getRandomMaze(screenSize)
            mazeSolver = MazeSolver(maze)
            maze.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
        
        pygame.display.update()
        deltaTime = clock.tick(30) / 1000


if __name__ == "__main__":
    main()
