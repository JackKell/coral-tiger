from abc import ABC, abstractmethod

from pygame.surface import Surface

from coraltiger.types import Point


class BaseGameObject(ABC):
    def __init__(self, origin: Point):
        self.origin: Point = origin

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        ...
