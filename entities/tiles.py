# Standard Library Imports
from typing import Any

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import AnimatedEntity, Entity


class Tile(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)


class AnimatedTile(AnimatedEntity):

    def __init__(self, world, images, loc):
        super().__init__(world, images, loc)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
    

class MovingTile(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
