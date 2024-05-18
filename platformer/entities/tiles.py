# Standard Library Imports
from typing import Any

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import AnimatedEntity, Entity
from platformer.resource_manager import ResourceManager


class Tile(Entity):

    def __init__(self, world, loc, tile_type):
        self.resource_manager = ResourceManager()
        super().__init__(world, self.set_image(tile_type), loc)

    def set_image(self, tile_type):
        return self.resource_manager.images['tiles'][tile_type]


class AnimatedTile(AnimatedEntity):

    def __init__(self, world, images, loc):
        super().__init__(world, images, loc)

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass
    

class MovingTile(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass
