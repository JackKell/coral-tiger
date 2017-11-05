from decimal import Decimal
import math
from typing import Tuple
from random import randint
import pygame
from pygame.surface import Surface

from coraltiger.types import TPoint


def drawArrow(surface: Surface,
              color: Tuple[int, int, int],
              startPoint: TPoint,
              endPoint: TPoint,
              headSize: TPoint,
              lineWidth: int = 1) -> None:
    lineAngle = math.atan2(endPoint[1] - startPoint[1], endPoint[0] - startPoint[0])
    arrowHeadWidth = headSize[0]
    halfArrowHeadWidth = arrowHeadWidth / 2
    arrowHeadHeight = headSize[1]
    z = math.atan(halfArrowHeadWidth / arrowHeadHeight)
    d = math.hypot(halfArrowHeadWidth, arrowHeadHeight)
    angleA = lineAngle + (math.pi - z)
    angleB = lineAngle - (math.pi - z)
    pointA = (d * math.cos(angleA) + endPoint[0], d * math.sin(angleA) + endPoint[1])
    pointB = (d * math.cos(angleB) + endPoint[0], d * math.sin(angleB) + endPoint[1])
    pygame.draw.line(surface, color, startPoint, endPoint, lineWidth)
    pygame.draw.polygon(surface, color, [pointA, pointB, endPoint])


def getPointFromPolarCoordinate(distance: float, angle: float, origin: TPoint=(0, 0)) -> Tuple[float, float]:
    return (distance * math.cos(angle) + origin[0],
            distance * math.sin(angle) + origin[1])


def getRandomPoint(xMin: int, xMax: int, yMin: int, yMax: int) -> TPoint:
    return randint(xMin, xMax), randint(yMin, yMax)


def frange(start: float, end: float, step: float) -> list:
    while start < end:
        yield start
        start += Decimal(step)
