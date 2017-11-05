from abc import ABC, abstractmethod

from pygame.surface import Surface

from coraltiger.types import TPoint


class BaseGameObject(ABC):
    def __init__(self, origin: TPoint):
        self._origin: TPoint = origin

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        ...

    @abstractmethod
    def update(self, deltaTime: float) -> None:
        ...
