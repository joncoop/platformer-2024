# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import AnimatedEntity, Entity


class Gem(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)

    def apply(self, character):
        character.score += settings.GEM_VALUE


class Heart(Entity):

    def __init__(self, world, image, loc):
        super().__init__(world, image, loc)

    def apply(self, character):
        if character.hearts < character.max_hearts:
            character.hearts += 1